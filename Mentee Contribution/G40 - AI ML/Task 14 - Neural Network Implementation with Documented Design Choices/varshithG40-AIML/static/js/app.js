document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initDropzone();
  loadUnseenSamples();
  loadDecisionTable();
});

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(content => content.style.display = "none");

  const activeBtn = document.querySelector(`.tab-btn[onclick="switchTab('${tabId}')"]`);
  if (activeBtn) activeBtn.classList.add("active");

  const targetContent = document.getElementById(`tab-${tabId}`);
  if (targetContent) targetContent.style.display = "block";
}

function initTabs() {
  switchTab("inspector");
}

function initDropzone() {
  const dropzone = document.getElementById("dropzone");
  
  ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.add("dragover"), false);
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove("dragover"), false);
  });

  dropzone.addEventListener("drop", handleDrop, false);
}

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  if (files.length > 0) {
    uploadAndPredict(files[0]);
  }
}

function handleFileSelect(e) {
  const files = e.target.files;
  if (files.length > 0) {
    uploadAndPredict(files[0]);
  }
}

async function uploadAndPredict(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    document.getElementById("image-preview").src = e.target.result;
  };
  reader.readAsDataURL(file);

  const formData = new FormData();
  formData.append("file", file);

  const startTime = performance.now();
  document.getElementById("infer-time").textContent = "Analyzing...";

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    const duration = Math.round(performance.now() - startTime);

    if (data.success) {
      document.getElementById("infer-time").textContent = `Inference: ${duration}ms`;
      renderResult(data);
    } else {
      alert("Error: " + (data.detail || "Failed to classify image"));
    }
  } catch (err) {
    console.error("Upload error:", err);
    document.getElementById("infer-time").textContent = "Error";
  }
}

function renderResult(data) {
  const isDefective = (data.prediction === "Defective");
  const badge = document.getElementById("result-badge");
  const resultText = document.getElementById("result-text");
  const probValue = document.getElementById("prob-value");
  const fill = document.getElementById("progress-fill");
  const actionBox = document.getElementById("action-box");
  const actionText = document.getElementById("action-text");

  if (isDefective) {
    badge.className = "result-badge defective";
    badge.querySelector("i").className = "fa-solid fa-triangle-exclamation";
    resultText.textContent = "DEFECTIVE";

    fill.className = "progress-bar-fill defective";
    actionBox.className = "action-recommendation defective";
    actionBox.querySelector("i").className = "fa-solid fa-shield-virus";
  } else {
    badge.className = "result-badge ok";
    badge.querySelector("i").className = "fa-solid fa-circle-check";
    resultText.textContent = "NON-DEFECTIVE";

    fill.className = "progress-bar-fill ok";
    actionBox.className = "action-recommendation ok";
    actionBox.querySelector("i").className = "fa-solid fa-circle-check";
  }

  const probPercent = (data.defective_probability * 100).toFixed(1);
  probValue.textContent = `${probPercent}%`;
  fill.style.width = `${probPercent}%`;

  actionText.innerHTML = `<strong>Action Recommendation:</strong> ${data.action_recommendation}`;
}

async function loadUnseenSamples() {
  try {
    const res = await fetch("/api/samples");
    const data = await res.json();
    const grid = document.getElementById("samples-grid");
    grid.innerHTML = "";

    data.samples.forEach(sample => {
      const isDef = sample.ground_truth === "Defective";
      const item = document.createElement("div");
      item.className = "sample-item";
      item.innerHTML = `
        <img src="${sample.path}" alt="${sample.filename}">
        <div class="sample-badge ${isDef ? 'defective' : 'ok'}">
          ${isDef ? 'DEFECTIVE' : 'NON-DEFECTIVE'}
        </div>
      `;
      item.onclick = () => selectSample(sample);
      grid.appendChild(item);
    });
  } catch (err) {
    console.error("Failed to load unseen samples:", err);
  }
}

async function selectSample(sample) {
  document.getElementById("image-preview").src = sample.path;
  const res = await fetch(sample.path);
  const blob = await res.blob();
  const file = new File([blob], sample.filename, { type: "image/png" });
  uploadAndPredict(file);
}

async function loadDecisionTable() {
  try {
    const res = await fetch("/api/decision-table");
    const data = await res.json();
    const tbody = document.getElementById("decision-table-body");
    tbody.innerHTML = "";

    data.decision_table.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.decision}</td>
        <td>${row.value}</td>
        <td>${row.reason}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Failed to load decision table:", err);
  }
}
