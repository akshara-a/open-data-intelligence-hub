const countrySelect = document.querySelector("#countrySelect");
const remoteWorkSelect = document.querySelector("#remoteWorkSelect");
const yearsInput = document.querySelector("#yearsInput");
const predictionForm = document.querySelector("#predictionForm");
const resultCard = document.querySelector("#resultCard");
const resultText = document.querySelector("#resultText");
const errorCard = document.querySelector("#errorCard");
const errorText = document.querySelector("#errorText");
const downloadPdfBtn = document.querySelector("#downloadPdfBtn");
const currencySelect = document.querySelector("#currencySelect");

let lastPrediction = null;
let rawPredictedSalary = 0;
let rawTrajectory = [];

const exchangeRates = {
  USD: { rate: 1, symbol: "$" },
  EUR: { rate: 0.92, symbol: "€" },
  GBP: { rate: 0.79, symbol: "£" },
  INR: { rate: 83.5, symbol: "₹" },
  CAD: { rate: 1.37, symbol: "C$" },
  AUD: { rate: 1.52, symbol: "A$" }
};

async function loadMetadata() {
  try {
    const response = await fetch("/metadata");
    if (!response.ok) {
      throw new Error("Unable to load metadata.");
    }
    const metadata = await response.json();
    populateSelect(countrySelect, metadata.countries, "Select a country");
    populateSelect(remoteWorkSelect, metadata.remoteWorkOptions, "Select a remote work style");
    return;
  } catch (error) {
    return loadMetadataFromStatic();
  }
}

async function loadMetadataFromStatic() {
  try {
    const response = await fetch("model_metadata.json");
    if (!response.ok) {
      throw new Error("Unable to load metadata from local file.");
    }
    const metadata = await response.json();
    populateSelect(countrySelect, metadata.countries, "Select a country");
    populateSelect(remoteWorkSelect, metadata.remoteWorkOptions, "Select a remote work style");
  } catch (error) {
    showError(
      "Unable to load metadata. Make sure the app is running from the Flask server and that model_metadata.json is present."
    );
  }
}

function populateSelect(selectElement, values, placeholder) {
  selectElement.innerHTML = "";
  const placeholderOption = document.createElement("option");
  placeholderOption.value = "";
  placeholderOption.textContent = placeholder;
  placeholderOption.disabled = true;
  placeholderOption.selected = true;
  selectElement.appendChild(placeholderOption);

  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    selectElement.appendChild(option);
  });
}

function showResult(message) {
  resultText.textContent = message;
  resultCard.classList.remove("hidden");
  errorCard.classList.add("hidden");
}

function showError(message) {
  errorText.textContent = message;
  errorCard.classList.remove("hidden");
  resultCard.classList.add("hidden");
}

predictionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const country = countrySelect.value;
  const remoteWork = remoteWorkSelect.value;
  const years = parseFloat(yearsInput.value);

  if (!country || !remoteWork || Number.isNaN(years)) {
    showError("Please select country, remote work style, and enter years of experience.");
    return;
  }

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Country: country,
        YearsCodePro: years,
        RemoteWork: remoteWork,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction request failed.");
    }

    rawPredictedSalary = data.predictedSalary;
    rawTrajectory = data.trajectory || [];

    updateDisplayedSalary();

    resultCard.classList.remove("hidden");
    errorCard.classList.add("hidden");
  } catch (error) {
    showError(error.message);
  }
});

function formatSalary(amount, currency) {
  const { rate, symbol } = exchangeRates[currency];
  const converted = amount * rate;
  return `${symbol}${converted.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function updateDisplayedSalary() {
  if (rawPredictedSalary > 0) {
    const currency = currencySelect.value;
    const formattedSalary = formatSalary(rawPredictedSalary, currency);
    resultText.textContent = `Estimated yearly salary: ${formattedSalary}`;
    
    // Update lastPrediction for PDF
    lastPrediction = {
      country: countrySelect.value,
      remoteWork: remoteWorkSelect.value,
      years: parseFloat(yearsInput.value),
      salary: formattedSalary
    };
    
    renderTrajectoryChart();
  }
}

if (currencySelect) {
  currencySelect.addEventListener("change", updateDisplayedSalary);
}

function renderTrajectoryChart() {
  if (!rawTrajectory || rawTrajectory.length === 0 || typeof Plotly === 'undefined') return;

  const currency = currencySelect.value;
  const { rate, symbol } = exchangeRates[currency];

  const xData = rawTrajectory.map(t => t.years);
  const yData = rawTrajectory.map(t => t.salary * rate);

  const chartData = [{
    x: xData,
    y: yData,
    type: 'scatter',
    mode: 'lines+markers',
    line: { color: '#3b82f6', width: 3, shape: 'spline' },
    marker: { color: '#60a5fa', size: 8 },
    fill: 'tozeroy',
    fillcolor: 'rgba(59, 130, 246, 0.1)'
  }];

  const chartLayout = {
    plot_bgcolor: 'transparent',
    paper_bgcolor: 'transparent',
    font: { color: '#f8fafc', family: 'Inter, system-ui, sans-serif' },
    margin: { t: 30, r: 20, l: 60, b: 40 },
    height: 250,
    title: { text: 'Career Trajectory Estimate', font: { size: 14, color: '#94a3b8' } },
    xaxis: {
      title: { text: 'Years of Experience', font: { size: 12 } },
      gridcolor: '#334155'
    },
    yaxis: {
      title: { text: `Salary (${symbol})`, font: { size: 12 } },
      gridcolor: '#334155',
      zerolinecolor: '#334155'
    }
  };

  const chartConfig = { responsive: true, displayModeBar: false };
  Plotly.newPlot('trajectoryChart', chartData, chartLayout, chartConfig);
}

if (downloadPdfBtn) {
  downloadPdfBtn.addEventListener("click", async () => {
    if (!lastPrediction || !window.jspdf) return;

    // Show loading state on button
    const originalText = downloadPdfBtn.textContent;
    downloadPdfBtn.textContent = "Generating PDF...";
    downloadPdfBtn.disabled = true;

    try {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();

      // 1. Top Header Bar
      doc.setFillColor(30, 41, 59); // Dark blue header
      doc.rect(0, 0, pageWidth, 28, 'F');
      
      // 2. Header Text
      doc.setFontSize(22);
      doc.setTextColor(255, 255, 255);
      doc.text("Salary Analytics Dashboard", 14, 18);
      
      // 3. Report Date & ID
      const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
      const reportId = "RPT-" + Math.floor(Math.random() * 1000000);
      doc.setFontSize(10);
      doc.setTextColor(148, 163, 184); // Slate 400
      doc.text(`Date: ${today}`, pageWidth - 14, 14, { align: 'right' });
      doc.text(`Ref ID: ${reportId}`, pageWidth - 14, 20, { align: 'right' });

      // 4. Sub Heading & Intro
      doc.setFontSize(16);
      doc.setTextColor(15, 23, 42); // Dark slate
      doc.text("Confidential Compensation Estimate", 14, 45);
      
      doc.setFontSize(11);
      doc.setTextColor(71, 85, 105);
      const introText = "Based on our proprietary machine learning model trained on global software engineering survey data, we have prepared the following estimate tailored to the candidate's profile parameters.";
      const splitIntro = doc.splitTextToSize(introText, pageWidth - 28);
      doc.text(splitIntro, 14, 55);

      // 5. Table using autoTable
      doc.autoTable({
        startY: 75,
        head: [['Parameter', 'Selected Profile Value']],
        body: [
          ['Country of Residence', lastPrediction.country],
          ['Work Arrangement', lastPrediction.remoteWork],
          ['Professional Experience', `${lastPrediction.years} Years`],
          ['Predicted Compensation', lastPrediction.salary]
        ],
        theme: 'grid',
        headStyles: { 
          fillColor: [59, 130, 246], // Blue 500
          textColor: 255, 
          fontStyle: 'bold',
          fontSize: 12
        },
        bodyStyles: { 
          fontSize: 11,
          textColor: [51, 65, 85]
        },
        alternateRowStyles: { 
          fillColor: [241, 245, 249] // Slate 100
        },
        columnStyles: {
          0: { fontStyle: 'bold', cellWidth: 80 }
        },
        margin: { left: 14, right: 14 }
      });

      // 6. Disclaimer
      let currentY = doc.lastAutoTable.finalY + 15;
      doc.setFontSize(9);
      doc.setTextColor(100, 116, 139);
      doc.text("Disclaimer: This compensation estimate is generated for informational and comparative purposes only. Actual market rates may vary based on specific company resources, comprehensive benefits packages, and individual negotiations.", 14, currentY, { maxWidth: pageWidth - 28 });
      
      // 7. Trajectory Chart
      currentY += 20;
      try {
        const trajectoryDiv = document.getElementById('trajectoryChart');
        // Only try to generate image if Plotly has rendered something
        if (trajectoryDiv && trajectoryDiv.data) {
          const imgData = await Plotly.toImage(trajectoryDiv, { format: 'png', width: 800, height: 450 });
          doc.setFontSize(14);
          doc.setTextColor(15, 23, 42);
          doc.text("Career Trajectory Projection", 14, currentY);
          currentY += 8;
          doc.addImage(imgData, 'PNG', 14, currentY, 180, 101); // Aspect ratio ~1.77
        }
      } catch (e) {
        console.warn("Could not capture Plotly chart", e);
      }

      // 8. Footer
      doc.setDrawColor(226, 232, 240);
      doc.line(14, pageHeight - 20, pageWidth - 14, pageHeight - 20);
      doc.setFontSize(10);
      doc.setTextColor(148, 163, 184);
      doc.text('Created by "Varsha Chinnanarasannagari" | Salary Analytics Dashboard', 14, pageHeight - 12);

      // Download
      doc.save(`Salary_Prediction_${lastPrediction.country.replace(/\s+/g, '_')}.pdf`);
    } finally {
      // Restore button state
      downloadPdfBtn.textContent = originalText;
      downloadPdfBtn.disabled = false;
    }
  });
}

loadMetadata();

// Render top countries chart using Plotly
function renderChart() {
  const chartData = [{
    x: ['Gabon', 'Ethiopia', 'United States', 'Singapore', 'South Africa', 'Taiwan', 'Antigua & Barbuda', 'Andorra', 'Israel', 'Switzerland'],
    y: [2000000, 930000, 160000, 135000, 135000, 130000, 130000, 125000, 125000, 125000],
    type: 'bar',
    marker: {
      color: '#3b82f6'
    }
  }];

  const chartLayout = {
    plot_bgcolor: 'transparent',
    paper_bgcolor: 'transparent',
    font: { color: '#f8fafc', family: 'Inter, system-ui, sans-serif' },
    margin: { t: 40, r: 20, l: 60, b: 80 },
    height: 320,
    xaxis: {
      tickangle: -45,
      title: { text: 'Country', font: { size: 14 } }
    },
    yaxis: {
      title: { text: 'Average Salary ($)', font: { size: 14 } },
      gridcolor: '#334155',
      zerolinecolor: '#334155'
    }
  };

  const chartConfig = { responsive: true, displayModeBar: false };

  Plotly.newPlot('topCountriesChart', chartData, chartLayout, chartConfig);
}

// Try to render the chart immediately or wait for Plotly to load
function tryRenderChart() {
  if (typeof Plotly !== 'undefined') {
    renderChart();
  } else {
    // Retry periodically if Plotly is loaded asynchronously
    const retryInterval = setInterval(() => {
      if (typeof Plotly !== 'undefined') {
        clearInterval(retryInterval);
        renderChart();
      }
    }, 100);
    // Stop retrying after 5 seconds to prevent infinite loop
    setTimeout(() => clearInterval(retryInterval), 5000);
  }
}

tryRenderChart();
