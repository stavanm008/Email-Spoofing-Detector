import email
import os
from detector import analyze_email

def load_email(path):
    """
    Reads the email file in binary mode.
    Binary mode is CRITICAL for DKIM verification to ensure 
    the signature matches the raw data exactly.
    """
    try:
        with open(path, "rb") as f:
            raw_bytes = f.read()
        
        # Convert raw bytes into an email message object
        msg = email.message_from_bytes(raw_bytes)
        return msg, raw_bytes
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None, None

def get_email_body(msg):
    """Extracts the plain text body for content analysis."""
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

if __name__ == "__main__":
    # Update this path to your sample file
    sample_path = "samples/spoof1.eml"
    
    if os.path.exists(sample_path):
        msg, raw_bytes = load_email(sample_path)
        
        if msg and raw_bytes:
            body = get_email_body(msg)
            
            # Now passing all three required arguments to the upgraded detector
            result = analyze_email(msg, body, raw_bytes)
            
            print(f"--- DIAGNOSTIC REPORT: {sample_path} ---")
            print(f"RESULT: {result['label']}")
            print(f"TOTAL SCORE: {result['score']}")
            print(f"OSINT INTEL: {result['dmarc_reason']}")
            print("THREAT INDICATORS:")
            for reason in result['reasons']:
                print(f" [!] {reason}")
    else:
        print(f"File not found: {sample_path}. Please check your samples directory.")