import json

from shared.config import get_logger
from shared.responses import success_response, error_response
from shared.auth_utils import require_auth
from shared.db import get_user_library

logger = get_logger(__name__)


@require_auth
def lambda_handler(event, context):
    """
    Get user track library with cursor-based pagination.

    Query params:
        limit: Number of tracks to return (default 50, max 100)
        lastKey: Pagination cursor from previous response
    """
    user_id = event.get("userId")
    if not user_id:
        return error_response("No such user", 404)

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
