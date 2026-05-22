import json


def load_rules(file_path):
    """운동 추천 규칙 JSON 파일을 불러오는 함수"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def remove_duplicates(items):
    """리스트에서 중복을 제거하는 함수"""
    return list(dict.fromkeys(items))


def get_user_input():
    """사용자 입력을 받는 함수"""
    print("건강 데이터 기반 운동 추천 시스템")
    print("-" * 40)

    age = int(input("나이를 입력하세요: "))
    weight = float(input("체중을 입력하세요(kg): "))
    goal = input("운동 목표를 입력하세요(체중 감량/근력 증가/건강 관리): ")
    disease = input("기저 질환을 입력하세요(고혈압/당뇨/허리디스크/없음): ")
    pain_area = input("통증 부위를 입력하세요(무릎/허리/어깨/없음): ")
    place = input("운동 장소를 입력하세요(집/헬스장/야외): ")
    exercise_time = int(input("운동 가능 시간을 입력하세요(분): "))
    equipment = input("보유 장비를 입력하세요(없음/덤벨/러닝머신/자전거 등): ")

    return {
        "age": age,
        "weight": weight,
        "goal": goal,
        "disease": disease,
        "pain_area": pain_area,
        "place": place,
        "exercise_time": exercise_time,
        "equipment": equipment
    }


def recommend_exercise(user_data, rules):
    """사용자 정보와 규칙을 바탕으로 운동을 추천하는 함수"""
    disease = user_data["disease"]
    pain_area = user_data["pain_area"]
    place = user_data["place"]

    disease_rules = rules["disease_rules"]
    pain_rules = rules["pain_rules"]
    place_rules = rules["place_rules"]

    disease_info = disease_rules.get(disease, disease_rules["없음"])
    pain_info = pain_rules.get(pain_area, pain_rules["없음"])
    place_info = place_rules.get(place, [])

    recommend_list = []
    avoid_list = []
    reasons = []

    recommend_list.extend(disease_info["recommend"])
    avoid_list.extend(disease_info["avoid"])
    reasons.append(disease_info["reason"])

    recommend_list.extend(pain_info["recommend"])
    avoid_list.extend(pain_info["avoid"])
    reasons.append(pain_info["reason"])

    recommend_list.extend(place_info)

    recommend_list = remove_duplicates(recommend_list)
    avoid_list = remove_duplicates(avoid_list)

    # 금지 운동에 포함된 운동은 추천 운동에서 제거
    recommend_list = [
        exercise for exercise in recommend_list
        if exercise not in avoid_list
    ]

    return {
        "recommend": recommend_list,
        "avoid": avoid_list,
        "reasons": reasons
    }


def make_routine(recommend_list, exercise_time):
    """운동 가능 시간에 따라 간단한 루틴을 만드는 함수"""
    if exercise_time <= 20:
        return [
            "준비 스트레칭 5분",
            f"{recommend_list[0] if recommend_list else '걷기'} {exercise_time - 10}분",
            "마무리 스트레칭 5분"
        ]
    elif exercise_time <= 40:
        return [
            "준비 스트레칭 5분",
            f"{recommend_list[0] if recommend_list else '걷기'} 15분",
            f"{recommend_list[1] if len(recommend_list) > 1 else '가벼운 근력 운동'} 10분",
            "마무리 스트레칭 5분"
        ]
    else:
        return [
            "준비 스트레칭 10분",
            f"{recommend_list[0] if recommend_list else '걷기'} 20분",
            f"{recommend_list[1] if len(recommend_list) > 1 else '가벼운 근력 운동'} 20분",
            "마무리 스트레칭 10분"
        ]


def print_result(user_data, result):
    """추천 결과를 출력하는 함수"""
    routine = make_routine(result["recommend"], user_data["exercise_time"])

    print("\n" + "=" * 40)
    print("운동 추천 결과")
    print("=" * 40)

    print("\n[입력 정보]")
    print(f"나이: {user_data['age']}세")
    print(f"체중: {user_data['weight']}kg")
    print(f"운동 목표: {user_data['goal']}")
    print(f"기저 질환: {user_data['disease']}")
    print(f"통증 부위: {user_data['pain_area']}")
    print(f"운동 장소: {user_data['place']}")
    print(f"운동 가능 시간: {user_data['exercise_time']}분")
    print(f"보유 장비: {user_data['equipment']}")

    print("\n[추천 운동]")
    if result["recommend"]:
        for exercise in result["recommend"]:
            print(f"- {exercise}")
    else:
        print("- 추천 가능한 운동이 부족합니다.")

    print("\n[금지/주의 운동]")
    if result["avoid"]:
        for exercise in result["avoid"]:
            print(f"- {exercise}")
    else:
        print("- 특별히 제한할 운동이 없습니다.")

    print("\n[추천 이유]")
    for reason in result["reasons"]:
        print(f"- {reason}")

    print("\n[추천 루틴]")
    for item in routine:
        print(f"- {item}")

    print("\n[주의사항]")
    print("- 본 결과는 일반적인 운동 추천 예시입니다.")
    print("- 통증이 발생하면 즉시 운동을 중단해야 합니다.")
    print("- 실제 질환이 있는 경우 전문가 상담이 필요합니다.")


def main():
    rules = load_rules("data/exercise_rules.json")
    user_data = get_user_input()
    result = recommend_exercise(user_data, rules)
    print_result(user_data, result)


if __name__ == "__main__":
    main()


