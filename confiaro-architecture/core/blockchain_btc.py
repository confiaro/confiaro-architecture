"""
Bitcoin Interface (Conceptual)

Describes how a local Bitcoin wallet or node
would conceptually interact with the conversion protocol.

No RPC calls are implemented.
"""


class BitcoinInterface:
    """
    Conceptual interface for Bitcoin operations.
    """

    def create_psbt(self):
        """
        Describes PSBT creation for swap locking.
        """
        pass

    def sign_transaction(self):
        """
        Describes local signing behavior.
        """
        pass
