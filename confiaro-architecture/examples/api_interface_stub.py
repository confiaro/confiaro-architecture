"""
Public API Interface Stub

This file documents the public-facing API surface.
No backend logic is implemented here.
"""

class PublicAPI:
    def start_conversion(self, payload: dict) -> dict:
        return {"status": "accepted"}

    def get_status(self, account_id: str) -> dict:
        return {"active": True}
