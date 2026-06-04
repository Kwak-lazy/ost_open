from src.bmi import calculate_bmi, classify_bmi
from src.recommendation import print_recommendation


def get_user_input():
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
        "condition": disease,
        "pain_area": pain_area,
        "goal": goal,
    }


def main():
    user_data = get_user_input()

    bmi = calculate_bmi(user_data["height"], user_data["weight"])
    bmi_category = classify_bmi(bmi)

    user_data["bmi"] = bmi
    user_data["bmi_category"] = bmi_category

    print_recommendation(user_data)


if __name__ == "__main__":
    main()
