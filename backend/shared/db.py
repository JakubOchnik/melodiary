import boto3
import os
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource(
    "dynamodb", region_name=os.environ.get("AWS_REGION", "eu-central-1")
)

# Table references
users_table = dynamodb.Table("Melodiary-Users")
connections_table = dynamodb.Table("Melodiary-PlatformConnections")
library_table = dynamodb.Table("Melodiary-UserLibrary")


def create_user(email, display_name, spotify_id, has_real_email):
    """
    Create a new user

    Args:
        email: User email
        display_name: Display name
        spotify_id: Optional Spotify user ID
        has_real_email: Whether email is real or generated

    Returns:
        Created user object
    """
    user_id = str(uuid.uuid4())
    user = {
        "userId": user_id,
        "email": email,
        "displayName": display_name or email.split("@")[0],
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "hasRealEmail": has_real_email,
        "preferences": {
            "emailNotifications": has_real_email,
            "notificationFrequency": "weekly",
        },
    }

    if spotify_id:
        user["spotifyId"] = spotify_id

    users_table.put_item(Item=user)
    return user


def get_user(user_id):
    """Get user by ID"""
    response = users_table.get_item(Key={"userId": user_id})
    return response.get("Item")


def get_value_from_db(table, filter, expression_values):
    """
    Gets a single object by filter

    Args:
        table: Searched table
        filter: FilterExpression
        expression_values: expression_values

    Returns:
        Object if found, None otherwise
    """

    # DynamoDB Scan returns a single page (max 1 MB of data),
    # so we need pagination via LastEvaluatedKey
    last_key = None
    while True:
        scan_kwargs = {
            "FilterExpression": filter,
            "ExpressionAttributeValues": expression_values,
        }
        if last_key:
            scan_kwargs["ExclusiveStartKey"] = last_key

        response = table.scan(**scan_kwargs)

        items = response.get("Items", [])
        if items:
            return items[0]
        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            return None


def get_user_by_email(email):
    """
    Gets user object by email (requires scanning)

    Args:
        email: User email

    Returns:
        User object if found, None otherwise
    """
    return get_value_from_db(users_table, "email = :email", {":email": email})


def get_user_by_spotify_id(spotify_id):
    """
    Get user by Spotify ID (requires scanning)

    Args:
        spotify_id: Spotify user ID

    Returns:
        User object if found, None otherwise
    """
    return get_value_from_db(
        users_table, "spotifyId = :spotifyId", {":spotifyId": spotify_id}
    )


def link_spotify_id_to_user(user_id: str, spotify_id: str) -> None:
    """
    Link a Spotify ID to an existing user

    Args:
        user_id: User ID
        spotify_id: Spotify user ID
    """
    users_table.update_item(
        Key={"userId": user_id},
        UpdateExpression="SET spotifyId = :spotifyId",
        ExpressionAttributeValues={":spotifyId": spotify_id},
    )


def save_platform_connection(user_id, platform, tokens, profile_data):
    """
    Save platform connection tokens

    Args:
        user_id: User ID
        platform: Platform name
        tokens: Token data from OAuth
        profile_data: Optional profile data from platform
    """
    if "access_token" not in tokens:
        raise ValueError("tokens must contain 'access_token'")

    item = {
        "userId": user_id,
        "platform": platform,
        "accessToken": tokens["access_token"],
        "refreshToken": tokens.get("refresh_token"),
        "expiresAt": tokens.get("expires_at"),
        "connectedAt": datetime.now(timezone.utc).isoformat(),
    }

    if profile_data:
        item["displayName"] = profile_data.get("display_name")
        item["profileUrl"] = profile_data.get("external_urls", {}).get("spotify")
        item["platformUserId"] = profile_data.get("id")  # Store Spotify ID

        if profile_data.get("email"):
            item["email"] = profile_data.get("email")

    connections_table.put_item(Item=item)


def get_platform_connection(user_id, platform):
    """Get platform connection"""
    response = connections_table.get_item(Key={"userId": user_id, "platform": platform})
    return response.get("Item")


def update_platform_tokens(user_id, platform, tokens):
    """
    Update platform tokens for refresh purposes

    Args:
        user_id: User ID
        platform: Platform type
        tokens: New token data
    """
    if "access_token" not in tokens:
        raise ValueError("Tokens must contain 'access_token'")

    update_parts = ["accessToken = :access", "expiresAt = :expires"]
    expr_values = {
        ":access": tokens["access_token"],
        ":expires": tokens.get("expires_at"),
    }
    refresh_token = tokens.get("refresh_token")
    if refresh_token:
        update_parts.append("refreshToken = :refresh")
        expr_values[":refresh"] = refresh_token

    connections_table.update_item(
        Key={"userId": user_id, "platform": platform},
        UpdateExpression=f"SET {",".join(update_parts)}",
        ExpressionAttributeValues=expr_values,
    )


def save_tracks(user_id, tracks):
    """
    Batch save tracks to user library

    Args:
        user_id: User ID
        tracks: List of track objects

    Returns:
        Number of saved tracks
    """
    with library_table.batch_writer() as batch:
        for track in tracks:
            batch.put_item(
                Item={
                    "userId": user_id,
                    "trackId": track["trackId"],
                    "trackName": track["trackName"],
                    "artistName": track["artistName"],
                    "albumName": track["albumName"],
                    "platform": track["platform"],
                    "platformTrackId": track.get("platformTrackId"),
                    "platformAlbumId": track.get("platformAlbumId"),
                    "platformArtistId": track.get("platformArtistId"),
                    "coverArtUrl": track.get("coverArtUrl"),
                    "addedDate": track.get(
                        "addedDate", datetime.now(timezone.utc).isoformat()
                    ),
                    "isManual": track.get("isManual", False),
                }
            )

    return len(tracks)


def get_user_library(user_id, limit=50, last_key=None):
    """
    Get user library with pagination

    Args:
        user_id: User ID
        limit: Max number of items to return
        last_key: Last evaluated key for pagination

    Returns:
        Dict with items and pagination info
    """

    query_params = {
        "KeyConditionExpression": "userId = :userId",
        "ExpressionAttributeValues": {":userId": user_id},
        "Limit": limit,
        "ScanIndexForward": False,
    }

    if last_key:
        query_params["ExclusiveStartKey"] = last_key

    response = library_table.query(**query_params)
    return {
        "items": response.get("Items", []),
        "lastKey": response.get("LastEvaluatedKey"),
        "count": response.get("Count", 0),
    }
