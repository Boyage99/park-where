# 🚖 주차 어디 프로젝트

> GPS 좌표 기반의 일정 반경에 위치한 주차장 위치,정보 제공 앱

## ✨ 기능

- 회원가입, 로그인(JWT)
- 현재 위치정보로 원하는 반경(km)내의 주차장 정보 가져오기
- 원하는 주소지 근처의 일정 반경(km)내의 주차장 정보 가져오기
- 주차장에 대한 평점+후기 CRD(Create, Read, Delete)

## ⚒ 개발 스택

- Python / Flask / Jinja2
- JavaScript / JQuery
- MongoDB
- HTML / CSS / Bootstrap

## 📅 기간

- 2022년 6월 20일 ~ 6월 23일

## 👨‍💻 팀원
- [공태민](https://github.com/livemehere), [김현](https://github.com/uoahy), [안병규](https://github.com/fox9d), [윤수영](https://github.com/ddooyn)

## 📱 웹앱 화면

<div align="center">
<h3>로그인 및 회원가입</h3>
<img src="https://user-images.githubusercontent.com/84499458/176114038-867477ed-5730-46d7-801e-c46cbc841f0c.gif" width="300" alt="로그인 화면"/>
<img src="https://user-images.githubusercontent.com/84499458/176114053-5b557832-1330-49fb-b0c0-9f5ecc9b7fa6.png" width="300" alt="회원가입 화면"/>
</div>
<div align="center">
<h3>메인 화면 / 주소로 찾기</h3>
<img src="https://user-images.githubusercontent.com/84499458/176114061-337d61ea-65b6-4e6f-82d3-e76b2302e5c1.gif" width="300" alt="메인"/>
<img src="https://user-images.githubusercontent.com/84499458/176114072-4482379f-64e7-4bb1-a2bd-bff37a502623.gif" width="300" alt="주소로 찾기"/>
</div>
<div align="center">
<h3>주변 찾기 / 주차장 검색 결과 (마커 및 리스트 클릭 시 이동)</h3>
<img src="https://user-images.githubusercontent.com/84499458/176114144-f7ff7f28-1c67-496d-a950-b1b2767302d1.gif" width="300" alt="주변 찾기"/>
<img src="https://user-images.githubusercontent.com/84499458/176114090-1b1fa836-ed7e-4bfa-832e-61ca61e17f13.gif" width="300" alt="주차장 검색 결과"/>
</div>
<div align="center">
<h3>주차장 상세 화면(리뷰 작성 및 삭제) / 리뷰 전체보기</h3>
<img src="https://user-images.githubusercontent.com/84499458/176114120-63f4c815-f26a-40b7-80eb-83214b4fb4eb.gif" width="300" alt="주차장 상세 화면"/>
<img src="https://user-images.githubusercontent.com/84499458/176114955-fa949095-c6aa-45af-9c97-de90a02c8ff2.png" width="300" alt="리뷰 전체보기"/>
</div>

## 🚀 트러블 슈팅

- Flask SSL + EC2 인증 적용하기
- Header의 Token인증 미들웨어 적용하기

---

## 🔧 환경세팅

```bash
# mac 기준
python -m venv venv #가상환경 설치
source venv/bin/activate # 활성화
deactivate #비활성화
```

## 😀 새로운 모듈을 설치했다면

```bash
pip freeze > requirements.txt
pip install -r ./requirements.txt
```
