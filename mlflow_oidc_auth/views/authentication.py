import secrets

from flask import redirect, session, url_for

import mlflow_oidc_auth.utils as utils
from mlflow_oidc_auth.auth import get_oauth_instance
from mlflow_oidc_auth.app import app
from mlflow_oidc_auth.config import config
from mlflow_oidc_auth.user import create_user, populate_groups, update_user


def login():
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state
    return get_oauth_instance(app).oidc.authorize_redirect(config.OIDC_REDIRECT_URI, state=state)


def logout():
    session.clear()
    return redirect("/")

import requests

def callback():
    """Validate the state to protect against CSRF"""    


    if "oauth_state" not in session or utils.get_request_param("state") != session["oauth_state"]:
        return "Invalid state parameter", 401

    token = get_oauth_instance(app).oidc.authorize_access_token()
    app.logger.debug(f"Token: {token}")
    # session["user"] = token["userinfo"]
    # print("oauth_state", session["oauth_state"])
    # print("\ntoken", token)
    # print("\nsession_user",session["user"])
    # # Use the email key from the userinfo response
    # email = token["userinfo"].get("email")
    # print('\nemail', email)
    
    
    # app.logger.debug(f"Userinfo: {token['userinfo']}")
    # print(f"Userinfo: {token['userinfo']}")

    #email = token["userinfo"]["email"]
        # Get the access token from the authorization code
       # Extract the access token from the token response
    access_token = token.get("access_token")
    print(access_token)
    if not access_token:
        app.logger.error("Access token not found in the response")
        return "Access token not found", 400

    # Check if the OIDC Discovery URL is set and fetch the necessary URLs
    if config.OIDC_DISCOVERY_URL:
        # Fetch the OIDC discovery information if not already fetched
        response = requests.get(config.OIDC_DISCOVERY_URL)
        if response.status_code == 200:
            discovery_config = response.json()
            config.OIDC_TOKEN_URL = discovery_config.get("token_endpoint")
            config.OIDC_USER_URL = discovery_config.get("userinfo_endpoint")
        else:
            app.logger.error(f"Failed to fetch OIDC Discovery URL: {config.OIDC_DISCOVERY_URL}")
            return "Discovery failed", 400
    
    # Ensure the necessary URLs are available
    if not config.OIDC_TOKEN_URL or not config.OIDC_USER_URL:
        app.logger.error("Missing OIDC token or user URL.")
        return "Configuration error", 400

    # Use the access token to fetch user info
    user_response = requests.get(config.OIDC_USER_URL, headers={"Authorization": f"Bearer {access_token}"})
    if user_response.status_code != 200:
        app.logger.error(f"Failed to fetch user info: {user_response.status_code}")
        return "User info fetch failed", 400
    
    # Process user data
    user_data = user_response.json()
    print("\nUser data",  user_data)
    email = user_data.get("email", None)  # Get the email, if available
    if not email:
        return "No email provided", 401

    # Get the display name (fallback to 'Unknown' if not provided)
    display_name = user_data.get("name", "Unknown")

    is_admin = False
    user_groups = []
    

    if config.OIDC_GROUP_DETECTION_PLUGIN:
        import importlib

        user_groups = importlib.import_module(config.OIDC_GROUP_DETECTION_PLUGIN).get_user_groups(token["access_token"])
    else:
        #user_groups = token["userinfo"][config.OIDC_GROUPS_ATTRIBUTE]
        user_groups = user_data.get(config.OIDC_GROUPS_ATTRIBUTE, [])

    app.logger.debug(f"User groups: {user_groups}")
    print(user_groups)

    if config.OIDC_ADMIN_GROUP_NAME in user_groups:
        is_admin = True
    elif not any(group in user_groups for group in config.OIDC_GROUP_NAME):
        return "User is not allowed to login", 401

    create_user(username=email.lower(), display_name=display_name, is_admin=is_admin)
    populate_groups(group_names=user_groups)
    update_user(email.lower(), user_groups)
    session["username"] = email.lower()

    return redirect(url_for("oidc_ui"))
