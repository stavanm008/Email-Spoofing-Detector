# 📧 SatyaPatra

## 🛡️ Email Spoofing Detection & Forensic Analysis Tool

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-black?style=for-the-badge\&logo=flask)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Email%20Forensics-green?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Naive%20Bayes-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

---

## 🚀 Project Overview

**SatyaPatra** is a cybersecurity-focused email forensic analysis tool designed to verify whether an email is **genuine, suspicious, or spoofed**.

The name **SatyaPatra** means a **truthful or verified message**. Since email spoofing attacks fake sender identity, this project checks whether the visible sender identity and technical sender details are properly aligned or mismatched.

SatyaPatra analyzes raw `.eml` email files and evaluates them using a multi-layer detection engine that combines:

* 🧾 SPF verification
* 🔐 DKIM verification
* 🛡️ Sender identity alignment
* 🌐 AbuseIPDB IP reputation intelligence
* 🤖 Machine Learning-based content classification
* ⚡ Bulk asynchronous email processing
* 📊 Risk scoring and dashboard visualization

Instead of simply saying “spam” or “not spam,” SatyaPatra gives an explainable risk score and classifies each email as:

| Final Score | Classification | Status Color | Meaning                                                                        |
| ----------- | -------------- | ------------ | ------------------------------------------------------------------------------ |
| `< 30`      | 🟢 **SECURE**  | Green        | Low-risk email with no major spoofing, phishing, or reputation indicators      |
| `30 - 59`   | 🟡 **CAUTION** | Yellow       | Suspicious email requiring manual review                                       |
| `60+`       | 🔴 **THREAT**  | Red          | High-risk email likely involving spoofing, impersonation, or phishing behavior |

---

## 👨‍💻 Author

**Glen Fernandes**
Cybersecurity Enthusiast | Web Developer | B.E. CSE Undergrad

🔗 LinkedIn: https://www.linkedin.com/in/glen-ferns/
💻 GitHub: https://github.com/glenjr009

---

## 🎯 Objectives

The main objectives of this project are:

* 🔍 Analyze raw `.eml` email files for spoofing and phishing indicators
* 🛡️ Validate sender infrastructure using SPF checks
* 🧾 Detect mismatches between visible sender and technical sender domains
* 🔐 Verify DKIM-based cryptographic integrity
* 🌐 Use AbuseIPDB for sender IP reputation analysis
* 🤖 Apply Machine Learning for phishing-like content detection
* ⚡ Process multiple emails concurrently using asynchronous workers
* 📊 Classify emails as `SECURE`, `CAUTION`, or `THREAT`
* 📤 Export structured forensic reports in CSV format

---

## ✨ Key Features

| Feature                          | Description                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------ |
| ⚡ **Asynchronous Processing**    | Uses `ThreadPoolExecutor` with 20 workers for concurrent bulk email analysis         |
| 📤 **Manual Diagnostics**        | Allows users to upload one or more `.eml` files directly through the dashboard       |
| 📁 **Automated Batch Ingestion** | Scans emails placed inside the `/TEST_SAMPLES` directory                             |
| 🧾 **SPF Verification**          | Checks whether the sending server is authorized to send email for the claimed domain |
| 🔐 **DKIM Verification**         | Validates cryptographic email signatures                                             |
| 🛡️ **Identity Alignment**       | Compares visible `From` domain with technical `Return-Path` domain                   |
| 🌐 **OSINT Threat Intelligence** | Uses AbuseIPDB to check sender IP reputation                                         |
| 🧠 **L1 Reputation Cache**       | Stores repeated IP reputation lookups in memory to improve speed                     |
| 🤖 **ML Content Classification** | Uses TF-IDF and Multinomial Naive Bayes for phishing-like text detection             |
| 📊 **Dashboard Visualization**   | Uses Chart.js to show risk distribution, scores, and processing latency              |
| 🎨 **Cyber-Themed UI**           | Hacker-style responsive dashboard using Bootstrap 5                                  |
| 📤 **CSV Export**                | Exports structured forensic reports for review and incident response                 |

---

## 🧱 Tech Stack

| Layer                  | Technology                         |
| ---------------------- | ---------------------------------- |
| 🐍 Core Language       | Python                             |
| 🌐 Web Framework       | Flask                              |
| 🗂️ Session Management | Flask-Session                      |
| 🚀 Production Server   | Waitress                           |
| 📧 Email Parsing       | Python `email` module              |
| 🧾 SPF Check           | pyspf                              |
| 🔐 DKIM Check          | dkimpy                             |
| 🌐 DNS Operations      | dnspython                          |
| 📡 Threat Intelligence | AbuseIPDB API                      |
| ⚡ Concurrency          | ThreadPoolExecutor                 |
| 🤖 Machine Learning    | scikit-learn                       |
| 🧠 Feature Extraction  | TfidfVectorizer                    |
| 📊 ML Classifier       | MultinomialNB                      |
| 📈 Visualization       | Chart.js                           |
| 🎨 Frontend            | Bootstrap 5, HTML, CSS, JavaScript |
| 📤 Reporting           | CSV Export                         |

---

## 🏗️ System Architecture

```text
Raw .eml Email File
        ↓
Email Header Parsing
        ↓
Sender IP Extraction
        ↓
SPF Verification
        ↓
DKIM Verification
        ↓
Identity Alignment Check
        ↓
AbuseIPDB Reputation Lookup
        ↓
ML-Based Content Classification
        ↓
Multi-Signal Risk Score
        ↓
SECURE / CAUTION / THREAT
        ↓
CSV Forensic Report Export
```

---

## 🧮 Multi-Signal Risk Scoring Matrix

SatyaPatra calculates a final risk score from **0 to 100** using multiple independent threat layers.

| No. | Threat Layer                        | Weight     | Detection Logic                                                                |
| --- | ----------------------------------- | ---------- | ------------------------------------------------------------------------------ |
| 1   | 🧾 Infrastructure Protection Layer  | `+20`      | Performs SPF validation to verify whether the sending server is authorized     |
| 2   | 🛡️ Identity Verification Layer     | `+25`      | Compares the visible `From` domain with the technical `Return-Path` domain     |
| 3   | 🔐 Cryptographic Integrity Layer    | `+15`      | Checks whether DKIM signature is valid, missing, or invalid                    |
| 4   | 🌐 Global Intelligence Layer        | `0 to +50` | Applies penalty based on AbuseIPDB abuse confidence score                      |
| 5   | 🤖 Machine Learning Heuristic Layer | `0 to +30` | Applies penalty based on phishing/spam probability from Naive Bayes classifier |

---

## 🚦 Risk Classification Thresholds

| Final Score | Classification | Status Color | Meaning                                                                        |
| ----------- | -------------- | ------------ | ------------------------------------------------------------------------------ |
| `< 30`      | 🟢 **SECURE**  | Green        | Low-risk email with no major spoofing, phishing, or reputation indicators      |
| `30 - 59`   | 🟡 **CAUTION** | Yellow       | Suspicious email requiring manual review                                       |
| `60+`       | 🔴 **THREAT**  | Red          | High-risk email likely involving spoofing, impersonation, or phishing behavior |

---

## 🤖 Machine Learning Layer

SatyaPatra includes a lightweight Machine Learning-based content analysis layer.

The ML pipeline uses:

* `TfidfVectorizer` for text feature extraction
* `MultinomialNB` for probabilistic classification
* `alpha=1.0` Laplace smoothing for stable classification

### How it works

```text
Email Body Text
      ↓
TF-IDF Vectorization
      ↓
Multinomial Naive Bayes Classifier
      ↓
Spam / Phishing Probability
      ↓
Content Risk Penalty
```

This helps detect suspicious language patterns such as:

* Urgency-based messages
* Fake reward messages
* Password verification requests
* Account suspension warnings
* Phishing-style wording
* Social engineering phrases

---

## ⚡ Asynchronous Processing

SatyaPatra uses Python’s `ThreadPoolExecutor` for concurrent email processing.

```python
ThreadPoolExecutor(max_workers=20)
```

### Benefits

* Faster bulk email analysis
* Better throughput
* Improved demo performance
* More realistic enterprise-style email gateway behavior
* Reduced waiting time during batch scanning

---

## 🌐 AbuseIPDB Threat Intelligence

The system integrates with **AbuseIPDB** to check whether the extracted sender or relay IP address has a bad reputation.

To improve speed and reduce repeated API calls, the system uses an in-memory cache:

```python
intel_cache = {}
```

### Benefits

* Faster repeated scans
* Reduced API usage
* Better rate-limit handling
* Improved batch-processing performance
* More reliable demonstrations

---

## 📁 Project Directory Structure

```text
SatyaPatra-Email-Spoofing-Detector/
│
├── app.py
│   └── Flask routes, dashboard UI, file upload, batch processing, CSV export
│
├── detector.py
│   └── SPF, DKIM, identity alignment, AbuseIPDB, ML scoring engine
│
├── generate_varied.py
│   └── Utility script for generating varied email test samples
│
├── generator_data.py
│   └── Sample data support for email generation
│
├── TEST_SAMPLES/
│   └── Folder for automated batch ingestion of .eml files
│
├── samples/
│   └── Example sample emails
│
├── LICENSE
│   └── MIT License
│
└── README.md
    └── Project documentation
```

---

## ⚙️ Installation Guide

Follow these steps to run the project locally.

---

### ✅ Prerequisites

Make sure you have:

* 🐍 Python 3.10 or above
* 🌿 Git
* 📦 pip
* 🌐 Modern web browser
* 🔑 AbuseIPDB API key

Check Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

## 📥 1. Clone the Repository

```bash
git clone https://github.com/glenjr009/Email-Spoofing-Detector.git
cd Email-Spoofing-Detector
```

---

## 🧪 2. Create a Virtual Environment

### 🪟 Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

### 🐧 Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 3. Install Dependencies

Install dependencies manually:

```bash
pip install flask flask-session pyspf dkimpy dnspython requests waitress pandas scikit-learn
```

Or using `requirements.txt`:

```bash
pip install -r requirements.txt
```

Recommended `requirements.txt`:

```text
flask
flask-session
pyspf
dkimpy
dnspython
requests
waitress
pandas
scikit-learn
```

---

## 🔑 4. Configure AbuseIPDB API Key

SatyaPatra uses AbuseIPDB for live IP reputation scoring.

Create an environment variable named:

```text
ABUSE_IPDB_KEY
```

### 🪟 Windows PowerShell

```powershell
$env:ABUSE_IPDB_KEY="YOUR_API_KEY_HERE"
```

### 🐧 Linux / macOS

```bash
export ABUSE_IPDB_KEY="YOUR_API_KEY_HERE"
```

> ⚠️ Do not hardcode your API key directly inside `detector.py`.

---

## ▶️ 5. Run the Application

```bash
python app.py
```

or:

```bash
python3 app.py
```

---

## 🌐 6. Open the Web Interface

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

## 🧭 Operational Modes

SatyaPatra supports two main workflows:

---

### 📤 Mode 1: Manual Diagnostics

Manual diagnostics allow users to upload `.eml` files directly from the dashboard.

Workflow:

1. Start the application.
2. Open the dashboard.
3. Upload one or more `.eml` files.
4. The system analyzes each email.
5. Review the result as:

   * 🟢 SECURE
   * 🟡 CAUTION
   * 🔴 THREAT
6. Export the forensic CSV report if required.

---

### 📁 Mode 2: Automated Batch Ingestion

The automated pipeline scans emails from the local batch directory.

Workflow:

1. Place `.eml` files inside:

```text
TEST_SAMPLES/
```

2. Start the application.

```bash
python app.py
```

3. Click:

```text
EXECUTE AUTO-SCAN [BATCH]
```

4. Review results on the dashboard.
5. Export the combined CSV report.

---

## 🧪 Generate Test Email Samples

The project includes a utility script to generate different test email samples.

Run:

```bash
python generate_varied.py
```

or:

```bash
python3 generate_varied.py
```

Possible generated test profiles include:

* SPF failure
* DKIM missing
* DKIM invalid
* Identity mismatch
* Suspicious content
* Malicious relay reputation
* Multi-vector threat combinations

---

## 🖥️ Example Pipeline Telemetry

```text
[INIT] SatyaPatra starting forensic gateway...
[INIT] Flask session engine loaded using filesystem-backed storage
[INIT] Waitress WSGI server initialized
[INIT] ML pipeline loading TfidfVectorizer and MultinomialNB(alpha=1.0)
[INIT] Threat intelligence cache initialized: L1_MEMORY_CACHE

[INGEST] Source: TEST_SAMPLES/
[INGEST] Detected file: invoice_security_alert.eml
[QUEUE] Submitted job to ThreadPoolExecutor worker pool

[WORKER-07] Parsing RFC 5322 headers...
[WORKER-07] SPF result: FAIL | Penalty: +20
[WORKER-07] DKIM result: MISSING | Penalty: +15
[WORKER-07] Identity alignment: MISMATCH | Penalty: +25
[WORKER-07] AbuseIPDB lookup: 42 confidence | Penalty: +21
[WORKER-07] ML phishing probability: 73% | Penalty: +22
[WORKER-07] Final risk score: 100
[WORKER-07] Classification: THREAT

[EXPORT] CSV forensic report generated successfully
[STATUS] Dashboard telemetry updated
```

---

## 📊 Example Risk Output

```text
Email File: invoice_security_alert.eml
Classification: 🔴 THREAT
Final Score: 100

Triggered Signals:
- SPF Check Failure: +20
- Identity Verification Mismatch: +25
- Missing DKIM Signature: +15
- AbuseIPDB Reputation Penalty: +21
- ML Phishing Confidence Penalty: +22

Recommendation:
This email should be treated as a high-risk phishing or spoofing attempt.
Do not click embedded links or download attachments.
Escalate the sample for manual incident response review.
```

---

## 📤 CSV Export Report

The forensic export hub generates a structured `.csv` report for scanned emails.

| Field          | Description                                |
| -------------- | ------------------------------------------ |
| File           | Name of the analyzed `.eml` file           |
| Subject        | Email subject line                         |
| Score          | Final calculated risk score                |
| Classification | SECURE, CAUTION, or THREAT                 |
| Status Color   | Green, Yellow, or Red                      |
| Meaning        | Human-readable interpretation of the score |
| Reasons        | Triggered detection signals                |

---

## 🧠 Detection Logic Summary

SatyaPatra does not rely on a single signal.

Instead, it combines deterministic verification and probabilistic ML scoring:

* 🧾 SPF validates sender infrastructure
* 🛡️ Identity alignment detects impersonation gaps
* 🔐 DKIM checks cryptographic integrity
* 🌐 AbuseIPDB evaluates network reputation
* 🤖 MultinomialNB estimates phishing-like content probability
* ⚡ ThreadPoolExecutor enables concurrent bulk scanning

This layered approach provides a more explainable and practical email forensic assessment.

---

## 🎨 Dashboard Preview

The dashboard includes:

* Cyber-themed responsive UI
* Manual `.eml` upload module
* Automated batch scan module
* Three-level risk classification guide
* Real-time risk distribution chart
* Score visualization chart
* Pipeline latency chart
* Structured forensic logs
* CSV export option
* Clickable developer signature

---

## 🚀 Future Enhancements

Planned improvements include:

* 🔗 Authenticated Received Chain support
* 🧠 Redis-based L2 reputation caching
* 📩 DMARC RUA XML report parser
* 📎 Email attachment scanning
* 🔍 Embedded URL extraction and phishing domain analysis
* 🌐 VirusTotal or URLScan.io integration
* 🗂️ Case management and investigation tagging
* 👥 Role-based analyst dashboard
* 📄 PDF incident report export
* 🐳 Docker deployment support
* ⚙️ CI/CD pipeline with automated test execution
* 🧪 Unit tests for scoring and protocol modules
* 📬 Real-time mailbox ingestion using IMAP
* 📈 Model retraining pipeline using labeled phishing datasets

---

## 🎓 Academic Relevance

This project demonstrates practical implementation of cybersecurity and software engineering concepts, including:

* Email authentication protocols
* Digital forensics
* Threat intelligence integration
* Machine Learning-based text classification
* TF-IDF feature extraction
* Naive Bayes classification
* Concurrent programming
* Web application development
* Incident response reporting
* Risk-based classification systems

---

## 🧹 Recommended `.gitignore`

To keep the repository clean, use this `.gitignore`:

```gitignore
__pycache__/
*.pyc
flask_session/
venv/
.env
.DS_Store
*.log
```

If generated folders were already committed, remove them from Git tracking:

```bash
git rm -r --cached __pycache__ flask_session
git add .gitignore
git commit -m "Clean generated cache and session files"
git push
```

---

## ⚠️ Disclaimer

This project is developed strictly for educational, academic, portfolio, and defensive cybersecurity purposes.

It must not be used for:

* Phishing
* Spamming
* Unauthorized testing
* Malicious email generation
* Attacking third-party systems
* Bypassing security controls
* Any activity that violates law, policy, or ethical cybersecurity practice

The purpose of this project is to help users understand, detect, and defend against email spoofing, phishing, and identity impersonation attacks.

---

## 📄 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project for educational and research purposes, provided proper credit is given.

---

## 🔗 Repository

Clone the project using:

```bash
git clone https://github.com/glenjr009/Email-Spoofing-Detector.git
```

If you like this project or found it useful, consider giving it a ⭐ on GitHub.

---

## 💡 Final Note

**SatyaPatra** provides a structured and explainable approach to email spoofing detection by combining protocol verification, OSINT threat intelligence, asynchronous processing, and Machine Learning-based phishing content analysis.

The project demonstrates how modern email forensic systems can move beyond static keyword heuristics and adopt a layered detection model that is scalable, interpretable, and practical for real-world cybersecurity workflows.

---

<p align="center">
  <b>🛡️ Developed by Glen Fernandes aka cyb3rPh03n1x🛡️</b>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/glen-ferns/">LinkedIn</a> •
  <a href="https://github.com/glenjr009">GitHub</a>
</p>
