import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHealth:
    def test_status_ok(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200
        assert res.get_json()["status"] == "ok"


class TestRecommend:
    VALID_PAYLOAD = {
        "age": 45,
        "height": 175.0,
        "weight": 80.0,
        "conditions": ["고혈압"],
        "pain_area": "무릎",
        "goal": "건강 관리",
    }

    @patch("app.get_db", return_value=None)
    def test_success(self, _, client):
        res = client.post("/api/recommend", json=self.VALID_PAYLOAD)
        assert res.status_code == 200
        data = res.get_json()
        assert "bmi" in data
        assert "bmi_category" in data
        assert "recommended" in data
        assert isinstance(data["recommended"], list)

    @patch("app.get_db", return_value=None)
    def test_bmi_calculated(self, _, client):
        res = client.post("/api/recommend", json=self.VALID_PAYLOAD)
        data = res.get_json()
        assert data["bmi"] == 26.12
        assert data["bmi_category"] == "비만"

    @patch("app.get_db", return_value=None)
    def test_recommended_fields(self, _, client):
        res = client.post("/api/recommend", json=self.VALID_PAYLOAD)
        for ex in res.get_json()["recommended"]:
            assert "name" in ex
            assert "intensity" in ex
            assert "duration" in ex
            assert "score" in ex

    def test_missing_required_fields(self, client):
        res = client.post("/api/recommend", json={"age": 30})
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_empty_body(self, client):
        res = client.post("/api/recommend", json=None,
                          content_type="application/json")
        assert res.status_code == 400

    @patch("app.get_db", return_value=None)
    def test_no_conditions(self, _, client):
        payload = {**self.VALID_PAYLOAD, "conditions": [], "pain_area": "없음"}
        res = client.post("/api/recommend", json=payload)
        assert res.status_code == 200

    @patch("app.get_db", return_value=None)
    def test_forbidden_not_in_recommended(self, _, client):
        res = client.post("/api/recommend", json=self.VALID_PAYLOAD)
        data = res.get_json()
        rec_names = [ex["name"] for ex in data["recommended"]]
        for exercises in data["forbidden_by_source"].values():
            for ex in exercises:
                assert ex not in rec_names


class TestHistory:
    @patch("app.get_db", return_value=None)
    def test_no_db_returns_empty_list(self, _, client):
        res = client.get("/api/history")
        assert res.status_code == 200
        assert res.get_json() == []
