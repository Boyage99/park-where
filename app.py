from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
import os
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
client = MongoClient("mongodb+srv://"+ID+":"+PW+"@cluster0.4bw3y.mongodb.net/?retryWrites=true&w=majority")
db = client.dbparkwhere


# Index Page
@app.route('/')
def home():
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("index.html")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route("/result", methods=["GET"])
def nearby():
    return render_template("result.html")


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
        payload = {
            "id": user["id"],
            "username": user["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode(
            'utf-8')  # FIXME: 이거 Pytharm 과 vscode 차이로 안됨..

        return jsonify({"result": "success", "token": token})
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


# ---- login ,signup end ----

# ----- review API -----
@app.route("/reviews", methods=["GET"])
# 모든 리뷰 페이지
def reviews():
    return render_template('reviews/index.html')


# 모든 리뷰 받아오기
@app.route("/api/reviews", methods=["GET"])
def get_all_reviews():
    reviews = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': reviews})


# 개별 주차장 리뷰 페이지
@app.route("/reviews/<parkid>", methods=["GET"])
def show_reviews(parkid):
    return render_template('reviews/show.html')


# 개별 주차장 리뷰 작성 페이지
@app.route("/reviews/<parkid>/new", methods=["GET"])
def new_review(parkid):
    return render_template('reviews/new.html', parkid=parkid)


# 리뷰 작성하기
@app.route("/api/reviews", methods=["POST"])
def create_review():
    userid_receive = request.form['userid_give']
    parkid_receive = request.form['parkid_give']
    comment_receive = request.form['comment_give']
    rate_receive = request.form['rate_give']

    doc = {
        'userid': int(userid_receive),
        'parkid': parkid_receive,
        'comment': comment_receive,
        'rate': rate_receive,
    }
    db.reviews.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


# 개별 주차장 리뷰 받아오기 (주차장id)
@app.route("/api/reviews/<parkid>", methods=["GET"])
def get_reviews(parkid):
    reviews = list(db.reviews.find({'parkid': parkid}, {'_id': False}))
    return jsonify({'reviews': reviews})


# 개별 주차장 리뷰 수정하기 (리뷰id)
@app.route("/api/reviews/<reviewid>", methods=["PATCH"])
def patch_review(reviewid):
    comment_receive = request.form['comment_give']
    db.reviews.find_one_and_update(
        {'reviewid': reviewid},
        {'$set': {'comment': comment_receive}},
        return_document=ReturnDocument.AFTER)


# 개별 주차장 리뷰 삭제하기 (리뷰id)
@app.route("/api/reviews/<reviewid>", methods=["DELETE"])
def delete_review(reviewid):
    db.reviews.find_one_and_delete(
        {'reviewid': reviewid},
        return_document=ReturnDocument.AFTER)


# ---- review end ----

# ---- find parks api ---
@app.route("/api/findParks", methods=["POST"])
def find_parks():
    lat_receive = float(request.form['lat_give'])
    longi_receive = float(request.form['longi_give'])
    radius_receive = int(request.form['radius_give'])

    # # test code
    # lat_receive = 37.541
    # longi_receive = 126.986
    # radius_receive = 5

    park_list = list(db.park.find({}, {'_id': False}))
    return_park_list = list()

    for park in park_list:

        if park['위도'] != '' and park['경도'] != '':
            park_lat = float(park['위도'])
            park_longi = float(park['경도'])

            user_location = (lat_receive, longi_receive)  # Latitude, Longitude
            park_location = (park_lat, park_longi)  # Latitude, Longitude

            print(park_lat, park_longi)
            km = haversine(user_location, park_location, unit='km')

            if km <= radius_receive:
                return_park_list.append(park)

    print(return_park_list)
    return jsonify({'list': return_park_list})


# ---- end parks api ----


# 서버 config
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
