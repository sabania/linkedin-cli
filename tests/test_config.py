"""Tests for CLI config management and rate limiter integration.

These tests are pure unit tests — no browser or LinkedIn session needed.
They use a temp config dir to avoid touching real settings.

Run: pytest tests/test_config.py -v
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Redirect all config I/O to a temp directory."""
    config_file = tmp_path / "cli_config.json"
    daily_file = tmp_path / "daily_calls.json"

    # Patch config module
    monkeypatch.setattr("commands.config.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("commands.config.CONFIG_FILE", config_file)

    # Patch rate limiter
    monkeypatch.setattr("linkedin_wrapper.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("linkedin_wrapper._RateLimiter.DAILY_FILE", daily_file)

    return tmp_path


# ──────────────────────────────────────────────
# Config: get_setting / set_setting
# ──────────────────────────────────────────────

class TestConfigGetSet:
    def test_get_setting_returns_default_when_no_config(self):
        from commands.config import get_setting
        assert get_setting("rate_limits.daily_limit") == 80
        assert get_setting("rate_limits.calls_per_minute") == 15
        assert get_setting("browser.headless") is True

    def test_set_setting_persists_value(self, isolated_config):
        from commands.config import get_setting, set_setting
        set_setting("rate_limits.daily_limit", 200)
        assert get_setting("rate_limits.daily_limit") == 200

    def test_set_setting_creates_nested_dicts(self, isolated_config):
        from commands.config import set_setting, _load_config
        set_setting("rate_limits.calls_per_minute", 25)
        config = _load_config()
        assert config["rate_limits"]["calls_per_minute"] == 25

    def test_set_setting_does_not_clobber_siblings(self, isolated_config):
        from commands.config import get_setting, set_setting
        set_setting("rate_limits.daily_limit", 100)
        set_setting("rate_limits.calls_per_minute", 20)
        assert get_setting("rate_limits.daily_limit") == 100
        assert get_setting("rate_limits.calls_per_minute") == 20

    def test_get_setting_unknown_key_returns_none(self):
        from commands.config import get_setting
        assert get_setting("nonexistent.key") is None

    def test_get_setting_with_explicit_default(self):
        from commands.config import get_setting
        assert get_setting("nonexistent.key", 42) == 42


# ──────────────────────────────────────────────
# Config: save / load roundtrip
# ──────────────────────────────────────────────

class TestConfigPersistence:
    def test_config_file_created_on_set(self, isolated_config):
        from commands.config import set_setting, CONFIG_FILE
        assert not CONFIG_FILE.exists()
        set_setting("browser.headless", False)
        assert CONFIG_FILE.exists()

    def test_config_file_is_valid_json(self, isolated_config):
        from commands.config import set_setting, CONFIG_FILE
        set_setting("rate_limits.daily_limit", 150)
        data = json.loads(CONFIG_FILE.read_text())
        assert data["rate_limits"]["daily_limit"] == 150

    def test_reset_clears_config(self, isolated_config):
        from commands.config import set_setting, get_setting, _save_config
        set_setting("rate_limits.daily_limit", 999)
        _save_config({})
        assert get_setting("rate_limits.daily_limit") == 80  # default


# ──────────────────────────────────────────────
# RateLimiter reads from config
# ──────────────────────────────────────────────

class TestRateLimiterConfig:
    def test_rate_limiter_uses_defaults(self):
        from linkedin_wrapper import _RateLimiter
        rl = _RateLimiter()
        assert rl._calls_per_minute == 15
        assert rl._daily_limit == 80

    def test_rate_limiter_reads_custom_config(self, isolated_config):
        from commands.config import set_setting
        set_setting("rate_limits.daily_limit", 200)
        set_setting("rate_limits.calls_per_minute", 30)

        from linkedin_wrapper import _RateLimiter
        rl = _RateLimiter()
        assert rl._daily_limit == 200
        assert rl._calls_per_minute == 30

    def test_rate_limiter_acquire_increments_count(self, isolated_config):
        from linkedin_wrapper import _RateLimiter
        rl = _RateLimiter()
        assert rl._daily_count == 0
        rl.acquire()
        assert rl._daily_count == 1
        rl.acquire()
        assert rl._daily_count == 2

    def test_rate_limiter_persists_daily_count(self, isolated_config):
        from linkedin_wrapper import _RateLimiter
        rl = _RateLimiter()
        rl.acquire()
        rl.acquire()
        rl.acquire()

        # New instance should load the persisted count
        rl2 = _RateLimiter()
        assert rl2._daily_count == 3

    def test_rate_limiter_daily_limit_raises(self, isolated_config):
        from commands.config import set_setting
        set_setting("rate_limits.daily_limit", 3)

        from linkedin_wrapper import _RateLimiter
        rl = _RateLimiter()
        rl.acquire()
        rl.acquire()
        rl.acquire()
        with pytest.raises(RuntimeError, match="Daily LinkedIn API limit reached"):
            rl.acquire()

    def test_rate_limiter_daily_file_is_valid_json(self, isolated_config):
        from linkedin_wrapper import _RateLimiter
        rl = _RateLimiter()
        rl.acquire()

        data = json.loads(rl.DAILY_FILE.read_text())
        assert "date" in data
        assert "count" in data
        assert data["count"] == 1


# ──────────────────────────────────────────────
# CLI: config commands
# ──────────────────────────────────────────────

class TestConfigCLI:
    @pytest.fixture
    def cli_app(self):
        from main import app
        return app

    def test_config_show_exits_ok(self, cli_app):
        from typer.testing import CliRunner
        result = CliRunner().invoke(cli_app, ["config", "show"])
        assert result.exit_code == 0, f"Failed: {result.output}"
        assert "rate_limits.daily_limit" in result.output
        assert "rate_limits.calls_per_minute" in result.output
        assert "browser.headless" in result.output

    def test_config_set_and_show(self, cli_app):
        from typer.testing import CliRunner
        runner = CliRunner()

        result = runner.invoke(cli_app, ["config", "set", "rate_limits.daily_limit", "150"])
        assert result.exit_code == 0
        assert "150" in result.output

        result = runner.invoke(cli_app, ["config", "show"])
        assert result.exit_code == 0
        assert "150" in result.output

    def test_config_set_invalid_key(self, cli_app):
        from typer.testing import CliRunner
        result = CliRunner().invoke(cli_app, ["config", "set", "fake.key", "123"])
        assert result.exit_code == 1
        assert "Unknown setting" in result.output

    def test_config_set_boolean(self, cli_app):
        from typer.testing import CliRunner
        runner = CliRunner()

        result = runner.invoke(cli_app, ["config", "set", "browser.headless", "false"])
        assert result.exit_code == 0

        from commands.config import get_setting
        assert get_setting("browser.headless") is False

    def test_config_set_invalid_int(self, cli_app):
        from typer.testing import CliRunner
        result = CliRunner().invoke(cli_app, ["config", "set", "rate_limits.daily_limit", "abc"])
        assert result.exit_code == 1
        assert "Expected integer" in result.output

    def test_config_reset(self, cli_app):
        from typer.testing import CliRunner
        runner = CliRunner()

        runner.invoke(cli_app, ["config", "set", "rate_limits.daily_limit", "999"])
        result = runner.invoke(cli_app, ["config", "reset"])
        assert result.exit_code == 0
        assert "reset" in result.output.lower()

        from commands.config import get_setting
        assert get_setting("rate_limits.daily_limit") == 80

    def test_config_help(self, cli_app):
        from typer.testing import CliRunner
        result = CliRunner().invoke(cli_app, ["config", "--help"])
        assert result.exit_code == 0
        assert "show" in result.output
        assert "set" in result.output
        assert "reset" in result.output
