import logging
from playwright.async_api import Page, Locator

# Get a logger named after this module — shows "aria.base_page" in log output
logger = logging.getLogger(__name__)


class BasePage:
    """
    Parent class for all Page Objects.

    Every page in your app (LoginPage, HomePage, etc.) will
    inherit from this and get all these methods for free.

    Usage:
        class LoginPage(BasePage):
            async def login(self, email, password):
                await self.fill("#email", email)
                await self.click("#loginBtn")
    """

    def __init__(self, page: Page):
        self.page = page  # The Playwright Page object

    async def navigate(self, url: str) -> None:
        """Go to a URL and wait for the page to load."""
        logger.info(f"Navigating to: {url}")
        await self.page.goto(url, wait_until="domcontentloaded")
        # wait_until="domcontentloaded" means: wait until HTML is loaded
        # (faster than "networkidle" which waits for ALL network calls to stop)

    async def get_title(self) -> str:
        """Return the browser tab title."""
        return await self.page.title()

    async def wait_for_element(self, selector: str, timeout: int = 10000) -> Locator:
        """
        Wait for an element to be visible on screen.
        timeout is in milliseconds — 10000 = 10 seconds.
        Raises an error if element doesn't appear in time.
        """
        locator = self.page.locator(selector)
        await locator.wait_for(state="visible", timeout=timeout)
        return locator

    async def click(self, selector: str) -> None:
        """Wait for element then click it."""
        logger.info(f"Clicking element: {selector}")
        element = await self.wait_for_element(selector)
        await element.click()

    async def fill(self, selector: str, value: str) -> None:
        """Clear a field and type a value into it."""
        logger.info(f"Filling '{selector}' with value")
        element = await self.wait_for_element(selector)
        await element.fill(value)  # fill() clears first, then types

    async def get_text(self, selector: str) -> str:
        """Get the visible text of an element."""
        element = await self.wait_for_element(selector)
        return (await element.inner_text()).strip()

    async def is_visible(self, selector: str) -> bool:
        """Check if an element is visible — returns True/False, never raises."""
        return await self.page.locator(selector).is_visible()

    async def take_screenshot(self, name: str = "screenshot") -> None:
        """Save a full-page screenshot to reports folder."""
        path = f"reports/{name}.png"
        await self.page.screenshot(path=path, full_page=True)
        logger.info(f"Screenshot saved: {path}")