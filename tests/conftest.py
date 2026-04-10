import pytest
import logging
from playwright.async_api import async_playwright
from aria.config import settings

# Set up logging so you see INFO messages in terminal during test runs
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config():
    """
    Session-scoped fixture: created ONCE for the entire test run.
    Use this when you need settings inside a test:
        def test_something(config):
            print(config.base_url)
    """
    return settings


@pytest.fixture(scope="function")
async def browser():
    """
    Function-scoped fixture: a fresh browser for EACH test.
    'async with' ensures the browser is properly closed even if the test crashes.
    """
    async with async_playwright() as playwright:
        # Dynamically get the right browser type from settings
        browser_launcher = getattr(playwright, settings.browser)
        browser = await browser_launcher.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo,
        )
        logger.info(f"Opened browser: {settings.browser}")
        yield browser  # 'yield' hands the browser to the test; code after runs on cleanup
        await browser.close()
        logger.info("Browser closed cleanly")


@pytest.fixture(scope="function")
async def page(browser):
    """
    Function-scoped fixture: a fresh browser tab for EACH test.
    BrowserContext = an isolated session (separate cookies, localStorage, etc.)
    Think of it like an incognito window — clean slate every test.
    """
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,  # Don't fail on SSL certificate errors
    )
    page = await context.new_page()
    logger.info("New browser context and page created")

    yield page  # Hand the page to the test

    # Cleanup after test — take screenshot on failure (we'll improve this later)
    await context.close()
    logger.info("Browser context closed")