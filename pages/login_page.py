import logging
from playwright.async_api import Page
from aria.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Page Object for automationexercise.com/login page.

    Covers both the Login section and Signup section
    (they're on the same page on this site).
    """

    # --- Selectors ---
    # Login section
    LOGIN_EMAIL = "input[data-qa='login-email']"
    LOGIN_PASSWORD = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGIN_ERROR = "p:has-text('Your email or password is incorrect!')"

    # Signup section (we'll use this later)
    SIGNUP_NAME = "input[data-qa='signup-name']"
    SIGNUP_EMAIL = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"

    # Post-login
    LOGGED_IN_USERNAME = "a:has-text('Logged in as')"
    LOGOUT_BUTTON = "a[href='/logout']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://automationexercise.com/login"

    async def open(self) -> "LoginPage":
        """Navigate directly to login page."""
        await self.navigate(self.url)
        return self

    async def login(self, email: str, password: str) -> None:
        """
        Perform login with given credentials.
        This is a complete action — fill email, fill password, click button.
        """
        logger.info(f"Attempting login with email: {email}")
        await self.fill(self.LOGIN_EMAIL, email)
        await self.fill(self.LOGIN_PASSWORD, password)
        await self.click(self.LOGIN_BUTTON)

    async def is_login_error_visible(self) -> bool:
        """Returns True if the 'incorrect credentials' error message is shown."""
        return await self.is_visible(self.LOGIN_ERROR)

    async def is_logged_in(self) -> bool:
        """Returns True if 'Logged in as username' text is visible in navbar."""
        return await self.is_visible(self.LOGGED_IN_USERNAME)

    async def get_logged_in_username(self) -> str:
        """Returns the username shown in navbar after login."""
        text = await self.get_text(self.LOGGED_IN_USERNAME)
        # Text looks like "Logged in as John" — extract just the name
        return text.replace("Logged in as", "").strip()

    async def logout(self) -> None:
        """Click the logout button."""
        await self.click(self.LOGOUT_BUTTON)
        logger.info("Logged out")