import pytest
from src.bmi import calculate_bmi, classify_bmi


def test_calculate_bmi():
    # 키 170cm, 몸무게 70kg -> 70 / (1.7^2) = 24.2214... -> 반올림하여 24.22
    assert calculate_bmi(170, 70) == 24.22
    # 키 160cm, 몸무게 50kg -> 50 / (1.6^2) = 19.5312... -> 반올림하여 19.53
    assert calculate_bmi(160, 50) == 19.53


@pytest.mark.parametrize(
    "bmi, expected",
    [
        (18.0, "저체중"),
        (18.5, "정상"),
        (22.9, "정상"),
        (23.0, "과체중"),
        (24.9, "과체중"),
        (25.0, "비만"),
        (30.0, "비만"),
    ],
)
def test_classify_bmi(bmi, expected):
    assert classify_bmi(bmi) == expected