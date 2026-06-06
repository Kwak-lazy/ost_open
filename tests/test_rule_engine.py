import pytest
from src.rule_engine import get_forbidden_set, get_cautions, score_exercise, apply_rules


def test_get_forbidden_set():
    # 고혈압과 무릎 통증이 있을 때 금지 운동 세트가 잘 결합되는지 확인
    forbidden = get_forbidden_set(["고혈압"], ["무릎"])
    assert "버피테스트" in forbidden  # 고혈압 금지
    assert "계단 오르기(고강도)" in forbidden  # 무릎 금지


def test_get_cautions():
    cautions = get_cautions(["당뇨"], ["허리"])
    assert "당뇨" in cautions
    assert "통증 부위(허리)" in cautions


def test_score_exercise_forbidden():
    # 금지된 운동은 무조건 -999점을 반환해야 함
    exercise = ("데드리프트", "고강도", 30)
    forbidden_set = {"데드리프트"}
    score = score_exercise(
        exercise,
        conditions=["허리디스크"],
        pain_area=["허리"],
        goal="근력 증가",
        age=30,
        bmi=22.0,
        forbidden_set=forbidden_set,
    )
    assert score == -999.0


def test_score_exercise_bonus():
    # 질환 추천 운동 및 목표 강도가 맞을 때 가산점이 붙는지 확인
    exercise = ("걷기", "저강도", 30)  # 고혈압 추천 운동(5.0) + 건강관리 강도(1.0) + 건강관리 시간(0.5)
    forbidden_set = set()
    score = score_exercise(
        exercise,
        conditions=["고혈압"],
        pain_area=["없음"],
        goal="건강 관리",
        age=30,
        bmi=22.0,
        forbidden_set=forbidden_set,
    )
    assert score == 6.5


def test_apply_rules():
    result = apply_rules(
        conditions=["고혈압"], pain_area=["무릎"], goal="건강 관리", age=30, bmi=22.0
    )
    assert "recommended" in result
    assert "forbidden_by_source" in result
    assert "cautions" in result
    # 상위 추천 운동 목록이 비어있지 않아야 함
    assert len(result["recommended"]) > 0