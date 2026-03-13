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

    def test_search_people_has_degree(self, api):
        results = api.search_people(keywords="software", limit=3)
        if results:
            assert "connection_degree" in results[0]

    def test_search_people_network_filter(self, api):
        results = api.search_people(keywords="", network_depths=["F"], limit=3)
        assert isinstance(results, list)

    def test_search_posts(self, api):
        results = api.search_posts(keywords="AI", limit=3)
        assert isinstance(results, list)

    def test_search_posts_has_content(self, api):
        results = api.search_posts(keywords="python", limit=3)
        if results:
            assert any(p.get("text") or p.get("activity_id") for p in results)

    def test_search_posts_has_posted_at(self, api):
        results = api.search_posts(keywords="AI", limit=3)
        if results:
            assert any(p.get("posted_at") for p in results)

    def test_search_groups(self, api):
        results = api.search_groups(keywords="python", limit=3)
        assert isinstance(results, list)

    def test_search_groups_has_name(self, api):
        results = api.search_groups(keywords="data science", limit=3)
        if results:
            assert any(g.get("name") for g in results)

    def test_search_events(self, api):
        results = api.search_events(keywords="AI", limit=3)
        assert isinstance(results, list)


# ──────────────────────────────────────────────
# Notifications
# ──────────────────────────────────────────────

class TestNotifications:
    def test_returns_list(self, api):
        result = api.get_notifications(limit=3)
        assert isinstance(result, list)

    def test_notification_has_headline(self, api):
        result = api.get_notifications(limit=5)
        if result:
            assert any(n.get("headline") for n in result)

    def test_notification_has_enriched_fields(self, api):
        result = api.get_notifications(limit=3)
        if result:
            assert "notification_urn" in result[0]
            assert "actor_name" in result[0]


# ──────────────────────────────────────────────
# Post Details
# ──────────────────────────────────────────────

class TestPostDetails:
    def test_get_post(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        post = api.get_post(post_urn=first_post_urn)
        assert isinstance(post, dict)

    def test_post_has_fields(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        post = api.get_post(post_urn=first_post_urn)
        if post:
            assert "author" in post
            assert "reactions" in post

    def test_get_post_analytics(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        result = api.get_post_analytics(post_urn=first_post_urn)
        assert isinstance(result, dict)


# ──────────────────────────────────────────────
# Company
# ──────────────────────────────────────────────

class TestCompany:
    def test_get_company(self, api):
        company = api.get_company(public_id="microsoft")
        assert isinstance(company, dict)

    def test_get_company_updates(self, api):
        updates = api.get_company_updates(public_id="microsoft", limit=2)
        assert isinstance(updates, list)


# ──────────────────────────────────────────────
# Jobs
# ──────────────────────────────────────────────

class TestJobs:
    def test_search_jobs(self, api):
        jobs = api.search_jobs(keywords="python", limit=3)
        assert isinstance(jobs, list)


# ──────────────────────────────────────────────
# Data Enrichment
# ──────────────────────────────────────────────

class TestPostedAt:
    def test_profile_posts_have_posted_at(self, my_posts):
        assert "posted_at" in my_posts[0]
        assert my_posts[0]["posted_at"]

    def test_profile_posts_have_post_url(self, my_posts):
        assert "post_url" in my_posts[0]
        assert "linkedin.com" in my_posts[0]["post_url"]

    def test_profile_posts_have_shares(self, my_posts):
        assert "shares" in my_posts[0]

    def test_feed_posts_have_posted_at(self, api):
        posts = api.get_feed_posts(limit=2)
        if posts:
            assert posts[0].get("posted_at")

    def test_feed_posts_have_author_profile_id(self, api):
        posts = api.get_feed_posts(limit=3)
        assert any(p.get("author_profile_id") for p in posts)

    def test_feed_posts_have_shares(self, api):
        posts = api.get_feed_posts(limit=2)
        if posts:
            assert "shares" in posts[0]

    def test_snowflake_decode(self):
        from linkedin_wrapper import _urn_to_timestamp
        ts = _urn_to_timestamp("7435982583777169408")
        assert ts
        assert "20" in ts  # year should be 20XX


class TestInvitationNormalization:
    def test_invitations_have_name(self, api):
        invs = api.get_invitations(limit=3)
        if invs:
            assert "name" in invs[0]
            assert "headline" in invs[0]

    def test_invitations_have_shared_secret(self, api):
        invs = api.get_invitations(limit=3)
        if invs:
            assert "shared_secret" in invs[0]
            assert "entity_urn" in invs[0]


# ──────────────────────────────────────────────
# Post Engagers
# ──────────────────────────────────────────────

class TestPostEngagers:
    def test_returns_list(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        result = api.get_post_engagers(post_urn=first_post_urn, limit=5)
        assert isinstance(result, list)

    def test_has_interaction_type(self, api, first_post_urn):
        if not first_post_urn:
            pytest.skip("No posts found")
        result = api.get_post_engagers(post_urn=first_post_urn, limit=5)
        if result:
            assert result[0].get("interaction_type") in ("reaction", "comment", "both")


# ──────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────

class TestSignals:
    def test_returns_dict(self, api, first_post_urn):
        urns = [first_post_urn] if first_post_urn else []
        result = api.get_signals(recent_post_urns=urns, limit=2)
        assert isinstance(result, dict)
        assert "profile_views" in result
        assert "post_engagers" in result
        assert "invitations" in result
        assert "notifications" in result
