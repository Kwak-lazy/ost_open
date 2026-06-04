const CONFIG = {
    API_BASE_URL: ""
};

const form = document.getElementById("recommendation-form");
const inputSection = document.getElementById("input-section");
const resultSection = document.getElementById("result-section");
const btnRetry = document.getElementById("btn-retry");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const age = parseInt(document.getElementById("age").value, 10);
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("weight").value);
    const goal = document.getElementById("goal").value;

    const conditions = Array.from(document.querySelectorAll('input[name="conditions"]:checked')).map(el => el.value);
    const checkedPain = Array.from(document.querySelectorAll('input[name="pain_area"]:checked')).map(el => el.value);
    const pain_area = checkedPain.length > 0 ? checkedPain[0] : "없음";

    const requestData = {
        age: age,
        height: height,
        weight: weight,
        conditions: conditions,
        pain_area: pain_area,
        goal: goal
    };

    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/recommend`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "추천 분석 서버 오류가 발생했습니다.");
        }

        const resultData = await response.json();
        
        // 결과 UI 매핑 호출
        renderResults(requestData, resultData);
        
        // 섹션 토글 전환
        inputSection.classList.add("hidden");
        resultSection.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });

    } catch (error) {
        alert(`오류가 발생했습니다: ${error.message}`);
        console.error(error);
    }
});

// 데이터 출력 전담 렌더러 함수
function renderResults(input, data) {
    // 요약 테이블 바인딩
    if(document.getElementById("res-age")) document.getElementById("res-age").textContent = input.age;
    if(document.getElementById("res-specs")) document.getElementById("res-specs").textContent = `${input.height}cm / ${input.weight}kg`;
    if(document.getElementById("res-bmi")) document.getElementById("res-bmi").textContent = `${data.bmi} (${data.bmi_category})`;
    if(document.getElementById("res-goal")) document.getElementById("res-goal").textContent = input.goal;

    // 1. 추천 운동 리스트
    const recommendedList = document.getElementById("recommended-list");
    if (recommendedList) {
        recommendedList.innerHTML = "";
        if (data.recommended && data.recommended.length > 0) {
            data.recommended.forEach(ex => {
                const li = document.createElement("li");
                li.className = "exercise-item";
                let badgeClass = "mid";
                if (ex.intensity.includes("고")) badgeClass = "high";
                if (ex.intensity.includes("저")) badgeClass = "low";

                li.innerHTML = `
                    <span class="exercise-info">${ex.name}</span>
                    <div class="exercise-meta">
                        <span>⏱️ ${ex.duration}분</span>
                        <span class="badge ${badgeClass}">${ex.intensity}</span>
                        
                    </div>
                `;
                recommendedList.appendChild(li);
            });
        } else {
            recommendedList.innerHTML = "<li>추천된 안전 운동 조합이 없습니다.</li>";
        }
    }

    // 2. 금지 운동 바인딩
    const forbiddenContainer = document.getElementById("forbidden-container");
    if (forbiddenContainer) {
        forbiddenContainer.innerHTML = "";
        if (data.forbidden_by_source && Object.keys(data.forbidden_by_source).length > 0) {
            Object.entries(data.forbidden_by_source).forEach(([source, exercises]) => {
                if (exercises && exercises.length > 0) {
                    const group = document.createElement("div");
                    group.className = "source-group";
                    group.innerHTML = `
                        <div class="source-title">🚫 [${source}] 관련 금지 운동</div>
                        <ul class="source-items">
                            ${exercises.map(ex => `<li>${ex}</li>`).join("")}
                        </ul>
                    `;
                    forbiddenContainer.appendChild(group);
                }
            });
        } else {
            forbiddenContainer.innerHTML = "<p style='color:#38a169;'>제한이 필요한 금지 행동이 없습니다.</p>";
        }
    }

    // 3. 추천 가이드 라인 맵핑
    const reasonList = document.getElementById("reason-list");
    if (reasonList) {
        reasonList.innerHTML = "";
        if (data.goal_notes) {
            const notes = Array.isArray(data.goal_notes) ? data.goal_notes : [data.goal_notes];
            notes.forEach(note => {
                const li = document.createElement("li");
                li.textContent = note;
                reasonList.appendChild(li);
            });
        }
    }

    // 4. 종합 주의사항 맵핑
    const cautionList = document.getElementById("caution-list");
    if (cautionList) {
        cautionList.innerHTML = "";
        if (data.cautions) {
            const cautionItems = typeof data.cautions === "object" ? Object.values(data.cautions) : [data.cautions];
            cautionItems.flat().forEach(caution => {
                const li = document.createElement("li");
                li.textContent = caution;
                cautionList.appendChild(li);
            });
        }
    }
}

// 다시 작성하기
btnRetry.addEventListener("click", () => {
    resultSection.classList.add("hidden");
    inputSection.classList.remove("hidden");
    form.reset();
});