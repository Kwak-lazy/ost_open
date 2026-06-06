import pytest
import mongomock
from src import db


def test_get_db_without_uri(monkeypatch):
    # 환경 변수가 없을 때 None을 반환하는지 테스트
    monkeypatch.delenv("MONGO_URI", raising=False)
    db._client = None  # 싱글톤 초기화
    assert db.get_db() is None


def test_get_db_with_uri(monkeypatch):
    # 환경 변수가 있을 때 Mock 클라이언트를 반환하는지 테스트
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGO_DB", "test_db")

    # MongoClient 호출 시 mongomock을 사용하도록 패치
    monkeypatch.setattr("pymongo.MongoClient", mongomock.MongoClient)

    db._client = None  # 싱글톤 초기화
    database = db.get_db()

    assert database is not None
    assert database.name == "test_db"