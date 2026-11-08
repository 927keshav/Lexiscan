// ── LexiScan Auto — Frontend Logic ──────────────────────────

const API_BASE = window.location.origin;

// DOM Elements
const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const fileInfo = document.getElementById("file-info");
const fileName = document.getElementById("file-name");
const clearFileBtn = document.getElementById("clear-file");
const extractBtn = document.getElementById("extract-btn");
const btnText = extractBtn.querySelector(".btn-text");
const btnLoader = extractBtn.querySelector(".btn-loader");
const resultsSection = document.getElementById("results-section");
const errorSection = document.getElementById("error-section");
const errorMessage = document.getElementById("error-message");
const toggleJsonBtn = document.getElementById("toggle-json");
const jsonOutput = document.getElementById("json-output");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

let selectedFile = null;
let lastResult = null;


// ── Health Check ────────────────────────────────────────────

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        if (data.status === "ok") {
            statusDot.className = "status-dot online";
            statusText.textContent = "API Online";
        } else {
            throw new Error();
        }
    } catch {
        statusDot.className = "status-dot offline";
        statusText.textContent = "API Offline";
    }
}

checkHealth();
setInterval(checkHealth, 15000);


// ── File Selection ──────────────────────────────────────────

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
});

clearFileBtn.addEventListener("click", () => {
    clearFile();
});

function handleFile(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
        showError("Please select a PDF file.");
        return;
    }

    selectedFile = file;
    fileName.textContent = file.name + " (" + formatSize(file.size) + ")";
    fileInfo.classList.remove("hidden");
    dropZone.classList.add("hidden");
    extractBtn.disabled = false;
    hideError();
}

function clearFile() {
    selectedFile = null;
    fileInput.value = "";
    fileInfo.classList.add("hidden");
    dropZone.classList.remove("hidden");
    extractBtn.disabled = true;
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
}


// ── Extract ─────────────────────────────────────────────────

extractBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    setLoading(true);
    hideError();
    resultsSection.classList.add("hidden");

    try {
        const formData = new FormData();
        formData.append("file", selectedFile);

        const res = await fetch(`${API_BASE}/extract`, {
            method: "POST",
            body: formData,
        });

        const data = await res.json();

        if (!res.ok) {
            showError(data.error || "Server returned an error.");
            return;
        }

        if (data.error && data.dates) {
            showError(data.error);
        }

        lastResult = data;
        renderResults(data);

    } catch (err) {
        showError("Failed to connect to the API. Make sure the server is running.");
    } finally {
        setLoading(false);
    }
});

function setLoading(loading) {
    extractBtn.disabled = loading;
    btnText.textContent = loading ? "Processing..." : "Extract Entities";
    btnLoader.classList.toggle("hidden", !loading);
}


// ── Render Results ──────────────────────────────────────────

function renderResults(data) {
    // Parties
    renderList("parties-list", data.parties, "No parties found");
    document.getElementById("parties-count").textContent = data.parties.length;

    // Dates
    renderList("dates-list", data.dates, "No dates found");
    document.getElementById("dates-count").textContent = data.dates.length;

    // Dollar Amounts
    const amountTexts = data.dollar_amounts.map(
        (a) => `${a.raw}  →  ${a.value.toLocaleString("en-US", { style: "currency", currency: "USD" })}`
    );
    renderList("amounts-list", amountTexts, "No amounts found");
    document.getElementById("amounts-count").textContent = data.dollar_amounts.length;

    // Termination Clauses
    renderList("clauses-list", data.termination_clauses, "No clauses found");
    document.getElementById("clauses-count").textContent = data.termination_clauses.length;

    // JSON
    jsonOutput.textContent = JSON.stringify(data, null, 2);
    jsonOutput.classList.add("hidden");
    toggleJsonBtn.textContent = "Show Raw JSON";

    resultsSection.classList.remove("hidden");
}

function renderList(listId, items, emptyText) {
    const list = document.getElementById(listId);
    list.innerHTML = "";

    if (!items || items.length === 0) {
        const li = document.createElement("li");
        li.className = "empty";
        li.textContent = emptyText;
        list.appendChild(li);
        return;
    }

    items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        list.appendChild(li);
    });
}


// ── JSON Toggle ─────────────────────────────────────────────

toggleJsonBtn.addEventListener("click", () => {
    const isHidden = jsonOutput.classList.contains("hidden");
    jsonOutput.classList.toggle("hidden");
    toggleJsonBtn.textContent = isHidden ? "Hide Raw JSON" : "Show Raw JSON";
});


// ── Error Handling ──────────────────────────────────────────

function showError(msg) {
    errorMessage.textContent = msg;
    errorSection.classList.remove("hidden");
}

function hideError() {
    errorSection.classList.add("hidden");
}
