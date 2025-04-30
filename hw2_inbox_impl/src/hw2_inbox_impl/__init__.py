"""Implementation module."""

import hw2_inbox_api

from . import gmail_client

# Type ignore is needed because we're intentionally modifying the API module
hw2_inbox_api.connect = lambda: gmail_client.GmailClient().connect()  # type: ignore[attr-defined]

__all__ = ["GmailClient", "gmail_client"]
