"""
Centralized test data for ARIA framework.
Keep all test inputs here — never hardcode in test files.
"""

# Valid credentials for automationexercise.com
# Create a free account at https://automationexercise.com/login first!
VALID_USER = {
    "email": "sdet@qa.com",  # ← Replace with your actual registered email
    "password": "sdet",                    # ← Replace with your actual password
    "username": "sdet"                      # ← Your display name on the site
}

# Invalid credential combinations for negative testing
INVALID_CREDENTIALS = [
    ("wrong@email.com", "wrongpassword", "completely wrong credentials"),
    ("your_registered_email@example.com", "wrongpassword", "correct email wrong password"),
]