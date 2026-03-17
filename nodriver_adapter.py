"""Sync adapter wrapping Nodriver's async API behind Selenium's driver interface.

This lets linkedin_wrapper.py work with Nodriver without ANY code changes —
same driver.get(), driver.execute_script(), driver.get_cookies() etc.

Nodriver communicates with Chrome via CDP directly — no WebDriver binary,
no navigator.webdriver, no cdc_ variables. Undetectable by PerimeterX/HUMAN.
"""

import asyncio
import json

import nodriver as uc


def _deserialize(obj):
    """Recursively convert CDP RemoteObject / DeepSerializedValue to plain Python.

    Nodriver's evaluate() with return_by_value=True returns RemoteObject wrappers
    where complex values (dicts, arrays) are in deep_serialized_value instead of .value.
    This function reconstructs plain dicts/lists/primitives.
    """
    # Plain Python value — return as-is
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    # RemoteObject → check .value first, then deep_serialized_value
    if hasattr(obj, "value") and hasattr(obj, "deep_serialized_value"):
        # Primitive types have .value set directly
        if obj.value is not None:
            return obj.value
        dsv = obj.deep_serialized_value
        if dsv is not None:
            return _deserialize_dsv(dsv)
        return None

    # List/dict already deserialized
    if isinstance(obj, dict):
        return {k: _deserialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deserialize(v) for v in obj]

    return obj


def _deserialize_dsv(dsv):
    """Convert a DeepSerializedValue node to plain Python."""
    t = dsv.type_ if hasattr(dsv, "type_") else dsv.get("type") if isinstance(dsv, dict) else None
    v = dsv.value if hasattr(dsv, "value") else dsv.get("value") if isinstance(dsv, dict) else None

    if t in ("string", "number", "boolean", "bigint"):
        return v
    if t in ("undefined", "null", "symbol"):
        return None
    if t == "object":
        if v is None:
            return {}
        # v is a list of [key, value_dsv] pairs
        result = {}
        for pair in v:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                key, val_dsv = pair
                result[key] = _deserialize_dsv(val_dsv)
        return result
    if t == "array":
        if v is None:
            return []
        return [_deserialize_dsv(item) for item in v]

    # Fallback: return raw value
    return v


def _get_loop():
    """Get or create the Nodriver event loop."""
    try:
        loop = uc.loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


class NodriverAdapter:
    """Drop-in replacement for selenium.webdriver.Chrome using Nodriver.

    Exposes the same sync API that linkedin_wrapper.py expects:
      - driver.get(url)
      - driver.execute_script(js, *args)
      - driver.get_cookies()
      - driver.add_cookie(cookie_dict)
      - driver.current_url
      - driver.page_source
      - driver.quit()
      - driver.minimize_window()
    """

    def __init__(self, browser, tab, loop):
        self._browser = browser
        self._tab = tab
        self._loop = loop

    def get(self, url: str):
        """Navigate to a URL."""
        self._loop.run_until_complete(self._tab.get(url))

    def execute_script(self, script: str, *args):
        """Execute JavaScript, compatible with Selenium's execute_script.

        Selenium wraps scripts in function(){...} so 'return' and 'arguments[N]'
        work. We detect async scripts (containing 'await') and use
        'async function' so the await keyword is valid.
        """
        # Serialize args for injection into JS
        args_js = json.dumps(list(args), default=str) if args else "[]"

        # Use async function if script contains await, otherwise sync
        if "await " in script:
            wrapped = f"(async function() {{ {script} }}).apply(null, {args_js})"
        else:
            wrapped = f"(function() {{ {script} }}).apply(null, {args_js})"

        result = self._loop.run_until_complete(
            self._tab.evaluate(wrapped, await_promise=True, return_by_value=True)
        )

        # Nodriver returns RemoteObject wrappers — deserialize to plain Python
        return _deserialize(result)

    def get_cookies(self) -> list:
        """Get all cookies in Selenium-compatible dict format."""
        cdp_cookies = self._loop.run_until_complete(
            self._browser.cookies.get_all()
        )
        result = []
        for c in cdp_cookies:
            cookie = {
                "name": c.name,
                "value": c.value,
                "domain": c.domain,
                "path": c.path,
                "secure": c.secure,
                "httpOnly": c.http_only,
            }
            if c.expires and c.expires > 0:
                cookie["expiry"] = int(c.expires)
            if c.same_site:
                cookie["sameSite"] = c.same_site.value if hasattr(c.same_site, "value") else str(c.same_site)
            result.append(cookie)
        return result

    def add_cookie(self, cookie_dict: dict):
        """Add a cookie in Selenium-compatible dict format."""
        from nodriver.cdp import network

        params = {
            "name": cookie_dict["name"],
            "value": cookie_dict["value"],
            "domain": cookie_dict.get("domain", ".linkedin.com"),
            "path": cookie_dict.get("path", "/"),
        }
        if cookie_dict.get("secure"):
            params["secure"] = True
        if cookie_dict.get("httpOnly"):
            params["http_only"] = True

        cookie_param = network.CookieParam(**params)
        self._loop.run_until_complete(
            self._tab.send(network.set_cookies(cookies=[cookie_param]))
        )

    @property
    def current_url(self) -> str:
        """Get current page URL."""
        target = self._tab.target
        return target.url if target else ""

    @property
    def page_source(self) -> str:
        """Get page HTML source."""
        return self._loop.run_until_complete(self._tab.get_content())

    def quit(self):
        """Close the browser."""
        try:
            self._browser.stop()
        except Exception:
            pass


async def create_browser(headless: bool = True):
    """Create a Nodriver browser and return (browser, tab).

    headless=True:  True headless Chrome (no window at all).
                    Safe with Nodriver because there's no WebDriver fingerprint.
    headless=False: Visible browser window (needed for interactive login).
    """
    browser = await uc.start(headless=headless)
    tab = browser.main_tab
    return browser, tab


def create_driver(headless: bool = True) -> NodriverAdapter:
    """Create a NodriverAdapter (sync entry point).

    Returns a driver object compatible with Selenium's webdriver.Chrome API.
    headless=True for all automated operations, headless=False for login.
    """
    loop = _get_loop()
    browser, tab = loop.run_until_complete(create_browser(headless=headless))
    return NodriverAdapter(browser, tab, loop)
