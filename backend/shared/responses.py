import json

STANDARD_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
}


def get_standard_headers():
    return STANDARD_HEADERS.copy()


def success_response(data, status_code=200):
    """Return a successful API response"""
    return create_response(status_code, get_standard_headers(), json.dumps(data))


def error_response(message, status_code=400):
    """Return an error API response"""
    return create_response(
        status_code, get_standard_headers(), json.dumps({"error": message})
    )


def create_response(status_code, headers, body):
    return {"statusCode": status_code, "headers": headers, "body": body}
