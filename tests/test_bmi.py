import pytest
from src.bmi import calculate_bmi, classify_bmi
from src.rule_engine import apply_rules


class TestCalculateBmi:
    def test_normal_value(self):
        assert calculate_bmi(175, 70) == 22.86

    def test_tall_heavy(self):
        bmi = calculate_bmi(190, 100)
        assert bmi == round(100 / (1.9 ** 2), 2)

    def test_returns_float(self):
        assert isinstance(calculate_bmi(160, 55), float)


class TestClassifyBmi:
    def test_underweight(self):
        assert classify_bmi(17.0) == "저체중"

    def test_normal(self):
        assert classify_bmi(21.0) == "정상"

    def test_overweight(self):
        assert classify_bmi(23.5) == "과체중"

    def test_obese(self):
        assert classify_bmi(27.0) == "비만"

    def test_boundary_underweight(self):
        assert classify_bmi(18.4) == "저체중"

    def test_boundary_normal(self):
        assert classify_bmi(18.5) == "정상"

    def test_boundary_overweight(self):
        assert classify_bmi(23.0) == "과체중"

    def test_boundary_obese(self):
        assert classify_bmi(25.0) == "비만"


class TestApplyRules:
    def test_returns_required_keys(self):
        result = apply_rules([], "없음", "건강 관리", 30, 22.0)
        assert "recommended" in result
        assert "forbidden_by_source" in result
        assert "cautions" in result
        assert "goal_notes" in result

    def test_recommended_top_n(self):
        result = apply_rules([], "없음", "건강 관리", 30, 22.0, top_n=3)
        assert len(result["recommended"]) <= 3

    def test_forbidden_excluded_from_recommended(self):
        result = apply_rules(["허리디스크"], "없음", "건강 관리", 30, 22.0)
        rec_names = [ex[0] for ex in result["recommended"]]
        for forbidden in result["forbidden_by_source"].get("허리디스크", []):
            assert forbidden not in rec_names

    def test_condition_caution_included(self):
        result = apply_rules(["고혈압"], "없음", "건강 관리", 30, 22.0)
        assert "고혈압" in result["cautions"]

    def test_pain_area_forbidden_included(self):
        result = apply_rules([], "무릎", "건강 관리", 30, 22.0)
        assert "통증 부위(무릎)" in result["forbidden_by_source"]

    def test_no_condition_no_caution(self):
        result = apply_rules([], "없음", "건강 관리", 30, 22.0)
        assert result["cautions"] == {}

    def test_goal_notes_present(self):
        result = apply_rules([], "없음", "체중 감량", 30, 22.0)
        assert result["goal_notes"] != ""

    def test_elderly_prefers_low_intensity(self):
        result = apply_rules([], "없음", "건강 관리", 65, 22.0)
        top = result["recommended"][0]
        assert top[1] == "저강도"

    def test_multiple_conditions(self):
        result = apply_rules(["고혈압", "당뇨"], "없음", "건강 관리", 50, 22.0)
        assert "고혈압" in result["forbidden_by_source"]
        assert "당뇨" in result["forbidden_by_source"]
