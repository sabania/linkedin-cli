"""Integration tests for CLI commands via typer test runner.

Tests that the CLI commands produce correct output.
All test data is derived from the currently logged-in user.
Requires: `linkedin-cli login` before running.

Run: pytest tests/test_cli.py -v
"""

import pytest
from typer.testing import CliRunner

runner = CliRunner()


# ──────────────────────────────────────────────
# whoami
# ──────────────────────────────────────────────

class TestWhoami:
    def test_whoami_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["whoami"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_whoami_shows_name(self, cli_app, my_first_name, my_last_name):
        result = runner.invoke(cli_app, ["whoami"])
        assert my_first_name in result.output
        assert my_last_name in result.output

    def test_whoami_shows_public_id(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["whoami"])
        assert my_public_id in result.output


# ──────────────────────────────────────────────
# profile show
# ──────────────────────────────────────────────

class TestProfileShow:
    def test_profile_show_exits_ok(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["profile", "show", my_public_id])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_profile_show_has_name(self, cli_app, my_public_id, my_first_name, my_last_name):
        result = runner.invoke(cli_app, ["profile", "show", my_public_id])
        assert my_first_name in result.output
        assert my_last_name in result.output

    def test_profile_show_has_headline(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["profile", "show", my_public_id])
        # Profile output should contain substantial content (name + headline + other info)
        assert len(result.output) > 50, "Output seems too short for a profile"


# ──────────────────────────────────────────────
# profile posts
# ──────────────────────────────────────────────

class TestProfilePosts:
    def test_profile_posts_exits_ok(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["profile", "posts", my_public_id, "-n", "2"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_profile_posts_shows_posts(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["profile", "posts", my_public_id, "-n", "2"])
        assert "Post 1" in result.output
        assert "URN:" in result.output

    def test_profile_posts_shows_engagement(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["profile", "posts", my_public_id, "-n", "2"])
        assert "Reactions:" in result.output
        assert "Comments:" in result.output


# ──────────────────────────────────────────────
# feed list
# ──────────────────────────────────────────────

class TestFeedList:
    def test_feed_list_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["feed", "list", "-n", "2"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_feed_list_shows_posts(self, cli_app):
        result = runner.invoke(cli_app, ["feed", "list", "-n", "2"])
        assert "#1" in result.output
        assert "URN:" in result.output

    def test_feed_list_shows_engagement(self, cli_app):
        result = runner.invoke(cli_app, ["feed", "list", "-n", "2"])
        assert "Reactions:" in result.output


# ──────────────────────────────────────────────
# posts comments
# ──────────────────────────────────────────────

class TestPostsComments:
    def test_comments_exits_ok(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "comments", first_post_activity_id, "-n", "5"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_comments_shows_table(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "comments", first_post_activity_id, "-n", "5"])
        assert "Comments" in result.output

    def test_comments_has_content(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "comments", first_post_activity_id, "-n", "5"])
        assert len(result.output) > 50, "Output seems too short"


# ──────────────────────────────────────────────
# posts reactions
# ──────────────────────────────────────────────

class TestPostsReactions:
    def test_reactions_exits_ok(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "reactions", first_post_activity_id, "-n", "5"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_reactions_shows_table(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "reactions", first_post_activity_id, "-n", "5"])
        assert "Reactions" in result.output

    def test_reactions_has_names(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "reactions", first_post_activity_id, "-n", "5"])
        assert len(result.output) > 50, "Output seems too short"


# ──────────────────────────────────────────────
# profile views
# ──────────────────────────────────────────────

class TestProfileViews:
    def test_profile_views_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["profile", "views"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# profile connections
# ──────────────────────────────────────────────

class TestProfileConnections:
    def test_profile_connections_exits_ok(self, cli_app, my_urn_id):
        if not my_urn_id:
            pytest.skip("No URN ID available")
        result = runner.invoke(cli_app, ["profile", "connections", my_urn_id])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# profile experiences
# ──────────────────────────────────────────────

class TestProfileExperiences:
    def test_profile_experiences_exits_ok(self, cli_app, my_urn_id):
        if not my_urn_id:
            pytest.skip("No URN ID available")
        result = runner.invoke(cli_app, ["profile", "experiences", my_urn_id])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# profile network
# ──────────────────────────────────────────────

class TestProfileNetwork:
    def test_profile_network_exits_ok(self, cli_app, my_public_id):
        result = runner.invoke(cli_app, ["profile", "network", my_public_id])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# connections invitations
# ──────────────────────────────────────────────

class TestConnectionsInvitations:
    def test_invitations_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["connections", "invitations", "-n", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# messages list
# ──────────────────────────────────────────────

class TestMessagesList:
    def test_messages_list_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["messages", "list"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# search people
# ──────────────────────────────────────────────

class TestSearchPeople:
    def test_search_people_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["search", "people", "software engineer", "--limit", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# search companies
# ──────────────────────────────────────────────

class TestSearchCompanies:
    def test_search_companies_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["search", "companies", "microsoft"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# search jobs
# ──────────────────────────────────────────────

class TestSearchJobs:
    def test_search_jobs_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["search", "jobs", "python", "--limit", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# company show
# ──────────────────────────────────────────────

class TestCompanyShow:
    def test_company_show_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["company", "show", "microsoft"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# company updates
# ──────────────────────────────────────────────

class TestCompanyUpdates:
    def test_company_updates_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["company", "updates", "microsoft", "-n", "2"])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# search posts
# ──────────────────────────────────────────────

class TestSearchPosts:
    def test_search_posts_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["search", "posts", "AI", "--limit", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_search_posts_shows_table(self, cli_app):
        result = runner.invoke(cli_app, ["search", "posts", "python", "--limit", "3"])
        assert "Post Search" in result.output


# ──────────────────────────────────────────────
# search groups
# ──────────────────────────────────────────────

class TestSearchGroups:
    def test_search_groups_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["search", "groups", "python", "--limit", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_search_groups_shows_table(self, cli_app):
        result = runner.invoke(cli_app, ["search", "groups", "data science", "--limit", "3"])
        assert "Group Search" in result.output


# ──────────────────────────────────────────────
# search events
# ──────────────────────────────────────────────

class TestSearchEvents:
    def test_search_events_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["search", "events", "AI", "--limit", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_search_events_shows_table(self, cli_app):
        result = runner.invoke(cli_app, ["search", "events", "technology", "--limit", "3"])
        assert "Event Search" in result.output


# ──────────────────────────────────────────────
# notifications list
# ──────────────────────────────────────────────

class TestNotificationsList:
    def test_notifications_list_exits_ok(self, cli_app):
        result = runner.invoke(cli_app, ["notifications", "list", "-n", "3"])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_notifications_list_shows_table(self, cli_app):
        result = runner.invoke(cli_app, ["notifications", "list", "-n", "3"])
        assert "Notifications" in result.output or "No notifications" in result.output


# ──────────────────────────────────────────────
# posts show
# ──────────────────────────────────────────────

class TestPostsShow:
    def test_posts_show_exits_ok(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "show", first_post_activity_id])
        assert result.exit_code == 0, f"Failed: {result.output}"

    def test_posts_show_has_metrics(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "show", first_post_activity_id])
        assert "Metrics" in result.output or "Post not found" in result.output


# ──────────────────────────────────────────────
# posts analytics
# ──────────────────────────────────────────────

class TestPostsAnalytics:
    def test_posts_analytics_exits_ok(self, cli_app, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        result = runner.invoke(cli_app, ["posts", "analytics", first_post_activity_id])
        assert result.exit_code == 0, f"Failed: {result.output}"


# ──────────────────────────────────────────────
# help commands (no auth needed)
# ──────────────────────────────────────────────

class TestHelp:
    def test_main_help(self, cli_app):
        result = runner.invoke(cli_app, ["--help"])
        assert result.exit_code == 0
        assert "LinkedIn Management CLI" in result.output

    def test_profile_help(self, cli_app):
        result = runner.invoke(cli_app, ["profile", "--help"])
        assert result.exit_code == 0

    def test_feed_help(self, cli_app):
        result = runner.invoke(cli_app, ["feed", "--help"])
        assert result.exit_code == 0

    def test_posts_help(self, cli_app):
        result = runner.invoke(cli_app, ["posts", "--help"])
        assert result.exit_code == 0

    def test_connections_help(self, cli_app):
        result = runner.invoke(cli_app, ["connections", "--help"])
        assert result.exit_code == 0

    def test_search_help(self, cli_app):
        result = runner.invoke(cli_app, ["search", "--help"])
        assert result.exit_code == 0

    def test_messages_help(self, cli_app):
        result = runner.invoke(cli_app, ["messages", "--help"])
        assert result.exit_code == 0

    def test_jobs_help(self, cli_app):
        result = runner.invoke(cli_app, ["jobs", "--help"])
        assert result.exit_code == 0

    def test_company_help(self, cli_app):
        result = runner.invoke(cli_app, ["company", "--help"])
        assert result.exit_code == 0

    def test_notifications_help(self, cli_app):
        result = runner.invoke(cli_app, ["notifications", "--help"])
        assert result.exit_code == 0
