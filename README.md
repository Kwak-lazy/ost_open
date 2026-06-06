# Personalized exercise recommendation system

건강 데이터 기반 개인 맞춤형 운동 추천 시스템

## 프로젝트 소개

사용자의 건강 정보와 기저 질환 정보를 기반으로 추천 운동과 금지 운동을 제공하는 시스템입니다.

## 주요 기능

- 사용자 건강 정보 입력
- BMI 계산 및 체중 상태 분류
- 기저 질환 기반 추천 운동 제공
- 통증 부위 기반 금지/주의 운동 필터링
- 추천 이유 출력

## 기술 스택 및 의존성
본 프로젝트는 아래 명시된 환경 및 라이브러리 버전을 기준으로 개발 및 테스트되었으며, 정상적인 구동을 위해 해당 스펙을 충족해야 합니다.

### 1. 운영체제 (OS) 및 런타임 환경
- OS: Windows 10 / 11, macOS (Ventura 이상), Linux (Ubuntu 22.04 LTS 이상)
- Runtime: Python 3.14.0a1+ (또는 Python 3.10+ 호환)

### 2. 주요 백엔드 패키지
- Flask (v3.1.0): 웹 애플리케이션 프레임워크 및 라우팅 제어
- Flask-CORS (v5.0.0): 프론트엔드와 백엔드 간의 교차 출처 자원 공유(CORS) 허용 및 통신 보안 정책 적용
- python-dotenv (v1.0.1): `.env` 환경 변수 파일 로드 및 인프라 설정 관리
- PyMongo (v4.11.1): NoSQL 데이터베이스 MongoDB 커넥션 생성 및 데이터 적재 제어

## 설치 방법

### 1. 저장소 클론 및 폴더 진입
```bash
git clone <본인의-레포지토리-주소>
cd ost_test
```

## 실행 방법

### 1. 최상위 디렉토리에서 아래 명령어를 실행하여 프론트엔드와 백엔드가 결합된 통합 Flask 서버를 실행합니다.
```bash
python app.py
```

### 2. 브라우저를 열고 아래 주소로 접속하면 정보 입력 화면이 나타납니다.
```Plaintext
http://127.0.0.1:5000
```
### Unit Test 실행 방법
```
pip install pytest pytest-cov mongomock flask flask-cors python-dotenv pymongo

python -m pytest --cov=.
```

## 라이선스

The MIT License (MIT)

Copyright (c) <2026> <Personalized_exercise_recommendation_system>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contributor Name

- 곽동현 (Kwak-lazy)
- 김진식 (2023040007)
- Xu Horan (3321675635@qq.com)
- DINH VAN TUAN KHANH