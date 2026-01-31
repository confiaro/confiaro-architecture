# Confiaro Core — Local Execution Engine (Conceptual Reference)

> **Status:** Conceptual / Reference Design  
> **Scope:** Architecture, lifecycle, and cryptographic primitives (non-operational)  
> **Model:** Open architecture, closed execution core  
> **Custody:** Non-custodial  
> **Topology:** Peer-to-peer (no central server)

---

## Abstract

This document defines the **conceptual core architecture** of the Confiaro protocol,
a privacy-first BTC ⇄ XMR conversion system designed for **local execution**, **deterministic
state transitions**, and **non-custodial guarantees**.

This repository **does not include production code**. It provides a **reference design**
describing how a compliant implementation *would* behave, without exposing execution
details, secrets, or operational infrastructure.

---

## Design Objectives

- **Local-first execution:** All critical operations are executed on the participant’s device.
- **Non-custodial guarantees:** Private keys never leave the wallet context.
- **No central coordinator:** No servers, no order books, no custodial escrows.
- **Deterministic lifecycle:** Explicit states and transitions with verifiable outcomes.
- **Privacy by default:** Encrypted P2P transport, onion routing compatibility.
- **Failure safety:** Explicit refund and timeout paths.

---

## Non-Goals

- Providing runnable conversion logic
- Exposing wallet or RPC integrations
- Publishing cryptographic secrets
- Offering a hosted service or backend
- Acting as a liquidity provider

---

## Terminology

- **Participant:** A local node controlled by a user.
- **Session:** A single conversion lifecycle instance.
- **Peer:** A counterparty participating in a session.
- **State Machine:** Deterministic model governing transitions.
- **Adaptor Signature:** Cryptographic primitive enforcing atomicity.
- **Refund Path:** Deterministic failure resolution.

---

## Architectural Overview

The Confiaro core is modeled as a **local orchestration engine** composed of independent
conceptual modules. Each module has a **single responsibility** and **explicit interfaces**.

### Core Modules

- `orchestrator`: Session coordination and lifecycle control
- `state_machine`: Deterministic state transitions
- `p2p_client`: Encrypted peer communication (conceptual)
- `blockchain_btc`: Bitcoin-side interaction model (abstract)
- `blockchain_xmr`: Monero-side interaction model (abstract)
- `crypto_adaptor`: Atomicity primitives (conceptual)

Each module is intentionally **interface-only** in this repository.

---

## Execution Model

### Local Execution

All actions are assumed to execute **locally**:

- Key material remains inside wallet boundaries
- Signing occurs in user-controlled contexts
- No remote procedure calls are assumed
- No shared databases exist

### Peer-to-Peer Coordination

Peers communicate via an abstract P2P layer with the following properties:

- End-to-end encryption
- Onion routing compatibility (Tor / I2P)
- No metadata amplification
- Session-scoped channels

---

## Trust Model

The protocol assumes:

- **No trusted third parties**
- **No trusted servers**
- **No trusted price oracles**
- **No trusted liquidity sources**

Atomicity is enforced cryptographically, not institutionally.

---

## Threat Model (High-Level)

### Out of Scope Attacks

- Physical compromise of the user’s device
- Malicious wallet software
- OS-level key exfiltration

### In Scope Mitigations

- Counterparty aborts
- Network partition
- Timing manipulation
- Replay attempts
- Partial execution failures

Each threat is addressed through **state transitions** and **refund determinism**.

---

## Conversion Lifecycle (Conceptual)

1. **Initialization**
2. **Parameter Negotiation**
3. **Locking Phase**
4. **Execution Phase**
5. **Finalization**
6. **Completion or Refund**

No step proceeds without explicit preconditions.

---

## Deterministic State Machine

States are **explicit**, **ordered**, and **terminally resolvable**.

### Canonical States

- `initialized`
- `negotiating`
- `locked`
- `executing`
- `completed`
- `failed`
- `refunded`

Transitions are **monotonic** and **non-reversible**.

---

## Failure Handling

Failures are not exceptional; they are **first-class outcomes**.

Failure scenarios include:

- Peer disconnect
- Timeout expiration
- Invalid message sequence
- Cryptographic verification failure

Each scenario maps to a **deterministic refund path**.

---

## Refund Semantics

Refunds are:

- Time-locked
- Unilateral
- Deterministic
- Non-interactive after timeout

Refund logic is described conceptually and not implemented here.

---

## Cryptographic Primitives (Conceptual)

### Adaptor Signatures

Adaptor signatures enable atomicity by binding the revelation of a secret
on one chain to the spend condition on another.

This repository **does not implement** adaptor signatures.

### Time Locks

Time locks enforce bounded execution windows and guarantee refunds.

---

## Bitcoin Interaction Model (Abstract)

Bitcoin-side interaction assumes:

- PSBT-based workflows
- Local signing
- No remote broadcasting assumed
- Explicit refund transactions

No wallet APIs are included.

---

## Monero Interaction Model (Abstract)

Monero-side interaction assumes:

- View key isolation
- Stealth address semantics
- RingCT privacy guarantees
- Local wallet context

No RPC bindings are included.

---

## Privacy Considerations

The protocol is designed to minimize:

- Metadata leakage
- Timing correlation
- Amount linkage
- Network fingerprinting

Privacy is a **system property**, not a feature toggle.

---

## Auditability

Although execution is private, **state transitions are auditable locally**.

Audit logs (conceptual) include:

- State changes
- Timeout triggers
- Verification outcomes

No global logs exist.

---

## Extensibility

The architecture allows:

- Multiple transport backends
- Alternative cryptographic primitives
- Different timeout strategies
- Wallet-agnostic integrations

All extensions must preserve non-custodial guarantees.

---

## Compliance Posture

Confiaro does not:

- Collect personal data
- Perform identity verification
- Store user profiles
- Track behavioral analytics

Compliance is achieved through **non-custodial design**, not surveillance.

---

## Implementation Notes

This document is intentionally **verbose and explicit** to avoid ambiguity.

Any real-world implementation must:

- Independently validate all cryptographic assumptions
- Undergo professional security review
- Respect local regulations

---

## Disclaimer

This document is provided **for educational and architectural transparency purposes only**.
It does not constitute financial advice, legal advice, or an operational system.

---

## References (Partial)

- Atomic Cross-Chain Swaps
- Adaptor Signatures (Lindell)
- Bitcoin PSBT (BIP 174)
- Monero RingCT
- Libp2p Specifications
- Threat Modeling for P2P Systems

---

*End of Part 1.*
