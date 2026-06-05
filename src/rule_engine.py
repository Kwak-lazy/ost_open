# src/rule_engine.py
# 기저질환 + 통증부위 + 운동목표를 모두 반영한 룰 엔진

# ──────────────────────────────────────────────
# 1. 데이터 레이어 (기존 코드에 있던 데이터 → 여기로 통합)
# ──────────────────────────────────────────────

# {질환: {"forbidden": [...], "recommended": [(이름, 강도, 분)], "caution": str}}
CONDITION_RULES = {
    "고혈압": {
        "forbidden": ["무거운 역도", "버피테스트", "고강도 인터벌 트레이닝", "레슬링", "복싱"],
        "recommended": [
            ("걷기", "저강도", 30), ("수영", "저강도", 30),
            ("자전거 타기(평지)", "저강도", 30), ("스트레칭", "저강도", 20),
            ("요가(하타)", "저강도", 30),
        ],
        "caution": "혈압이 180/110 이상이면 운동 전 의사와 상담하세요.",
    },
    "당뇨": {
        "forbidden": ["공복 고강도 운동", "극한 마라톤"],
        "recommended": [
            ("걷기", "저강도", 30), ("수영", "중강도", 30),
            ("저항 운동(가벼운 덤벨)", "중강도", 20),
            ("자전거 타기", "저강도", 30), ("댄스", "중강도", 30),
        ],
        "caution": "운동 전후 혈당을 반드시 측정하세요. 저혈당 시 즉시 중단.",
    },
    "허리디스크": {
        "forbidden": ["데드리프트", "윗몸일으키기", "무거운 스쿼트", "달리기", "역도"],
        "recommended": [
            ("수영(배영)", "저강도", 20), ("걷기(평지)", "저강도", 20),
            ("코어 안정화 운동", "저강도", 15), ("가벼운 스트레칭", "저강도", 20),
            ("필라테스(전문가 지도)", "저강도", 20),
        ],
        "caution": "통증이 있을 때는 운동하지 마세요. 물리치료사 지도를 권장합니다.",
    },
    "천식": {
        "forbidden": ["차가운 공기 중 달리기", "먼지 많은 환경 운동"],
        "recommended": [
            ("수영(따뜻한 물)", "중강도", 30), ("걷기", "저강도", 30),
            ("요가", "저강도", 30), ("자전거 타기(실내)", "중강도", 20),
        ],
        "caution": "운동 전 흡입기를 준비하세요. 증상 발생 시 즉시 중단.",
    },
    "심장질환": {
        "forbidden": ["무거운 역도", "고강도 인터벌 트레이닝", "버피테스트", "스프린트", "복싱"],
        "recommended": [
            ("걷기(평지)", "저강도", 20), ("수중 걷기", "저강도", 20),
            ("스트레칭", "저강도", 15), ("태극권", "저강도", 20),
        ],
        "caution": "가슴 통증, 호흡곤란 시 즉시 중단. 심장 전문의 허가 후 운동.",
    },
    "관절염": {
        "forbidden": ["달리기(장거리)", "점프 운동", "스쿼트(깊은)", "축구", "농구"],
        "recommended": [
            ("수영", "저강도", 30), ("수중 에어로빅", "저강도", 30),
            ("자전거 타기(고정식)", "저강도", 20), ("스트레칭", "저강도", 20),
        ],
        "caution": "관절 통증이 심해지면 즉시 중단하고 휴식을 취하세요.",
    },
    "골다공증": {
        "forbidden": ["높은 충격 점프", "격렬한 비틀기", "무거운 역도"],
        "recommended": [
            ("걷기", "중강도", 30), ("태극권", "저강도", 30),
            ("필라테스", "저강도", 30), ("저항 운동(가벼운)", "저강도", 20),
        ],
        "caution": "낙상 위험이 높은 운동은 피하세요. 균형 훈련을 병행하세요.",
    },
    "비만": {
        "forbidden": ["고강도 점프 운동(초보자)", "무거운 역도(초보자)"],
        "recommended": [
            ("수영", "중강도", 45), ("걷기(빠르게)", "중강도", 45),
            ("자전거 타기", "중강도", 40), ("수중 에어로빅", "중강도", 40),
        ],
        "caution": "점진적으로 운동 강도와 시간을 늘려가세요.",
    },
}

# {통증부위: {"forbidden": [...], "caution": str}}
PAIN_RULES = {
    "무릎": {
        "forbidden": ["달리기(장거리)", "점프 운동", "스쿼트(깊은)", "계단 오르기(고강도)", "농구", "축구"],
        "caution": "무릎에 충격이 가는 운동을 피하고, 수중 운동을 권장합니다.",
    },
    "허리": {
        "forbidden": ["데드리프트", "윗몸일으키기", "무거운 스쿼트", "달리기", "역도"],
        "caution": "허리를 과도하게 굽히거나 비트는 동작은 피하세요.",
    },
    "어깨": {
        "forbidden": ["수영(접영)", "무거운 overhead press", "테니스(서브)", "야구(투구)"],
        "caution": "팔을 머리 위로 올리는 동작은 피하세요.",
    },
    "목": {
        "forbidden": ["헤드스탠드", "무거운 숄더프레스", "격렬한 수영"],
        "caution": "목에 압박이 가는 동작과 급격한 회전을 피하세요.",
    },
    "손목": {
        "forbidden": ["푸시업", "역도", "테니스", "배드민턴(강타)"],
        "caution": "손목에 체중을 싣는 동작을 피하세요.",
    },
    "발목": {
        "forbidden": ["달리기", "점프 운동", "축구", "농구", "등산(급경사)"],
        "caution": "발목에 충격이 가는 운동을 피하고, 평지 걷기나 수중 운동을 권장합니다.",
    },
    "고관절": {
        "forbidden": ["깊은 스쿼트", "달리기(장거리)", "축구", "급격한 방향 전환"],
        "caution": "고관절에 부담이 가는 자세는 피하세요.",
    },
    "팔꿈치": {
        "forbidden": ["테니스", "배드민턴", "역도(팔꿈치 굴곡)", "푸시업"],
        "caution": "팔꿈치에 반복 충격이 가는 운동을 피하세요.",
    },
    "없음": {
        "forbidden": [],
        "caution": "",
    },
}

# {운동목표: {"preferred_intensity": [str], "score_bonus": float, "notes": str}}
GOAL_RULES = {
    "체중 감량": {
        "preferred_intensity": ["중강도", "고강도"],
        "min_duration": 40,           # 권장 최소 운동 시간(분)
        "score_bonus": 1.5,           # 해당 강도 운동에 추가 점수
        "notes": "유산소 위주, 40분 이상 지속 운동을 권장합니다.",
    },
    "근력 증가": {
        "preferred_intensity": ["중강도", "고강도"],
        "min_duration": 30,
        "score_bonus": 1.5,
        "notes": "저항 운동 위주, 단백질 섭취를 병행하세요.",
    },
    "건강 관리": {
        "preferred_intensity": ["저강도", "중강도"],
        "min_duration": 20,
        "score_bonus": 1.0,
        "notes": "규칙적인 운동 습관 형성을 목표로 하세요.",
    },
}

# 기저질환 없을 때 일반 추천 운동 풀
GENERAL_EXERCISES = [
    ("달리기", "고강도", 30), ("수영", "중강도", 45),
    ("자전거 타기", "중강도", 40), ("요가", "저강도", 40),
    ("필라테스", "저강도", 40), ("댄스", "중강도", 40),
    ("등산", "중강도", 60), ("테니스", "중강도", 45),
    ("고강도 인터벌 트레이닝", "고강도", 25),
    ("스트레칭", "저강도", 20), ("걷기", "저강도", 45),
    ("저항 운동", "중강도", 40), ("플랭크", "중강도", 15),
    ("수영(배영)", "저강도", 30),
]


def get_forbidden_set(conditions: list, pain_area: list) -> set:
    """질환 + 통증 부위를 모두 고려한 금지 운동 집합 반환."""
    forbidden = set()
    for cond in conditions:
        if cond in CONDITION_RULES:
            forbidden.update(CONDITION_RULES[cond]["forbidden"])
    if pain_area:
        for area in pain_area:
            if area in PAIN_RULES:
                forbidden.update(PAIN_RULES[area]["forbidden"])
    return forbidden


def get_cautions(conditions: list, pain_area: list) -> dict:
    """질환 + 통증 부위 주의사항 반환."""
    cautions = {}
    for cond in conditions:
        if cond in CONDITION_RULES and CONDITION_RULES[cond].get("caution"):
            cautions[cond] = CONDITION_RULES[cond]["caution"]
    if pain_area:
        for area in pain_area:
            if area in PAIN_RULES and PAIN_RULES[area].get("caution"):
                cautions[f"통증 부위({area})"] = PAIN_RULES[area]["caution"]
    return cautions


def score_exercise(exercise: tuple, conditions: list,
                   pain_area: list, goal: str,
                   age: int, bmi: float,
                   forbidden_set: set) -> float:
    """
    운동 적합도 점수 계산.

    가산점 항목
    ──────────────────────────────────────────
    질환 추천 운동 일치          +5.0 / 질환
    통증 부위 금지 운동 아님     (금지면 -999)
    운동목표 강도 일치           +goal_bonus
    나이 60세 이상 저강도        +2.0
    나이 40~59세 중강도이하      +1.0
    BMI 25 이상 저/중강도        +1.0
    ──────────────────────────────────────────
    """
    name, intensity, duration = exercise

    if name in forbidden_set:
        return -999.0

    score = 0.0

    # 질환 추천 운동 가산
    for cond in conditions:
        if cond in CONDITION_RULES:
            rec_names = [r[0] for r in CONDITION_RULES[cond]["recommended"]]
            if name in rec_names:
                score += 5.0

    # 운동 목표 강도 가산
    if goal and goal in GOAL_RULES:
        goal_info = GOAL_RULES[goal]
        if intensity in goal_info["preferred_intensity"]:
            score += goal_info["score_bonus"]
        if duration >= goal_info["min_duration"]:
            score += 0.5

    # 나이 기반 강도 선호
    intensity_val = {"저강도": 1, "중강도": 2, "고강도": 3}.get(intensity, 2)
    if age >= 60 and intensity_val == 1:
        score += 2.0
    elif 40 <= age < 60 and intensity_val <= 2:
        score += 1.0

    # BMI 과체중 이상이면 저/중강도 선호
    if bmi >= 25.0 and intensity_val <= 2:
        score += 1.0

    return score


def apply_rules(conditions: list, pain_area: list, goal: str,
                age: int, bmi: float, top_n: int = 5) -> dict:
    """
    전체 룰을 적용해 추천 결과 딕셔너리 반환.

    Returns:
        {
          "recommended": [(이름, 강도, 시간, 점수), ...],
          "forbidden_by_source": {출처: [운동명, ...]},
          "cautions": {출처: str},
          "goal_notes": str,
        }
    """
    forbidden_set = get_forbidden_set(conditions, pain_area)

    # 후보 운동 수집 (질환별 추천 + 일반 풀)
    candidates = list(GENERAL_EXERCISES)
    seen = set(ex[0] for ex in candidates)
    for cond in conditions:
        if cond in CONDITION_RULES:
            for ex in CONDITION_RULES[cond]["recommended"]:
                if ex[0] not in seen:
                    candidates.append(ex)
                    seen.add(ex[0])

    # 점수 계산 및 정렬
    scored = sorted(
        [(*ex, score_exercise(ex, conditions, pain_area, goal, age, bmi, forbidden_set))
         for ex in candidates],
        key=lambda x: x[3],
        reverse=True,
    )
    recommended = [(n, i, d, s) for n, i, d, s in scored if s >= 0][:top_n]

    # 금지 운동 출처별 정리
    forbidden_by_source = {}
    for cond in conditions:
        if cond in CONDITION_RULES:
            forbidden_by_source[cond] = CONDITION_RULES[cond]["forbidden"]
    if pain_area:
        for area in pain_area:
            if area in PAIN_RULES and PAIN_RULES[area]["forbidden"]:
                forbidden_by_source[f"통증 부위({area})"] = PAIN_RULES[area]["forbidden"]

    return {
        "recommended": recommended,
        "forbidden_by_source": forbidden_by_source,
        "cautions": get_cautions(conditions, pain_area),
        "goal_notes": GOAL_RULES.get(goal, {}).get("notes", ""),
    }
