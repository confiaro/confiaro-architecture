# Conversion Lifecycle – Confiaro  
Fully Decentralized, Non-Custodial, Trustless BTC ↔ XMR Atomic Conversion Protocol  
Version: Conceptual Reference v0.7 – Early 2026  
Status: Exhaustive state machine specification (non-operational, no runtime implementation)

## 1. Philosophy of the Lifecycle

Every conversion in Confiaro is a finite, strictly cyclic process. There is no infinite loop, no hidden state, no external oracle that can alter the path. The lifecycle is designed to be:

- **Deterministic**: Given the same inputs and on-chain events, the outcome is always the same.
- **Auditable**: Every transition leaves verifiable on-chain or cryptographic proof.
- **Time-bound**: All paths eventually terminate (success, refund, or cooperative abort).
- **Direction-aware**: The primary flow (BTC → XMR) is symmetric in safety; the reverse flow (XMR → BTC) is deliberately asymmetric with additional safeguards.

The lifecycle is the ultimate enforcer of atomicity: either both parties receive their assets, or neither does, with no partial loss except time (griefing).

## 2. Global State Machine Overview

The conversion lifecycle is modeled as a finite state machine with the following core states:

- **idle** (pre-swap, not shown in UI – implicit)
- **pending** (offer accepted, negotiation complete, waiting for first on-chain action)
- **locked** (BTC locked on-chain – primary direction only)
- **sent** (XMR sent on-chain – fulfillment step)
- **claimed** (final asset claimed)
- **refunded** (timeout triggered, funds returned)
- **aborted** (cooperative or forced abort)
- **failed** (irrecoverable error, usually user-side)
- **finalized** (success or clean refund/abort)

Every state transition is triggered by one of:
- Local user action
- Peer message (encrypted, signed)
- On-chain event (confirmation, timeout)
- Local timeout

No transition is automatic without verification.

### 2.1 State Definitions (Detailed)

**idle**  
- No swap in progress.
- User browsing offers or idle.
- No keys generated, no funds at risk.

**pending**  
- Offer accepted.
- Session keys exchanged.
- Adaptor pubkeys shared.
- Agreed parameters locked (rate, amount, timeouts).
- Waiting for first on-chain action (usually BTC lock in primary direction).
- Funds not yet at risk.
- Transition out: lock broadcast or abort.

**locked** (BTC → XMR primary)  
- BTC lock transaction broadcast and confirmed (configurable depth).
- Funds at risk but protected by timeout refund path.
- Maker monitoring for lock.
- Transition out: XMR send detected or timeout.

**sent**  
- Counterparty asset sent on-chain (XMR in primary, BTC claim in reverse).
- Receipt verified locally.
- Preimage extracted or revealed.
- Ready for final claim.

**claimed**  
- Final transaction broadcast (BTC claim or XMR receipt acknowledged).
- Both parties have assets.
- Transition to finalized (success).

**refunded**  
- Timeout expired.
- Refund transaction broadcast (BTC side).
- Funds returned to originator.
- Transition to finalized (refund).

**aborted**  
- Mutual signed abort message.
- No on-chain action needed if pre-lock.
- Post-lock: cooperative close or timeout fallback.

**failed**  
- Irrecoverable local error (invalid address, key loss, node sync failure).
- User must manually recover (if possible).
- No automatic fund loss — only stalled state.

**finalized**  
- Terminal state (success, refund, or clean abort).
- Local ledger updated.
- Session keys discarded.
- Ready for new swap.

## 3. Primary Flow State Machine: BTC → XMR (Lower-Risk Direction)

This is the recommended direction due to Bitcoin's native timelock capabilities.

### 3.1 Detailed States & Transitions

| Current State | Trigger | Next State | Conditions | On-Chain Action | Proof Generated |
|---------------|---------|------------|------------|-----------------|-----------------|
| idle          | User accepts offer | pending | Session keys exchanged, parameters signed | None | Session commitment |
| pending       | Taker broadcasts BTC lock | locked | PSBT signed, broadcast success | BTC lock tx | TxID + adaptor proof |
| pending       | Abort message | aborted | Mutual signed abort | None | Abort signature |
| locked        | Maker broadcasts XMR send | sent | Local wallet detects incoming XMR, preimage extracted | XMR tx | Receipt proof + preimage |
| locked        | Timeout expires | refunded | CLTV-like timeout reached | BTC refund tx | Refund TxID |
| sent          | Taker broadcasts BTC claim | claimed | Adaptor signature adapted with preimage | BTC claim tx | Final TxID |
| claimed       | Confirmations reached | finalized (success) | Default 3 confs on claim | None | Success proof |
| refunded      | Confirmations reached | finalized (refund) | Default 3 confs | None | Refund proof |
| aborted       | Mutual acknowledgment | finalized (abort) | None | None | Abort proof |

### 3.2 Transition Justifications (Expanded)

**idle → pending**  
- Requires explicit user confirmation.
- Generates ephemeral key pair.
- Signs commitment message with rate, amount, timeouts, adaptor pubkey.
- Justification: Prevents accidental swaps; binds both parties early without risk.

**pending → locked**  
- Taker constructs PSBT with adaptor output + timeout refund.
- Local node broadcasts.
- Waits for configurable confirmations (default 3–6).
- Justification: BTC lock first ensures Maker has no risk until funds committed.

**locked → sent**  
- Maker monitors mempool/chain via local node.
- Upon detection, broadcasts standard Monero RingCT tx to Taker stealth address.
- Preimage revealed in encrypted channel or via view tag.
- Justification: Atomic link — Maker only sends after seeing lock.

**sent → claimed**  
- Taker adapts pre-signature with extracted preimage.
- Broadcasts claim tx.
- Justification: Preimage revelation enables claim; once on-chain, atomicity complete.

**Any state → aborted (pre-lock)**  
- Mutual signed message.
- No on-chain footprint.
- Justification: Early exit without cost.

**locked → refunded**  
- Asymmetric timeout (BTC longer than expected XMR confs).
- Taker broadcasts refund after expiry.
- Justification: Protects Taker from non-fulfillment.

### 3.3 Failure Modes in Primary Flow

- Node offline during lock confirmation → local retry, resume from TxID.
- Invalid XMR tx → Maker retry or abort.
- Reorg undoing lock → deep confs + monitoring.
- Preimage not extractable → protocol fallback to channel reveal.

## 4. Reverse Flow State Machine: XMR → BTC (Higher-Risk Direction)

Asymmetric due to Monero's lack of timelocks.

### 4.1 Detailed States & Transitions

| Current State | Trigger | Next State | Conditions | On-Chain Action | Proof Generated |
|---------------|---------|------------|------------|-----------------|-----------------|
| idle          | User accepts offer | pending | Same as primary | None | Same |
| pending       | Maker broadcasts BTC lock (with collateral) | locked | Extended timeout | BTC lock + collateral | TxIDs |
| locked        | Taker broadcasts XMR send | sent | Maker verifies tx | XMR tx | Receipt proof |
| sent          | Maker reveals preimage | claimed | After verification | BTC claim possible | Preimage |
| claimed       | Taker broadcasts claim | finalized (success) | None | BTC claim tx | Final proof |
| locked        | Extended timeout | refunded | Collateral slashed if non-coop | BTC refund | Refund proof |

### 4.2 Additional Mitigations for Asymmetry

- Extended BTC timeout (48–72 hours default).
- Optional collateral output (separate BTC lock, forfeited on non-reveal).
- Reputation penalty on abort.
- Cooperative reveal encouragement.
- Future: ZK proof of XMR send without view key share.

### 4.3 Failure Modes in Reverse Flow

- Taker griefing (send XMR, never claim) → Maker waits timeout, keeps XMR.
- Maker non-reveal → collateral slash or reputation loss.
- Invalid proof → abort before reveal.

## 5. ASCII Diagrams

### 5.1 Primary Flow Diagram
