from backend.app.security.jwt import get_password_hash, verify_password, create_access_token, verify_access_token
from backend.app.security.validation import sanitize_text, is_safe_string
from datetime import timedelta

def test_password_hashing():
    pw = "SuperSecurePassword123"
    hashed = get_password_hash(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_lifecycle():
    subject = "user-uuid-12345"
    token = create_access_token(subject, expires_delta=timedelta(minutes=5))
    decoded = verify_access_token(token)
    assert decoded == subject

def test_input_sanitization():
    unsafe_xss = "<script>alert('xss')</script>Hello & welcome"
    sanitized = sanitize_text(unsafe_xss)
    assert "<script>" not in sanitized
    assert "&" in sanitized  # converted to entity

def test_sql_injection_detection():
    safe_str = "Apple Whole Foods"
    unsafe_sql = "1' OR 1=1 --"
    assert is_safe_string(safe_str) is True
    assert is_safe_string(unsafe_sql) is False
