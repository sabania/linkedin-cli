"""Authentication and credential management using Selenium."""

import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from linkedin_wrapper import LinkedinClient

CONFIG_DIR = Path.home() / ".linkedin-cli"
CHROME_PROFILE = CONFIG_DIR / "chrome_profile"
COOKIES_FILE = CONFIG_DIR / "cookies.json"

_client: LinkedinClient | None = None


def _get_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome driver (no persistent profile — cookies are stored separately)."""
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def _save_cookies(driver: webdriver.Chrome):
    """Save all LinkedIn cookies to disk."""
    cookies = driver.get_cookies()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2))


def _load_cookies(driver: webdriver.Chrome) -> bool:
    """Load saved cookies into the driver. Returns True if li_at was found."""
    if not COOKIES_FILE.exists():
        return False

    cookies = json.loads(COOKIES_FILE.read_text())
    # Navigate to LinkedIn first so we can set cookies for the domain
    driver.get("https://www.linkedin.com")
    time.sleep(1)

    for cookie in cookies:
        # Remove problematic fields that Selenium doesn't accept
        for key in ["sameSite", "expiry"]:
            cookie.pop(key, None)
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

    # Check if li_at was loaded
    return any(c["name"] == "li_at" for c in driver.get_cookies())


def browser_login() -> LinkedinClient:
    """Open Chrome for user to log in. Returns authenticated client."""
    driver = _get_driver(headless=False)
    driver.get("https://www.linkedin.com/login")

    print("Waiting for login...", end="", flush=True)
    li_at = None
    for _ in range(300):  # 5 min timeout
        for c in driver.get_cookies():
            if c["name"] == "li_at":
                li_at = c["value"]
                break
        if li_at:
            break
        time.sleep(1)
        print(".", end="", flush=True)

    if not li_at:
        driver.quit()
        print()
        raise SystemExit("Login timed out.")

    # Navigate to feed to fully load session
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(2)
    print(" OK")

    # Save cookies for headless sessions
    _save_cookies(driver)
    driver.quit()
    return get_client()


def get_client() -> LinkedinClient:
    """Get authenticated LinkedIn client using headless Chrome with saved cookies."""
    global _client
    if _client is not None:
        return _client

    driver = _get_driver(headless=True)

    # Inject saved cookies
    if not _load_cookies(driver):
        driver.quit()
        raise SystemExit("Not logged in. Run 'linkedin-cli login' first.")

    # Reload with cookies active
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(2)

    # Verify login
    li_at = None
    for c in driver.get_cookies():
        if c["name"] == "li_at":
            li_at = c["value"]
            break

    if not li_at:
        driver.quit()
        raise SystemExit("Session expired. Run 'linkedin-cli login' again.")

    _client = LinkedinClient(driver)
    return _client
