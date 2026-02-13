import json

from shared.config import get_logger
from shared.responses import success_response, error_response
from shared.auth_utils import require_auth
from shared.db import get_user_library, soft_delete_track

logger = get_logger(__name__)


@require_auth
def lambda_handler(event, context):
    """
    Library resource handler. Routes based on HTTP method:
        GET    /library             - List tracks with pagination
        DELETE /library/{trackId}   - Soft-delete a track
    """
    # REST API (v1) uses "httpMethod", HTTP API (v2) uses "requestContext.http.method"
    method = event.get("httpMethod") or (
        event.get("requestContext", {}).get("http", {}).get("method", "")
    )
    user_id = event.get("userId")

    if not user_id:
        return error_response("No such user", 404)

    if method == "GET":
        return _get_library(event, user_id)
    elif method == "DELETE":
        return _delete_track(event, user_id)
    else:
        return error_response("Method not allowed", 405)


def _get_library(event, user_id):
    """Get user track library with cursor-based pagination."""
    params = event.get("queryStringParameters") or {}

    try:
        limit = min(int(params.get("limit", 50)), 100)
        if limit < 1:
            return error_response("Limit must be a positive integer", 400)
    except (ValueError, TypeError):
        return error_response("Invalid limit parameter", 400)

    last_key = params.get("lastKey")
    if last_key:
        try:
            last_key = json.loads(last_key)
        except json.JSONDecodeError:
            return error_response("Invalid lastKey format", 400)

    try:
        result = get_user_library(user_id, limit=limit, last_key=last_key)
    except Exception as e:
        logger.error("Failed to retrieve library for user %s: %s", user_id, e)
        return error_response("Failed to retrieve library", 500)

    return success_response(
        {
            "items": result["items"],
            "lastKey": result["lastKey"],
            "count": result["count"],
        }
    )


def _delete_track(event, user_id):
    """Soft-delete a track from user's library."""
    path_params = event.get("pathParameters") or {}
    track_id = path_params.get("trackId")

    if not track_id:
        return error_response("Missing trackId", 400)

    try:
        deleted = soft_delete_track(user_id, track_id)
    except Exception as e:
        logger.error("Failed to delete track %s for user %s: %s", track_id, user_id, e)
        return error_response("Failed to delete track", 500)

    if not deleted:
        return error_response("Track not found", 404)

    return success_response({"message": "Track deleted"})
