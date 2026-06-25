import re
# Sanitization utilities

def sanitize_text(text: str) -> str:
    """Sanitize input text by stripping HTML tags and escaping dangerous characters."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]*>', '', text)
    # Escape basic HTML symbols to prevent XSS injection
    clean = (
        clean.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;')
             .replace('"', '&quot;')
             .replace("'", '&#x27;')
             .replace('/', '&#x2F;')
    )
    return clean

def is_safe_string(text: str) -> bool:
    """Detect potential SQL/command injection patterns in arbitrary input fields."""
    if not text:
        return True
    # Look for common SQL injection markers
    suspicious_patterns = [
        r"(?i)\bUNION\b\s+(?i)\bALL\b",
        r"(?i)\bSELECT\b.*\bFROM\b",
        r"--",
        r"/\*",
        r"\bOR\b\s+\d+\s*=\s*\d+",
        r";\s*(?i)\bDROP\b",
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, text):
            return False
    return True
