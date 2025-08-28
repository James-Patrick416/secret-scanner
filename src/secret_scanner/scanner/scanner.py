import re
import os

# -------------------
# Simple secret regex patterns
# -------------------
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    "Password": r"(?i)password\s*=\s*['\"].+['\"]",
    "API Key": r"(?i)api[_-]?key\s*=\s*['\"].+['\"]",
}

def scan_file(path):
    """Scan a single file for secrets. Returns list of findings."""
    findings = []
    if not os.path.isfile(path):
        return findings

    with open(path, "r", errors="ignore") as f:
        for lineno, line in enumerate(f, start=1):
            for secret_type, pattern in SECRET_PATTERNS.items():
                if re.search(pattern, line):
                    findings.append({
                        "file_path": path,
                        "line_number": lineno,
                        "secret_type": secret_type,
                        "secret_value": line.strip()
                    })
    return findings

def scan_directory(directory):
    """Recursively scan all files in a directory."""
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            results.extend(scan_file(file_path))
    return results

def scan_target(target):
    """Scan a file or directory for secrets."""
    if os.path.isdir(target):
        return scan_directory(target)
    return scan_file(target)
