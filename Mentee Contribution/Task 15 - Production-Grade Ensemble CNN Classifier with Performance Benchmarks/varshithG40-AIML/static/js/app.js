/**
 * app.js
 * ======
 * Frontend JavaScript Controller for Ensemble CNN Classifier Dashboard.
 * Handles async API requests, live inference, perturbation simulations, and interactive charts.
 */

document.addEventListener("DOMContentLoaded", () => {
    // State
    let currentStrategy = "soft";
    let currentThreshold = 0.70;
    let selectedSampleId = 0;
    let customUploadedFile = null;
    let chartLatencyInstance = null;
    let chartSizeInstance = null;

    // DOM Elements
    const navItems = document.querySelectorAll(".nav-item");
    const tabPanes = document.querySelectorAll(".tab-pane");
    const sampleCarousel = document.getElementById("sample-carousel");
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("file-input");
    const btnBrowse = document.getElementById("btn-browse");
    const activePreviewImg = document.getElementById("active-image-preview");
    const previewLabel = document.getElementById("preview-label");
    const previewFilename = document.getElementById("preview-filename");
    const strategyButtons = document.querySelectorAll(".pill-btn");
    const confidenceSlider = document.getElementById("confidence-slider");
    const thresholdVal = document.getElementById("threshold-val");

    // Hero Elements
    const heroClassName = document.getElementById("hero-class-name");
    const heroEmoji = document.getElementById("hero-emoji");
    const heroConfNum = document.getElementById("hero-conf-num");
    const heroConsensusBadge = document.getElementById("hero-consensus-badge");
    const heroDecisionBadge = document.getElementById("hero-decision-badge");
    const ringBar = document.getElementById("ring-bar");
    const telemetryTimer = document.getElementById("telemetry-timer");

    // Model Cards
    const m1Pred = document.getElementById("m1-pred");
    const m1Conf = document.getElementById("m1-conf");
    const m1CatP = document.getElementById("m1-cat-p");
    const m1DogP = document.getElementById("m1-dog-p");
    const m1Bar = document.getElementById("m1-bar");

    const m2Pred = document.getElementById("m2-pred");
    const m2Conf = document.getElementById("m2-conf");
    const m2CatP = document.getElementById("m2-cat-p");
    const m2DogP = document.getElementById("m2-dog-p");
    const m2Bar = document.getElementById("m2-bar");

    const m3Pred = document.getElementById("m3-pred");
    const m3Conf = document.getElementById("m3-conf");
    const m3CatP = document.getElementById("m3-cat-p");
    const m3DogP = document.getElementById("m3-dog-p");
    const m3Bar = document.getElementById("m3-bar");

    // Robustness Elements
    const pertRot = document.getElementById("pert-rot");
    const pertBlur = document.getElementById("pert-blur");
    const pertNoise = document.getElementById("pert-noise");
    const pertIll = document.getElementById("pert-ill");
    const pertCrop = document.getElementById("pert-crop");
    const valRot = document.getElementById("val-rot");
    const valBlur = document.getElementById("val-blur");
    const valNoise = document.getElementById("val-noise");
    const valIll = document.getElementById("val-ill");
    const valCrop = document.getElementById("val-crop");
    const btnStressTest = document.getElementById("btn-stress-test");
    const btnResetPert = document.getElementById("btn-reset-pert");
    const imgCleanPert = document.getElementById("img-clean-pert");
    const imgDistortedPert = document.getElementById("img-distorted-pert");

    // Wizard Elements
    const wizardLatencySlider = document.getElementById("wizard-latency-slider");
    const wizardLatencyVal = document.getElementById("wizard-latency-val");
    const wizardOutcomeBox = document.getElementById("wizard-outcome-box");

    // ----------------------------------------------------------------------
    // 1. Tab Navigation
    // ----------------------------------------------------------------------
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetTab = item.getAttribute("data-tab");
            
            navItems.forEach(i => i.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));
            
            item.classList.add("active");
            const activePane = document.getElementById(targetTab);
            if (activePane) activePane.classList.add("active");

            // Lazy load charts when benchmarks tab is opened
            if (targetTab === "tab-benchmarks") {
                loadBenchmarksData();
            } else if (targetTab === "tab-robustness") {
                loadRobustnessData();
            }
        });
    });

    // ----------------------------------------------------------------------
    // 2. Strategy Selector & Confidence Slider
    // ----------------------------------------------------------------------
    strategyButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            strategyButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentStrategy = btn.getAttribute("data-strategy");
            runInference();
        });
    });

    confidenceSlider.addEventListener("input", (e) => {
        currentThreshold = parseInt(e.target.value) / 100.0;
        thresholdVal.textContent = `${e.target.value}%`;
        runInference();
    });

    // ----------------------------------------------------------------------
    // 3. Load Test Split Carousel Samples
    // ----------------------------------------------------------------------
    async function loadTestSamples() {
        try {
            const res = await fetch("/api/dataset/samples");
            const data = await res.json();
            
            if (data.samples && data.samples.length > 0) {
                sampleCarousel.innerHTML = "";
                data.samples.forEach((sample, idx) => {
                    const card = document.createElement("div");
                    card.className = `carousel-thumb-card ${idx === 0 ? 'active' : ''}`;
                    card.innerHTML = `
                        <img src="${sample.thumbnail}" class="thumb-img" alt="${sample.label}">
                        <span class="thumb-tag">${sample.label.toUpperCase()} #${sample.id+1}</span>
                    `;
                    card.addEventListener("click", () => {
                        document.querySelectorAll(".carousel-thumb-card").forEach(c => c.classList.remove("active"));
                        card.classList.add("active");
                        selectedSampleId = sample.id;
                        customUploadedFile = null;
                        activePreviewImg.src = sample.thumbnail;
                        imgCleanPert.src = sample.thumbnail;
                        imgDistortedPert.src = sample.thumbnail;
                        previewLabel.textContent = `Label: ${sample.label.toUpperCase()}`;
                        previewFilename.textContent = sample.filename;
                        runInference();
                    });
                    sampleCarousel.appendChild(card);
                });

                // Set initial sample
                selectedSampleId = 0;
                activePreviewImg.src = data.samples[0].thumbnail;
                imgCleanPert.src = data.samples[0].thumbnail;
                imgDistortedPert.src = data.samples[0].thumbnail;
                previewLabel.textContent = `Label: ${data.samples[0].label.toUpperCase()}`;
                previewFilename.textContent = data.samples[0].filename;
                
                runInference();
            }
        } catch (err) {
            console.error("Error loading test samples:", err);
            sampleCarousel.innerHTML = `<span style="color:#ef4444; font-size:0.8rem;">Failed to load samples. Please check API server.</span>`;
        }
    }

    // ----------------------------------------------------------------------
    // 4. File Upload & Dropzone Handling
    // ----------------------------------------------------------------------
    btnBrowse.addEventListener("click", () => fileInput.click());
    dropzone.addEventListener("click", () => fileInput.click());

    dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    function handleFileUpload(file) {
        customUploadedFile = file;
        document.querySelectorAll(".carousel-thumb-card").forEach(c => c.classList.remove("active"));
        
        const reader = new FileReader();
        reader.onload = (event) => {
            activePreviewImg.src = event.target.result;
            imgCleanPert.src = event.target.result;
            imgDistortedPert.src = event.target.result;
            previewLabel.textContent = "Label: CUSTOM UPLOAD";
            previewFilename.textContent = file.name;
            runInference();
        };
        reader.readAsDataURL(file);
    }

    // ----------------------------------------------------------------------
    // 5. Live Inference Execution
    // ----------------------------------------------------------------------
    async function runInference() {
        const formData = new FormData();
        formData.append("strategy", currentStrategy);
        formData.append("confidence_threshold", currentThreshold);

        if (customUploadedFile) {
            formData.append("file", customUploadedFile);
        } else {
            formData.append("sample_id", selectedSampleId);
        }

        try {
            const res = await fetch("/api/predict", {
                method: "POST",
                body: formData
            });
            const data = await res.json();

            // Update Hero Card
            const predClass = data.predictedClass.toUpperCase();
            heroClassName.textContent = predClass;
            heroEmoji.textContent = predClass === "CAT" ? "🐱" : "🐶";
            heroConfNum.textContent = `${Math.round(data.confidence * 100)}%`;

            // Animate SVG Radial Progress Ring
            const circumference = 2 * Math.PI * 50; // r=50 -> ~314.159
            const offset = circumference - (data.confidence * circumference);
            ringBar.style.strokeDashoffset = offset;
            ringBar.style.stroke = data.confidence >= currentThreshold ? "#10b981" : "#ef4444";

            // Badges
            if (data.isUnanimous) {
                heroConsensusBadge.className = "badge badge-consensus";
                heroConsensusBadge.textContent = "✨ Unanimous Consensus (3/3)";
            } else {
                heroConsensusBadge.className = "badge badge-disagreement";
                heroConsensusBadge.textContent = "⚠️ Model Disagreement (2 vs 1)";
            }

            if (data.meetsConfidenceThreshold) {
                heroDecisionBadge.className = "badge badge-decision";
                heroDecisionBadge.textContent = "🚀 Production Approved";
            } else {
                heroDecisionBadge.className = "badge badge-disagreement";
                heroDecisionBadge.textContent = "🛑 Manual Review Required";
            }

            telemetryTimer.textContent = `⏱️ Latency: ${data.inferenceTimeMs} ms`;

            // Individual Model Cards
            const indiv = data.individualModels;
            if (indiv) {
                updateModelCard("m1", indiv.cnn1_baseline);
                updateModelCard("m2", indiv.cnn2_regularized);
                updateModelCard("m3", indiv.cnn3_deep);
            }

        } catch (err) {
            console.error("Inference failed:", err);
        }
    }

    function updateModelCard(prefix, modelData) {
        const predElem = document.getElementById(`${prefix}-pred`);
        const confElem = document.getElementById(`${prefix}-conf`);
        const catPElem = document.getElementById(`${prefix}-cat-p`);
        const dogPElem = document.getElementById(`${prefix}-dog-p`);
        const barElem = document.getElementById(`${prefix}-bar`);

        const pClass = modelData.predictedClass.toUpperCase();
        predElem.textContent = pClass;
        confElem.textContent = `${Math.round(modelData.confidence * 100)}%`;
        catPElem.textContent = `${Math.round(modelData.catProb * 100)}%`;
        dogPElem.textContent = `${Math.round(modelData.dogProb * 100)}%`;

        barElem.style.width = `${modelData.catProb * 100}%`;
        barElem.style.background = pClass === "CAT" ? "#6366f1" : "#ec4899";
    }

    // ----------------------------------------------------------------------
    // 6. Robustness Studio Sliders & Perturbation API
    // ----------------------------------------------------------------------
    pertRot.addEventListener("input", (e) => { valRot.textContent = `${e.target.value}°`; });
    pertBlur.addEventListener("input", (e) => { valBlur.textContent = `${e.target.value} px`; });
    pertNoise.addEventListener("input", (e) => { valNoise.textContent = Number(e.target.value).toFixed(2); });
    pertIll.addEventListener("input", (e) => { valIll.textContent = `${Number(e.target.value).toFixed(1)}x`; });
    pertCrop.addEventListener("input", (e) => { valCrop.textContent = `${Math.round(e.target.value * 100)}%`; });

    btnResetPert.addEventListener("click", () => {
        pertRot.value = 0; valRot.textContent = "0°";
        pertBlur.value = 0; valBlur.textContent = "0 px";
        pertNoise.value = 0; valNoise.textContent = "0.00";
        pertIll.value = 1.0; valIll.textContent = "1.0x";
        pertCrop.value = 1.0; valCrop.textContent = "100%";
        runStressTest();
    });

    btnStressTest.addEventListener("click", runStressTest);

    async function runStressTest() {
        const formData = new FormData();
        formData.append("sample_id", selectedSampleId);
        formData.append("rotation_deg", pertRot.value);
        formData.append("blur_ksize", pertBlur.value);
        formData.append("noise_sigma", pertNoise.value);
        formData.append("illumination", pertIll.value);
        formData.append("crop_ratio", pertCrop.value);

        try {
            const res = await fetch("/api/perturb", {
                method: "POST",
                body: formData
            });
            const data = await res.json();

            imgDistortedPert.src = data.perturbedImageBase64;

            // Update Stress Cards
            const indiv = data.individualModels;
            document.getElementById("s-m1-pred").textContent = indiv.cnn1_baseline.predictedClass.toUpperCase();
            document.getElementById("s-m1-conf").textContent = `${Math.round(indiv.cnn1_baseline.confidence * 100)}%`;

            document.getElementById("s-m2-pred").textContent = indiv.cnn2_regularized.predictedClass.toUpperCase();
            document.getElementById("s-m2-conf").textContent = `${Math.round(indiv.cnn2_regularized.confidence * 100)}%`;

            document.getElementById("s-m3-pred").textContent = indiv.cnn3_deep.predictedClass.toUpperCase();
            document.getElementById("s-m3-conf").textContent = `${Math.round(indiv.cnn3_deep.confidence * 100)}%`;

            document.getElementById("s-ens-pred").textContent = data.predictedClass.toUpperCase();
            document.getElementById("s-ens-conf").textContent = `${Math.round(data.confidence * 100)}%`;

        } catch (err) {
            console.error("Stress test failed:", err);
        }
    }

    // ----------------------------------------------------------------------
    // 7. Load Benchmarks & Render Charts
    // ----------------------------------------------------------------------
    async function loadBenchmarksData() {
        try {
            const res = await fetch("/api/benchmarks");
            const data = await res.json();

            // Populate Table
            const tbody = document.getElementById("tbody-final-comparison");
            tbody.innerHTML = "";

            const modelsList = [];
            const latencies = [];
            const sizes = [];

            data.final_comparison.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><b>${row["Model / Method"]}</b></td>
                    <td><span class="highlight-text">${row["Accuracy (%)"]}%</span></td>
                    <td>${row["Precision (%)"]}%</td>
                    <td>${row["Recall (%)"]}%</td>
                    <td>${row["F1-Score (%)"]}%</td>
                    <td><code>${row["Trainable Params"]}</code></td>
                    <td><b>${row["Model Size (MB)"]} MB</b></td>
                    <td><span style="color:#60a5fa;">${row["Avg Latency (ms)"]} ms</span></td>
                    <td>${row["Throughput (img/s)"]} img/s</td>
                    <td>${row["RAM Usage (MB)"]} MB</td>
                `;
                tbody.appendChild(tr);

                modelsList.push(row["Model / Method"]);
                latencies.push(row["Avg Latency (ms)"]);
                sizes.push(row["Model Size (MB)"]);
            });

            // Render Charts with Chart.js
            renderLatencyChart(modelsList, latencies);
            renderSizeChart(modelsList, sizes);

        } catch (err) {
            console.error("Failed to load benchmarks:", err);
        }
    }

    function renderLatencyChart(labels, latencies) {
        const ctx = document.getElementById("chart-latency").getContext("2d");
        if (chartLatencyInstance) chartLatencyInstance.destroy();

        chartLatencyInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Inference Latency (ms)",
                    data: latencies,
                    backgroundColor: [
                        "rgba(96, 165, 250, 0.7)",
                        "rgba(167, 139, 250, 0.7)",
                        "rgba(52, 211, 153, 0.9)",
                        "rgba(244, 114, 182, 0.7)",
                        "rgba(99, 102, 241, 0.85)",
                        "rgba(99, 102, 241, 0.85)"
                    ],
                    borderColor: [
                        "#3b82f6", "#8b5cf6", "#10b981", "#ec4899", "#6366f1", "#6366f1"
                    ],
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
                    y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.06)" } }
                }
            }
        });
    }

    function renderSizeChart(labels, sizes) {
        const ctx = document.getElementById("chart-size").getContext("2d");
        if (chartSizeInstance) chartSizeInstance.destroy();

        chartSizeInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Disk File Size (MB)",
                    data: sizes,
                    backgroundColor: [
                        "rgba(148, 163, 184, 0.6)",
                        "rgba(148, 163, 184, 0.6)",
                        "rgba(16, 185, 129, 0.85)",
                        "rgba(239, 68, 68, 0.6)",
                        "rgba(239, 68, 68, 0.6)",
                        "rgba(239, 68, 68, 0.6)"
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { ticks: { color: "#94a3b8", font: { size: 10 } }, grid: { display: false } },
                    y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.06)" } }
                }
            }
        });
    }

    // ----------------------------------------------------------------------
    // 8. Load Robustness Table
    // ----------------------------------------------------------------------
    async function loadRobustnessData() {
        try {
            const res = await fetch("/api/robustness");
            const data = await res.json();
            const tbody = document.getElementById("tbody-robustness");
            tbody.innerHTML = "";

            data.robustness_results.forEach(row => {
                const tr = document.createElement("tr");
                const adv = row["Ensemble Advantage (%)"];
                const advClass = adv >= 0 ? "color:#34d399;" : "color:#f87171;";

                tr.innerHTML = `
                    <td><b>${row["Condition"]}</b></td>
                    <td>${row["CNN 1 (Baseline) (%)"]}%</td>
                    <td>${row["CNN 2 (Regularized) (%)"]}%</td>
                    <td>${row["CNN 3 (Deeper) (%)"]}%</td>
                    <td><span class="highlight-text">${row["Ensemble (Soft Voting) (%)"]}%</span></td>
                    <td><b style="${advClass}">${adv >= 0 ? '+' : ''}${adv}%</b></td>
                `;
                tbody.appendChild(tr);
            });
        } catch (err) {
            console.error("Failed to load robustness metrics:", err);
        }
    }

    // ----------------------------------------------------------------------
    // 9. Deployment Decision Wizard
    // ----------------------------------------------------------------------
    wizardLatencySlider.addEventListener("input", (e) => {
        const budget = parseInt(e.target.value);
        wizardLatencyVal.textContent = `${budget} ms`;
        updateWizardOutcome(budget);
    });

    function updateWizardOutcome(budget) {
        if (budget < 350) {
            wizardOutcomeBox.innerHTML = `
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:2rem;">⚡</span>
                    <div>
                        <b style="color:#34d399; font-size:1.1rem;">Optimal Choice: CNN 3 (Deeper CNN)</b>
                        <p style="margin:4px 0 0 0; color:#94a3b8;">At a target SLA budget of <b>${budget} ms</b>, CNN 3 is the clear winner. It delivers <b>100% test accuracy</b>, requires only <b>70,050 parameters</b>, and consumes just <b>0.86 MB</b> on disk with a lightning-fast <b>183.6 ms</b> average latency.</p>
                    </div>
                </div>
            `;
        } else {
            wizardOutcomeBox.innerHTML = `
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:2rem;">🛡️</span>
                    <div>
                        <b style="color:#818cf8; font-size:1.1rem;">Optimal Choice: Soft Voting Ensemble</b>
                        <p style="margin:4px 0 0 0; color:#94a3b8;">With a generous budget of <b>${budget} ms</b>, the Soft Voting Ensemble is recommended. It eliminates single-model blindspots, guarantees multi-model consensus, and provides automated disagreement gating for high-stakes audits.</p>
                    </div>
                </div>
            `;
        }
    }

    // Initializations
    loadTestSamples();
    updateWizardOutcome(250);
});
