"""
State Machine (Conceptual)

Defines the conceptual states and transitions involved
in a BTC ⇄ XMR conversion lifecycle.

This is a reference-only state model.
"""


class ConversionStateMachine:
    """
    Conceptual finite state machine for conversion sessions.
    """

    STATES = [
        "initialized",
        "negotiating",
        "locked",
        "executing",
        "completed",
        "failed",
        "refunded"
    ]

    def current_state(self):
        """
        Returns the current conceptual state.

        No persistence or execution logic is implemented.
        """
        pass

    def transition_to(self, next_state: str):
        """
        Describes a state transition.

        In a real implementation, transitions would be strictly validated.
        """
        pass
