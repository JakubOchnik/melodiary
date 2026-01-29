import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'eu-central-1'))

# Table references
users_table = dynamodb.Table('Melodiary-Users')
connections_table = dynamodb.Table('Melodiary-PlatformConnections')
library_table = dynamodb.Table('Melodiary-UserLibrary')

def create_user(user_id, email):
    users_table.put_item(
        Item = {
            'userId': user_id,
            'email': email,
            'createdAt': datetime.now().isoformat(),
            'displayName': email.split('@')[0]
        }
    )

def get_user(user_id):
    """Get user by ID"""
    response = users_table.get_item(Key={'userId': user_id})
    return response.get('Item')

def save_platform_connection(user_id, platform, tokens):
    """Save platform connection tokens"""
    connections_table.put_item(
        Item={
            'userId': user_id,
            'platform': platform,
            'accessToken': tokens['access_token'],
            'refreshToken': tokens.get('refresh_token'),
            'expiresAt': tokens.get('expires_at'),
            'connectedAt': datetime.now().isoformat()
        }
    )

def get_platform_connection(user_id, platform):
    """Get platform connection"""
    response = connections_table.get_item(
        Key={
            'userId': user_id,
            'platform': platform
        }
    )
    return response.get('Item')
