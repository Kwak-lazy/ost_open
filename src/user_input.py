from src.rule_engine import CONDITION_RULES, PAIN_RULES, GOAL_RULES

VALID_CONDITIONS = set(CONDITION_RULES.keys())
VALID_PAIN_AREAS = set(PAIN_RULES.keys())
VALID_GOALS = set(GOAL_RULES.keys())


def validate_recommend_input(data: dict) -> tuple[dict | None, str | None]:
    """
    추천 요청 입력값을 검증한다.

    Returns:
        (parsed_input, None)  — 정상
        (None, error_message) — 오류
    """
    if not data:
        return None, "요청 본문이 없습니다."

    age = data.get("age")
    height = data.get("height")
    weight = data.get("weight")

    if age is None or height is None or weight is None:
        return None, "age, height, weight 는 필수입니다."

    try:
        age = int(age)
        height = float(height)
        weight = float(weight)
    except (TypeError, ValueError):
        return None, "age, height, weight 는 숫자여야 합니다."

    if not (1 <= age <= 120):
        return None, "age 는 1~120 사이여야 합니다."
    if not (50 <= height <= 250):
        return None, "height 는 50~250(cm) 사이여야 합니다."
    if not (10 <= weight <= 300):
        return None, "weight 는 10~300(kg) 사이여야 합니다."

    conditions = data.get("conditions", [])
    if not isinstance(conditions, list):
        return None, "conditions 는 리스트여야 합니다."
    invalid_cond = [c for c in conditions if c not in VALID_CONDITIONS]
    if invalid_cond:
        return None, f"유효하지 않은 기저 질환: {invalid_cond}"

    pain_area = data.get("pain_area", ["없음"])
    if not isinstance(pain_area, list):
        return None, "pain_area 는 리스트여야 합니다."
    invalid_pain = [p for p in pain_area if p not in VALID_PAIN_AREAS]
    if invalid_pain:
        return None, f"유효하지 않은 통증 부위: {invalid_pain}"

    goal = data.get("goal", "건강 관리")
    if goal not in VALID_GOALS:
        return None, f"유효하지 않은 운동 목표: {goal}"

    return {
        "age": age,
        "height": height,
        "weight": weight,
        "conditions": conditions,
        "pain_area": pain_area,
        "goal": goal,
    }, None
