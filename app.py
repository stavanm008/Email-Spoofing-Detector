import os
import csv
import io
import email
import concurrent.futures
import time
from flask import Flask, request, render_template_string, send_file, session
from flask_session import Session
from detector import analyze_email
from waitress import serve

app = Flask(__name__)
app.secret_key = "v0rtex_secure_gate"

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(app.root_path, "flask_session")

if not os.path.exists(app.config["SESSION_FILE_DIR"]):
    os.makedirs(app.config["SESSION_FILE_DIR"])

Session(app)

TEST_SAMPLES_DIR = "TEST_SAMPLES"

if not os.path.exists(TEST_SAMPLES_DIR):
    os.makedirs(TEST_SAMPLES_DIR)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SATYAPATRA // THREAT_STREAM</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Orbitron:wght@500;800;900&display=swap" rel="stylesheet">

    <style>
        :root {
            --neon-green: #00ff41;
            --neon-cyan: #00d2ff;
            --neon-red: #ff3131;
            --neon-yellow: #ffd166;
            --neon-pink: #ff2bd6;
            --dark-bg: #020403;
            --card-bg: rgba(8, 14, 12, 0.88);
            --soft-border: rgba(0, 255, 65, 0.18);
        }

        * {
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            background:
                radial-gradient(circle at 18% 12%, rgba(0, 255, 65, 0.14), transparent 28%),
                radial-gradient(circle at 85% 18%, rgba(0, 210, 255, 0.12), transparent 30%),
                linear-gradient(135deg, #010101, #04100b 50%, #010101);
            color: #e5e7eb;
            font-family: 'JetBrains Mono', monospace;
            overflow-x: hidden;
            position: relative;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(0, 255, 65, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.04) 1px, transparent 1px);
            background-size: 36px 36px;
            pointer-events: none;
            z-index: -2;
        }

        body::after {
            content: "";
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                to bottom,
                rgba(255,255,255,0.025),
                rgba(255,255,255,0.025) 1px,
                transparent 1px,
                transparent 4px
            );
            pointer-events: none;
            z-index: -1;
        }

        .navbar {
            min-height: 70px;
            border-bottom: 1px solid var(--neon-green);
            background: rgba(0, 0, 0, 0.92);
            backdrop-filter: blur(14px);
            box-shadow: 0 6px 35px rgba(0, 255, 65, 0.08);
        }

        .navbar-brand {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 1.15rem;
            color: var(--neon-green) !important;
            letter-spacing: 1.5px;
            text-shadow: 0 0 12px rgba(0, 255, 65, 0.85);
        }

        .nav-subtitle {
            color: var(--neon-cyan);
            font-size: 0.78rem;
            letter-spacing: 2px;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
        }

        .status-dot {
            height: 9px;
            width: 9px;
            border-radius: 50%;
            display: inline-block;
            background: var(--neon-green);
            box-shadow: 0 0 12px var(--neon-green);
            margin-right: 8px;
            animation: blink 1.1s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.35; }
        }

        .main-shell {
            max-width: 1380px;
        }

        .hero-panel {
            margin-top: 2.5rem;
            margin-bottom: 2rem;
            padding: 2.5rem;
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(0, 255, 65, 0.10), rgba(0, 210, 255, 0.04), rgba(0, 0, 0, 0.35));
            border: 1px solid rgba(0, 255, 65, 0.22);
            box-shadow:
                0 25px 80px rgba(0, 0, 0, 0.65),
                inset 0 0 45px rgba(0, 255, 65, 0.035);
            position: relative;
            overflow: hidden;
        }

        .hero-panel::before {
            content: "";
            position: absolute;
            top: 0;
            left: -120%;
            width: 80%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.13), transparent);
            animation: scanHero 5s infinite;
        }

        @keyframes scanHero {
            0% { left: -120%; }
            55% { left: 130%; }
            100% { left: 130%; }
        }

        .hero-kicker {
            font-family: 'Rajdhani', sans-serif;
            color: var(--neon-cyan);
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 4px;
            text-transform: uppercase;
            position: relative;
            z-index: 2;
        }

        .hero-title {
            position: relative;
            z-index: 2;
            font-family: 'Rajdhani', sans-serif;
            font-size: clamp(3rem, 7vw, 6.3rem);
            line-height: 0.92;
            font-weight: 700;
            letter-spacing: -1px;
            color: #f8fafc;
            text-shadow:
                0 0 18px rgba(0, 255, 65, 0.32),
                0 0 36px rgba(0, 210, 255, 0.18);
            margin: 1.1rem 0 1.1rem;
        }

        .hero-title span {
            color: var(--neon-green);
            text-shadow:
                0 0 18px rgba(0, 255, 65, 0.9),
                0 0 38px rgba(0, 255, 65, 0.35);
        }

        .hero-desc {
            position: relative;
            z-index: 2;
            color: #a1a1aa;
            max-width: 860px;
            font-size: 1rem;
            line-height: 1.75;
        }

        .hero-chips {
            position: relative;
            z-index: 2;
            margin-top: 1.4rem;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            margin: 6px 7px 0 0;
            padding: 8px 14px;
            border-radius: 999px;
            color: var(--neon-cyan);
            background: rgba(0, 210, 255, 0.06);
            border: 1px solid rgba(0, 210, 255, 0.30);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .cyber-card {
            background: var(--card-bg);
            border: 1px solid var(--soft-border);
            border-radius: 22px;
            padding: 2rem;
            transition: 0.28s ease;
            box-shadow:
                0 22px 70px rgba(0,0,0,0.58),
                inset 0 0 30px rgba(0,255,65,0.018);
            backdrop-filter: blur(14px);
            position: relative;
            overflow: hidden;
        }

        .cyber-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0, 255, 65, 0.48);
            box-shadow:
                0 28px 85px rgba(0,0,0,0.72),
                0 0 28px rgba(0,255,65,0.10);
        }

        .section-header {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--neon-cyan);
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
            border-left: 4px solid var(--neon-cyan);
            padding-left: 12px;
            text-transform: uppercase;
        }

        .upload-box {
            border: 1px dashed rgba(0, 255, 65, 0.48);
            border-radius: 18px;
            padding: 1.1rem;
            background: rgba(0, 255, 65, 0.035);
            margin-bottom: 1.4rem;
            transition: 0.25s ease;
        }

        .upload-box:hover {
            border-color: var(--neon-green);
            background: rgba(0, 255, 65, 0.065);
            box-shadow: 0 0 22px rgba(0, 255, 65, 0.09);
        }

        .upload-label {
            color: #9ca3af;
            font-size: 0.86rem;
            margin-bottom: 0.8rem;
        }

        .form-control {
            border-radius: 12px;
            background-color: #020202 !important;
            color: #f8fafc !important;
            border: 1px solid #4b5563 !important;
        }

        .form-control:hover {
            border-color: var(--neon-green) !important;
        }

        .file-status {
            margin-top: 0.8rem;
            color: var(--neon-cyan);
            font-size: 0.78rem;
        }

        .btn-cyber {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            border-radius: 12px;
            padding: 13px 16px;
            transition: 0.25s ease;
            letter-spacing: 1.4px;
            text-transform: uppercase;
        }

        .btn-manual {
            background: var(--neon-green);
            color: #000;
            border: 1px solid var(--neon-green);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.15);
        }

        .btn-manual:hover {
            background: transparent;
            color: var(--neon-green);
            box-shadow: 0 0 28px rgba(0, 255, 65, 0.35);
        }

        .btn-auto {
            background: transparent;
            color: var(--neon-cyan);
            border: 1px solid var(--neon-cyan);
        }

        .btn-auto:hover {
            background: var(--neon-cyan);
            color: #000;
            box-shadow: 0 0 28px rgba(0, 210, 255, 0.35);
        }

        .hint-text {
            color: #71717a;
            font-size: 0.85rem;
            line-height: 1.6;
        }

        .metric-pill {
            background: rgba(0, 0, 0, 0.55);
            border: 1px solid rgba(0, 255, 65, 0.25);
            padding: 11px 20px;
            border-radius: 999px;
            display: inline-block;
            margin: 6px 9px 6px 0;
            font-size: 0.86rem;
            color: #cbd5e1;
        }

        .metric-value {
            color: var(--neon-green);
            font-weight: 900;
            text-shadow: 0 0 10px rgba(0,255,65,0.55);
        }

        .classification-guide {
            margin-bottom: 1.5rem;
        }

        .guide-box {
            border-radius: 16px;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.38);
            border: 1px solid rgba(255, 255, 255, 0.08);
            height: 100%;
        }

        .guide-secure {
            border-color: rgba(0, 255, 65, 0.45);
            box-shadow: 0 0 14px rgba(0, 255, 65, 0.06);
        }

        .guide-caution {
            border-color: rgba(255, 209, 102, 0.45);
            box-shadow: 0 0 14px rgba(255, 209, 102, 0.06);
        }

        .guide-threat {
            border-color: rgba(255, 49, 49, 0.50);
            box-shadow: 0 0 14px rgba(255, 49, 49, 0.06);
        }

        .guide-title {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 0.3rem;
        }

        .guide-score {
            color: #9ca3af;
            font-size: 0.8rem;
        }

        .guide-meaning {
            color: #a1a1aa;
            font-size: 0.78rem;
            margin-top: 0.4rem;
            line-height: 1.5;
        }

        .chart-title {
            font-family: 'Rajdhani', sans-serif;
            color: var(--neon-cyan);
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 2px;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }

        .table {
            --bs-table-bg: transparent;
        }

        .table thead th {
            color: var(--neon-cyan);
            font-size: 0.85rem;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(0, 210, 255, 0.25);
            font-family: 'Rajdhani', sans-serif;
            text-transform: uppercase;
        }

        .table td {
            border-color: rgba(255,255,255,0.07);
            color: #d1d5db;
        }

        .secure-row {
            border-left: 4px solid var(--neon-green) !important;
            background: rgba(0,255,65,0.025);
        }

        .caution-row {
            border-left: 4px solid var(--neon-yellow) !important;
            background: rgba(255,209,102,0.035);
        }

        .threat-row {
            border-left: 4px solid var(--neon-red) !important;
            background: rgba(255,49,49,0.04);
        }

        .risk-badge {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 900;
            letter-spacing: 1px;
            font-family: 'Rajdhani', sans-serif;
            white-space: nowrap;
        }

        .risk-secure {
            color: var(--neon-green);
            background: rgba(0, 255, 65, 0.09);
            border: 1px solid rgba(0, 255, 65, 0.62);
            box-shadow: 0 0 12px rgba(0, 255, 65, 0.14);
        }

        .risk-caution {
            color: var(--neon-yellow);
            background: rgba(255, 209, 102, 0.10);
            border: 1px solid rgba(255, 209, 102, 0.70);
            box-shadow: 0 0 12px rgba(255, 209, 102, 0.13);
        }

        .risk-threat {
            color: #fff;
            background: rgba(255, 49, 49, 0.20);
            border: 1px solid rgba(255, 49, 49, 0.70);
            box-shadow: 0 0 12px rgba(255, 49, 49, 0.18);
        }

        .empty-state {
            background: rgba(0, 210, 255, 0.04);
            border: 1px solid rgba(0, 210, 255, 0.22);
            border-radius: 20px;
            padding: 1.8rem;
            color: #9ca3af;
        }

        .cyber-footer {
            margin-top: 3rem;
            border-top: 1px solid var(--neon-green);
            background: rgba(0, 0, 0, 0.96);
            color: #777;
            font-size: 0.9rem;
            letter-spacing: 1.5px;
            font-family: 'JetBrains Mono', monospace;
            box-shadow: 0 -2px 24px rgba(0, 255, 65, 0.08);
        }

        .cyber-footer .pulse {
            color: var(--neon-cyan);
            text-shadow: 0 0 8px var(--neon-cyan);
        }

        .dev-link {
            color: var(--neon-green);
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            text-decoration: none;
            text-shadow: 0 0 8px var(--neon-green);
            transition: 0.3s ease;
            position: relative;
            cursor: pointer;
        }

        .dev-link::after {
            content: "";
            position: absolute;
            width: 0%;
            height: 1px;
            left: 0;
            bottom: -3px;
            background: var(--neon-green);
            transition: width 0.3s ease;
            box-shadow: 0 0 8px var(--neon-green);
        }

        .dev-link:hover {
            color: var(--neon-cyan);
            text-shadow: 0 0 12px var(--neon-cyan), 0 0 24px var(--neon-cyan);
            letter-spacing: 2px;
        }

        .dev-link:hover::after {
            width: 100%;
            background: var(--neon-cyan);
            box-shadow: 0 0 10px var(--neon-cyan);
        }

        #scanOverlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.86);
            backdrop-filter: blur(9px);
            z-index: 9999;
            display: none;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }

        .loader-ring {
            width: 78px;
            height: 78px;
            border-radius: 50%;
            border: 3px solid rgba(0,255,65,0.14);
            border-top: 3px solid var(--neon-green);
            animation: rotateLoader 0.9s linear infinite;
            box-shadow: 0 0 24px rgba(0,255,65,0.25);
        }

        @keyframes rotateLoader {
            to { transform: rotate(360deg); }
        }

        .loader-text {
            margin-top: 1.5rem;
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            letter-spacing: 2px;
            color: var(--neon-green);
            text-shadow: 0 0 12px rgba(0,255,65,0.7);
        }

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #000;
        }

        ::-webkit-scrollbar-thumb {
            background: #333;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--neon-green);
        }
    </style>
</head>

<body>

<div id="scanOverlay">
    <div class="loader-ring"></div>
    <div class="loader-text">RUNNING THREAT DIAGNOSTICS</div>
    <div class="small text-secondary mt-2">Parsing headers • validating identity • scoring risk</div>
</div>

<nav class="navbar sticky-top">
    <div class="container-fluid px-4">
        <span class="navbar-brand">🛡️ SATYAPATRA // THREAT_STREAM</span>
        <span class="nav-subtitle d-none d-md-inline">
            <span class="status-dot"></span>ZERO TRUST EMAIL FORENSICS
        </span>
    </div>
</nav>

<div class="container main-shell py-4">

    <div class="hero-panel">
        <div class="hero-kicker">SATYAPATRA EMAIL FORENSIC ENGINE</div>

        <div class="hero-title">
            Detect. Analyze. <span>Expose.</span>
        </div>

        <p class="hero-desc">
            SatyaPatra verifies whether an email is truthful or spoofed by analyzing sender identity,
            headers, reputation signals, threat score, and phishing indicators.
        </p>

        <div class="hero-chips">
            <span class="hero-chip">● SPF / DKIM ANALYSIS</span>
            <span class="hero-chip">● BULK .EML SCAN</span>
            <span class="hero-chip">● 3-LEVEL RISK CLASSIFICATION</span>
            <span class="hero-chip">● CSV FORENSIC REPORT</span>
        </div>
    </div>

    <div class="row g-4 mb-5">
        <div class="col-lg-7">
            <div class="cyber-card h-100">
                <div class="section-header">MANUAL_INGESTION_MODULE</div>

                <form method="POST" action="/" enctype="multipart/form-data" onsubmit="showScanOverlay()">
                    <div class="upload-box">
                        <p class="upload-label">Upload one or more raw email files for forensic inspection.</p>

                        <input type="file"
                               id="emailFileInput"
                               name="email_files"
                               multiple
                               accept=".eml"
                               class="form-control p-3">

                        <div class="file-status" id="fileStatus">No files selected yet.</div>
                        <p class="small text-secondary mt-2 mb-0">Accepted format: <code>.eml</code></p>
                    </div>

                    <button type="submit" class="btn btn-cyber btn-manual w-100">
                        RUN DIAGNOSTICS [MANUAL]
                    </button>
                </form>
            </div>
        </div>

        <div class="col-lg-5">
            <div class="cyber-card h-100 text-center d-flex flex-column justify-content-center">
                <div class="section-header text-start">AUTOMATED_PIPELINE</div>

                <p class="hint-text mb-4">
                    Ingesting data from directory:
                    <br>
                    <code>/TEST_SAMPLES</code>
                </p>

                <form method="POST" action="/auto_scan" onsubmit="showScanOverlay()">
                    <button type="submit" class="btn btn-cyber btn-auto w-100">
                        EXECUTE AUTO-SCAN [BATCH]
                    </button>
                </form>

                <p class="hint-text mt-4 mb-0">
                    Best for demo: keep safe, suspicious, and spoofed <code>.eml</code> files inside TEST_SAMPLES.
                </p>
            </div>
        </div>
    </div>

    <div class="classification-guide">
        <div class="row g-3">
            <div class="col-md-4">
                <div class="guide-box guide-secure">
                    <div class="guide-title" style="color: var(--neon-green);">🟢 SECURE</div>
                    <div class="guide-score">Final Score: &lt; 30</div>
                    <div class="guide-meaning">Low-risk email with no major spoofing, phishing, or reputation indicators.</div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="guide-box guide-caution">
                    <div class="guide-title" style="color: var(--neon-yellow);">🟡 CAUTION</div>
                    <div class="guide-score">Final Score: 30 - 59</div>
                    <div class="guide-meaning">Suspicious email requiring manual review.</div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="guide-box guide-threat">
                    <div class="guide-title" style="color: var(--neon-red);">🔴 THREAT</div>
                    <div class="guide-score">Final Score: 60+</div>
                    <div class="guide-meaning">High-risk email likely involving spoofing, impersonation, or phishing behavior.</div>
                </div>
            </div>
        </div>
    </div>

    {% if results %}

    {% if metrics %}
    <div class="row mb-4">
        <div class="col-12">
            <div class="cyber-card p-3">
                <div class="metric-pill">TOTAL_OBJECTS: <span class="metric-value">{{ metrics.count }}</span></div>
                <div class="metric-pill">LATENCY: <span class="metric-value">{{ metrics.time }}s</span></div>
                <div class="metric-pill">THROUGHPUT: <span class="metric-value">{{ (metrics.count / metrics.time)|round(2) if metrics.time > 0 else 0 }} msg/sec</span></div>
            </div>
        </div>
    </div>
    {% endif %}

    <div class="row g-4 mb-5">
        <div class="col-md-4">
            <div class="cyber-card">
                <div class="chart-title">RISK_CLASSIFICATION_DISTRIBUTION</div>
                <canvas id="resultChart"></canvas>
            </div>
        </div>

        <div class="col-md-4">
            <div class="cyber-card">
                <div class="chart-title">ANOMALY_MAGNITUDE</div>
                <canvas id="scoreChart"></canvas>
            </div>
        </div>

        <div class="col-md-4">
            <div class="cyber-card">
                <div class="chart-title">PIPELINE_LATENCY</div>
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
    </div>

    <div class="cyber-card">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
            <div class="section-header mb-0">FORENSIC_ANALYSIS_LOGS</div>
            <a href="/download_csv" class="btn btn-outline-info btn-sm">DOWNLOAD_FORENSIC_REPORT.CSV</a>
        </div>

        <div class="table-responsive">
            <table class="table table-dark table-hover align-middle">
                <thead>
                    <tr>
                        <th>OBJECT_ID</th>
                        <th>IDENTITY_SUBJECT</th>
                        <th>SCORE</th>
                        <th>CLASSIFICATION</th>
                        <th>MEANING</th>
                        <th>INTEL_LOGS</th>
                    </tr>
                </thead>

                <tbody>
                {% for r in results %}
                <tr class="{% if r.score < 30 %}secure-row{% elif r.score < 60 %}caution-row{% else %}threat-row{% endif %}">
                    <td class="small text-secondary">{{ r.filename }}</td>
                    <td>{{ r.subject }}</td>
                    <td class="fw-bold">{{ r.score }}</td>

                    <td>
                        {% if r.score < 30 %}
                            <span class="risk-badge risk-secure">🟢 SECURE</span>
                        {% elif r.score < 60 %}
                            <span class="risk-badge risk-caution">🟡 CAUTION</span>
                        {% else %}
                            <span class="risk-badge risk-threat">🔴 THREAT</span>
                        {% endif %}
                    </td>

                    <td class="small text-secondary">
                        {% if r.score < 30 %}
                            Low-risk email with no major spoofing, phishing, or reputation indicators.
                        {% elif r.score < 60 %}
                            Suspicious email requiring manual review.
                        {% else %}
                            High-risk email likely involving spoofing, impersonation, or phishing behavior.
                        {% endif %}
                    </td>

                    <td class="small">
                        {% for x in r.reasons %}
                            <div>▸ {{ x }}</div>
                        {% endfor %}
                    </td>
                </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        const results = {{ results|tojson }};
        const metrics = {{ metrics|tojson if metrics else 'null' }};
        const chartDefaults = { color: '#9ca3af', font: { family: 'JetBrains Mono' } };

        const secureCount = results.filter(r => r.score < 30).length;
        const cautionCount = results.filter(r => r.score >= 30 && r.score < 60).length;
        const threatCount = results.filter(r => r.score >= 60).length;

        new Chart(document.getElementById('resultChart'), {
            type: 'doughnut',
            data: {
                labels: ['SECURE', 'CAUTION', 'THREAT'],
                datasets: [{
                    data: [secureCount, cautionCount, threatCount],
                    backgroundColor: ['#00ff41', '#ffd166', '#ff3131'],
                    borderWidth: 0
                }]
            },
            options: {
                plugins: {
                    legend: { position: 'bottom', labels: chartDefaults },
                    title: { display: false }
                }
            }
        });

        new Chart(document.getElementById('scoreChart'), {
            type: 'bar',
            data: {
                labels: results.map(r => r.filename.substring(0,8)),
                datasets: [{
                    label: 'RISK_SCORE',
                    data: results.map(r => r.score),
                    backgroundColor: results.map(r => {
                        if (r.score < 30) return '#00ff41';
                        if (r.score < 60) return '#ffd166';
                        return '#ff3131';
                    })
                }]
            },
            options: {
                plugins: {
                    legend: { display: false },
                    title: { display: false }
                },
                scales: {
                    x: {
                        ticks: { color: '#9ca3af' },
                        grid: { color: '#222' }
                    },
                    y: {
                        ticks: { color: '#9ca3af' },
                        grid: { color: '#222' },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });

        if (metrics) {
            new Chart(document.getElementById('performanceChart'), {
                type: 'line',
                data: {
                    labels: ['Start', 'Processing', 'End'],
                    datasets: [{
                        label: 'Latency (s)',
                        data: [0, metrics.time, metrics.time],
                        borderColor: '#ff2bd6',
                        tension: 0.4,
                        fill: true,
                        backgroundColor: 'rgba(255, 43, 214, 0.10)'
                    }]
                },
                options: {
                    plugins: {
                        legend: { labels: chartDefaults },
                        title: { display: false }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#9ca3af' },
                            grid: { color: '#222' }
                        },
                        y: {
                            ticks: { color: '#9ca3af' },
                            grid: { color: '#222' }
                        }
                    }
                }
            });
        }
    </script>

    {% else %}

    <div class="empty-state mb-4">
        <div class="section-header">SYSTEM_IDLE</div>
        <h5 class="text-white">No forensic scan executed yet.</h5>
        <p class="mb-0">
            Upload <code>.eml</code> files or run the automated batch scanner to activate threat analysis.
        </p>
    </div>

    {% endif %}
</div>

<footer class="cyber-footer text-center py-3">
    <span class="pulse">[SYS]</span>
    // DEVELOPED BY
    <a href="https://www.linkedin.com/in/glen-ferns/"
       target="_blank"
       rel="noopener noreferrer"
       class="dev-link"
       title="Connect with cyb3rPh03n1x on LinkedIn">
       cyb3rPh03n1x
    </a>
    //
    <span class="pulse">SATYAPATRA ACTIVE</span>
</footer>

<script>
    function showScanOverlay() {
        document.getElementById("scanOverlay").style.display = "flex";
    }

    const emailInput = document.getElementById("emailFileInput");
    const fileStatus = document.getElementById("fileStatus");

    if (emailInput) {
        emailInput.addEventListener("change", function() {
            const count = emailInput.files.length;

            if (count === 0) {
                fileStatus.textContent = "No files selected yet.";
            } else if (count === 1) {
                fileStatus.textContent = "1 email object loaded into buffer.";
            } else {
                fileStatus.textContent = count + " email objects loaded into buffer.";
            }
        });
    }
</script>

</body>
</html>
"""


def classify_score(score):
    if score < 30:
        return {
            "classification": "SECURE",
            "status_color": "Green",
            "meaning": "Low-risk email with no major spoofing, phishing, or reputation indicators"
        }

    if score < 60:
        return {
            "classification": "CAUTION",
            "status_color": "Yellow",
            "meaning": "Suspicious email requiring manual review"
        }

    return {
        "classification": "THREAT",
        "status_color": "Red",
        "meaning": "High-risk email likely involving spoofing, impersonation, or phishing behavior"
    }


def extract_sender_ip(msg):
    received = msg.get_all("Received", []) or []

    import re
    import ipaddress

    for h in received:
        ips = re.findall(r"[0-9]{1,3}(?:\\.[0-9]{1,3}){3}", h)

        for ip in ips:
            try:
                ip_obj = ipaddress.ip_address(ip)

                if not ip_obj.is_private and not ip_obj.is_loopback:
                    return str(ip_obj)

            except Exception:
                continue

    return "127.0.0.1"


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)

                if payload:
                    return payload.decode(errors="ignore")
    else:
        payload = msg.get_payload(decode=True)

        if payload:
            return payload.decode(errors="ignore")

    return ""


def process_email_task(file_data):
    filename, raw_bytes = file_data

    try:
        msg = email.message_from_bytes(raw_bytes)
        body = get_email_body(msg)

        report = analyze_email(msg, body, raw_bytes)
        score = int(report.get("score", 0))
        classification_data = classify_score(score)

        result = {
            "filename": filename,
            "subject": str(msg.get("Subject", "(No Subject)")),
            "score": score,
            "reasons": report.get("reasons", [])
        }

        result.update(classification_data)
        return result

    except Exception as e:
        result = {
            "filename": filename,
            "subject": "(Processing Error)",
            "score": 30,
            "reasons": [str(e)]
        }

        result.update(classify_score(30))
        return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_files = request.files.getlist("email_files")
        tasks = [(f.filename, f.read()) for f in uploaded_files if f.filename != ""]

        return run_bulk_analysis(tasks)

    return render_template_string(
        HTML,
        results=session.get("results", []),
        metrics=session.get("metrics")
    )


@app.route("/auto_scan", methods=["POST"])
def auto_scan():
    tasks = []

    if os.path.exists(TEST_SAMPLES_DIR):
        for filename in os.listdir(TEST_SAMPLES_DIR):
            if filename.endswith(".eml"):
                filepath = os.path.join(TEST_SAMPLES_DIR, filename)

                with open(filepath, "rb") as f:
                    tasks.append((filename, f.read()))

    return run_bulk_analysis(tasks)


def run_bulk_analysis(tasks):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(process_email_task, tasks))

    duration = round(time.time() - start_time, 2)

    metrics = {
        "count": len(tasks),
        "time": duration
    }

    session["results"] = results
    session["metrics"] = metrics

    return render_template_string(
        HTML,
        results=results,
        metrics=metrics
    )


@app.route("/download_csv")
def download_csv():
    results = session.get("results", [])

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "File",
        "Subject",
        "Score",
        "Classification",
        "Status Color",
        "Meaning",
        "Reasons"
    ])

    for r in results:
        score = int(r.get("score", 0))
        classification_data = classify_score(score)

        writer.writerow([
            r.get("filename"),
            r.get("subject"),
            score,
            classification_data["classification"],
            classification_data["status_color"],
            classification_data["meaning"],
            "; ".join(r.get("reasons", []))
        ])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="threat_report.csv"
    )


if __name__ == "__main__":
    print(">> SATYAPATRA IS ONLINE [WAITRESS SERVER]")
    serve(app, host="127.0.0.1", port=5000)