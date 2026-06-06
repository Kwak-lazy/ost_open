import pytest
from src.user_input import validate_recommend_input


def test_validate_recommend_input_success():
    valid_data = {
        "age": 30,
        "height": 175.5,
        "weight": 70.0,
        "conditions": ["고혈압", "당뇨"],
        "pain_area": ["무릎"],
        "goal": "체중 감량",
    }
    parsed, error = validate_recommend_input(valid_data)
    assert error is None
    assert parsed["age"] == 30
    assert parsed["height"] == 175.5


def test_validate_recommend_input_missing_fields():
    invalid_data = {"age": 30}  # height, weight 누락
    parsed, error = validate_recommend_input(invalid_data)
    assert parsed is None
    assert "필수입니다" in error


def test_validate_recommend_input_invalid_range():
    invalid_data = {
        "age": 150,  # 범위 초과 (1~120)
        "height": 170,
        "weight": 70,
        "conditions": [],
        "pain_area": ["없음"],
        "goal": "건강 관리",
    }
    parsed, error = validate_recommend_input(invalid_data)
    assert parsed is None
    assert "age 는 1~120 사이" in error


def test_validate_recommend_input_invalid_condition():
    invalid_data = {
        "age": 30,
        "height": 170,
        "weight": 70,
        "conditions": ["외계질환"],  # 존재하지 않는 질환
        "pain_area": ["없음"],
        "goal": "건강 관리",
    }
    parsed, error = validate_recommend_input(invalid_data)
    assert parsed is None
    assert "유효하지 않은 기저 질환" in error