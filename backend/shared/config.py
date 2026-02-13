import boto3
import logging
import os

_ssm_client = None
_cache = {}

SSM_PREFIX = os.environ.get("SSM_PREFIX", "/melodiary")


def get_logger(name):
    """
    Get a configured logger for a module.

    AWS Lambda sends Python logging output to CloudWatch automatically.
    Setting the level on the root logger ensures all the loggers respect it.
    The LOG_LEVEL env var can override the default (INFO) per-lambda if needed.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        level = os.environ.get("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, level, logging.INFO))
    return logger


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
    logger = get_logger(__name__)
    try:
        response = client.get_parameter(Name=param_path, WithDecryption=True)
    except client.exceptions.ParameterNotFound:
        logger.error("SSM parameter not found: %s", param_path)
        return None
    except Exception as e:
        logger.error("Failed to fetch SSM parameter %s: %s", param_path, e)
        return None
    value = response["Parameter"]["Value"]
    _cache[name] = value
    return value
