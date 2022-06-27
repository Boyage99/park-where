# 주차 어디 프로젝트

> GPS 좌표 기반의 일정 반경에 위치한 주차장 위치,정보 제공 앱

## 기능

- 회원가입, 로그인(JWT)
- 현재 위치정보로 원하는 반경(km)내의 주차장 정보 가져오기
- 원하는 주소지 근처의 일정 반경(km)내의 주차장 정보 가져오기
- 주차장에 대한 평점+후기 CRD(Create, Read, Delete)

## ⚒ Stack

- Flask
- Bootstrap
- JQuery

## 웹앱 화면

<사진을 넣어주세요1>
<사진을 넣어주세요2>
<사진을 넣어주세요3>
.
.
.

## 🚀 Trouble Shooting

- Flask SSL + EC2 인증 적용하기
- Header의 Token인증 미들웨어 적용하기

## 환경세팅

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
