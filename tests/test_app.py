import pytest
from app import app
from src import db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_recommend_endpoint_success(client, monkeypatch):
    # DB 저장을 모킹하여 실제 DB 없이 테스트 진행
    monkeypatch.setattr(db, "get_db", lambda: None)

    payload = {
        "age": 28,
        "height": 180.0,
        "weight": 75.0,
        "conditions": ["당뇨"],
        "pain_area": ["없음"],
        "goal": "건강 관리",
    }

    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200

    json_data = response.get_json()
    assert "bmi" in json_data
    assert "bmi_category" in json_data
    assert "recommended" in json_data
    assert isinstance(json_data["recommended"], list)


def test_recommend_endpoint_bad_request(client):
    # 잘못된 요청 데이터 전송 시 400 에러 반환 검증
    payload = {
        "age": -5,  # 잘못된 나이
        "height": 180.0,
        "weight": 75.0,
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()