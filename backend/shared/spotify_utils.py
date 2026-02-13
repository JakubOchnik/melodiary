import requests
import os
import base64
from datetime import datetime, timedelta, timezone

from shared.config import get_secret, get_logger

logger = get_logger(__name__)

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
    client_id = get_secret("SPOTIFY_CLIENT_ID")
    client_secret = get_secret("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        return {}, f"Failed to exchange code: missing configuration"

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
    client_id = get_secret("SPOTIFY_CLIENT_ID")
    client_secret = get_secret("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return {}, f"Failed to refresh token: missing configuration"

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


def parse_track(track):
    """
    Map Spotify track JSON to internal structure

    Returns:
        Processed track structure or None if failed
    """
    try:
        artists = track.get("artists", [])
        album = track.get("album", {})
        return {
            "trackId": f"spotify:{track['id']}",
            "trackName": track.get("name", "Unknown"),
            "artistName": ", ".join(artist.get("name", "") for artist in artists),
            "albumName": album.get("name", "Unknown"),
            "platform": "spotify",
            "platformTrackId": track["id"],
            "platformAlbumId": album.get("id"),
            "platformArtistId": (artists[0].get("id") if artists else None),
            "coverArtUrl": (
                album.get("images", [{}])[0].get("url") if album.get("images") else None
            ),
            "addedDate": track.get("added_at", datetime.now(timezone.utc).isoformat()),
            "isManual": False,
            "duration": track.get("duration_ms"),
            "releaseYear": (
                album.get("release_date", "")[:4] if album.get("release_date") else None
            ),
        }
    except (KeyError, IndexError) as fmt_error:
        logger.warning("Skipping malformed track: %s", fmt_error)
    return None


def get_user_saved_tracks(access_token, limit=50):
    """
    Get user saved tracks from Spotify

    Args:
        access_token: API access token
        limit: Number of tracks per request (max 50)

    Returns:
        Tuple of (list of tracks, error message)
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    all_tracks = []
    offset = 0

    # TODO: Set up a maximum page count / track cap to avoid timeouts for huge libraries (thousands of songs)
    try:
        while True:
            url = f"{SPOTIFY_API_BASE}/me/tracks?limit={limit}&offset={offset}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            for item in items:
                track = item.get("track")
                if track:
                    track["added_at"] = item.get("added_at", "")
                    all_tracks.append(track)

            if data.get("next") is None:
                break

            offset += limit
            logger.info("Fetched %d tracks so far...", len(all_tracks))
        return all_tracks, None
    except requests.exceptions.RequestException as e:
        return [], f"Failed to get saved tracks: {str(e)}"
