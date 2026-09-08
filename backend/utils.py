#+-----------------------------------+
#| Created by: fgatto13 @2026-02-10  |
#+-----------------------------------+

# utils.py
import azure.functions as func
import os

CORS_ORIGIN = os.environ.get("CORS_ORIGIN", "*")

def cors_response() -> func.HttpResponse:
    headers = {
        "Access-Control-Allow-Origin": CORS_ORIGIN,
        "Access-Control-Allow-Methods": "GET,POST,PUT,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
    }
    return func.HttpResponse(status_code=200, headers=headers)

def add_cors_headers(response: func.HttpResponse) -> func.HttpResponse:
    response.headers.update({
        "Access-Control-Allow-Origin": CORS_ORIGIN,
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
    })
    return response

