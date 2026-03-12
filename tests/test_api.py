"""Integration tests for the LinkedIn API wrapper.

All test data is derived from the currently logged-in user.
Run: pytest tests/test_api.py -v
"""

import pytest


# ──────────────────────────────────────────────
# Auth / Session
# ──────────────────────────────────────────────

class TestAuth:
    def test_client_has_browser(self, api):
        assert api.driver is not None

    def test_get_user_profile(self, me):
        assert me, "Profile should not be empty"
        mini = me.get("miniProfile", {})
        assert mini.get("firstName")
        assert mini.get("lastName")
        assert mini.get("publicIdentifier")

    def test_user_profile_caching(self, api):
        p1 = api.get_user_profile()
        p2 = api.get_user_profile(use_cache=True)
        assert p1 is p2


# ──────────────────────────────────────────────
# Profile
# ──────────────────────────────────────────────

class TestProfile:
    def test_get_own_profile(self, api, my_public_id):
        profile = api.get_profile(public_id=my_public_id)
        assert profile
        assert profile.get("firstName")
        assert profile.get("lastName")

    def test_profile_has_headline(self, api, my_public_id):
        profile = api.get_profile(public_id=my_public_id)
        assert profile.get("headline")

    def test_profile_empty_id_returns_empty(self, api):
        assert api.get_profile() == {}

    def test_profile_invalid_id(self, api):
        profile = api.get_profile(public_id="zzz-nonexistent-profile-99999")
        assert profile == {} or not profile.get("firstName")


# ──────────────────────────────────────────────
# Profile Posts
# ──────────────────────────────────────────────

class TestProfilePosts:
    def test_returns_list(self, my_posts):
        assert isinstance(my_posts, list)

    def test_has_posts(self, my_posts):
        assert len(my_posts) > 0, "User should have at least 1 post"

    def test_post_has_urn(self, my_posts):
        assert "urn" in my_posts[0]
        assert "activity" in my_posts[0]["urn"]

    def test_post_has_text(self, my_posts):
        posts_with_text = [p for p in my_posts if p.get("text")]
        assert len(posts_with_text) > 0

    def test_post_has_engagement(self, my_posts):
        assert "reactions" in my_posts[0]
        assert "comments" in my_posts[0]

    def test_post_count_limit(self, api, my_public_id):
        posts = api.get_profile_posts(public_id=my_public_id, post_count=2)
        assert len(posts) <= 2


# ──────────────────────────────────────────────
# Feed
# ──────────────────────────────────────────────

class TestFeed:
    def test_returns_list(self, api):
        posts = api.get_feed_posts(limit=3)
        assert isinstance(posts, list)
        assert len(posts) > 0

    def test_post_structure(self, api):
        posts = api.get_feed_posts(limit=2)
        post = posts[0]
        assert "urn" in post
        assert "author" in post
        assert "reactions" in post
        assert "comments" in post

    def test_post_has_text(self, api):
        posts = api.get_feed_posts(limit=5)
        assert any(p.get("text") for p in posts)

    def test_limit_respected(self, api):
        posts = api.get_feed_posts(limit=2)
        assert len(posts) <= 2


# ──────────────────────────────────────────────
# Comments
# ──────────────────────────────────────────────

class TestComments:
    def test_returns_list(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        comments = api.get_post_comments(post_urn=first_post_urn, comment_count=5)
        assert isinstance(comments, list)

    def test_comment_has_text(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        comments = api.get_post_comments(post_urn=first_post_urn, comment_count=5)
        if not comments:
            pytest.skip("Post has no comments")
        assert any(c.get("text") for c in comments)

    def test_comment_has_profile(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        comments = api.get_post_comments(post_urn=first_post_urn, comment_count=5)
        if not comments:
            pytest.skip("Post has no comments")
        assert any(c.get("profileUrl") for c in comments)

    def test_accepts_activity_id(self, api, first_post_activity_id):
        if not first_post_activity_id:
            pytest.skip("No posts found")
        comments = api.get_post_comments(post_urn=first_post_activity_id, comment_count=3)
        assert isinstance(comments, list)


# ──────────────────────────────────────────────
# Reactions
# ──────────────────────────────────────────────

class TestReactions:
    def test_returns_list(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        reactions = api.get_post_reactions(post_urn=first_post_urn, max_results=5)
        assert isinstance(reactions, list)

    def test_reaction_has_name(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        reactions = api.get_post_reactions(post_urn=first_post_urn, max_results=5)
        if not reactions:
            pytest.skip("Post has no reactions")
        assert any(r.get("name") for r in reactions)

    def test_reaction_has_profile(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        reactions = api.get_post_reactions(post_urn=first_post_urn, max_results=5)
        if not reactions:
            pytest.skip("Post has no reactions")
        assert any(r.get("profileUrl") for r in reactions)

    def test_reaction_has_headline(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        reactions = api.get_post_reactions(post_urn=first_post_urn, max_results=5)
        if not reactions:
            pytest.skip("Post has no reactions")
        assert any(r.get("headline") for r in reactions)


# ──────────────────────────────────────────────
# Profile Views
# ──────────────────────────────────────────────

class TestProfileViews:
    def test_returns_list(self, api):
        views = api.get_current_profile_views()
        assert isinstance(views, list)


# ──────────────────────────────────────────────
# Profile Connections
# ──────────────────────────────────────────────

class TestProfileConnections:
    def test_returns_list(self, api, my_urn_id):
        if not my_urn_id:
            pytest.skip("No URN ID available")
        conns = api.get_profile_connections(urn_id=my_urn_id)
        assert isinstance(conns, list)


# ──────────────────────────────────────────────
# Profile Experiences
# ──────────────────────────────────────────────

class TestProfileExperiences:
    def test_returns_list(self, api, my_urn_id):
        if not my_urn_id:
            pytest.skip("No URN ID available")
        exps = api.get_profile_experiences(urn_id=my_urn_id)
        assert isinstance(exps, list)


# ──────────────────────────────────────────────
# Profile Network
# ──────────────────────────────────────────────

class TestProfileNetwork:
    def test_returns_dict(self, api, my_public_id):
        info = api.get_profile_network_info(public_profile_id=my_public_id)
        assert isinstance(info, dict)


# ──────────────────────────────────────────────
# Messaging (read-only)
# ──────────────────────────────────────────────

class TestMessaging:
    def test_get_conversations(self, api):
        convos = api.get_conversations()
        assert isinstance(convos, list)


# ──────────────────────────────────────────────
# Connections (read-only)
# ──────────────────────────────────────────────

class TestConnections:
    def test_get_invitations(self, api):
        invitations = api.get_invitations(limit=3)
        assert isinstance(invitations, list)


# ──────────────────────────────────────────────
# Search
# ──────────────────────────────────────────────

class TestSearch:
    def test_search_people(self, api):
        results = api.search_people(keywords="software engineer", limit=3)
        assert isinstance(results, list)


# ──────────────────────────────────────────────
# Company
# ──────────────────────────────────────────────

class TestCompany:
    def test_get_company(self, api):
        company = api.get_company(public_id="microsoft")
        assert isinstance(company, dict)


# ──────────────────────────────────────────────
# Jobs
# ──────────────────────────────────────────────

class TestJobs:
    def test_search_jobs(self, api):
        jobs = api.search_jobs(keywords="python", limit=3)
        assert isinstance(jobs, list)
