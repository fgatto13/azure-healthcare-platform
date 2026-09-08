#+-----------------------------------+
#| Created by: fgatto13 @2026-02-10  |
#+-----------------------------------+
import os
import logging
import jwt
from jwt import PyJWKClient, InvalidTokenError, ExpiredSignatureError
from dotenv import load_dotenv

load_dotenv()

def validate_jwt(token: str) -> dict:
    """
    Validates an Entra ID JWT using PyJWKClient.
    Returns claims dict if valid, raises ValueError if invalid.
    """
    try:
        TENANT_ID = os.getenv("TENANT_ID")
        CLIENT_ID = os.getenv("CLIENT_ID")  # backend API app id
        if not TENANT_ID or not CLIENT_ID:
            raise ValueError("Missing TENANT_ID or CLIENT_ID environment variables")
        jwks_url = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
        valid_issuers = [
            f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
            f"https://sts.windows.net/{TENANT_ID}/"
        ]
        audience = f"api://{CLIENT_ID}"

        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=audience,
            issuer=valid_issuers,
        )

        return claims

    except ExpiredSignatureError:
        logging.warning("JWT expired")
        raise ValueError("Token expired")
    except InvalidTokenError as e:
        logging.warning(f"JWT invalid: {e}")
        unverified = jwt.decode(token, options={"verify_signature": False})
        logging.warning(f"TOKEN ISSUER: {unverified.get('iss')}")
        logging.warning(f"EXPECTED ISSUER: https://login.microsoftonline.com/{TENANT_ID}/v2.0")
        raise ValueError("Unauthorized")
    except Exception as e:
        raise ValueError(f"Server error: {e}")
