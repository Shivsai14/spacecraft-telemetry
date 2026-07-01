# Project Overview: Spacecraft Telemetry Health Console

The Spacecraft Telemetry Health Console is an advanced decision-support interface engineered to assist mission operators during critical, high-pressure satellite passes. By unifying structured numerical engineering metrics with unstructured operational commentary, the system delivers real-time severity verdicts, clear diagnostic reasoning, and multi-source uncertainty metrics. 

---

## 🏗️ System Fundamentals & Architecture

Modern space missions require ground operators to cross-reference multiple data domains simultaneously under strict time constraints. This tool addresses that challenge through a modular, deterministic three-stage processing pipeline that fuses qualitative human observations with quantitative sensor telemetry.
┌──────────────────────────────┐
              │ Unstructured Operator Notes  │
              └──────────────┬───────────────┘
                             │
┌──────────────────────┐         ▼         ┌─────────────────────────┐
│ Raw Telemetry Stream ├─> [Pipeline Core] ├─> [Context Fusion Layer]│
└──────────────────────┘         │         └────────────┬────────────┘
▼                      │
┌──────────────────────────────┐      │
│   Deterministic Safety Gate  │<─────┘
└──────────────┬───────────────┘
│
▼
┌──────────────────────────────┐
│   High-Visibility Dashboard  │
└──────────────────────────────┘


### 1. Hard-Limit & Out-of-Limits (OOL) Guarding
At the foundation of the pipeline is a strict, rule-based safety gate. Raw telemetry streams are immediately verified against hardcoded hardware thresholds (e.g., maximum temperature envelopes or critical voltage floors). If an operational red-line is crossed, the system immediately forces a **CRITICAL** status. This deterministic layer cannot be overridden or downgraded by any downstream probabilistic models, aligning with baseline aerospace safety procedures.

### 2. Statistical Anomaly & Trend Parsing
For values within nominal bounds, the system evaluates contextual health by computing parametric $Z$-scores against established historical baselines. Rather than relying on single-point telemetry checks, the backend analyzes temporal gradients using linear regression over preceding pass windows. This isolates slow, cross-pass structural degradation trends—such as sub-component thermal degradation—before they cause an emergency boundary breach.

### 3. Multi-Modal Context Fusion
The final stage correlates statistical telemetry summaries with unstructured, qualitative notes logged by console personnel. This enables the console to recognize critical operational context. For example, a sudden drop in battery voltage is interpreted as a expected, stable event if the telemetry indicates an active eclipse window and the operator's notes confirm it. Crucially, if an operator note states "all clear" while the telemetry shows an ongoing structural anomaly, the system flags a severe contradiction, drops its overall confidence rating, and prompts the user to investigate the data divergence.

---

## 📊 Core Directory Map

* **`app.py`** – The interactive graphical front-end built using Streamlit. Tailored for intense monitoring rooms, it provides clean sidebar menus, responsive telemetry metrics, visual hazard indicators, and a human-in-the-loop decision capture form with a persistent session log.
* **`analyzer.py`** – The multi-modal processing engine. Houses the programmatic limit checkers, statistical trend tools, and the deterministic fallback reasoning structures.
* **`telemetry_data.py`** – The synthetic operational data layer. Generates realistic, diverse orbital pass scenarios, modeling failure profiles such as thermal runaway, orbital eclipse transitions, and operator-sensor data contradictions.

---

## 🚀 Deployment & Local Execution

### Prerequisites
Ensure your local environment has Python installed. Then, initialize the required dependencies using the terminal:
```bash
pip install -r requirements.txt
