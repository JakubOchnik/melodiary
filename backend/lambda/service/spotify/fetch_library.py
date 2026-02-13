from shared.config import get_logger
from shared.responses import success_response, error_response
from shared.auth_utils import require_auth

logger = get_logger(__name__)
from shared.db import get_platform_connection, save_tracks, update_platform_tokens
from shared.spotify_utils import (
    is_token_expired,
    refresh_access_token,
    get_user_saved_tracks,
    parse_track,
)


@require_auth
def lambda_handler(event, context):
    """
    Fetch user's saved tracks from Spotify and store in library

    Returns:
        Number of tracks synced
    """

    if "userId" not in event:
        return error_response("No such user", 404)

    user_id = event["userId"]
    try:
        connection = get_platform_connection(user_id, "spotify")

        if not connection:
            return error_response("Spotify not connected", 400)

        access_token = connection["accessToken"]
        if is_token_expired(connection.get("expiresAt", "")):
            logger.info("Token expired for user %s, refreshing...", user_id)
            new_tokens, error = refresh_access_token(connection["refreshToken"])

            if error:
                logger.error("Token refresh failed for user %s: %s", user_id, error)
                return error_response("Failed to refresh Spotify token", 401)

            update_platform_tokens(user_id, "spotify", new_tokens)
            access_token = new_tokens["access_token"]

        logger.info("Fetching saved tracks for user %s...", user_id)
        tracks, error = get_user_saved_tracks(access_token)

        if error:
            logger.error("Track fetch failed for user %s: %s", user_id, error)
            return error_response("Failed to fetch tracks", 500)

        if not tracks:
            return success_response(
                {"synced": 0, "message": "No tracks found in library"}
            )

        formatted_tracks = []
        malformed_track_count = 0
        for track in tracks:
            processed_track = parse_track(track)
            if processed_track:
                formatted_tracks.append(processed_track)
            else:
                malformed_track_count += 1

        logger.info("Saving %d tracks to DB...", len(formatted_tracks))
        saved_count = save_tracks(user_id, formatted_tracks)

        return success_response(
            {
                "synced": saved_count,
                "malformed": malformed_track_count,
                "message": f"Synced {saved_count} tracks from Spotify",
            }
        )
    except Exception as e:
        logger.error("Error fetching library: %s", e)
        return error_response("Failed to sync library", 500)
