# src/recommendation.py
# rule_engine 결과를 받아 터미널에 출력하는 모듈
# 기존 출력 포맷을 최대한 유지하면서 통증부위·운동목표 반영

from src.rule_engine import apply_rules

INTENSITY_MARK = {"저강도": "🟢", "중강도": "🟡", "고강도": "🔴"}


def _sep(char="─", n=50):
    print(char * n)


# ── 핵심 공개 함수 ──────────────────────────────────────

def print_recommendation(user_info: dict) -> None:
    """
    user_info 딕셔너리를 받아 추천 결과를 출력한다.

    user_info 키:
        name, age, height, weight, bmi, bmi_category,
        condition (str),   ← 기존 단일 문자열도 호환
        conditions (list), ← 리스트 형식 우선
        pain_area (str),
        goal (str),
    """
    # 기존 코드와 호환 — condition 단일 문자열도 수용
    conditions = user_info.get("conditions") or []
    if not conditions:
        raw = user_info.get("condition", "없음")
        conditions = [] if raw == "없음" else [raw]

    pain_area = user_info.get("pain_area", "없음")
    goal      = user_info.get("goal", "건강 관리")
    age       = user_info.get("age", 30)
    bmi       = user_info.get("bmi", 22.0)

    result = apply_rules(conditions, pain_area, goal, age, bmi)

    _print_user_info(user_info, conditions, pain_area, goal)
    _print_recommended(result["recommended"])
    _print_forbidden(result["forbidden_by_source"])
    _print_reason(result, conditions, pain_area)
    _print_cautions(result["cautions"])


# ── 출력 헬퍼 ──────────────────────────────────────────

def _print_user_info(info: dict, conditions: list, pain_area: str, goal: str) -> None:
    print("\n" + "=" * 50)
    print("운동 추천 결과")
    print("=" * 50)
    print("\n[사용자 정보]")
    print(f"나이: {info.get('age')}세")
    print(f"키: {info.get('height')}cm")
    print(f"체중: {info.get('weight')}kg")
    print(f"BMI: {info.get('bmi')}")
    print(f"BMI 분류: {info.get('bmi_category')}")
    print(f"기저 질환: {', '.join(conditions) if conditions else '없음'}")
    print(f"통증 부위: {pain_area}")
    print(f"운동 목표: {goal}")


def _print_recommended(recommended: list) -> None:
    print("\n[추천 운동]")
    if not recommended:
        print("- 조건에 맞는 추천 운동이 없습니다.")
        return
    for rank, (name, intensity, minutes, _) in enumerate(recommended, 1):
        mark = INTENSITY_MARK.get(intensity, "⚪")
        print(f"{rank}. {name}  {mark} {intensity} / {minutes}분")


def _print_forbidden(forbidden_by_source: dict) -> None:
    if not forbidden_by_source:
        return
    print("\n[금지/주의 운동]")
    for source, exercises in forbidden_by_source.items():
        print(f"  [{source}]")
        for ex in exercises:
            print(f"  - {ex}")


def _print_reason(result: dict, conditions: list, pain_area: str) -> None:
    print("\n[추천 이유]")
    if conditions:
        print(f"- {', '.join(conditions)} 질환을 고려하여 무리가 없는 운동을 우선 추천했습니다.")
    if pain_area and pain_area != "없음":
        print(f"- {pain_area} 통증 부위에 부담이 가는 운동은 금지 목록에서 제외했습니다.")
    if result.get("goal_notes"):
        print(f"- {result['goal_notes']}")


def _print_cautions(cautions: dict) -> None:
    print("\n[주의사항]")
    for source, msg in cautions.items():
        print(f"- [{source}] {msg}")
    print("- 본 결과는 프로젝트용 일반 운동 추천 예시입니다.")
    print("- 실제 질환이나 통증이 있는 경우 전문가 상담이 필요합니다.")
    print("- 운동 중 통증이 발생하면 즉시 중단해야 합니다.")
