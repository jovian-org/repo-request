import time
import requests


DEVICE_CODE_URL = "https://github.com/login/device/code"
ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"


def get_user_access_token(client_id: str) -> str:
    """Get a GitHub App user access token using device flow."""

    # Start the device authorization flow.
    device_response = requests.post(
        DEVICE_CODE_URL,
        data={"client_id": client_id},
        headers={"Accept": "application/json"},
        timeout=30,
    )
    device_response.raise_for_status()

    device_data = device_response.json()

    # Tell the user where to authorize the app.
    print(f"Open {device_data['verification_uri']}")
    print(f"Enter code: {device_data['user_code']}")

    device_code = device_data["device_code"]
    interval = int(device_data.get("interval", 5))

    while True:
        # Wait before polling again.
        time.sleep(interval)

        token_response = requests.post(
            ACCESS_TOKEN_URL,
            data={
                "client_id": client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
        token_response.raise_for_status()

        token_data = token_response.json()

        # Success: GitHub returns the user access token.
        if "access_token" in token_data:
            return token_data["access_token"]

        error = token_data.get("error")

        # User has not finished authorizing yet.
        if error == "authorization_pending":
            continue

        # GitHub is asking us to slow down polling.
        if error == "slow_down":
            interval += 5
            continue

        # The user denied access.
        if error == "access_denied":
            raise RuntimeError("GitHub authorization was denied.")

        # The device code expired.
        if error == "expired_token":
            raise RuntimeError("Device code expired. Start again.")

        raise RuntimeError(f"Unexpected OAuth response: {token_data}")