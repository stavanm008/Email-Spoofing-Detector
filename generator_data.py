import os

# Ensure the directory exists
target_dir = "TEST_SAMPLES"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Data templates for diversity
templates = [
    {
        "name": "secure_mail",
        "from": "admin@google.com",
        "return": "admin@google.com",
        "ip": "209.85.220.41",
        "subject": "System Update Successful",
        "body": "Your account security settings have been updated. No further action is required."
    },
    {
        "name": "dmarc_fail",
        "from": "billing@paypal.com",
        "return": "hacker-service@net-node.biz",
        "ip": "192.168.1.1",
        "subject": "Urgent: Invoice #99281",
        "body": "Your payment failed. Please click the link to update your billing information."
    },
    {
        "name": "osint_threat",
        "from": "support@bank-verify.com",
        "return": "support@bank-verify.com",
        "ip": "103.145.13.250",
        "subject": "New Login Detected",
        "body": "A login from a new IP was detected. If this wasn't you, please secure your account."
    },
    {
        "name": "keyword_phish",
        "from": "hr@your-college.edu",
        "return": "hr@your-college.edu",
        "ip": "127.0.0.1",
        "subject": "ACTION REQUIRED: Verify Payroll Details",
        "body": "URGENT: You must verify your account immediately to ensure salary is processed."
    },
    {
        "name": "critical_threat",
        "from": "ceo@big-company.com",
        "return": "attacker@dark-web.ru",
        "ip": "185.220.101.15",
        "subject": "!! URGENT WIRE TRANSFER !!",
        "body": "Verify your identity at this link to authorize the emergency fund transfer now."
    }
]

def generate_samples(count=50):
    for i in range(count):
        # Rotate through templates to get a mix of results
        t = templates[i % len(templates)]
        filename = f"{target_dir}/{t['name']}_{i}.eml"
        
        content = f"""Received: from {t['name']}.com ({t['ip']})
From: {t['from']}
Return-Path: <{t['return']}>
Subject: {t['subject']}

{t['body']}
"""
        with open(filename, "w") as f:
            f.write(content)
    print(f">> SUCCESS: {count} diverse .eml files generated in /{target_dir}")

if __name__ == "__main__":
    generate_samples(50)