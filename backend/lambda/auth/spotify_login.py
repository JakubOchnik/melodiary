import json
import os
import urllib.parse


def lambda_handler(event, context):
    """
    Generate Spotify authorization URL for OAuth flow.

    Returns:
        Authorization URL that frontend should redirect to
    """

    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")

    if not client_id or not redirect_uri:
        return {
            "statusCode": 500,
            "headers": get_cors_headers(),
            "body": json.dumps({"error": "Missing Spotify configuration"}),
        }

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

    return {
        "statusCode": 200,
        "headers": get_cors_headers(),
        "body": json.dumps({"authUrl": auth_url}),
    }


def get_cors_headers():
    """Return CORS headers for API responses"""
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    }
