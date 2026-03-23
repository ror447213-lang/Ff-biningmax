from flask import Flask, request, jsonify
from bind_logic import *

app = Flask(__name__)
API_KEY = "12345"

def check(key):
    return key == API_KEY

# ---------- HOME ----------
@app.route("/")
def home():
    return jsonify({
        "status": "FULL API RUNNING",
        "endpoints": [
            "/bind","/cancel","/links","/revoke",
            "/send_otp","/verify_otp",
            "/verify_security","/verify_identity_otp",
            "/rebind","/unbind"
        ],
        "usage": "?token=XXX&key=12345"
    })

# ---------- BASIC ----------
@app.route("/bind")
def bind():
    token = request.args.get("token")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(get_bind_info(token).json())

@app.route("/cancel")
def cancel():
    token = request.args.get("token")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(cancel_request(token).json())

@app.route("/links")
def links():
    token = request.args.get("token")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(get_platforms(token).json())

@app.route("/revoke")
def revoke():
    token = request.args.get("token")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    ok,msg = revoke_token(token)
    return jsonify({"success":ok,"message":msg})

# ---------- OTP ----------
@app.route("/send_otp")
def send():
    token = request.args.get("token")
    email = request.args.get("email")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(send_otp(token,email).json())

@app.route("/verify_otp")
def verify():
    token = request.args.get("token")
    email = request.args.get("email")
    otp = request.args.get("otp")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(verify_otp(token,email,otp).json())

# ---------- VERIFY ----------
@app.route("/verify_security")
def verify_sec():
    token = request.args.get("token")
    code = request.args.get("code")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(verify_identity_with_security_code(token,code).json())

@app.route("/verify_identity_otp")
def verify_id():
    token = request.args.get("token")
    email = request.args.get("email")
    otp = request.args.get("otp")
    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})
    return jsonify(verify_identity_with_otp(token,email,otp).json())

# ---------- REBIND ----------
@app.route("/rebind")
def rebind():
    token = request.args.get("token")
    identity = request.args.get("identity")
    verifier = request.args.get("verifier")
    email = request.args.get("email")

    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})

    return jsonify(
        create_rebind_request(token,identity,verifier,email).json()
    )

# ---------- UNBIND ----------
@app.route("/unbind")
def unbind():
    token = request.args.get("token")
    identity = request.args.get("identity")

    if not check(request.args.get("key")):
        return jsonify({"error":"unauthorized"})

    return jsonify(unbind_identity(token,identity).json())
