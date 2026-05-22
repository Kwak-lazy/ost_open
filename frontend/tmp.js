// ==========================================
// 1. 데이터 레이어 (rule_engine.py 데이터 이식)
// ==========================================

const CONDITION_RULES = {
    "고혈압": {
        "forbidden": ["무거운 역도", "버피테스트", "고강도 인터벌 트레이닝", "레슬링", "복싱"],
        "recommended": [
            ["걷기", "저강도", 30], ["수영", "저강도", 30],
            ["자전거 타기(평지)", "저강도", 30], ["스트레칭", "저강도", 20],
            ["요가(하타)", "저강도", 30]
        ],
        "caution": "혈압이 180/110 이상이면 운동 전 의사와 상담하세요."
    },
    "당뇨": {
        "forbidden": ["공복 고강도 운동", "극한 마라톤"],
        "recommended": [
            ["걷기", "저강도", 30], ["수영", "중강도", 30],
            ["저항 운동(가벼운 덤벨)", "중강도", 20],
            ["자전거 타기", "저강도", 30], ["댄스", "중강도", 30]
        ],
        "caution": "운동 전후 혈당을 반드시 측정하세요. 저혈당 시 즉시 중단."
    },
    "허리디스크": {
        "forbidden": ["데드리프트", "윗몸일으키기", "무거운 스쿼트", "달리기", "역도"],
        "recommended": [
            ["수영(배영)", "저강도", 20], ["걷기(평지)", "저강도", 20],
            ["코어 안정화 운동", "저강도", 15], ["가벼운 스트레칭", "저강도", 20],
            ["필라테스(전문가 지도)", "저강도", 20]
        ],
        "caution": "통증이 있을 때는 운동하지 마세요. 물리치료사 지도를 권장합니다."
    },
    "천식": {
        "forbidden": ["차가운 공기 중 달리기", "먼지 많은 환경 운동"],
        "recommended": [
            ["수영(따뜻한 물)", "중강도", 30], ["걷기", "저강도", 30],
            ["요가", "저강도", 30], ["자전거 타기(실내)", "중강도", 20]
        ],
        "caution": "운동 전 흡입기를 준비하세요. 증상 발생 시 즉시 중단."
    },
    "심장질환": {
        "forbidden": ["무거운 역도", "고강도 인터벌 트레이닝", "버피테스트", "스프린트", "복싱"],
        "recommended": [
            ["걷기(평지)", "저강도", 20], ["수중 걷기", "저강도", 20],
            ["스트레칭", "저강도", 15], ["태극권", "저강도", 20]
        ],
        "caution": "가슴 통증, 호흡곤란 시 즉시 중단. 심장 전문의 허가 후 운동."
    },
    "관절염": {
        "forbidden": ["달리기(장거리)", "점프 운동", "스쿼트(깊은)", "축구", "농구"],
        "recommended": [
            ["수영", "저강도", 30], ["수중 에어로빅", "저강도", 30],
            ["자전거 타기(고정식)", "저강도", 20], ["스트레칭", "저강도", 20]
        ],
        "caution": "관절 통증이 심해지면 즉시 중단하고 휴식을 취하세요."
    },
    "골다공증": {
        "forbidden": ["높은 충격 점프", "격렬한 비틀기", "무거운 역도"],
        "recommended": [
            ["걷기", "중강도", 30], ["태극권", "저강도", 30],
            ["필라테스", "저강도", 30], ["저항 운동(가벼운)", "저강도", 20]
        ],
        "caution": "낙상 위험이 높은 운동은 피하세요. 균형 훈련을 병행하세요."
    },
    "비만": {
        "forbidden": ["고강도 점프 운동(초보자)", "무거운 역도(초보자)"],
        "recommended": [
            ["수영", "중강도", 45], ["걷기(빠르게)", "중강도", 45],
            ["자전거 타기", "중강도", 40], ["수중 에어로빅", "중강도", 40]
        ],
        "caution": "점진적으로 운동 강도와 시간을 늘려가세요."
    }
};

const PAIN_RULES = {
    "무릎": { "forbidden": ["달리기(장거리)", "점프 운동", "스쿼트(깊은)", "계단 오르기(고강도)", "농구", "축구"], "caution": "무릎에 충격이 가는 운동을 피하고, 수중 운동을 권장합니다." },
    "허리": { "forbidden": ["데드리프트", "윗몸일으키기", "무거운 스쿼트", "달리기", "역도"], "caution": "허리를 과도하게 굽히거나 비트는 동작은 피하세요." },
    "어깨": { "forbidden": ["수영(접영)", "무거운 overhead press", "테니스(서브)", "야구(투구)"], "caution": "팔을 머리 위로 올리는 동작은 피하세요." },
    "목": { "forbidden": ["헤드스탠드", "무거운 숄더프레스", "격렬한 수영"], "caution": "목에 압박이 가는 동작과 급격한 회전을 피하세요." },
    "손목": { "forbidden": ["푸시업", "역도", "테니스", "배드민턴(강타)"], "caution": "손목에 체중을 싣는 동작을 피하세요." },
    "발목": { "forbidden": ["달리기", "점프 운동", "축구", "농구", "등산(급경사)"], "caution": "발목에 충격이 가는 운동을 피하고, 평지 걷기나 수중 운동을 권장합니다." },
    "고관절": { "forbidden": ["깊은 스쿼트", "달리기(장거리)", "축구", "급격한 방향 전환"], "caution": "고관절에 부담이 가는 자세는 피하세요." },
    "팔꿈치": { "forbidden": ["테니스", "배드민턴", "역도(팔꿈치 굴곡)", "푸시업"], "caution": "팔꿈치에 반복 충격이 가는 운동을 피하세요." },
    "없음": { "forbidden": [], "caution": "" }
};

const GOAL_RULES = {
    "체중 감량": { "preferred_intensity": ["중강도", "고강도"], "min_duration": 40, "score_bonus": 1.5, "notes": "유산소 위주, 40분 이상 지속 운동을 권장합니다." },
    "근력 증가": { "preferred_intensity": ["중강도", "고강도"], "min_duration": 30, "score_bonus": 1.5, "notes": "저항 운동 위주, 단백질 섭취를 병행하세요." },
    "건강 관리": { "preferred_intensity": ["저강도", "중강도"], "min_duration": 20, "score_bonus": 1.0, "notes": "규칙적인 운동 습관 형성을 목표로 하세요." }
};

const GENERAL_EXERCISES = [
    ["달리기", "고강도", 30], ["수영", "중강도", 45], ["자전거 타기", "중강도", 40],
    ["요가", "저강도", 40], ["필라테스", "저강도", 40], ["댄스", "중강도", 40],
    ["등산", "중강도", 60], ["테니스", "중강도", 45], ["고강도 인터벌 트레이닝", "고강도", 25],
    ["스트레칭", "저강도", 20], ["걷기", "저강도", 45], ["저항 운동", "중강도", 40],
    ["플랭크", "중강도", 15], ["수영(배영)", "저강도", 30]
];

// ==========================================
// 2. 룰 엔진 로직 (자바스크립트로 변환)
// ==========================================

function calculateBmi(height, weight) {
    const heightM = height / 100;
    return (weight / (heightM * heightM)).toFixed(2);
}

function classifyBmi(bmi) {
    if (bmi < 18.5) return "저체중";
    if (bmi < 23) return "정상";
    if (bmi < 25) return "과체중";
    return "비만";
}

// 여러 통증 부위를 받아 금지 셋 생성
function getForbiddenSet(conditions, painAreas) {
    const forbidden = new Set();
    conditions.forEach(cond => {
        if (CONDITION_RULES[cond]) {
            CONDITION_RULES[cond].forbidden.forEach(ex => forbidden.add(ex));
        }
    });
    painAreas.forEach(pain => {
        if (pain !== "없음" && PAIN_RULES[pain]) {
            PAIN_RULES[pain].forbidden.forEach(ex => forbidden.add(ex));
        }
    });
    return forbidden;
}

function scoreExercise(exercise, conditions, painAreas, goal, age, bmi, forbiddenSet) {
    const [name, intensity, duration] = exercise;

    if (forbiddenSet.has(name)) return -999.0;

    let score = 0.0;

    // 질환 추천 운동 가산
    conditions.forEach(cond => {
        if (CONDITION_RULES[cond]) {
            const recNames = CONDITION_RULES[cond].recommended.map(r => r[0]);
            if (recNames.includes(name)) score += 5.0;
        }
    });

    // 운동 목표 강도 가산
    if (goal && GOAL_RULES[goal]) {
        const goalInfo = GOAL_RULES[goal];
        if (goalInfo.preferred_intensity.includes(intensity)) {
            score += goalInfo.score_bonus;
        }
        if (duration >= goalInfo.min_duration) {
            score += 0.5;
        }
    }

    // 나이 기반 강도 가산
    const intensityVal = { "저강도": 1, "중강도": 2, "고강도": 3 }[intensity] || 2;
    if (age >= 60 && intensityVal === 1) {
        score += 2.0;
    } else if (age >= 40 && age < 60 && intensityVal <= 2) {
        score += 1.0;
    }

    // BMI 기반 가산
    if (bmi >= 25.0 && intensityVal <= 2) {
        score += 1.0;
    }

    return score;
}

function applyRules(conditions, painAreas, goal, age, bmi, topN = 5) {
    const forbiddenSet = getForbiddenSet(conditions, painAreas);

    // 후보군 수집
    let candidates = [...GENERAL_EXERCISES];
    const seen = new Set(candidates.map(ex => ex[0]));

    conditions.forEach(cond => {
        if (CONDITION_RULES[cond]) {
            CONDITION_RULES[cond].recommended.forEach(ex => {
                if (!seen.has(ex[0])) {
                    candidates.push(ex);
                    seen.add(ex[0]);
                }
            });
        }
    });

    // 점수 계산 및 정렬
    let scored = candidates.map(ex => {
        const score = scoreExercise(ex, conditions, painAreas, goal, age, bmi, forbiddenSet);
        return [...ex, score];
    });

    // 필터링 및 정렬
    let recommended = scored
        .filter(ex => ex[3] >= 0)
        .sort((a, b) => b[3] - a[3])
        .slice(0, topN);

    // 금지 사유 소스별 취합
    const forbiddenBySource = {};
    conditions.forEach(cond => {
        if (CONDITION_RULES[cond]) forbiddenBySource[cond] = CONDITION_RULES[cond].forbidden;
    });
    
    painAreas.forEach(pain => {
        if (pain !== "없음" && PAIN_RULES[pain].forbidden.length > 0) {
            forbiddenBySource[`통증 부위(${pain})`] = PAIN_RULES[pain].forbidden;
        }
    });

    // 주의 사항 취합
    const cautions = {};
    conditions.forEach(cond => {
        if (CONDITION_RULES[cond]?.caution) cautions[cond] = CONDITION_RULES[cond].caution;
    });
    
    painAreas.forEach(pain => {
        if (pain !== "없음" && PAIN_RULES[pain]?.caution) {
            cautions[`통증 부위(${pain})`] = PAIN_RULES[pain].caution;
        }
    });

    return {
        recommended,
        forbiddenBySource,
        cautions,
        goalNotes: GOAL_RULES[goal]?.notes || ""
    };
}

// ==========================================
// 3. UI 렌더링 및 이벤트 바인딩
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
    const conditionsGroup = document.getElementById("conditions-group");
    const painGroup = document.getElementById("pain-group"); // 변경된 부위
    const goalSelect = document.getElementById("goal");
    const form = document.getElementById("recommendation-form");
    
    const inputSection = document.getElementById("input-section");
    const resultSection = document.getElementById("result-section");
    const btnRetry = document.getElementById("btn-retry");

    // 폼 옵션 초기화
    // 기저질환 생성
    Object.keys(CONDITION_RULES).forEach(cond => {
        const label = document.createElement("label");
        label.className = "checkbox-item";
        label.innerHTML = `<input type="checkbox" name="conditions" value="${cond}"> ${cond}`;
        conditionsGroup.appendChild(label);
    });

    // 통증부위 체크박스 생성
    Object.keys(PAIN_RULES).forEach(pain => {
        const label = document.createElement("label");
        label.className = "checkbox-item";
        // '없음'은 기본으로 체크되도록 설정
        const checked = pain === "없음" ? "checked" : "";
        label.innerHTML = `<input type="checkbox" name="painAreas" value="${pain}" ${checked}> ${pain}`;
        painGroup.appendChild(label);
    });

    // '없음'과 다른 통증 부위 간의 상호 배제 로직 추가
    painGroup.addEventListener("change", (e) => {
        if (e.target.name === "painAreas") {
            const noneCheckbox = painGroup.querySelector('input[value="없음"]');
            const otherCheckboxes = painGroup.querySelectorAll('input[name="painAreas"]:not([value="없음"])');
            
            if (e.target.value === "없음" && e.target.checked) {
                // '없음'을 선택하면 다른 통증 부위 모두 해제
                otherCheckboxes.forEach(cb => cb.checked = false);
            } else if (e.target.value !== "없음" && e.target.checked) {
                // 다른 부위를 선택하면 '없음' 해제
                noneCheckbox.checked = false;
            }
            
            // 만약 아무것도 선택되지 않았다면 '없음'에 다시 체크
            const anyChecked = painGroup.querySelectorAll('input[name="painAreas"]:checked').length > 0;
            if (!anyChecked) {
                noneCheckbox.checked = true;
            }
        }
    });

    // 운동 목표 생성
    Object.keys(GOAL_RULES).forEach(goal => {
        const option = document.createElement("option");
        option.value = goal;
        option.textContent = goal;
        goalSelect.appendChild(option);
    });

    // 제출 이벤트
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        // 데이터 수집
        const age = parseInt(document.getElementById("age").value);
        const height = parseFloat(document.getElementById("height").value);
        const weight = parseFloat(document.getElementById("weight").value);
        const goal = goalSelect.value;

        const checkedConditions = document.querySelectorAll('input[name="conditions"]:checked');
        const conditions = Array.from(checkedConditions).map(box => box.value);

        const checkedPain = document.querySelectorAll('input[name="painAreas"]:checked');
        const painAreas = Array.from(checkedPain).map(box => box.value);

        // 연산
        const bmi = calculateBmi(height, weight);
        const bmiStatus = classifyBmi(bmi);
        const result = applyRules(conditions, painAreas, goal, age, parseFloat(bmi));

        // 결과 반영
        document.getElementById("res-age").textContent = age;
        document.getElementById("res-specs").textContent = `${height}cm / ${weight}kg`;
        document.getElementById("res-bmi").textContent = `${bmi} (${bmiStatus})`;
        document.getElementById("res-goal").textContent = goal;

        // 1. 추천 운동 출력
        const recList = document.getElementById("recommended-list");
        recList.innerHTML = "";
        if (result.recommended.length === 0) {
            recList.innerHTML = `<li class="exercise-item">조건에 맞는 추천 운동이 없습니다.</li>`;
        } else {
            result.recommended.forEach(ex => {
                const [name, intensity, duration] = ex;
                const badgeClass = intensity === "저강도" ? "low" : intensity === "중강도" ? "mid" : "high";
                const li = document.createElement("li");
                li.className = "exercise-item";
                li.innerHTML = `
                    <span class="exercise-info">${name}</span>
                    <div class="exercise-meta">
                        <span class="badge ${badgeClass}">${intensity}</span>
                        <span>⏱️ ${duration}분</span>
                    </div>
                `;
                recList.appendChild(li);
            });
        }

        // 2. 금지 운동 출력
        const forbiddenContainer = document.getElementById("forbidden-container");
        forbiddenContainer.innerHTML = "";
        const sourceKeys = Object.keys(result.forbiddenBySource);
        if (sourceKeys.length === 0) {
            forbiddenContainer.innerHTML = "<div>특별히 제한할 운동이 없습니다.</div>";
        } else {
            sourceKeys.forEach(source => {
                const group = document.createElement("div");
                group.className = "source-group";
                group.innerHTML = `
                    <div class="source-title">[${source}]</div>
                    <div class="source-items">${result.forbiddenBySource[source].join(", ")}</div>
                `;
                forbiddenContainer.appendChild(group);
            });
        }

        // 3. 추천 이유 출력
        const reasonList = document.getElementById("reason-list");
        reasonList.innerHTML = "";
        if (conditions.length > 0) {
            reasonList.innerHTML += `<li>${conditions.join(", ")} 질환을 고려하여 무리가 없는 운동을 우선 추천했습니다.</li>`;
        }
        
        const validPainAreas = painAreas.filter(p => p !== "없음");
        if (validPainAreas.length > 0) {
            reasonList.innerHTML += `<li>${validPainAreas.join(", ")} 통증 부위에 부담이 가는 운동은 금지 목록에서 제외했습니다.</li>`;
        }
        if (result.goalNotes) {
            reasonList.innerHTML += `<li>${result.goalNotes}</li>`;
        }

        // 4. 주의사항 출력
        const cautionList = document.getElementById("caution-list");
        cautionList.innerHTML = "";
        Object.keys(result.cautions).forEach(source => {
            const li = document.createElement("li");
            li.innerHTML = `<strong>[${source}]</strong> ${result.cautions[source]}`;
            cautionList.appendChild(li);
        });
        cautionList.innerHTML += `<li>본 결과는 프로젝트용 일반 운동 추천 예시입니다.</li>`;
        cautionList.innerHTML += `<li>실제 질환이나 통증이 있는 경우 전문가 상담이 필요합니다.</li>`;
        cautionList.innerHTML += `<li>운동 중 통증이 발생하면 즉시 중단해야 합니다.</li>`;

        // 화면 전환
        inputSection.classList.add("hidden");
        resultSection.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 다시 하기 버튼 클릭 시
    btnRetry.addEventListener("click", () => {
        resultSection.classList.add("hidden");
        inputSection.classList.remove("hidden");
        form.reset();
        // 리셋 후 '없음' 체크박스 기본 선택 유지 처리
        setTimeout(() => {
            const noneCheckbox = painGroup.querySelector('input[value="없음"]');
            if(noneCheckbox) noneCheckbox.checked = true;
        }, 10);
    });
});