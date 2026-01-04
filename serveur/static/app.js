document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       ELEMENTS
    ========================= */
    const sendBtn = document.getElementById("send-btn");
    const resultsBody = document.getElementById("results");
    const resultIdBadge = document.getElementById("result-id");
    const downloadBtn = document.getElementById("download-btn");

    const wordlistBtn = document.getElementById("open-wordlist-btn");
    const wordlistContainer = document.getElementById("wordlist-container");
    const fuzzTypeInput = document.getElementById("fuzzing-type");

    let currentResultId = null;
    let wordlistModal = null;

    /* =========================
       EVENTS
    ========================= */
    sendBtn?.addEventListener("click", sendFuzz);
    downloadBtn?.addEventListener("click", downloadResult);
    wordlistBtn?.addEventListener("click", openWordlistModal);

    /* =========================
       SEND FUZZ REQUEST
    ========================= */
    async function sendFuzz() {
        clearResults();

        const payload = {
            url: document.getElementById("target-url").value,
            fuzzType: fuzzTypeInput.value,
            method: document.getElementById("method").value || "GET",
            headers: parseJSON("headers"),
            body: parseJSON("body")
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

            currentResultId = data.result_id;
            resultIdBadge.textContent = currentResultId;
            resultIdBadge.className = "badge bg-success";
            downloadBtn.disabled = false;

            renderResults(data.result);

        } catch (err) {
            alert("Erreur API : " + err.message);
            console.error(err);
        }
    }

    /* =========================
       WORDLIST MODAL
    ========================= */
    async function openWordlistModal() {
        if (!wordlistModal) {
            wordlistModal = new bootstrap.Modal(
                document.getElementById("wordlistModal")
            );
        }

        wordlistContainer.innerHTML = `
            <div class="text-center text-muted p-3">
                Loading wordlists...
            </div>
        `;

        try {
            const res = await fetch("/api/wordlist");
            if (!res.ok) throw new Error("Failed to load wordlists");

            const data = await res.json();
            renderWordlists(data);

            wordlistModal.show();

        } catch (err) {
            wordlistContainer.innerHTML = `
                <div class="alert alert-danger">${err.message}</div>
            `;
        }
    }

    function renderWordlists(wordlists) {
        wordlistContainer.innerHTML = "";

        Object.entries(wordlists).forEach(([name, desc]) => {
            const item = document.createElement("button");
            item.type = "button";
            item.className = "list-group-item list-group-item-action";

            item.innerHTML = `
                <strong>${name}</strong>
                <div class="small text-muted">${desc}</div>
            `;

            item.onclick = () => {
                fuzzTypeInput.value = `wordlist,${name}`;
                wordlistModal.hide();
            };

            wordlistContainer.appendChild(item);
        });
    }

    /* =========================
       RESULTS
    ========================= */
    function renderResults(resultArray) {
        resultArray.forEach(entry => {
            const key = Object.keys(entry)[0];
            if (key === "fuzz_context") return;

            const req = entry[key];
            const status = req.response.status;

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${key.replace("request ", "")}</td>
                <td><code>${req.payload}</code></td>
                <td>
                    <span class="badge ${status >= 200 && status < 300 ? "bg-success" : "bg-danger"}">
                        ${status}
                    </span>
                </td>
                <td><pre>${JSON.stringify(req.response.headers, null, 2)}</pre></td>
                <td><pre>${escapeHTML(req.response.body)}</pre></td>
            `;
            resultsBody.appendChild(tr);
        });
    }

    function downloadResult() {
        if (currentResultId) {
            window.open(`/api/result/${currentResultId}`, "_blank");
        }
    }

    function clearResults() {
        resultsBody.innerHTML = "";
        resultIdBadge.textContent = "-";
        resultIdBadge.className = "badge bg-secondary";
        downloadBtn.disabled = true;
        currentResultId = null;
    }

    function parseJSON(id) {
        const el = document.getElementById(id);
        if (!el || !el.value.trim()) return null;
        return JSON.parse(el.value);
    }

    function escapeHTML(str) {
        return str?.replace(/[&<>"']/g, m => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        })[m]) || "";
    }
});
