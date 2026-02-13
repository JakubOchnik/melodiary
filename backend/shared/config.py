import boto3
import os

_ssm_client = None
_cache = {}

SSM_PREFIX = os.environ.get("SSM_PREFIX", "/melodiary")


def _get_ssm_client():
    global _ssm_client
    if _ssm_client is None:
        _ssm_client = boto3.client(
            "ssm", region_name=os.environ.get("AWS_REGION", "eu-central-1")
        )
    return _ssm_client


def get_secret(name):
    """
    Get a secret from SSM Parameter Store.

    Values are cached after the first fetch, so SSM is only called once
    per Lambda cold start.

    Args:
        name: Parameter name (e.g. "SPOTIFY_CLIENT_ID").
              Will be prefixed with SSM_PREFIX ("/melodiary" by default).

    Returns:
        The decrypted parameter value.
    """
    if name in _cache:
        return _cache[name]

    client = _get_ssm_client()
    param_path = f"{SSM_PREFIX}/{name}"
    try:
        response = client.get_parameter(Name=param_path, WithDecryption=True)
    except client.exceptions.ParameterNotFound:
        print(f"SSM parameter not found: {param_path}")
        return None
    except Exception as e:
        print(f"Failed to fetch SSM parameter {param_path}: {e}")
        return None
    value = response["Parameter"]["Value"]
    _cache[name] = value
    return value
