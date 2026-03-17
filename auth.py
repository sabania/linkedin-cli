"""Authentication and credential management using Nodriver.

Nodriver communicates with Chrome via CDP directly — no WebDriver binary,
no navigator.webdriver flag, no cdc_ variables. Undetectable by LinkedIn's
PerimeterX/HUMAN anti-bot system.
"""

import json
import random
import time
from pathlib import Path

from nodriver_adapter import create_driver
from linkedin_wrapper import LinkedinClient

CONFIG_DIR = Path.home() / ".linkedin-cli"
COOKIES_FILE = CONFIG_DIR / "cookies.json"

_client: LinkedinClient | None = None


def _get_driver(headless: bool | None = None):
    """Create an undetectable Chrome driver via Nodriver adapter.

    If headless is None, reads from config (default: True).
    Explicit True/False overrides the config (e.g. login always needs headed).
    """
    if headless is None:
        from commands.config import get_setting
        headless = get_setting("browser.headless", True)
    return create_driver(headless=headless)


def _save_cookies(driver):
    """Save all LinkedIn cookies to disk."""
    cookies = driver.get_cookies()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2))


def _load_cookies(driver) -> bool:
    """Load saved cookies into the driver. Returns True if li_at was found."""
    if not COOKIES_FILE.exists():
        return False

    cookies = json.loads(COOKIES_FILE.read_text())
    # Navigate to LinkedIn first so we can set cookies for the domain
    driver.get("https://www.linkedin.com")
    time.sleep(random.uniform(0.7, 1.5))

    for cookie in cookies:
        # Remove fields not supported by CDP cookie params
        for key in ["sameSite", "expiry"]:
            cookie.pop(key, None)
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

    # Check if li_at was loaded
    return any(c["name"] == "li_at" for c in driver.get_cookies())


def cookie_login(li_at: str) -> LinkedinClient:
    """Login using a manually provided li_at cookie. Works on headless servers.

    The user copies the li_at cookie from their browser's DevTools:
    DevTools → Application → Cookies → linkedin.com → li_at
    """
    driver = _get_driver()  # reads browser.headless from config
    driver.get("https://www.linkedin.com")
    time.sleep(random.uniform(0.7, 1.5))

    # Set the li_at session cookie
    driver.add_cookie({
        "name": "li_at",
        "value": li_at,
        "domain": ".linkedin.com",
        "path": "/",
        "secure": True,
        "httpOnly": True,
    })

    # Load feed to establish full session (picks up JSESSIONID etc.)
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(random.uniform(1.4, 3.0))

    # Verify the cookie works
    cookies = driver.get_cookies()
    has_session = any(c["name"] == "JSESSIONID" for c in cookies)
    if not has_session:
        driver.quit()
        raise SystemExit("Cookie invalid or expired. Get a fresh li_at from your browser.")

    # Save full cookie set for future headless sessions
    _save_cookies(driver)
    driver.quit()
    return get_client()


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
        time.sleep(1)  # Polling interval — intentionally fixed
        print(".", end="", flush=True)

    if not li_at:
        driver.quit()
        print()
        raise SystemExit("Login timed out.")

    # Navigate to feed to fully load session
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(random.uniform(1.4, 3.0))
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

    driver = _get_driver()  # reads browser.headless from config

    # Inject saved cookies
    if not _load_cookies(driver):
        driver.quit()
        raise SystemExit("Not logged in. Run 'linkedin-cli login' first.")

    # Reload with cookies active
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(random.uniform(1.4, 3.0))

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
