"""
Monero Interface (Conceptual)

Describes conceptual interaction with a Monero wallet
for swap coordination.

No wallet RPC or key handling is implemented.
"""


class MoneroInterface:
    """
    Conceptual interface for Monero-side operations.
    """

    def lock_funds(self):
        """
        Describes conceptual fund locking.
        """
        pass

    def release_funds(self):
        """
        Describes conceptual fund release.
        """
        pass
