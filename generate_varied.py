import os

target_dir = "TEST_SAMPLES"
if not os.path.exists(target_dir): os.makedirs(target_dir)

samples = [
    ("01_perfect.eml", "glen@gmail.com", "glen@gmail.com", "209.85.220.41", "Normal Subject", "Hello how are you?"),
    ("02_just_keywords.eml", "bank@legit.com", "bank@legit.com", "127.0.0.1", "Urgent Action", "Please verify your account immediately."),
    ("03_spf_fail.eml", "friend@site.com", "hacker@site.com", "1.1.1.1", "Hey!", "Check out this link."),
    ("04_osint_warning.eml", "service@cloud.com", "service@cloud.com", "103.145.13.250", "Update", "Regular system update."),
    ("05_alignment_fail.eml", "ceo@company.com", "random@attacker.net", "192.168.1.1", "Transfer", "Send the files."),
    ("06_osint_plus_keywords.eml", "support@app.com", "support@app.com", "185.220.101.15", "URGENT", "Verify your password now."),
    ("07_total_failure.eml", "paypal@secure.com", "mal@bad.ru", "103.145.13.250", "ACCOUNT SUSPENDED", "Verify immediately or lose access."),
]

for name, from_em, ret_em, ip, sub, body in samples:
    content = f"Received: from mail.com ({ip})\nFrom: {from_em}\nReturn-Path: <{ret_em}>\nSubject: {sub}\n\n{body}"
    with open(os.path.join(target_dir, name), "w") as f: f.write(content)

print(">> 10 DIFFERENT Test Samples Created.")