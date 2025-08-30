import re
import os

# -------------------
# Simple secret regex patterns
# -------------------
# Using a DICTIONARY to map secret types to their regex patterns
# Dictionaries are perfect for key-value pairs like this
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    "Password": r"(?i)password\s*=\s*['\"].+['\"]",
    "API Key": r"(?i)api[_-]?key\s*=\s*['\"].+['\"]",
}

def scan_file(path):
    """Scan a single file for secrets. Returns list of findings."""
    # Using a LIST to store multiple findings - lists are great for collections of similar items
    findings = []
    if not os.path.isfile(path):
        return findings

    with open(path, "r", errors="ignore") as f:
        for lineno, line in enumerate(f, start=1):
            # Using dictionary.items() to get both key and value in the loop
            for secret_type, pattern in SECRET_PATTERNS.items():
                if re.search(pattern, line):
                    # Using a DICTIONARY to store structured data about each finding
                    # Dictionaries are ideal for representing objects with named fields
                    findings.append({
                        "file_path": path,
                        "line_number": lineno,
                        "secret_type": secret_type,
                        "secret_value": line.strip()
                    })
    return findings

def scan_directory(directory):
    """Recursively scan all files in a directory."""
    # Using a LIST to accumulate results from multiple file scans
    results = []
    # os.walk returns a TUPLE for each directory it traverses: (root, dirs, files)
    # We use _ to ignore the dirs part we don't need
    for root, _, files in os.walk(directory):
        for file in files:
            # os.path.join handles path construction across different operating systems
            file_path = os.path.join(root, file)
            # Using list.extend() to add multiple items from scan_file to our results
            results.extend(scan_file(file_path))
    return results

def scan_target(target):
    """Scan a file or directory for secrets."""
    # Simple conditional that returns different data structures based on input type
    if os.path.isdir(target):
        return scan_directory(target)
    return scan_file(target)