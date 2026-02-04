import jwt
import os
from datetime import datetime, timedelta, timezone


JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET env var must be set")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 30

BEARER_PREFIX = "Bearer "
BEARER_PREFIX_LEN = len(BEARER_PREFIX)


def generate_jwt(user_id, email):
    """
    Generate a JWT token for user

    Args:
        user_id: Unique user ID
        email: User's e-mail

    Returns:
        JWT token str
    """
    payload = {
        "userId": user_id,
        "email": email,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRATION_DAYS),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt(token):
    """
    Verify and decode JWT token

    Args:
        token: JWT token str

    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        if token.startswith("Bearer "):
            token = token[BEARER_PREFIX_LEN:]

        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None


def require_auth(lambda_handler):
    """
    Decorator to require authentication for Lambda functions

    Usage:
        @require_auth
        def lambda_handler(event, context):
            user_id = event['userId']  # Added by decorator
            ...
    """

    def wrapper(event, context):
        # Get token from Authorization header
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization") or headers.get("authorization")

        if not auth_header:
            from shared.responses import error_response

            return error_response("Missing authorization header", 401)

        payload = verify_jwt(auth_header)
        if not payload:
            from shared.responses import error_response

            return error_response("Invalid or expired token", 401)

        user_id = payload.get("userId")
        if user_id:
            event["userId"] = user_id

        user_email = payload.get("email")
        if user_email:
            event["userEmail"] = user_email

        return lambda_handler(event, context)

    return wrapper
