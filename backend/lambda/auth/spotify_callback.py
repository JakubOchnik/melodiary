import json

from shared.responses import success_response, error_response
from shared.spotify_utils import exchange_code_for_tokens, get_user_profile
from shared.auth_utils import generate_jwt
from shared.db import (
    get_user_by_email,
    create_user,
    save_platform_connection,
    get_user_by_spotify_id,
)


def lambda_handler(event, context):
    """
    Handle Spotify OAuth callback

    Expects:
        code: Authorization code from Spotify

    Returns:
        JWT token and user info
    """

    code = None

    query_params = event.get("queryStringParameters") or {}
    code = query_params.get("code")

    if not code:
        try:
            body = json.loads(event.get("body", "{}"))
            code = body.get("code")
        except json.JSONDecodeError:
            pass

    if not code:
        return error_response("Missing authorization code", 400)

    tokens, error = exchange_code_for_tokens(code)
    if error:
        return error_response(f"Failed to authenticate with Spotify: {error}", 400)

    profile, error = get_user_profile(tokens["access_token"])
    if error:
        return error_response(f"Failed to get user profile: {error}", 400)

    # Get Spotify user ID (this is always present)
    spotify_id = profile.get("id")
    if not spotify_id:
        return error_response("Failed to get Spotify user ID", 400)

    spotify_email = profile.get("email")
    display_name = profile.get("display_name") or f"spotify_user_{spotify_id[:8]}"

    user = None

    user = get_user_by_spotify_id(spotify_id)

    if not user and spotify_email:
        user = get_user_by_email(spotify_email)

        if user:
            from shared.db import link_spotify_id_to_user

            link_spotify_id_to_user(user["userId"], spotify_id)

    # Create if doesn't exist
    if not user:
        email = spotify_email or f"{spotify_id}@spotify.melodiary.local"

        user = create_user(
            email=email,
            display_name=display_name,
            spotify_id=spotify_id,
            has_real_email=bool(spotify_email),
        )
        print(f"Created new user: {user['userId']} (Spotify ID: {spotify_id})")
    else:
        print(f"Existing user logged in: {user['userId']} (Spotify ID: {spotify_id})")

    save_platform_connection(
        user_id=user["userId"], platform="spotify", tokens=tokens, profile_data=profile
    )

    jwt_token = generate_jwt(user["userId"], user["email"])

    return success_response(
        {
            "token": jwt_token,
            "user": {
                "userId": user["userId"],
                "email": user["email"],
                "displayName": user["displayName"],
            },
            "spotify": {
                "connected": True,
                "displayName": profile.get("display_name"),
                "profileUrl": profile.get("external_urls", {}).get("spotify"),
                "spotifyId": spotify_id,
            },
        }
    )
