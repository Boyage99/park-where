from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from functools import wraps
from dotenv import load_dotenv
import os
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import jwt
import hashlib
import datetime
from haversine import haversine

# 환경 변수
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
ID = os.environ.get('DB_ID')
PW = os.environ.get('DB_PW')

app = Flask(__name__)

# DB 연결
client = MongoClient("mongodb+srv://" + ID + ":" + PW + "@cluster0.4bw3y.mongodb.net/?retryWrites=true&w=majority")
db = client.dbparkwhere


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token is None or refresh_token is None:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

        try:
            jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            refresh_token = request.cookies.get("refresh_token")

            access_token, refresh_token = refresh(access_token, refresh_token)

            if access_token is not None and refresh_token is not None:
                resp = make_response(f(*args, **kwargs))
                resp.set_cookie("access_token", access_token)
                resp.set_cookie("refresh_token", refresh_token)
                return resp
            else:
                return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

    return decorated_function


# Index Page
@app.route('/')
@login_required
def home():
    return render_template("index.html")


@app.route("/result", methods=["GET"])
def nearby():
    MAP_API_ID = os.environ.get('MAP_API_ID')
    return render_template("result.html", data={'mapId': MAP_API_ID})

@app.route("/selectAddress")
def selectAddress():
    MAP_API_ID = os.environ.get('MAP_API_ID')
    NAVER_SECRET_KEY = os.environ.get('NAVER_SECRET_KEY')
    return render_template("selectAddress.html",data={'mapId': MAP_API_ID,'key':NAVER_SECRET_KEY})

@app.route("/searchArea")
def searchArea():
    return render_template("searchArea.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    id = request.form["id"]
    pw = request.form["pw"]

    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

    user = db.user.find_one({"id": id, "pw": pw_hash})

    if user is not None:
        now = datetime.datetime.utcnow()

        access_payload = {
            "id": user["id"],
            "username": user["username"],
            "exp": now + datetime.timedelta(minutes=1)
        }

        refresh_payload = {
            "exp": now + datetime.timedelta(minutes=5)
        }

        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256").decode("utf-8")
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256").decode("utf-8")

        return jsonify({"result": "success", "access_token": access_token, "refresh_token": refresh_token, "user_id": user["id"], "username": user["username"]})
    else:
        return jsonify({"result": "fail", "msg": "아이디 또는 비밀번호를 잘못 입력했습니다. 입력하신 내용을 다시 확인해주세요."})


@app.route("/api/signup", methods=["POST"])
def api_signup():
    id = request.form["id"]
    pw = request.form["pw"]
    username = request.form["username"]

    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

    db.user.insert_one({"id": id, "pw": pw_hash, "username": username})

    return jsonify({"result": "success"})

@app.route("/api/signup/check_dup", methods=["POST"])
def api_check_dup():
    id = request.form["id"]

    exists = bool(db.user.find_one({"id": id}))

    return jsonify({"exists": exists})

def refresh(access_token, refresh_token):
    try:
        refresh_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        access_payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})

        now = datetime.datetime.utcnow()

        access_payload["exp"] = now + datetime.timedelta(minutes=1)
        refresh_payload["exp"] = now + datetime.timedelta(minutes=5)

        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256").decode("utf-8")
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256").decode("utf-8")

        return access_token, refresh_token
    except jwt.ExpiredSignatureError:
        return None, None
    except jwt.exceptions.DecodeError:
        return None, None


# ---- login ,signup end ----

# ----- review API -----
@app.route("/reviews", methods=["GET"])
# TODO: 라우트마다 @login_required 추가하기
# 모든 리뷰 페이지
def reviews():
    reviews = list(db.reviews.find({}, {'_id':False}))
    for idx in range(0,len(reviews)):
        parkid = reviews[idx]['parkid']
        park = db.park.find_one({'_id': ObjectId(f'{parkid}')}, {'_id': False})
        parkname = park['주차장명']
        reviews[idx]['parkname'] = parkname
    print(reviews)
    return render_template('reviews/index.html', data={'reviews': reviews})


# 모든 리뷰 받아오기
@app.route("/api/reviews", methods=["GET"])
def get_all_reviews():
    reviews = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': reviews})


# 개별 주차장 리뷰 페이지
@app.route("/reviews/<parkid>", methods=["GET"])
def show_reviews(parkid):
    park = db.park.find_one({'_id': ObjectId(f'{parkid}')}, {'_id':False})
    reviews = list(db.reviews.find({'parkid': f'{parkid}'}, {'_id':False}))
    reviews_len = (len(reviews))
    reviews_avg = 0
    if reviews_len == 0:
        reviews = []
    else:
        reviews_sum = (sum(int(review['rate']) for review in reviews))
        reviews_avg = f'{float(reviews_sum/reviews_len):.1f}'

    MAP_API_ID = os.environ.get('MAP_API_ID')
    return render_template('reviews/show.html', data={'park': park, 'reviews': reviews, 'avg': reviews_avg, 'mapId': MAP_API_ID})


# 리뷰 작성하기
@app.route("/api/reviews", methods=["POST"])
def create_review():
    user_id = request.form["user_id"]
    username = request.form["username"]
    park_id = request.form["park_id"]
    comment = request.form["comment"]
    rate = request.form["rate"]

    db.reviews.insert_one({
        "userid": user_id,
        "username": username,
        "parkid": park_id,
        "comment": comment,
        "rate": rate,
    })

    return jsonify({'msg': '등록 완료!'})


# 주차장 정보 가져오기
@app.route("/api/parks/<park_id>", methods=["GET"])
def get_park(park_id):
    park_id = park_id
    park = db.park.find_one({"_id": ObjectId(f"{park_id}")}, {"_id":False})
    return jsonify({"result": "success", "park": park})


# 개별 주차장 리뷰 받아오기 (주차장id)
@app.route("/api/reviews/<park_id>", methods=["GET"])
def get_reviews(park_id):
    reviews = list(db.reviews.find({"parkid": f"{park_id}"}))
    for review in reviews:
        review["_id"] = str(review["_id"])
    return jsonify({"result": "success", "reviews": reviews})


# 개별 주차장 리뷰 수정하기 (리뷰id)
@app.route("/api/reviews/<reviewid>", methods=["PATCH"])
def patch_review(reviewid):
    comment_receive = request.form['comment_give']
    db.reviews.find_one_and_update(
        {'reviewid': reviewid},
        {'$set': {'comment': comment_receive}},
        return_document=ReturnDocument.AFTER)


# 개별 주차장 리뷰 삭제하기 (리뷰id)
@app.route("/api/reviews", methods=["DELETE"])
def delete_review():
    review_id = request.form["review_id"]
    db.reviews.delete_one({'_id': ObjectId(f'{review_id}')})
    return jsonify({"result": "success"})


# ---- review end ----

@app.route("/api/search", methods=["POST"])
def find_parks():
    lat_receive = float(request.form['lat_give'])
    longi_receive = float(request.form['longi_give'])
    radius_receive = int(request.form['radius_give'])

    # park_list = list(db.park.find())
    park_list = list(db.park.find())

    return_park_list = list()

    for park in park_list:

        if park['위도'] != '' and park['경도'] != '':

            park['_id'] = str(park['_id'])

            park_lat = float(park['위도'])
            park_longi = float(park['경도'])

            user_location = (lat_receive, longi_receive)  # Latitude, Longitude
            park_location = (park_lat, park_longi)  # Latitude, Longitude

            km = haversine(user_location, park_location, unit='km')

            if km <= radius_receive:
                return_park_list.append(park)

    # print(return_park_list)
    return jsonify({'list': return_park_list})


# ---- end parks api ----


# 서버 config
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
