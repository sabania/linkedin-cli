"""Unit tests for messaging participant name resolution.

These run without a browser or a logged-in session: they exercise the pure
parsing helper against the response shapes LinkedIn returns.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from linkedin_wrapper import _participant_name


def _text(value):
    return {"_type": "com.linkedin.pemberly.text.AttributedText", "text": value}


class TestParticipantName:
    def test_member(self):
        participant = {
            "participantType": {
                "member": {"firstName": _text("Ada"), "lastName": _text("Lovelace")}
            }
        }
        assert _participant_name(participant) == "Ada Lovelace"

    def test_member_first_name_only(self):
        participant = {
            "participantType": {"member": {"firstName": _text("Prince"), "lastName": {}}}
        }
        assert _participant_name(participant) == "Prince"

    def test_organization(self):
        participant = {
            "participantType": {
                "member": None,
                "organization": {"name": _text("Example Corp"), "pageType": "COMPANY"},
            }
        }
        assert _participant_name(participant) == "Example Corp"

    def test_custom_sponsored_sender(self):
        participant = {
            "participantType": {
                "member": None,
                "organization": None,
                "custom": {"name": _text("Sponsored Sender")},
            }
        }
        assert _participant_name(participant) == "Sponsored Sender"

    def test_stripped_member_falls_through_to_empty(self):
        """LinkedIn returns empty name objects for conversationParticipants."""
        participant = {
            "participantType": {
                "member": {"firstName": {}, "lastName": {}, "distance": "DISTANCE_1"}
            }
        }
        assert _participant_name(participant) == ""

    def test_member_with_bare_string_names(self):
        """Older responses sometimes carried plain strings instead of AttributedText."""
        participant = {
            "participantType": {"member": {"firstName": "Grace", "lastName": "Hopper"}}
        }
        assert _participant_name(participant) == "Grace Hopper"

    def test_missing_and_malformed_inputs(self):
        assert _participant_name({}) == ""
        assert _participant_name(None) == ""
        assert _participant_name({"participantType": None}) == ""
        assert _participant_name({"participantType": {}}) == ""
        assert _participant_name({"participantType": "nonsense"}) == ""
        assert _participant_name({"participantType": {"member": "nonsense"}}) == ""
