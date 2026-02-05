import json

STANDARD_CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
}


def get_standard_cors_headers():
    """
    Return CORS headers
    Note: These are now redundant after using API Gateway CORS
    """
    return STANDARD_CORS_HEADERS.copy()


def success_response(data, status_code=200):
    """Return a successful API response"""
    return create_response(
        status_code,
        json.dumps(data) if not isinstance(data, str) else data,
    )


def error_response(message, status_code=400, details=None):
    """Return an error API response"""
    error_body = {"error": message}
    if details:
        error_body["details"] = details

    return create_response(status_code, json.dumps(error_body))


def create_response(status_code, body, headers=None):
    response = {"statusCode": status_code, "body": body}
    if headers:
        response["headers"] = headers
    return response
