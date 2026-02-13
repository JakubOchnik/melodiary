import os
import urllib.parse

from shared.config import get_secret
from shared.responses import success_response, error_response


def lambda_handler(event, context):
    """
    Generate Spotify authorization URL for OAuth flow.

    Returns:
        Authorization URL that frontend should redirect to
    """

    client_id = get_secret("SPOTIFY_CLIENT_ID")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")

    if not client_id or not redirect_uri:
        return error_response("Missing Spotify configuration", 500)

    # Spotify OAuth scopes
    scopes = [
        "user-library-read",  # Read saved tracks
        "user-follow-read",  # Read followed artists
        "playlist-read-private",  # Read private playlists
        "playlist-modify-public",  # Modify public playlists (for migration)
        "playlist-modify-private",  # Modify private playlists (for migration)
    ]

    # Build authorization URL
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "show_dialog": "false",
    }
    auth_url = (
        f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(auth_params)}"
    )

    return success_response({"authUrl": auth_url})
