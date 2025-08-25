import re
from typing import List, Dict, Tuple

# Define patterns for secrets detection
SECRET_PATTERNS: List[Tuple[str, str]] = [
    ('api_key', r'AKIA[0-9A-Z]{16}'),
    ('password', r'password\s*=\s*[\'\"][^\'\"]+[\'\"]'),
    ('long_string', r'[0-9a-zA-Z]{32,}')
]

def scan_file(file_path: str) -> List[Dict]:
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                for pattern_name, pattern in SECRET_PATTERNS:
                    flags = re.IGNORECASE if pattern_name == 'password' else 0
                    matches = re.finditer(pattern, line, flags)
                    for match in matches:
                        findings.append({
                            'file_path': file_path,
                            'line_number': line_num,
                            'secret_type': pattern_name,
                            'secret_value': match.group()
                        })
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")
    return findings