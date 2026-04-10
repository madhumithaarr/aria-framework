import logging
from playwright.async_api import Page
from aria.base_page import BasePage
from aria.config import settings

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    Page Object for automationexercise.com homepage.

    Inherits all base methods (navigate, click, fill, etc.)
    and adds homepage-specific actions and selectors.
    """

    # --- Selectors ---
    # Storing selectors as class variables means one place to update if they change
    NAV_LOGIN = "a[href='/login']"
    NAV_PRODUCTS = "a[href='/products']"
    NAV_CART = "a[href='/view_cart']"
    LOGO = "div#logo img"
    SLIDER = "div#slider"

    def __init__(self, page: Page):
        super().__init__(page)  # Call BasePage's __init__ so self.page is set
        self.url = settings.base_url

    async def open(self) -> "HomePage":
        """Navigate to homepage. Returns self so you can chain: await HomePage(page).open()"""
        await self.navigate(self.url)
        logger.info("Homepage opened")
        return self

    async def go_to_login(self) -> None:
        """Click the Signup/Login link in the navbar."""
        await self.click(self.NAV_LOGIN)
        logger.info("Navigated to login page")

    async def go_to_products(self) -> None:
        """Click the Products link in the navbar."""
        await self.click(self.NAV_PRODUCTS)

    async def is_logo_visible(self) -> bool:
        """Check if the site logo is visible — confirms page loaded correctly."""
        return await self.is_visible(self.LOGO)

    async def is_slider_visible(self) -> bool:
        """Check if the homepage image slider is visible."""
        return await self.is_visible(self.SLIDER)