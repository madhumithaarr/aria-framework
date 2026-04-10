import pytest
from pages.login_page import LoginPage
from tests.test_data import VALID_USER, INVALID_CREDENTIALS


@pytest.mark.smoke
@pytest.mark.ui
async def test_login_page_loads(login_page):
    """Verify the login page has both login and signup sections."""
    # Check login form elements are visible
    assert await login_page.is_visible(login_page.LOGIN_EMAIL), \
        "Email field not visible"
    assert await login_page.is_visible(login_page.LOGIN_PASSWORD), \
        "Password field not visible"
    assert await login_page.is_visible(login_page.LOGIN_BUTTON), \
        "Login button not visible"


@pytest.mark.regression
@pytest.mark.ui
async def test_successful_login(login_page):
    """
    Verify a registered user can log in successfully.
    This is a CRITICAL test — login is the gateway to everything else.
    """
    await login_page.login(VALID_USER["email"], VALID_USER["password"])

    # After login, navbar should show "Logged in as username"
    assert await login_page.is_logged_in(), \
        "User does not appear to be logged in after valid credentials"

    # Optionally verify the correct username is shown
    username = await login_page.get_logged_in_username()
    assert VALID_USER["username"].lower() in username.lower(), \
        f"Expected username '{VALID_USER['username']}' but got '{username}'"


@pytest.mark.regression
@pytest.mark.ui
async def test_logout_after_login(login_page):
    """Verify user can log out after logging in."""
    await login_page.login(VALID_USER["email"], VALID_USER["password"])
    assert await login_page.is_logged_in(), "Login failed — cannot test logout"

    await login_page.logout()

    # After logout, login button should be visible again
    assert await login_page.is_visible(login_page.LOGIN_BUTTON), \
        "Login button not visible after logout — logout may have failed"


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("email,password,scenario", INVALID_CREDENTIALS)
async def test_invalid_login_shows_error(login_page, email, password, scenario):
    """
    Verify invalid credentials show an error message.

    @pytest.mark.parametrize runs this ONE test function multiple times,
    once for each set of credentials in INVALID_CREDENTIALS.
    Much cleaner than writing 3 separate test functions.
    """
    await login_page.login(email, password)

    assert await login_page.is_login_error_visible(), \
        f"Expected error message for scenario: '{scenario}' but none appeared"
    
@pytest.mark.regression
@pytest.mark.ui
async def test_invalid_email_format_browser_validation(login_page):
    """
    Verify browser-level HTML5 validation fires for invalid email format.
    This is separate from app-level validation — browser intercepts BEFORE
    the form is submitted to the server.

    Real-world insight: 'notanemail' never reaches the backend.
    """
    await login_page.fill(login_page.LOGIN_EMAIL, "notanemail")
    await login_page.fill(login_page.LOGIN_PASSWORD, "password123")

    # Check the input field itself has HTML5 validation error
    # :invalid is a CSS pseudo-class that Playwright can check
    email_input = login_page.page.locator(login_page.LOGIN_EMAIL)
    
    # Evaluate JS to check if field is valid per browser
    is_valid = await email_input.evaluate("el => el.validity.valid")
    
    assert not is_valid, \
        "Expected browser to flag 'notanemail' as invalid email format"
    
    # Also verify the field has the right validation message
    validation_msg = await email_input.evaluate("el => el.validationMessage")
    assert len(validation_msg) > 0, \
        f"Expected a browser validation message but got none"
    
    print(f"\nBrowser validation message: '{validation_msg}'")