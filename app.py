from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
import os

app = Flask(__name__)
load_dotenv()
ID = os.environ.get('DB_ID')
PW = os.environ.get('DB_PW')
client = MongoClient("mongodb+srv://"+ID+":"+PW+"@first-project.xac7l.mongodb.net/?retryWrites=true&w=majority")
db = client.dbparkwhere


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/reviews", methods=["GET"])
# 모든 리뷰 페이지
def reviews():
    return render_template('reviews/index.html')

@app.route("/api/reviews", methods=["GET"])
# 모든 리뷰 받아오기
def get_all_reviews():
    reviews = list(db.reviews.find({}, {'_id':False}))
    return jsonify({'reviews': reviews})

@app.route("/reviews/<parkid>", methods=["GET"])
# 개별 주차장 리뷰 페이지
def show_reviews(parkid):
    return render_template('reviews/show.html')

@app.route("/reviews/<parkid>/new", methods=["GET"])
# 개별 주차장 리뷰 작성 페이지
def new_review(parkid):
    return render_template('reviews/new.html', parkid=parkid)

@app.route("/api/reviews", methods=["POST"])
# 리뷰 작성하기
def create_review():
    userid_receive = request.form['userid_give']
    parkid_receive = request.form['parkid_give']
    comment_receive = request.form['comment_give']
    rate_receive = request.form['rate_give']

    doc = {
        'userid': userid_receive,
        'parkid': parkid_receive,
        'comment': comment_receive,
        'rate': rate_receive,
    }
    db.reviews.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/api/reviews/<parkid>", methods=["GET"])
# 개별 주차장 리뷰 받아오기 (주차장id)
def get_reviews(parkid):
    reviews = list(db.reviews.find({'parkid': parkid}, {'_id':False}))
    return jsonify({'reviews': reviews})

@app.route("/api/reviews/<reviewid>", methods=["PATCH"])
# 개별 주차장 리뷰 수정하기 (리뷰id)
def patch_review(reviewid):
    comment_receive = request.form['comment_give']
    db.reviews.find_one_and_update(
        {'reviewid': reviewid},
        {'$set': {'comment': comment_receive}},
        return_document=ReturnDocument.AFTER)

@app.route("/api/reviews/<reviewid>", methods=["DELETE"])
# 개별 주차장 리뷰 삭제하기 (리뷰id)
def delete_review(reviewid):
    db.reviews.find_one_and_delete(
        {'reviewid': reviewid},
        return_document=ReturnDocument.AFTER)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)