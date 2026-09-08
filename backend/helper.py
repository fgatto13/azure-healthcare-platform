#+-----------------------------------+
#| Created by: fgatto13 @2026-02-06  |
#+-----------------------------------+
# helper.py

import base64
import json
import logging

def parse_jwt(token: str):
    # JWT = header.payload.signature
    try:
        payload_enc = token.split(".")[1]
        # Base64 padding fix
        payload_enc += '=' * (-len(payload_enc) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_enc)
        return json.loads(payload_bytes)
    except Exception as e:
        return {"error": str(e)}
    
def log_auth_heaeder(auth_header):
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        claims = parse_jwt(token)
        logging.info(f"Token claims: {claims}")