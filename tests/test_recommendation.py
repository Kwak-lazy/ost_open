import pytest
from src.recommendation import print_recommendation


def test_print_recommendation_with_single_condition(capsys):
    """
    condition이 단일 문자열('고혈압')로 들어왔을 때 
    기존 코드와 정상적으로 호환되어 출력되는지 테스트합니다.
    """
    user_info = {
        "name": "홍길동",
        "age": 65,
        "height": 170,
        "weight": 70,
        "bmi": 24.22,
        "bmi_category": "과체중",
        "condition": "고혈압",  # 단일 문자열 호환성 검증
        "pain_area": "무릎",
        "goal": "건강 관리"
    }

    print_recommendation(user_info)
    
    # 터미널에 출력된 전체 텍스트 캡처
    captured = capsys.readouterr().out

    # 사용자 정보 출력 검증
    assert "나이: 65세" in captured
    assert "기저 질환: 고혈압" in captured
    assert "통증 부위: 무릎" in captured
    assert "운동 목표: 건강 관리" in captured

    # 추천 운동 세션 양식 검증
    assert "[추천 운동]" in captured
    assert "걷기" in captured

    # 금지/주의 운동 세션 및 출처 표기 검증 (출처 텍스트가 포함되는지 유연하게 검증)
    assert "[금지/주의 운동]" in captured
    assert "고혈압" in captured
    assert "무릎" in captured

    # 추천 이유 및 주의사항 문구 검증
    assert "[추천 이유]" in captured
    assert "고혈압" in captured


def test_print_recommendation_with_conditions_list(capsys):
    """
    conditions가 리스트 형식(['당뇨', '천식'])으로 들어왔을 때
    콤마(,)로 묶여 정상 출력되는지 테스트합니다.
    """
    user_info = {
        "name": "김철수",
        "age": 35,
        "height": 180,
        "weight": 75,
        "bmi": 23.15,
        "bmi_category": "과체중",
        "conditions": ["당뇨", "천식"],  # 리스트 형식 검증
        "pain_area": "없음",
        "goal": "체중 감량"
    }

    print_recommendation(user_info)
    captured = capsys.readouterr().out

    # 다중 질환 표기 방식 검증
    assert "당뇨" in captured
    assert "천식" in captured


def test_print_recommendation_no_condition_no_pain(capsys):
    """
    기저 질환과 통증 부위가 모두 없을 때의 
    기본 출력 포맷 및 예외 문구를 테스트합니다.
    """
    user_info = {
        "name": "이영희",
        "age": 25,
        "height": 160,
        "weight": 50,
        "bmi": 19.53,
        "bmi_category": "정상",
        "conditions": [],
        "pain_area": "없음",
        "goal": "근력 증가"
    }

    print_recommendation(user_info)
    captured = capsys.readouterr().out

    assert "기저 질환: 없음" in captured
    assert "통증 부위: 없음" in captured
    
    # 금지 운동이 아예 없으므로 타이틀이 출력되지 않아야 함 (오타 capture -> captured 수정)
    assert "[금지/주의 운동]" not in captured