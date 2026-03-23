import requests
import hashlib

BASE_URL = "https://100067.connect.garena.com"

HEADERS = {
    "User-Agent": "GarenaMSDK/4.0.39 (Android 10)",
    "Content-Type": "application/x-www-form-urlencoded"
}

APP_ID = "100067"

REFRESH_TOKEN = "1380dcb63ab3a077dc05bdf0b25ba4497c403a5b4eae96d7203010eafa6c83a8"


def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def get_bind_info(token):
    return requests.get(
        f"{BASE_URL}/game/account_security/bind:get_bind_info",
        headers=HEADERS,
        params={"app_id": APP_ID, "access_token": token}
    )


def send_otp(token, email):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:send_otp",
        headers=HEADERS,
        data={"app_id": APP_ID, "access_token": token, "email": email}
    )


def verify_otp(token, email, otp):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:verify_otp",
        headers=HEADERS,
        data={"app_id": APP_ID, "access_token": token, "email": email, "otp": otp}
    )


def verify_identity_with_otp(token, email, otp):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:verify_identity",
        headers=HEADERS,
        data={"app_id": APP_ID, "access_token": token, "email": email, "otp": otp}
    )


def verify_identity_with_security_code(token, code):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:verify_identity",
        headers=HEADERS,
        data={
            "app_id": APP_ID,
            "access_token": token,
            "secondary_password": sha256_hash(code)
        }
    )


def create_rebind_request(token, identity, verifier, email):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:create_rebind_request",
        headers=HEADERS,
        data={
            "app_id": APP_ID,
            "access_token": token,
            "identity_token": identity,
            "verifier_token": verifier,
            "email": email
        }
    )


def cancel_request(token):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:cancel_request",
        headers=HEADERS,
        data={"app_id": APP_ID, "access_token": token}
    )


def unbind_identity(token, identity):
    return requests.post(
        f"{BASE_URL}/game/account_security/bind:unbind_identity",
        headers=HEADERS,
        data={"app_id": APP_ID, "access_token": token, "identity_token": identity}
    )


def get_platforms(token):
    return requests.get(
        f"{BASE_URL}/bind/app/platform/info/get",
        headers=HEADERS,
        params={"access_token": token}
    )


def get_user_info(token):
    try:
        r = requests.get(
            "https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/",
            headers={"access-token": token}
        )
        return r.json() if r.status_code == 200 else None
    except:
        return None


def revoke_token(token):
    try:
        r = requests.get(
            "https://100067.connect.garena.com/oauth/logout",
            params={"access_token": token, "refresh_token": REFRESH_TOKEN}
        )
        return True, r.text if r.status_code == 200 else (False, r.text)
    except Exception as e:
        return False, str(e)