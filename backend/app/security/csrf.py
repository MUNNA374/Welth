from fastapi import Request, HTTPException, status
import secrets

def generate_csrf_token() -> str:
    """Generate a random cryptographically secure token."""
    return secrets.token_hex(32)

def verify_csrf_token(request: Request) -> bool:
    """Verify that the X-CSRF-Token header matches the csrf_token cookie for mutation requests."""
    # Exclude safe HTTP methods from verification
    if request.method in ["GET", "HEAD", "OPTIONS", "TRACE"]:
        return True
        
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_header = request.headers.get("x-csrf-token")
    
    if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token validation failed. State mutation requests require valid CSRF protection headers."
        )
    return True
