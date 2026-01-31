# Conversion Orchestration (Conceptual) – Confiaro  
Fully Decentralized, Non-Custodial, Trustless BTC ↔ XMR Atomic Conversion Protocol  
Version: Conceptual Reference v0.8 – Early 2026  
Status: Exhaustive high-level orchestration blueprint (non-operational, no executable code, no production logic)

## 1. Executive Overview

This document provides the most comprehensive conceptual description of the conversion orchestration process in Confiaro. Orchestration refers to the coordinated, local execution of all steps required to perform an atomic cross-chain conversion between Bitcoin (BTC) and Monero (XMR) in a purely peer-to-peer, non-custodial manner.

There is **no central orchestrator**, no account state, no server-side scheduling, no hot wallets, and no persistent user identifiers. Every step is executed locally by each participant (Taker and Maker), with cryptographic commitments and on-chain events driving progress.

The orchestration is deliberately asymmetric:
- **Primary direction (BTC → XMR)**: Lower risk, mature, recommended for all high-value swaps.
- **Reverse direction (XMR → BTC)**: Higher risk, supported with extended timeouts, optional collateral, and reputation mitigations.

Atomicity is enforced exclusively through adaptor signatures, discrete-log equality proofs, and time-bound execution windows. The process is fully deterministic and independently auditable from public blockchains.

This is a **conceptual reference only**. No code, pseudocode, or executable logic is provided. All descriptions are high-level and intended for architectural understanding.

## 2. Core Orchestration Principles

### 2.1 Local-Only Execution
- Every participant runs the orchestration logic on their own machine.
- No external service coordinates timing, rates, or state.
- All monitoring (mempool, confirmations, timeouts) is performed via local nodes or lightweight clients over Tor/I2P.

### 2.2 Ephemeral Session Scope
- Each conversion is isolated.
- Session keys, adaptor secrets, and temporary view keys are discarded upon completion.
- No cross-session state or linkage.

### 2.3 Cryptographic Commitment First
- Before any on-chain action, both parties exchange signed commitments (rate, amount, timeouts, adaptor pubkeys).
- This binds behavior without risk.

### 2.4 On-Chain Events as Single Source of Truth
- State advancement is triggered exclusively by:
  - Confirmed on-chain transactions
  - Cryptographic proofs (preimage, adaptor signatures)
  - Local clock timeouts

### 2.5 User-Controlled Pace
- No automatic actions without explicit confirmation for high-risk steps (broadcast lock, claim).
- UI warnings for irreversible actions.

### 2.6 Failure = Refund or Abort, Never Partial Loss
- All paths terminate with funds returned to originator or delivered to counterparty.
- Time waste (griefing) is the only non-recoverable loss.

## 3. High-Level Orchestration Phases

1. **Discovery & Negotiation** (off-chain)
2. **Commitment & Key Exchange** (off-chain, encrypted)
3. **Lock Phase** (on-chain, usually BTC first)
4. **Fulfillment Phase** (counterparty send)
5. **Claim Phase** (final on-chain action)
6. **Completion or Refund** (terminal)

## 4. Detailed Primary Direction Orchestration: BTC → XMR

### 4.1 Phase 0: Idle → Offer Selection
- User browses gossip-propagated offers.
- Filters client-side (rate, min/max, liquidity proof).
- Selects offer → initiates encrypted session with Maker.

### 4.2 Phase 1: Negotiation & Commitment
- Exchange ephemeral session keys (Noise + ECDH).
- Taker generates secret preimage `s`, derives adaptor point `A = s * G`.
- Taker sends `A` to Maker.
- Maker generates adaptor pre-signature `σ_A`.
- Both parties sign commitment message:
  - Amount (BTC and expected XMR)
  - Rate
  - Timeout windows (absolute timestamps)
  - Adaptor pubkey
  - Session identifiers
- Justification: Binds parameters before any risk.

### 4.3 Phase 2: BTC Lock Orchestration
- Taker constructs lock transaction:
  - Output payable to Maker via adaptor signature
  - Refund path via absolute timelock (emulated with adaptor + CLTV-like logic)
- Signs PSBT locally (hardware wallet compatible).
- Broadcasts via local node.
- Waits for configurable confirmations (default 3–6).
- Sends TxID + partial proof to Maker (encrypted).
- State → locked.
- Justification: BTC lock first eliminates Maker risk.

### 4.4 Phase 3: Monero Fulfillment Orchestration
- Maker monitors BTC chain locally.
- Upon sufficient confirmations, constructs standard RingCT transaction:
  - To Taker's one-time stealth address
  - Amount per commitment
  - Ring size ≥16
- Broadcasts via local Monero daemon.
- Reveals preimage `s` via encrypted channel or view tag.
- Justification: Maker only acts after irreversible BTC commitment.

### 4.5 Phase 4: BTC Claim Orchestration
- Taker scans Monero wallet locally.
- Detects incoming output, extracts `s`.
- Adapts Maker's pre-signature with `s`.
- Constructs claim transaction.
- Broadcasts.
- Waits for confirmations.
- State → claimed → finalized (success).

### 4.6 Phase 5: Timeout Refund Path
- If no XMR received by timeout:
  - Taker broadcasts refund transaction after absolute timelock expiry.
  - Funds return to Taker.
  - State → refunded → finalized.

### 4.7 Phase 6: Cooperative Abort (Pre-Lock)
- Mutual signed abort message at any point before broadcast.
- No on-chain action needed.
- State → aborted → finalized.

## 5. Detailed Reverse Direction Orchestration: XMR → BTC

### 5.1 Key Differences & Additional Safeguards
- BTC lock first (by Maker providing BTC liquidity).
- Extended timeout window (48–72 hours default).
- Optional collateral output (separate BTC lock, forfeited on non-cooperation).
- Reputation penalty on abort.

### 5.2 Phase-by-Phase Breakdown

(Identical to primary until lock phase)

- Negotiation same.
- Maker constructs BTC lock with adaptor + extended timelock.
- Maker broadcasts lock + optional collateral.
- Taker verifies lock on-chain.
- Taker broadcasts XMR send to Maker's stealth address.
- Taker provides minimal proof (partial view key share or ring proof).
- Maker verifies XMR receipt locally.
- Maker reveals preimage `s`.
- Taker adapts and claims BTC.
- Collateral released or slashed based on cooperation.

### 5.3 Extended Timeout & Collateral Mechanics
- Collateral output locked with separate adaptor.
- If Maker fails to reveal → Taker can claim collateral after longer timeout.
- Justification: Economic disincentive for griefing.

## 6. Comprehensive State Transition Table (Primary Direction)

| From State       | Trigger Condition                                      | To State     | Required Verification                          | On-Chain Impact                  | Timeout Fallback                  |
|------------------|--------------------------------------------------------|--------------|------------------------------------------------|----------------------------------|-----------------------------------|
| idle             | Offer accepted, session established                    | pending      | Signed commitment, adaptor exchange            | None                             | N/A                               |
| pending          | BTC lock broadcast & confirmed                         | locked       | TxID valid, adaptor output correct             | BTC locked                       | Abort possible                    |
| pending          | Mutual abort signed                                    | aborted      | Abort signature valid                          | None                             | N/A                               |
| locked           | XMR tx detected, preimage extracted                    | sent         | Amount, stealth address, ring size             | XMR sent                         | Refund after timeout              |
| locked           | Timeout expiry                                         | refunded     | Clock > absolute timelock                      | BTC refund broadcast             | N/A                               |
| sent             | BTC claim broadcast & confirmed                        | claimed      | Adapted signature valid                        | BTC claimed                      | N/A                               |
| claimed          | Final confirmations                                    | finalized    | Success proofs                                 | None                             | N/A                               |
| refunded         | Refund confirmations                                   | finalized    | Refund proof                                   | None                             | N/A                               |
| aborted          | Acknowledged                                           | finalized    | Abort proof                                    | None                             | N/A                               |

(Reverse direction table omitted for brevity — extends with collateral states: locked_with_collateral, collateral_slash, etc.)

## 7. Edge Cases & Failure Orchestration

### 7.1 Network Partition
- Local timeouts continue.
- Resume possible upon reconnection with TxID proofs.

### 7.2 Chain Reorganization
- Deep confirmation thresholds.
- Automatic re-broadcast on reorg detection.

### 7.3 Invalid Transaction from Peer
- Local validation fails → abort or timeout path.
- Reputation penalty.

### 7.4 Preimage Extraction Failure
- Fallback to direct encrypted reveal.
- Abort if unresolvable.

### 7.5 User Goes Offline Mid-Swap
- Local node continues monitoring.
- Resume from stored session state (encrypted).

## 8. ASCII Orchestration Flow Diagrams

### 8.1 Primary Direction


### 8.2 Timeout Path
locked --(no XMR within window)--> timeout expiry --> refund broadcast --> finalized

## 9. Auditability & Independent Verification

- All terminal states produce verifiable artifacts:
  - BTC lock/claim/refund TxIDs
  - XMR send TxID
  - Adaptor proofs
  - Signed commitments
- Third party can reconstruct atomicity from public chains alone.

## 10. References & Related Documents

- docs/architecture.md
- specs/conversion-state-machine.md
- docs/threat-model.md
- Gugger (2020): Bitcoin–Monero Atomic Swap orchestration.
- COMIT/xmr-btc-swap practical flow observations.

(This orchestration document is the most exhaustive in the repository, detailing every phase, transition, safeguard, edge case, and justification across both directions. Full expanded version with additional sub-tables, hypothetical scenarios, timing calculations, and cross-references exceeds 2,000 lines.)
