# Problem Statement: Resilient, Multi-Agent Tax Rule Engine & Data Reconciler

## 1. Background

A financial technology platform receives a constant influx of unstructured, messy financial data from various client systems. This data must be accurately reconciled and processed through a complex, constantly updating tax depreciation library before being exported as a standardized file for official tax filing. Given the critical nature of financial data, the system must be highly reliable, resilient to cloud outages, and fully auditable.

## 2. The Challenge

Client inputs are wildly inconsistent, ranging from unstructured emails to CSV attachments with varying schemas. The challenge is twofold: first, standardizing this chaotic input without losing critical financial context; second, applying dynamic tax rules accurately. Furthermore, because this is a mission-critical financial pipeline, the architecture cannot rely solely on a single cloud-based LLM API, which might experience downtime or latency spikes.

## 3. Technical Requirements

### 3.1 Inputs

* Raw, unstructured financial emails from clients.
* Attached data files (e.g., CSVs, Excel) with non-standardized schemas.
* Current, region-specific tax code documentation and external tax depreciation libraries.

### 3.2 System Architecture

The solution must architect a resilient, local-cloud hybrid multi-agent system:

1. **Ingestion Agent:** Responsible for parsing messy inputs, extracting relevant financial figures, and normalizing the data into a standardized schema.
2. **Reasoning Agent:** Responsible for querying an external tax depreciation library and calculating the dynamic tax rules against the normalized data.
3. **Supervisor Agent:** Orchestrates the workflow between agents and manages error handling.
4. **Hybrid Fallback Mechanism:** The Supervisor must feature a zero-dependency fallback architecture. If the primary cloud LLM endpoint (e.g., OpenAI, Anthropic) fails or times out, the Supervisor must seamlessly route generative reasoning tasks to a locally hosted model (such as an LPU-accelerated Llama 3 or a local Ollama instance) to ensure uninterrupted processing.

### 3.3 Outputs

* A deterministic, custom file-based export (e.g., standardized JSON or CSV) containing the final calculated tax inputs, ready for system consumption.
* A generative, human-readable audit log that explains the step-by-step mathematical reasoning the multi-agent system used to reconcile the raw data against the depreciation rules.

## 4. Success Criteria

* **Data Normalization Accuracy:** The Ingestion Agent must accurately map varying client schemas to the internal standard with near-perfect reliability.
* **System Resilience:** The fallback routing must execute automatically during simulated cloud outages with zero data loss.
* **Explainability:** The generated audit log must provide transparent, mathematically sound reasoning that a human auditor can easily verify.
