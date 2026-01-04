const sendBtn = document.getElementById("send-btn");
const resultsBody = document.getElementById("results");

sendBtn.addEventListener("click", sendFuzz);

async function sendFuzz() {
    clearResults();

    let headersObj = null;
    let bodyObj = null;

    // ---- Parse HEADERS ----
    const headersRaw = document.getElementById("headers").value.trim();
    if (headersRaw) {
        try {
            headersObj = JSON.parse(headersRaw);
        } catch (e) {
            alert("Headers JSON invalide");
            return;
        }
    }

    // ---- Parse BODY ----
    const bodyRaw = document.getElementById("body").value.trim();
    if (bodyRaw) {
        try {
            bodyObj = JSON.parse(bodyRaw);
        } catch (e) {
            alert("Body JSON invalide");
            return;
        }
    }

    const payload = {
        url: document.getElementById("target-url").value,
        fuzzType: document.getElementById("fuzzing-type").value,
        method: document.getElementById("method").value || null,
        headers: headersObj,
        body: bodyObj
    };

    try {
        const res = await fetch("/api/fuzz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const txt = await res.text();
            throw new Error(`HTTP ${res.status} - ${txt}`);
        }

        const data = await res.json();
        renderResults(data);

        const tab = document.querySelector('[data-bs-target="#response-tab"]');
        if (tab) tab.click();

    } catch (err) {
        alert("Erreur API : " + err.message);
        console.error(err);
    }
}

function renderResults(apiResponse) {
    const { result_id, result } = apiResponse;
    window.currentResultId = result_id;

    let index = 0;

    result.forEach(entry => {
        const key = Object.keys(entry)[0];

        if (key === "fuzz_context") return;

        if (key.startsWith("request")) {
            const req = entry[key];
            const status = req.response.status;

            const badgeClass =
                status >= 500 ? "bg-danger" :
                status >= 400 ? "bg-warning text-dark" :
                "bg-success";

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${index++}</td>
                <td><code>${req.payload}</code></td>
                <td><span class="badge ${badgeClass}">${status}</span></td>
                <td><pre>${JSON.stringify(req.response.headers, null, 2)}</pre></td>
                <td><pre>${escapeHtml(req.response.body)}</pre></td>
            `;

            resultsBody.appendChild(tr);
        }
    });
}

function clearResults() {
    resultsBody.innerHTML = "";
    window.currentResultId = null;
}

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
