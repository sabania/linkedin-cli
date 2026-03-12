"""LinkedIn API wrapper using Selenium to bypass bot detection.

LinkedIn actively detects non-browser HTTP clients (PerimeterX/HUMAN Security)
and invalidates cookies. Using Selenium with a real Chrome instance ensures
all fingerprinting checks pass.
"""

import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CONFIG_DIR = Path.home() / ".linkedin-cli"
VOYAGER_API = "https://www.linkedin.com/voyager/api"


class LinkedinClient:
    """LinkedIn client using Selenium for all API calls."""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self._me_cache = None

    def _api_get(self, endpoint: str) -> dict:
        """Execute a Voyager API GET request via the browser."""
        url = f"{VOYAGER_API}{endpoint}"

        # Use JavaScript fetch() inside the real browser
        script = """
        const resp = await fetch(arguments[0], {
            headers: {
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
            },
            credentials: 'include',
        });
        return {status: resp.status, body: await resp.json()};
        """
        result = self.driver.execute_script(f"return (async () => {{ {script} }})()", url)

        if result["status"] != 200:
            return {}
        return result["body"]

    def get_user_profile(self, use_cache=True) -> dict:
        if self._me_cache and use_cache:
            return self._me_cache
        self._me_cache = self._api_get("/me")
        return self._me_cache

    def get_profile(self, public_id=None, urn_id=None) -> dict:
        identifier = public_id or urn_id
        if not identifier:
            return {}
        # Base profile data (name, headline, summary, etc.)
        data = self._api_get(
            f"/identity/dash/profiles?q=memberIdentity&memberIdentity={identifier}"
        )
        elements = data.get("elements", [])
        if not elements:
            return {}
        raw = elements[0]
        # Supplementary data (follower count, connection count)
        sup = self._api_get(
            f"/identity/dash/profiles?q=memberIdentity&memberIdentity={identifier}"
            f"&decorationId=com.linkedin.voyager.dash.deco.identity.profile.TopCardSupplementary-126"
        )
        sup_elements = sup.get("elements", [])
        if sup_elements:
            raw["followingState"] = sup_elements[0].get("followingState")
            raw["connections"] = sup_elements[0].get("connections")
        return _normalize_profile(raw)

    def get_profile_contact_info(self, public_id=None, urn_id=None) -> dict:
        identifier = public_id or urn_id
        if not identifier:
            return {}
        # Use dash profile which has the actual contact fields
        data = self._api_get(
            f"/identity/dash/profiles?q=memberIdentity&memberIdentity={identifier}"
        )
        elements = data.get("elements", [])
        if not elements:
            return {}
        p = elements[0]
        email_obj = p.get("emailAddress", {})
        website_obj = p.get("creatorWebsite", {})
        website_url = ""
        if website_obj:
            for attr in website_obj.get("attributesV2", []):
                href = attr.get("detailDataUnion", {}).get("hyperlink", "")
                if href:
                    website_url = href
                    break
        return {
            "email_address": email_obj.get("emailAddress", "") if isinstance(email_obj, dict) else "",
            "phone_numbers": [],
            "twitter": p.get("twitterHandles", []),
            "websites": [website_url] if website_url else [],
        }

    def get_profile_skills(self, public_id=None, urn_id=None) -> list:
        identifier = public_id or urn_id
        if not identifier:
            return []
        # Scrape skills from the profile skills section
        self.driver.get(f"https://www.linkedin.com/in/{identifier}/details/skills/")
        time.sleep(3)
        script = """
        var skills = [];
        document.querySelectorAll('[data-field="skill_page_skill_topic"]').forEach(el => {
            var name = el.querySelector('span[aria-hidden="true"]');
            if (name) skills.push({name: name.innerText.trim()});
        });
        if (!skills.length) {
            document.querySelectorAll('.artdeco-list__item').forEach(el => {
                var span = el.querySelector('span[aria-hidden="true"]');
                if (span && span.innerText.trim().length > 1) {
                    skills.push({name: span.innerText.trim()});
                }
            });
        }
        return skills;
        """
        return self.driver.execute_script(script) or []

    def get_profile_posts(self, public_id=None, urn_id=None, post_count=10) -> list:
        """Get posts from a profile by scraping the activity page."""
        identifier = public_id or urn_id
        if not identifier:
            return []

        self.driver.get(f"https://www.linkedin.com/in/{identifier}/recent-activity/all/")
        time.sleep(4)

        # Scroll to load more posts
        for _ in range(max(1, post_count // 5)):
            self.driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(1)

        script = (
            "var posts = [];"
            "var els = document.querySelectorAll('[data-urn]');"
            "els.forEach(function(el) {"
            "  var urn = el.getAttribute('data-urn');"
            "  if (!urn || urn.indexOf('activity') === -1) return;"
            "  var text = '';"
            "  var spans = el.querySelectorAll('span[dir]');"
            "  for (var i = 0; i < spans.length; i++) {"
            "    var t = spans[i].innerText || '';"
            "    if (t.length > text.length && t.length > 20) text = t;"
            "  }"
            "  var rxBtn = el.querySelector('button[data-reaction-details]');"
            "  var rxText = rxBtn ? rxBtn.innerText.trim() : '';"
            "  var rxMatch = rxText.match(/(\\d[\\d.,]*)/);"
            "  var rxCount = rxMatch ? rxMatch[1] : (rxBtn ? '1' : '0');"
            "  var cmLi = el.querySelector('li.social-details-social-counts__comments');"
            "  var cmBtn = cmLi ? cmLi.querySelector('button') : null;"
            "  var cmText = cmBtn ? cmBtn.innerText.trim() : '';"
            "  var cmMatch = cmText.match(/(\\d[\\d.,]*)/);"
            "  var cmCount = cmMatch ? cmMatch[1] : '0';"
            "  posts.push({urn: urn, text: text.substring(0, 500), reactions: rxCount, comments: cmCount});"
            "});"
            "return posts;"
        )
        posts = self.driver.execute_script(script) or []
        return posts[:post_count]

    def get_feed_posts(self, limit=10, offset=0, exclude_promoted_posts=True) -> list:
        """Get feed posts by scraping the rendered feed page."""
        self.driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)

        # Scroll to load more posts
        for _ in range(max(1, limit // 5)):
            self.driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(1)

        # Extract posts from DOM
        script = """
        const posts = [];
        document.querySelectorAll('[data-urn]').forEach(el => {
            const urn = el.getAttribute('data-urn');
            if (!urn || !urn.includes('activity')) return;

            // Find post text - longest span with dir=ltr that's not the author name
            let text = '';
            el.querySelectorAll('span[dir="ltr"], .break-words span').forEach(span => {
                const t = span.innerText || '';
                if (t.length > text.length && t.length > 30) text = t;
            });

            // Author: first short span in actor area
            const authorEl = el.querySelector('.update-components-actor__name span span, .feed-shared-actor__name span');
            const author = authorEl ? authorEl.innerText.trim().split('\\n')[0] : '';

            // Reactions count - from button innerText (first number)
            const rxBtn = el.querySelector('button[data-reaction-details]');
            const rxText = rxBtn ? rxBtn.innerText.trim() : '';
            const rxMatch = rxText.match(/(\\d[\\d.,]*)/);
            const reactions = rxMatch ? rxMatch[1] : (rxBtn ? '1' : '0');

            // Comments count - from the comments list item button
            const cmLi = el.querySelector('li.social-details-social-counts__comments');
            const cmBtn = cmLi ? cmLi.querySelector('button') : null;
            const cmText = cmBtn ? cmBtn.innerText.trim() : '';
            const cmMatch = cmText.match(/(\\d[\\d.,]*)/);
            const comments = cmMatch ? cmMatch[1] : '0';

            posts.push({
                urn: urn,
                text: text.substring(0, 500),
                author: author,
                reactions: reactions,
                comments: comments,
            });
        });
        return posts;
        """
        posts = self.driver.execute_script(script) or []
        return posts[:limit]

    def get_post_comments(self, post_urn: str, comment_count=100) -> list:
        """Get comments on a post by loading the post page."""
        # Extract activity ID from URN
        activity_id = post_urn.split(":")[-1]
        self.driver.get(f"https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}/")
        time.sleep(4)

        # Click "load more comments" buttons
        for _ in range(3):
            try:
                self.driver.execute_script(
                    "var btn = document.querySelector('[class*=\"show-prev\"], button[class*=\"comments-comments-list__load-more\"]');"
                    "if (btn) btn.click();"
                )
                time.sleep(1)
            except Exception:
                break

        script = (
            "var comments = [];"
            "var els = document.querySelectorAll('[class*=\"comments-comment-item\"], [class*=\"comment-item\"]');"
            "els.forEach(function(el) {"
            "  var textEl = el.querySelector('[class*=\"comment-item__main-content\"] span[dir], [class*=\"comment__text\"] span[dir]');"
            "  if (!textEl) { var spans = el.querySelectorAll('span[dir]'); for (var i=0;i<spans.length;i++) { if (spans[i].innerText.length > 20) { textEl = spans[i]; break; } } }"
            "  var link = el.querySelector('a[href*=\"/in/\"]');"
            "  var nameEl = link ? link.querySelector('span') : null;"
            "  comments.push({"
            "    author: nameEl ? nameEl.innerText.trim().split('\\n')[0] : '',"
            "    text: textEl ? textEl.innerText.trim().substring(0, 500) : '',"
            "    profileUrl: link ? link.getAttribute('href') : '',"
            "    profileId: link ? link.getAttribute('href').split('/in/')[1].replace('/','') : ''"
            "  });"
            "});"
            "return comments;"
        )
        comments = self.driver.execute_script(script) or []
        # Filter out empty/duplicate entries
        seen = set()
        unique = []
        for c in comments:
            key = c.get("text", "")[:50]
            if key and key not in seen:
                seen.add(key)
                unique.append(c)
        unique = unique[:comment_count]

        # Resolve URN-based profile IDs to public identifiers
        urns = [c["profileId"] for c in unique if c.get("profileId")]
        if urns:
            resolved = self._resolve_public_ids(urns)
            for c in unique:
                c["profileId"] = resolved.get(c.get("profileId", ""), c.get("profileId", ""))
                if c["profileId"] and not c["profileUrl"].endswith(c["profileId"]):
                    c["profileUrl"] = f"https://www.linkedin.com/in/{c['profileId']}"

        return unique

    def get_post_reactions(self, post_urn: str, max_results=None, results=None) -> list:
        """Get reactions on a post by clicking the reactions count."""
        activity_id = post_urn.split(":")[-1]
        self.driver.get(f"https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}/")
        time.sleep(3)

        # Click reactions button to open modal (language-independent selector)
        self.driver.execute_script(
            "var btn = document.querySelector('button[data-reaction-details]');"
            "if (btn) btn.click();"
        )
        time.sleep(3)

        # Scroll inside modal to load more
        count = max_results or 50
        for _ in range(count // 10):
            self.driver.execute_script(
                "var modal = document.querySelector('.artdeco-modal__content');"
                "if (modal) modal.scrollTop = modal.scrollHeight;"
            )
            time.sleep(1)

        script = (
            "var reactions = [];"
            "var els = document.querySelectorAll('.social-details-reactors-tab-body-list-item');"
            "els.forEach(function(el) {"
            "  var link = el.querySelector('a[href*=\"/in/\"]');"
            "  var lockup = el.querySelector('.artdeco-entity-lockup');"
            "  var titleEl = lockup ? lockup.querySelector('.artdeco-entity-lockup__title') : null;"
            "  var subtitleEl = lockup ? lockup.querySelector('.artdeco-entity-lockup__subtitle, .artdeco-entity-lockup__caption, p') : null;"
            "  var name = titleEl ? titleEl.innerText.trim().split('\\n')[0] : '';"
            "  reactions.push({"
            "    name: name,"
            "    profileUrl: link ? link.getAttribute('href') : '',"
            "    profileId: link ? link.getAttribute('href').split('/in/')[1].replace('/','') : '',"
            "    headline: subtitleEl ? subtitleEl.innerText.trim().substring(0, 100) : ''"
            "  });"
            "});"
            "return reactions;"
        )
        reactions = self.driver.execute_script(script) or []
        reactions = reactions[:count]

        # Resolve URN-based profile IDs to public identifiers (parallel)
        urns = [r["profileId"] for r in reactions if r.get("profileId")]
        if urns:
            resolved = self._resolve_public_ids(urns)
            for r in reactions:
                r["profileId"] = resolved.get(r.get("profileId", ""), r.get("profileId", ""))
                if r["profileId"] and not r["profileUrl"].endswith(r["profileId"]):
                    r["profileUrl"] = f"https://www.linkedin.com/in/{r['profileId']}"

        return reactions

    def _extract_search_results(self, data: dict) -> list:
        """Extract entity results from search cluster response."""
        results = []
        for cluster in data.get("elements", []):
            for item in cluster.get("items", []):
                entity = (
                    item.get("itemUnion", {}).get("entityResult")
                    or item.get("item", {}).get("entityResult")
                    or {}
                )
                if not entity:
                    continue
                title = entity.get("title", {}).get("text", "")
                subtitle = entity.get("primarySubtitle", {}).get("text", "")
                secondary = entity.get("secondarySubtitle", {}).get("text", "") if entity.get("secondarySubtitle") else ""
                nav_url = entity.get("navigationUrl", "")
                urn = entity.get("entityUrn", "")
                public_id = nav_url.split("/in/")[-1].split("?")[0].rstrip("/") if "/in/" in nav_url else ""
                results.append({
                    "name": title,
                    "headline": subtitle,
                    "location": secondary,
                    "public_id": public_id,
                    "urn_id": urn,
                    "url": nav_url.split("?")[0] if nav_url else "",
                })
        return results

    def _resolve_public_ids(self, urns: list) -> dict:
        """Resolve a list of URN-based member IDs to public profile IDs in parallel."""
        script = """
        const urns = arguments[0];
        const csrf = document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '';
        const results = await Promise.all(urns.map(async (urn) => {
            try {
                const resp = await fetch(
                    'https://www.linkedin.com/voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity=' + urn,
                    { headers: {'X-RestLi-Protocol-Version':'2.0.0','csrf-token':csrf}, credentials:'include' }
                );
                if (resp.status !== 200) return {urn, publicId: urn};
                const data = await resp.json();
                const el = data.elements && data.elements[0];
                return {urn, publicId: (el && el.publicIdentifier) || urn};
            } catch(e) { return {urn, publicId: urn}; }
        }));
        return results;
        """
        resolved = self.driver.execute_script(
            f"return (async () => {{ {script} }})()", urns
        ) or []
        return {r["urn"]: r["publicId"] for r in resolved}

    def get_current_profile_views(self) -> list:
        """Get list of people who viewed your profile."""
        data = self._api_get("/identity/wvmpCards")
        return data.get("elements", [])

    def get_profile_connections(self, urn_id: str) -> list:
        """Get connections of a profile."""
        data = self._api_get(
            f"/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175"
            f"&origin=MEMBER_PROFILE_CANNED_SEARCH&q=all"
            f"&query=(flagshipSearchIntent:SEARCH_SRP,queryParameters:"
            f"(resultType:List(PEOPLE),network:List(F),connectionOf:List({urn_id})))"
        )
        results = []
        for cluster in data.get("elements", []):
            for item in cluster.get("items", []):
                entity = (
                    item.get("itemUnion", {}).get("entityResult")
                    or item.get("item", {}).get("entityResult")
                    or {}
                )
                if not entity:
                    continue
                title = entity.get("title", {}).get("text", "")
                subtitle = entity.get("primarySubtitle", {}).get("text", "")
                nav_url = entity.get("navigationUrl", "")
                public_id = nav_url.split("/in/")[-1].split("?")[0].rstrip("/") if "/in/" in nav_url else ""
                results.append({
                    "firstName": title.split(" ")[0] if title else "",
                    "lastName": " ".join(title.split(" ")[1:]) if title else "",
                    "headline": subtitle,
                    "public_id": public_id,
                })
        return results

    def get_profile_experiences(self, urn_id: str) -> list:
        """Get work experiences of a profile by scraping the experience section."""
        self.driver.get(f"https://www.linkedin.com/in/{urn_id}/details/experience/")
        time.sleep(4)
        for i in range(8):
            self.driver.execute_script(f"window.scrollTo(0, {(i + 1) * 600})")
            time.sleep(0.3)
        time.sleep(1)
        script = r'''
        var exps = [];
        var navItems = ['Start', 'Ihr Netzwerk', 'Jobs', 'Nachrichten',
                        'Mitteilungen', 'Sie', 'Produkte', 'Marketing',
                        'Home', 'My Network', 'Messaging', 'Notifications', 'Me'];
        var lis = document.querySelectorAll('li');
        for (var i = 0; i < lis.length; i++) {
            var li = lis[i];
            var text = li.innerText.trim();
            if (text.indexOf('\n') === -1 || text.length < 15) continue;
            var lines = text.split('\n').filter(function(l) {
                return l.trim().length > 0;
            }).map(function(l) { return l.trim(); });
            if (navItems.indexOf(lines[0]) >= 0) continue;
            if (lines.length < 2) continue;
            var title = lines[0] || '';
            var period = lines[1] || '';
            var location = lines.length > 2 ? lines[2] : '';
            // Get company from grandparent container
            var company = '';
            var gp = li.parentElement ? li.parentElement.parentElement : null;
            if (gp) {
                var gpLines = gp.innerText.trim().split('\n').filter(function(l) {
                    return l.trim().length > 0;
                }).map(function(l) { return l.trim(); });
                if (gpLines.length > 0 && gpLines[0] !== title) {
                    company = gpLines[0];
                }
            }
            exps.push({title: title, companyName: company, timePeriod: period, location: location});
        }
        return exps;
        '''
        return self.driver.execute_script(script) or []

    def get_profile_network_info(self, public_profile_id: str) -> dict:
        """Get network info (follower count, connection count)."""
        data = self._api_get(
            f"/identity/profiles/{public_profile_id}/networkinfo"
        )
        return data

    def get_conversations(self) -> list:
        """Get conversations by scraping the messaging page."""
        self.driver.get("https://www.linkedin.com/messaging/")
        time.sleep(4)
        script = r'''
        var convos = [];
        var items = document.querySelectorAll('.msg-conversation-listitem');
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var text = item.innerText.trim();
            var lines = text.split('\n').filter(function(l) { return l.trim().length > 0; }).map(function(l) { return l.trim(); });
            var name = '';
            var date = '';
            var lastMessage = '';
            for (var j = 0; j < lines.length; j++) {
                var line = lines[j];
                if (line.startsWith('Status:')) continue;
                if (!name) { name = line; continue; }
                if (!date && (line.match(/\d/) || line.indexOf('.') > 0)) { date = line; continue; }
                if (date === line) continue;
                if (!lastMessage && line.length > 5) { lastMessage = line; break; }
            }
            if (name) {
                convos.push({participants: name, lastMessage: lastMessage, date: date});
            }
        }
        return convos;
        '''
        return self.driver.execute_script(script) or []

    def get_conversation(self, conversation_urn_id: str) -> dict:
        data = self._api_get(f"/messaging/conversations/{conversation_urn_id}/events")
        return data

    def send_message(self, message_body: str, conversation_urn_id=None, recipients=None):
        # Messages require POST - use fetch in browser
        if conversation_urn_id:
            url = f"{VOYAGER_API}/messaging/conversations/{conversation_urn_id}/events"
        else:
            url = f"{VOYAGER_API}/messaging/conversations"

        payload = {"eventCreate": {"value": {"com.linkedin.voyager.messaging.create.MessageCreate": {"body": message_body}}}}
        if recipients:
            payload["recipients"] = recipients

        script = """
        const resp = await fetch(arguments[0], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
            },
            credentials: 'include',
            body: JSON.stringify(arguments[1]),
        });
        return {status: resp.status};
        """
        return self.driver.execute_script(
            f"return (async () => {{ {script} }})()", url, payload
        )

    def mark_conversation_as_seen(self, conversation_urn_id: str):
        """Mark a conversation as seen."""
        url = f"{VOYAGER_API}/messaging/conversations/{conversation_urn_id}"
        script = """
        const resp = await fetch(arguments[0], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
                'X-HTTP-Method-Override': 'PATCH',
            },
            credentials: 'include',
            body: JSON.stringify({patch: {$set: {read: true}}}),
        });
        return {status: resp.status};
        """
        return self.driver.execute_script(
            f"return (async () => {{ {script} }})()", url
        )

    def get_invitations(self, start=0, limit=10) -> list:
        data = self._api_get(f"/relationships/invitationViews?start={start}&count={limit}")
        return data.get("elements", [])

    def add_connection(self, profile_public_id: str, message="", profile_urn=None):
        url = f"{VOYAGER_API}/growth/normInvitations"
        payload = {
            "invitee": {
                "com.linkedin.voyager.growth.invitation.InviteeProfile": {
                    "profileId": profile_public_id
                }
            }
        }
        if message:
            payload["message"] = message

        script = """
        const resp = await fetch(arguments[0], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
            },
            credentials: 'include',
            body: JSON.stringify(arguments[1]),
        });
        return {status: resp.status};
        """
        return self.driver.execute_script(
            f"return (async () => {{ {script} }})()", url, payload
        )

    def remove_connection(self, public_profile_id: str):
        """Remove a connection."""
        url = f"{VOYAGER_API}/identity/profiles/{public_profile_id}/profileActions?action=disconnect"
        script = """
        const resp = await fetch(arguments[0], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
            },
            credentials: 'include',
        });
        return {status: resp.status};
        """
        return self.driver.execute_script(
            f"return (async () => {{ {script} }})()", url
        )

    def reply_invitation(self, invitation_entity_urn: str, invitation_shared_secret: str, action: str = "accept"):
        """Accept or reject an invitation."""
        url = f"{VOYAGER_API}/relationships/invitations/{invitation_entity_urn}?action={action}"
        payload = {"invitationSharedSecret": invitation_shared_secret}
        script = """
        const resp = await fetch(arguments[0], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
            },
            credentials: 'include',
            body: JSON.stringify(arguments[1]),
        });
        return {status: resp.status};
        """
        return self.driver.execute_script(
            f"return (async () => {{ {script} }})()", url, payload
        )

    def search_people(self, keywords=None, limit=20, **kwargs) -> list:
        kw = keywords or ""
        data = self._api_get(
            f"/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175"
            f"&origin=GLOBAL_SEARCH_HEADER&q=all&count={limit}"
            f"&query=(keywords:{kw},flagshipSearchIntent:SEARCH_SRP"
            f",queryParameters:(resultType:List(PEOPLE)))"
        )
        return self._extract_search_results(data)

    def get_company(self, public_id) -> dict:
        data = self._api_get(f"/organization/companies?q=universalName&universalName={public_id}")
        elements = data.get("elements", [])
        return elements[0] if elements else {}

    def get_company_updates(self, public_id=None, urn_id=None, max_results=10, results=None) -> list:
        identifier = public_id or urn_id
        data = self._api_get(
            f"/feed/updates?q=companyRelevanceFeed&moduleKey=member-share"
            f"&count={max_results}&companyUniversalName={identifier}"
        )
        return data.get("elements", [])

    def follow_company(self, following_state_urn: str, following: bool = True):
        """Follow or unfollow a company."""
        url = f"{VOYAGER_API}/feed/follows"
        payload = {"urn": following_state_urn, "following": following}
        script = """
        const resp = await fetch(arguments[0], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-RestLi-Protocol-Version': '2.0.0',
                'csrf-token': document.cookie.match(/JSESSIONID="?([^";]+)/)?.[1] || '',
            },
            credentials: 'include',
            body: JSON.stringify(arguments[1]),
        });
        return {status: resp.status};
        """
        return self.driver.execute_script(
            f"return (async () => {{ {script} }})()", url, payload
        )

    def unfollow_entity(self, urn_id: str):
        """Unfollow an entity by URN."""
        return self.follow_company(following_state_urn=urn_id, following=False)

    def get_job(self, job_id: str) -> dict:
        data = self._api_get(f"/jobs/jobPostings/{job_id}")
        # Scrape company name from job page if not resolved
        company_details = data.get("companyDetails", {})
        if isinstance(company_details, dict):
            inner = company_details.get("com.linkedin.voyager.jobs.JobPostingCompany", company_details)
            if not inner.get("companyResolutionResult"):
                try:
                    self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}/")
                    time.sleep(3)
                    name = self.driver.execute_script(
                        r'''var links = document.querySelectorAll('a[href*="/company/"]');
                        for (var i = 0; i < links.length; i++) {
                            var t = links[i].innerText.trim().split('\n')[0].trim();
                            if (t) return t;
                        }
                        return '';'''
                    )
                    if name:
                        inner["companyResolutionResult"] = {"name": name}
                except Exception:
                    pass
        return data

    def get_job_skills(self, job_id: str) -> dict:
        """Get skills required for a job."""
        return self._api_get(f"/jobs/jobPostings/{job_id}/skillMatchStatuses")

    def search_companies(self, keywords=None) -> list:
        kw = keywords[0] if isinstance(keywords, list) else (keywords or "")
        if not kw:
            return []
        data = self._api_get(
            f"/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175"
            f"&origin=SWITCH_SEARCH_VERTICAL&q=all"
            f"&query=(keywords:{kw},flagshipSearchIntent:SEARCH_SRP"
            f",queryParameters:(resultType:List(COMPANIES)))"
        )
        return self._extract_search_results(data)

    def search_jobs(self, keywords=None, limit=20, **kwargs) -> list:
        """Search jobs by scraping the LinkedIn jobs search page."""
        from urllib.parse import quote
        kw = quote(keywords or "")
        location = quote(kwargs.get("location_name", ""))
        url = f"https://www.linkedin.com/jobs/search/?keywords={kw}"
        if location:
            url += f"&location={location}"
        self.driver.get(url)
        time.sleep(4)
        # Scroll to load more results
        for i in range(5):
            self.driver.execute_script(f"window.scrollTo(0, {(i + 1) * 800})")
            time.sleep(0.3)
        time.sleep(1)
        script = r'''
        var results = [];
        var seen = {};
        var cards = document.querySelectorAll('[data-job-id], .job-card-container, .scaffold-layout__list-item');
        for (var i = 0; i < cards.length; i++) {
            var card = cards[i];
            var jobId = card.getAttribute('data-job-id') || '';
            if (!jobId || seen[jobId]) continue;
            seen[jobId] = true;
            var titleEl = card.querySelector('.job-card-list__title, .artdeco-entity-lockup__title, a[class*="job-card"]');
            var companyEl = card.querySelector('.job-card-container__primary-description, .artdeco-entity-lockup__subtitle');
            var locationEl = card.querySelector('.job-card-container__metadata-item, .artdeco-entity-lockup__caption');
            results.push({
                name: titleEl ? titleEl.innerText.trim().split('\n')[0] : '',
                headline: companyEl ? companyEl.innerText.trim() : '',
                location: locationEl ? locationEl.innerText.trim() : '',
                urn_id: 'urn:li:jobPosting:' + jobId
            });
        }
        return results;
        '''
        results = self.driver.execute_script(script) or []
        return results[:limit]

    def quit(self):
        """Close the browser and clean up temp profile."""
        try:
            self.driver.quit()
        except Exception:
            pass
        temp = getattr(self, "_temp_profile", None)
        if temp and Path(str(temp)).exists():
            import shutil
            shutil.rmtree(temp, ignore_errors=True)


def _normalize_profile(raw: dict) -> dict:
    """Normalize dash profile response to standard format."""
    first = ""
    last = ""

    multi_first = raw.get("multiLocaleFirstName", {})
    if multi_first:
        first = next(iter(multi_first.values()), "")

    multi_last = raw.get("multiLocaleLastName", {})
    if multi_last:
        last = next(iter(multi_last.values()), "")

    headline = ""
    multi_headline = raw.get("multiLocaleHeadline", {})
    if multi_headline:
        headline = next(iter(multi_headline.values()), "")

    # Location from geoLocation or location fields
    location = raw.get("geoLocationName", "")
    if not location:
        loc = raw.get("location", {})
        geo = raw.get("geoLocation", {})
        parts = [loc.get("city", ""), geo.get("postalCode", ""), loc.get("countryCode", "").upper()]
        location = ", ".join(p for p in parts if p)

    # Follower count from followingState (with TopCard decoration)
    following_state = raw.get("followingState") or {}
    follower_count = following_state.get("followerCount", "")

    # Connection count from connections paging
    connections = raw.get("connections") or {}
    paging = connections.get("paging", {})
    connection_count = paging.get("total", "")

    # Summary from multiLocale or plain
    summary = ""
    multi_summary = raw.get("multiLocaleSummary", {})
    if multi_summary:
        summary = next(iter(multi_summary.values()), "")
    if not summary:
        summary = raw.get("summary", "")

    return {
        "firstName": first or raw.get("firstName", ""),
        "lastName": last or raw.get("lastName", ""),
        "headline": headline,
        "locationName": location,
        "industryName": raw.get("industryName", ""),
        "summary": summary,
        "followerCount": follower_count,
        "connectionCount": connection_count,
        "entityUrn": raw.get("entityUrn", ""),
        "objectUrn": raw.get("objectUrn", ""),
        "publicIdentifier": raw.get("publicIdentifier", ""),
        "_raw": raw,
    }
