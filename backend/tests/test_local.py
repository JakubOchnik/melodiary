"""
Local testing script for Lambda functions
"""

import sys
import os
import json

# Add backend directory to path so 'shared' can be imported
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Add lambdas to path
sys.path.insert(0, os.path.join(backend_dir, "lambda"))

from dotenv import load_dotenv

load_dotenv()


def test_spotify_login():
    """Test Spotify login endpoint"""
    from auth.spotify_login import lambda_handler

    event = {}
    context = {}

    response = lambda_handler(event, context)

    print("\n=== Testing Spotify Login ===")
    print("Status Code:", response["statusCode"])

    body = json.loads(response["body"])
    print("Auth URL:", body.get("authUrl", "N/A"))

    assert response["statusCode"] == 200
    assert "authUrl" in body
    print("Spotify login test passed!\n")


def test_spotify_callback():
    """Test Spotify callback endpoint"""
    print("\n=== Testing Spotify Callback ===")
    print("This test requires a real authorization code from Spotify.")
    print("To get a code:")
    print("1. Run test_spotify_login() to get the auth URL")
    print("2. Visit the URL in a browser")
    print("3. After authorizing, copy the 'code' parameter from the redirect URL")
    print("4. Paste it here when prompted\n")

    code = input("Enter Spotify authorization code (or press Enter to skip): ").strip()

    if not code:
        print("Skipping callback test (no code provided)\n")
        return

    from auth.spotify_callback import lambda_handler

    event = {"body": json.dumps({"code": code})}
    context = {}

    response = lambda_handler(event, context)

    print("Status Code:", response["statusCode"])

    body = json.loads(response["body"])

    if response["statusCode"] == 200:
        print("User authenticated!")
        print(f"  User ID: {body['user']['userId']}")
        print(f"  Email: {body['user']['email']}")
        print(f"  Display Name: {body['user']['displayName']}")
        print(f"  JWT Token: {body['token'][:50]}...")
    else:
        print("Authentication failed:")
        print(f"  Error: {body.get('error', 'Unknown error')}")

    print()


if __name__ == "__main__":
    test_spotify_login()
    test_spotify_callback()
