import reflex as rx

from rxconfig import config
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

KINDE_HOST = os.environ.get("KINDE_HOST", "https://alavueltadeunclic.kinde.com")
KINDE_CLIENT_ID = os.environ.get("KINDE_CLIENT_ID", "22ce4f3bf7a542fb9c48b343e4564adb")
KINDE_CLIENT_SECRET = os.environ.get("KINDE_CLIENT_SECRET", "g4EQW9JHBaaurRg6IUKSFUisPpDv5toXZ1ek10e8SmArHhvUn0Ni")
KINDE_REDIRECT_URL = os.environ.get("KINDE_REDIRECT_URL", "http://localhost:3000")
KINDE_POST_LOGOUT_REDIRECT_URL = os.environ.get(
    "KINDE_POST_LOGOUT_REDIRECT_URL", "http://localhost:3000"
)

kinde_config = Configuration(host=KINDE_HOST)
kinde_client_params = {
    "configuration": kinde_config,
    "domain": KINDE_HOST,
    "client_id": KINDE_CLIENT_ID,
    "client_secret": KINDE_CLIENT_SECRET,
    "grant_type": GrantType.AUTHORIZATION_CODE,
    "callback_url": KINDE_REDIRECT_URL,
}

kinde_client = KindeApiClient(**kinde_client_params)


class AuthState(rx.State):
    """Auth state."""

    is_authenticated: bool = False
    user_details: dict = {}

    def initiate_login(self):
        logging.info("Initiating login process")
        return rx.redirect(kinde_client.get_login_url())

    def perform_logout(self):
        logging.info("Performing logout")
        self.is_authenticated = False
        self.user_details = {}
        logging.info("User state reset")
        return rx.redirect(
            kinde_client.logout(redirect_to=KINDE_POST_LOGOUT_REDIRECT_URL)
        )

    def process_authentication(self):
        logging.info("Processing authentication")
        auth_params = self.router.page.params
        logging.info(f"Query params: {auth_params}")

        error = auth_params.get("error")
        if error:
            logging.info(f"Authentication error from Kinde: {error}")
            return self.clean_url_and_redirect()

        if auth_params.get("code") and auth_params.get("state"):
            logging.info("Authorization code and state found in query params")
            self.exchange_code_for_token(auth_params)
            return self.clean_url_and_redirect()
        else:
            logging.info(
                "No authorization code and state in query params, attempting silent authentication"
            )
            #return self.attempt_silent_auth()

    def exchange_code_for_token(self, auth_params):
        logging.info("Exchanging authorization code for token")
        full_url = f"{KINDE_REDIRECT_URL}?code={auth_params['code']}&state={auth_params['state']}"
        try:
            kinde_client.fetch_token(authorization_response=full_url)
            logging.info("Token fetched successfully")
            self.update_auth_status()
        except Exception as e:
            logging.error(f"Token exchange error: {str(e)}")

    def update_auth_status(self):
        logging.info("Updating authentication status")
        self.is_authenticated = kinde_client.is_authenticated()
        logging.info(f"is_authenticated: {self.is_authenticated}")

        if self.is_authenticated:
            self.user_details = kinde_client.get_user_details()
            logging.info(f"User details fetched: {self.user_details}")
        else:
            logging.info("User is not authenticated")

    def attempt_silent_auth(self):
        logging.info("Attempting silent authentication")
        login_url = kinde_client.get_login_url(additional_params={"prompt": "none"})
        return rx.redirect(login_url)

    def initialize_auth(self):
        logging.info("Initializing authentication")
        self.update_auth_status()

    def clean_url_and_redirect(self):
        logging.info("Cleaning URL and redirecting")
        return rx.redirect("/")