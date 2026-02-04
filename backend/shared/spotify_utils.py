import requests
import os
import base64
from datetime import datetime, timedelta, timezone

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


def exchange_code_for_tokens(code):
    """
    Exchange auth code for access and refresh tokens

    Args:
        code: Authorization code from Spotify

    Returns:
        Tuple of (tokens dict, error message)
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")

    # Encode client credentials
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL, headers=headers, data=data, timeout=10
        )
        response.raise_for_status()

        tokens = response.json()

        tokens["expires_at"] = (
            datetime.now(timezone.utc) + timedelta(seconds=tokens["expires_in"])
        ).isoformat()

        return tokens, None
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to exchange code: {str(e)}"
        if hasattr(e, "response") and e.response is not None:
            error_msg += f" - {e.response.text}"

        return {}, error_msg


def refresh_access_token(refresh_token):
    """
    Refresh an expired access token

    Args:
        refresh_token: Spotify refresh token

    Returns:
        Tuple of (new tokens dict, error message)
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL, headers=headers, data=data, timeout=10
        )
        response.raise_for_status()

        tokens = response.json()

        tokens["expires_at"] = (
            datetime.now(timezone.utc) + timedelta(seconds=tokens["expires_in"])
        ).isoformat()

        # Refresh token might not be included, use the old one
        if "refresh_token" not in tokens:
            tokens["refresh_token"] = refresh_token

        return tokens, None
    except requests.exceptions.RequestException as e:
        return {}, f"Failed to refresh token: {str(e)}"


def get_user_profile(access_token):
    """
    Get Spotify user profile

    Args:
        access_token: Spotify access token

    Returns:
        Tuple of (profile dict, error message)
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"{SPOTIFY_API_BASE}/me", headers=headers, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"Failed to get user profile: {str(e)}"


def is_token_expired(expires_at):
    """
    Check if token is expired

    Args:
        expires_at: ISO timestamp

    Returns:
        True if expired, False otherwise
    """

    try:
        expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        return datetime.now(timezone.utc) >= expiry - timedelta(minutes=5)
    except:
        return True
