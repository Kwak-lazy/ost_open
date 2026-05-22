def calculate_bmi(height_cm, weight_kg):
    """키와 체중을 이용해 BMI를 계산하는 함수"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi):
    """BMI 수치를 기준으로 체중 상태를 분류하는 함수"""
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "과체중"
    else:
        return "비만"


def get_user_input():
    """사용자 건강 정보를 입력받는 함수"""
    print("건강 데이터 기반 개인 맞춤형 운동 추천 시스템")
    print("-" * 50)

    age = int(input("나이를 입력하세요: "))
    height = float(input("키를 입력하세요(cm): "))
    weight = float(input("체중을 입력하세요(kg): "))
    disease = input("기저 질환을 입력하세요(고혈압/당뇨/허리디스크/천식/심장질환/관절염/골다공증/비만/없음): ")
    pain_area = input("통증 부위를 입력하세요(무릎/허리/어깨/목/손목/발목/고관절/팔꿈치/없음): ")
    goal = input("운동 목표를 입력하세요(체중 감량/근력 증가/건강 관리): ")

    return {
        "age": age,
        "height": height,
        "weight": weight,
        "disease": disease,
        "pain_area": pain_area,
        "goal": goal
    }


def recommend_by_disease(disease):
    """질환별 추천 운동과 금지 운동을 반환하는 함수"""
    rules = {
        "고혈압": {
            "recommend": ["걷기", "가벼운 자전거", "스트레칭"],
            "avoid": ["고강도 인터벌 운동", "무거운 중량 운동"],
            "reason": "고혈압이 있는 경우 혈압이 급격히 상승할 수 있는 고강도 운동은 주의가 필요합니다."
        },
        "당뇨": {
            "recommend": ["걷기", "가벼운 근력 운동", "실내 자전거"],
            "avoid": ["공복 고강도 운동"],
            "reason": "당뇨가 있는 경우 혈당 변동을 고려해야 하므로 무리한 공복 운동은 주의가 필요합니다."
        },
        "허리디스크": {
            "recommend": ["걷기", "가벼운 스트레칭", "코어 안정화 운동"],
            "avoid": ["데드리프트", "윗몸일으키기", "무거운 스쿼트"],
            "reason": "허리에 큰 압박이 가는 운동은 통증을 악화시킬 수 있습니다."
        },
        "천식": {
            "recommend": ["걷기", "가벼운 자전거", "호흡 조절 운동"],
            "avoid": ["장시간 고강도 달리기", "찬 공기 속 고강도 운동"],
            "reason": "천식이 있는 경우 호흡 부담이 큰 운동은 주의가 필요합니다."
        },
        "심장질환": {
            "recommend": ["가벼운 걷기", "저강도 자전거", "스트레칭"],
            "avoid": ["고강도 인터벌 운동", "전력 질주", "무거운 중량 운동"],
            "reason": "심장질환이 있는 경우 심박수가 급격히 올라가는 운동은 주의가 필요합니다."
        },
        "관절염": {
            "recommend": ["수중 운동", "실내 자전거", "가벼운 스트레칭"],
            "avoid": ["점프 운동", "장거리 달리기"],
            "reason": "관절염이 있는 경우 관절 충격이 큰 운동은 피하는 것이 좋습니다."
        },
        "골다공증": {
            "recommend": ["걷기", "가벼운 근력 운동", "균형 운동"],
            "avoid": ["과도한 허리 굽힘", "충격 큰 점프 운동"],
            "reason": "골다공증이 있는 경우 낙상 위험이나 척추에 부담이 큰 운동은 주의가 필요합니다."
        },
        "비만": {
            "recommend": ["걷기", "실내 자전거", "수영", "저강도 유산소"],
            "avoid": ["점프 운동", "갑작스러운 고강도 운동"],
            "reason": "비만인 경우 관절 부담을 줄이기 위해 저충격 운동부터 시작하는 것이 좋습니다."
        },
        "없음": {
            "recommend": ["걷기", "스쿼트", "팔굽혀펴기", "스트레칭"],
            "avoid": [],
            "reason": "특별한 기저 질환이 없어 일반적인 운동을 추천합니다."
        }
    }

    return rules.get(disease, rules["없음"])



def filter_by_pain(pain_area):
    """통증 부위별 추천 운동과 금지 운동을 반환하는 함수"""
    rules = {
        "무릎": {
            "recommend": ["실내 자전거", "상체 운동", "가벼운 스트레칭"],
            "avoid": ["점프 운동", "런지", "계단 오르기"],
            "reason": "무릎 통증이 있는 경우 관절에 충격이 가는 운동은 피하는 것이 좋습니다."
        },
        "허리": {
            "recommend": ["걷기", "가벼운 스트레칭", "코어 안정화 운동"],
            "avoid": ["데드리프트", "윗몸일으키기"],
            "reason": "허리 통증이 있는 경우 허리를 과도하게 굽히는 운동은 주의가 필요합니다."
        },
        "어깨": {
            "recommend": ["걷기", "하체 운동", "가벼운 스트레칭"],
            "avoid": ["숄더프레스", "팔굽혀펴기"],
            "reason": "어깨 통증이 있는 경우 어깨 관절에 부담이 가는 운동은 피하는 것이 좋습니다."
        },
        "목": {
            "recommend": ["걷기", "목 주변 가벼운 스트레칭", "저강도 유산소"],
            "avoid": ["목에 힘이 많이 들어가는 운동", "무거운 중량 운동"],
            "reason": "목 통증이 있는 경우 목과 승모근에 과도한 긴장이 생기는 운동은 주의가 필요합니다."
        },
        "손목": {
            "recommend": ["걷기", "하체 운동", "실내 자전거"],
            "avoid": ["팔굽혀펴기", "플랭크", "무거운 덤벨 운동"],
            "reason": "손목 통증이 있는 경우 체중이 손목에 실리는 운동은 피하는 것이 좋습니다."
        },
        "발목": {
            "recommend": ["실내 자전거", "수영", "상체 운동"],
            "avoid": ["달리기", "점프 운동", "방향 전환 운동"],
            "reason": "발목 통증이 있는 경우 충격이나 방향 전환이 큰 운동은 주의가 필요합니다."
        },
        "고관절": {
            "recommend": ["걷기", "수중 운동", "가벼운 하체 스트레칭"],
            "avoid": ["깊은 스쿼트", "과도한 런지"],
            "reason": "고관절 통증이 있는 경우 관절 가동 범위를 과하게 사용하는 운동은 주의가 필요합니다."
        },
        "팔꿈치": {
            "recommend": ["걷기", "하체 운동", "가벼운 스트레칭"],
            "avoid": ["턱걸이", "무거운 덤벨 컬", "팔굽혀펴기"],
            "reason": "팔꿈치 통증이 있는 경우 팔꿈치에 반복적인 부하가 걸리는 운동은 피하는 것이 좋습니다."
        },
        "없음": {
            "recommend": [],
            "avoid": [],
            "reason": "특별한 통증 부위가 없습니다."
        }
    }

    return rules.get(pain_area, rules["없음"])




def make_recommendation(user_data):
    """사용자 정보를 바탕으로 최종 추천 결과를 만드는 함수"""
    disease_result = recommend_by_disease(user_data["disease"])
    pain_result = filter_by_pain(user_data["pain_area"])

    recommend = disease_result["recommend"] + pain_result["recommend"]
    avoid = disease_result["avoid"] + pain_result["avoid"]

    recommend = list(dict.fromkeys(recommend))
    avoid = list(dict.fromkeys(avoid))

    recommend = [exercise for exercise in recommend if exercise not in avoid]

    reasons = [
        disease_result["reason"],
        pain_result["reason"]
    ]

    return recommend, avoid, reasons


def print_result(user_data, bmi, bmi_status, recommend, avoid, reasons):
    """최종 결과를 출력하는 함수"""
    print("\n" + "=" * 50)
    print("운동 추천 결과")
    print("=" * 50)

    print("\n[사용자 정보]")
    print(f"나이: {user_data['age']}세")
    print(f"키: {user_data['height']}cm")
    print(f"체중: {user_data['weight']}kg")
    print(f"BMI: {bmi}")
    print(f"BMI 분류: {bmi_status}")
    print(f"기저 질환: {user_data['disease']}")
    print(f"통증 부위: {user_data['pain_area']}")
    print(f"운동 목표: {user_data['goal']}")

    print("\n[추천 운동]")
    if recommend:
        for exercise in recommend:
            print(f"- {exercise}")
    else:
        print("- 추천 가능한 운동이 부족합니다.")

    print("\n[금지/주의 운동]")
    if avoid:
        for exercise in avoid:
            print(f"- {exercise}")
    else:
        print("- 특별히 제한할 운동이 없습니다.")

    print("\n[추천 이유]")
    for reason in reasons:
        print(f"- {reason}")

    print("\n[주의사항]")
    print("※ 본 시스템의 결과는 참고용이며 의학적 진단을 대체하지 않습니다.")
    print("※ 운동 전 반드시 전문가 상담을 권장합니다.")

def main():
    user_data = get_user_input()

    bmi = calculate_bmi(user_data["height"], user_data["weight"])
    bmi_status = classify_bmi(bmi)

    recommend, avoid, reasons = make_recommendation(user_data)

    print_result(user_data, bmi, bmi_status, recommend, avoid, reasons)


if __name__ == "__main__":
    main()
