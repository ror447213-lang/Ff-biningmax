from fastapi import FastAPI
from bind_logic import *

app = FastAPI()

API_KEY = "12345"   # change this

def auth(key):
    return key == API_KEY


@app.get("/")
def home():
    return {"status": "API Running"}


@app.get("/bind")
def bind(token: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return get_bind_info(token).json()
    except:
        return {"error": "failed"}


@app.get("/cancel")
def cancel(token: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return cancel_request(token).json()
    except:
        return {"error": "failed"}


@app.get("/links")
def links(token: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return get_platforms(token).json()
    except:
        return {"error": "failed"}


@app.get("/user")
def user(token: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    return get_user_info(token) or {"error": "failed"}


@app.get("/revoke")
def revoke(token: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    ok, msg = revoke_token(token)
    return {"success": ok, "response": msg}


@app.get("/send_otp")
def send(token: str, email: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return send_otp(token, email).json()
    except:
        return {"error": "failed"}


@app.get("/verify_otp")
def verify(token: str, email: str, otp: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return verify_otp(token, email, otp).json()
    except:
        return {"error": "failed"}


@app.get("/verify_security")
def verify_sec(token: str, code: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return verify_identity_with_security_code(token, code).json()
    except:
        return {"error": "failed"}


@app.get("/rebind")
def rebind(token: str, identity: str, verifier: str, email: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return create_rebind_request(token, identity, verifier, email).json()
    except:
        return {"error": "failed"}


@app.get("/unbind")
def unbind(token: str, identity: str, key: str):
    if not auth(key): return {"error": "unauthorized"}
    try:
        return unbind_identity(token, identity).json()
    except:
        return {"error": "failed"}
