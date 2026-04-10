import pytest
from aria.config import settings


@pytest.mark.smoke
@pytest.mark.ui
async def test_homepage_loads(page):
    """
    Simplest possible test — does the site load at all?
    If this fails, nothing else will work either.
    """
    await page.goto(settings.base_url)
    title = await page.title()

    # Assert the title contains what we expect
    assert "Automation Exercise" in title, \
        f"Expected 'Automation Exercise' in title but got: '{title}'"


@pytest.mark.smoke
@pytest.mark.ui
async def test_navbar_is_visible(page):
    """Verify the top navigation bar renders correctly."""
    await page.goto(settings.base_url)

    # Playwright locator — CSS selector targeting the nav element
    navbar = page.locator("nav#header")
    assert await navbar.is_visible(), "Navigation bar is not visible on homepage"


@pytest.mark.smoke
@pytest.mark.ui
async def test_homepage_has_login_link(page):
    """Verify the Signup/Login link is present — critical for user flows."""
    await page.goto(settings.base_url)

    # :has-text() is a Playwright-specific selector — finds element containing this text
    login_link = page.locator("a:has-text('Signup / Login')")
    assert await login_link.is_visible(), "Login link not found on homepage"


@pytest.mark.smoke
@pytest.mark.ui
async def test_screenshot_on_load(page):
    """Load the homepage and capture a screenshot — verifies screenshot utility works."""
    await page.goto(settings.base_url)
    await page.screenshot(path="reports/homepage.png", full_page=True)

    # Verify file was created by trying to open it — if this line runs, file exists
    import os
    assert os.path.exists("reports/homepage.png"), "Screenshot was not saved"