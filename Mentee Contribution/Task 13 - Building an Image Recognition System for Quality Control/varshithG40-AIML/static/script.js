/**
 * AeroCast AI Front-end Controller
 * Handles interactive drag & drop, sample gallery, threshold slider, SVG gauge animation, and Heatmap toggling.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const samplesGrid = document.getElementById('samplesGrid');
    const thresholdSlider = document.getElementById('thresholdSlider');
    const thresholdDisplay = document.getElementById('thresholdDisplay');
    const tThreshold = document.getElementById('tThreshold');
    
    const activeFileName = document.getElementById('activeFileName');
    const verdictBanner = document.getElementById('verdictBanner');
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictTitle = document.getElementById('verdictTitle');
    const verdictSubtitle = document.getElementById('verdictSubtitle');
    
    const tabOriginal = document.getElementById('tabOriginal');
    const tabHeatmap = document.getElementById('tabHeatmap');
    const inspectionImage = document.getElementById('inspectionImage');
    
    const gaugeMeter = document.getElementById('gaugeMeter');
    const gaugeNumber = document.getElementById('gaugeNumber');
    const actionCard = document.getElementById('actionCard');
    const actionText = document.getElementById('actionText');

    let currentImageData = null; // Holds current file or sample_filename
    let currentPredictionResult = null;
    let activeVisualMode = 'original'; // 'original' or 'heatmap'

    // Fetch and populate factory sample gallery
    fetchSamples();

    // Slider Event
    thresholdSlider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value).toFixed(2);
        const pct = (val * 100).toFixed(0) + '%';
        thresholdDisplay.textContent = pct;
        tThreshold.textContent = pct;

        // If we already have prediction data, re-evaluate verdict instantly!
        if (currentPredictionResult) {
            updateUIResults(currentPredictionResult, parseFloat(val));
        }
    });

    // Dropzone Events
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('active');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('active');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('active');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Image Feed Tab Switching
    tabOriginal.addEventListener('click', () => {
        tabOriginal.classList.add('active');
        tabHeatmap.classList.remove('active');
        activeVisualMode = 'original';
        if (currentPredictionResult) {
            inspectionImage.src = currentPredictionResult.image_url;
        }
    });

    tabHeatmap.addEventListener('click', () => {
        tabHeatmap.classList.add('active');
        tabOriginal.classList.remove('active');
        activeVisualMode = 'heatmap';
        if (currentPredictionResult) {
            inspectionImage.src = currentPredictionResult.heatmap_url;
        }
    });

    // Helper: Fetch Factory Samples
    async function fetchSamples() {
        try {
            const res = await fetch('/api/samples');
            const data = await res.json();
            if (data.success && data.samples.length > 0) {
                samplesGrid.innerHTML = '';
                data.samples.forEach(sample => {
                    const chip = document.createElement('div');
                    chip.className = 'sample-chip';
                    chip.innerHTML = `
                        <img src="${sample.url}" alt="${sample.filename}">
                        <span>${sample.filename}</span>
                    `;
                    chip.addEventListener('click', () => {
                        document.querySelectorAll('.sample-chip').forEach(c => c.classList.remove('active'));
                        chip.classList.add('active');
                        handleSampleSelect(sample.filename);
                    });
                    samplesGrid.appendChild(chip);
                });
            }
        } catch (err) {
            console.error("Failed to load factory samples:", err);
        }
    }

    // Handle File Upload
    function handleFileUpload(file) {
        document.querySelectorAll('.sample-chip').forEach(c => c.classList.remove('active'));
        currentImageData = { type: 'file', data: file };
        runInference();
    }

    // Handle Sample Select
    function handleSampleSelect(filename) {
        currentImageData = { type: 'sample', data: filename };
        runInference();
    }

    // Execute Inference API call
    async function runInference() {
        if (!currentImageData) return;

        const formData = new FormData();
        formData.append('threshold', thresholdSlider.value);

        if (currentImageData.type === 'file') {
            formData.append('file', currentImageData.data);
        } else {
            formData.append('sample_filename', currentImageData.data);
        }

        activeFileName.textContent = "Analyzing Image...";
        
        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                currentPredictionResult = result;
                updateUIResults(result, parseFloat(thresholdSlider.value));
            } else {
                alert("Inspection Error: " + result.error);
            }
        } catch (err) {
            console.error("Inference request failed:", err);
            alert("Failed to connect to AeroCast AI backend server.");
        }
    }

    // Update UI with Prediction Results & Gauge Animation
    function updateUIResults(result, currentThreshold) {
        activeFileName.textContent = result.filename;

        const prob = result.defect_probability;
        const isDefective = prob >= currentThreshold;

        // Banner Verdict Update
        verdictBanner.className = `verdict-banner ${isDefective ? 'defect' : 'pass'}`;
        if (isDefective) {
            verdictIcon.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i>`;
            verdictTitle.textContent = "DEFECTIVE PRODUCT DETECTED";
            verdictSubtitle.textContent = `Defect probability (${(prob*100).toFixed(1)}%) exceeds safety threshold (${(currentThreshold*100).toFixed(1)}%).`;
            
            actionCard.className = "action-card defect";
            actionText.innerHTML = `<strong>🚨 REJECT ACTION:</strong> Divert product to manual inspection station / purge from conveyor.`;
        } else {
            verdictIcon.innerHTML = `<i class="fa-solid fa-circle-check"></i>`;
            verdictTitle.textContent = "NON-DEFECTIVE (PASSED)";
            verdictSubtitle.textContent = `Defect probability (${(prob*100).toFixed(1)}%) is within acceptable quality limits.`;
            
            actionCard.className = "action-card pass";
            actionText.innerHTML = `<strong>🟢 PASSED ACTION:</strong> Product meets factory quality criteria. Proceed on conveyor.`;
        }

        // Image View Update
        if (activeVisualMode === 'heatmap') {
            inspectionImage.src = result.heatmap_url;
        } else {
            inspectionImage.src = result.image_url;
        }

        // Animated SVG Gauge Meter Update
        const percentage = Math.round(prob * 100);
        gaugeNumber.textContent = `${(prob * 100).toFixed(1)}%`;
        
        const circumference = 314; // 2 * PI * r (r=50)
        const offset = circumference - (prob * circumference);
        gaugeMeter.style.strokeDashoffset = offset;
        
        if (isDefective) {
            gaugeMeter.style.stroke = "var(--defect-red)";
            gaugeNumber.style.color = "var(--defect-red)";
        } else {
            gaugeMeter.style.stroke = "var(--pass-green)";
            gaugeNumber.style.color = "var(--pass-green)";
        }
    }
});
