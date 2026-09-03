import os
import re
import spf
import dkim
import ipaddress
import requests
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# Prefer environment variable instead of hardcoding API key
# Windows PowerShell:
# $env:ABUSE_IPDB_KEY="your_api_key_here"
#
# Linux/Mac:
# export ABUSE_IPDB_KEY="your_api_key_here"

ABUSE_IPDB_KEY = os.getenv("ABUSE_IPDB_KEY", "")

intel_cache = {}


print("\n[SATYAPATRA] Initializing Content Analytics Pipeline...")
print("[SYSTEM] Compiling Training Corpus into Feature Vectors...")


training_corpus = {
    "text": [
        "Hey, are we still meeting for lunch tomorrow at 12?",
        "URGENT: Your account has been suspended! Click here to verify your password immediately.",
        "Free entry in a weekly competition to win prize cash rewards!",
        "Can you please send me the final project report by EOD?",
        "CONGRATULATIONS! You have won a gift card reward. Call now to claim your prize.",
        "Just checking in to see how your internship application went at the lab.",
        "Get cheap insurance rates today! No medical exam required. Guarantee approval.",
        "Dear student, your library books are overdue. Please return them to avoid fines.",
        "Winner! As a valued customer you have been selected to receive a cash prize reward!",
        "Are you coming to the cybersecurity bootcamp session this evening?"
    ],
    "label": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0]
}


ml_df = pd.DataFrame(training_corpus)

ml_vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    ngram_range=(1, 2)
)

X_train_tfidf = ml_vectorizer.fit_transform(ml_df["text"])

ml_classifier = MultinomialNB(alpha=1.0)
ml_classifier.fit(X_train_tfidf, ml_df["label"])

print("[SATYAPATRA] Multinomial Naive Bayes Engine Online.")


def extract_sender_ip(msg):
    received_headers = msg.get_all("Received", []) or []

    for header in received_headers:
        ips = re.findall(r"[0-9]{1,3}(?:\.[0-9]{1,3}){3}", header)

        for ip in ips:
            try:
                ip_obj = ipaddress.ip_address(ip)

                if not ip_obj.is_private and not ip_obj.is_loopback:
                    return str(ip_obj)

            except Exception:
                continue

    return "127.0.0.1"


def get_domain(address):
    match = re.search(r"[\w\.-]+@([\w\.-]+)", address)

    if match:
        return match.group(1).lower().strip()

    return ""


def is_domain_aligned(author_domain, return_path_domain):
    if not author_domain or not return_path_domain:
        return False

    return (
        author_domain == return_path_domain
        or author_domain.endswith("." + return_path_domain)
        or return_path_domain.endswith("." + author_domain)
    )


def get_ip_intel(ip):
    if not ABUSE_IPDB_KEY:
        return 0, "No AbuseIPDB API Key Configured"

    if ip in ["127.0.0.1", "localhost", "0.0.0.0"]:
        return 0, "No External Intel"

    if ip in intel_cache:
        return intel_cache[ip]

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Accept": "application/json",
        "Key": ABUSE_IPDB_KEY
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=3
        )

        if response.status_code == 200:
            score = response.json()["data"]["abuseConfidenceScore"]
            result = (score, f"Abuse Score: {score}%")
            intel_cache[ip] = result
            return result

        return 0, f"Intel API Error: HTTP {response.status_code}"

    except Exception:
        return 0, "Intel Offline"


def classify_score(score):
    if score < 30:
        return "SECURE"

    if score < 60:
        return "CAUTION"

    return "THREAT"


def analyze_email(msg, body, raw_bytes):
    start_time = time.time()

    reasons = []
    auth_score = 0
    content_score = 0

    from_hdr = str(msg.get("From", ""))
    return_path_hdr = str(msg.get("Return-Path", ""))

    author_domain = get_domain(from_hdr)
    return_path_domain = get_domain(return_path_hdr)

    sender_ip = extract_sender_ip(msg)

    # 1. SPF Check
    try:
        if author_domain and sender_ip != "127.0.0.1":
            spf_res, _ = spf.check2(
                i=sender_ip,
                s="postmaster@" + author_domain,
                h=author_domain
            )

            if spf_res != "pass":
                auth_score += 20
                reasons.append(f"Infrastructure: SPF {spf_res.upper()}")
        else:
            auth_score += 10
            reasons.append("Infrastructure: SPF Check Skipped / Missing Domain or IP")

    except Exception:
        auth_score += 15
        reasons.append("Infrastructure: SPF Resolution Timeout")

    # 2. Domain Alignment Check
    if not is_domain_aligned(author_domain, return_path_domain):
        auth_score += 25
        reasons.append("Identity: Domain Alignment Mismatch")

    # 3. DKIM Check
    try:
        if dkim.verify(raw_bytes):
            pass
        else:
            auth_score += 15
            reasons.append("Security: DKIM Signature Invalid")

    except Exception:
        auth_score += 10
        reasons.append("Security: Missing Digital Seal (DKIM)")

    # 4. AbuseIPDB Reputation Check
    abuse_score, intel_msg = get_ip_intel(sender_ip)

    if abuse_score > 10:
        penalty = int(abuse_score / 2)
        auth_score += penalty
        reasons.append(f"Reputation: {intel_msg}")

    # 5. ML-Based Content Heuristic
    if body and body.strip():
        try:
            body_vector = ml_vectorizer.transform([body])
            prediction = ml_classifier.predict(body_vector)[0]
            probabilities = ml_classifier.predict_proba(body_vector)[0]

            if prediction == 1:
                confidence = probabilities[1]
                ml_penalty = int(confidence * 30)
                content_score += ml_penalty

                reasons.append(
                    f"ML_Heuristic: Naive Bayes Classified Spam ({confidence * 100:.1f}% Confidence)"
                )

        except Exception as e:
            reasons.append(f"ML_Heuristic: Vector Processing Error [{str(e)}]")

    total_score = auth_score + content_score
    total_score = min(total_score, 100)

    duration = round(time.time() - start_time, 4)

    if not reasons:
        reasons.append("No major spoofing, phishing, or reputation indicators detected")

    return {
        "score": int(total_score),
        "auth_score": int(auth_score),
        "content_score": int(content_score),
        "label": classify_score(total_score),
        "reasons": list(dict.fromkeys(reasons)),
        "processing_time": duration
    }