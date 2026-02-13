import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """Handles DynamoDB Decimal types during JSON serialization."""

    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o == int(o) else float(o)
        return super().default(o)

STANDARD_CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
}


def get_standard_cors_headers():
    return STANDARD_CORS_HEADERS.copy()


def success_response(data, status_code=200):
    """Return a successful API response"""
    return create_response(
        status_code,
        get_standard_cors_headers(),
        json.dumps(data, cls=DecimalEncoder) if not isinstance(data, str) else data,
    )


def error_response(message, status_code=400, details=None):
    """Return an error API response"""
    error_body = {"error": message}
    if details:
        error_body["details"] = details

    return create_response(
        status_code, get_standard_cors_headers(), json.dumps(error_body, cls=DecimalEncoder)
    )


def create_response(status_code, headers, body):
    return {"statusCode": status_code, "headers": headers, "body": body}
