# System Architecture – Confiaro  
Fully Decentralized, Non-Custodial, Trustless Atomic Conversion Protocol for Bitcoin (BTC) ↔ Monero (XMR)  
Version: Conceptual Reference Design v0.2 – Early 2026  
Status: High-level blueprint (non-operational, no implementation code or production details)

## 1. Executive Summary

Confiaro is a peer-to-peer (P2P) protocol designed to enable atomic cross-chain conversions between Bitcoin (BTC) and Monero (XMR) in both directions, without any form of custody, centralized authority, KYC/AML enforcement, user accounts, or single points of failure/control.

Core characteristics:
- Cryptographically enforced atomicity using adaptor signatures (simulating HTLC-like behavior across chains with asymmetric scripting capabilities).
- Maximum privacy preservation: Monero retains full default unlinkability; Bitcoin exposes only the minimal necessary information.
- Complete user sovereignty: private keys never leave the user's device or wallet.
- Fully decentralized execution: peer discovery, negotiation, orchestration, and settlement happen entirely P2P.
- Direction-aware asymmetry: BTC → XMR is the primary and safer flow (mature since ~2021); XMR → BTC is supported with additional economic and cryptographic mitigations.

This document serves as a comprehensive conceptual blueprint, drawing inspiration from real-world implementations and academic research (COMIT Network's xmr-btc-swap, UnstoppableSwap, Farcaster, BasicSwap DEX, Haveno, and adaptor signature literature).

## 2. Historical Context and Technical Evolution (2013–2026)

### 2.1 Origins of Atomic Swaps (2013–2018)
- 2013: Tier Nolan proposes atomic cross-chain trading using hash time-locked contracts (HTLCs).
- Fundamental limitation: both chains must support hashlocks and conditional timelocks.
- Monero (launched 2014) lacks Turing-incomplete scripting and has no native OP_CHECKLOCKTIMEVERIFY equivalent → standard HTLC impossible.

### 2.2 Breakthroughs Enabling Monero Integration (2019–2020)
- 2019 (36C3 conference): Joël Gugger demonstrates that timelocks are only required on one chain.
- 2020: Academic paper “Bitcoin–Monero Cross-chain Atomic Swap” (ePrint 2020/1126) introduces adaptor signatures combined with asymmetric execution order.
- COMIT Network releases the first mainnet-capable CLI prototype (BTC → XMR direction).

### 2.3 Maturation and Ecosystem Growth (2021–2024)
- 2021–2022: UnstoppableSwap GUI makes the protocol accessible to non-technical users (built around xmr-btc-swap core).
- 2022: BasicSwap DEX integrates adaptor signatures with SMSG gossip protocol and mandatory Tor routing.
- 2023: Farcaster Project explores microservices-based architecture for broader multi-chain atomic swaps.
- Multiple Monero Community Crowdfunding System (CCS) proposals fund improvements: decentralized rendezvous points, improved GUIs, enforced Tor usage, and basic liquidity proofs.

### 2.4 State of the Art in 2026
- BTC → XMR: Multiple production-grade implementations (CLI + GUI), low fees, proven atomicity on mainnet.
- XMR → BTC: Supported in advanced prototypes using extended timeouts, optional collateral bonding, and local reputation scoring.
- Emerging trends: Taproot integration (BIP-341), Schnorr-based adaptors, libp2p gossip overlays, I2P as a Tor alternative.
- Confiaro conceptual goal: consolidate best practices into a unified, modular reference architecture free of any centralized remnants.

## 3. Core Architectural Principles

### 3.1 Strict Separation of Concerns
No single public component has full visibility of the entire flow.
- Public layers: limited to discovery and user interface.
- Private layers: handle orchestration, key management, and blockchain interaction.

### 3.2 Minimal Data Exposure
- Bitcoin side: only required UTXOs + adaptor public keys are revealed.
- Monero side: full ring signatures (minimum ring size 16), stealth addresses, and RingCT confidential transactions (amounts hidden by default).

### 3.3 Ephemeral and Stateless Sessions
- No persistent protocol state.
- Every conversion is an independent, one-off session with no login or tracking.

### 3.4 Asymmetric Execution Windows
- Bitcoin: native timeouts via adaptor signatures (emulating CLTV).
- Monero: no native timelock support → fixed execution order (BTC lock first in the primary flow).

### 3.5 Layered Privacy Design
- Network layer: mandatory Tor/I2P routing, libp2p with onion services.
- On-chain layer: Monero default privacy + Bitcoin minimalism (Taproot aggregation, single-output locks where possible).
- Metadata layer: randomized response delays, per-session ephemeral keys.

### 3.6 Trustlessness and Strict Non-Custodial Nature
- No central escrow.
- Atomicity enforced purely through adaptor signatures and discrete-log equality proofs (when required).

### 3.7 Fault Tolerance and Liveness Guarantees
- Timeouts bound griefing attacks.
- Cooperative abort and partial recovery paths.
- Local retry mechanisms with independent chain verification.

## 4. Architectural Layers (High-Level Breakdown)

### 4.1 Public Interface Layer
Possible implementations:
- CLI tool (Rust-based, similar to xmr-btc-swap CLI).
- Desktop GUI (Tauri + WASM, inspired by UnstoppableSwap).
- Wallet plugins (Monero GUI, Electrum, Sparrow).

Responsibilities:
- Direction and amount selection.
- Live offer browsing (rate, min/max, local reputation hints).
- Address validation (Bech32m for BTC, subaddress/integrated for Monero).
- Step-by-step swap initiation wizard.
- Real-time transaction monitoring (confirmations, status).

### 4.2 Decentralized Discovery & Liquidity Market
Discovery mechanisms:
- Gossip protocol (libp2p pub/sub channels).
- SMSG-style mixnet (as in BasicSwap).
- Community-operated or DHT-based rendezvous points.

Signed offer structure (conceptual):
- Direction (BTC→XMR or XMR→BTC)
- Proposed rate
- Minimum/maximum amount
- Offer expiry
- Adaptor public key
- Liquidity proof (partial PSBT signature or UTXO commitment hash)

Filtering and sorting: performed entirely client-side (avoids centralized curation).

### 4.3 Negotiation & Session Establishment
- End-to-end encrypted channel (ECDH + Noise protocol variant).
- Multi-round price haggling (optional).
- Mutual signed commitment (locks rate and agreed timeouts).

### 4.4 Conversion Orchestrator (Core Local Logic)

#### 4.4.1 Primary Flow: BTC → XMR
1. Taker (wants XMR) accepts offer → generates secret preimage s (32 bytes).
2. Derives adaptor point A = s * G.
3. Sends A to Maker over encrypted channel.
4. Maker computes adaptor pre-signature σ_A (decryptable only with s).
5. Taker constructs and broadcasts BTC lock transaction: adaptor output paying to Maker + refund path via timeout.
6. Waits for configurable BTC confirmations (3–6).
7. Maker monitors chain → broadcasts Monero transaction to Taker's stealth address, revealing s (via metadata or direct channel).
8. Taker verifies XMR receipt → adapts σ_A using s → broadcasts BTC claim transaction.
9. Fallback: BTC timeout expires → Taker publishes refund transaction.

#### 4.4.2 Reverse Flow: XMR → BTC
1. Maker (provides BTC liquidity) locks BTC with adaptor first.
2. Taker sends XMR transaction (no native refund mechanism).
3. Taker provides minimal proof of send (partial view key share or ring membership proof).
4. Maker reveals s → Taker adapts signature and claims BTC.
5. Asymmetry mitigations:
   - Extended BTC timeout window (24–72 hours).
   - Optional collateral bonding (separate BTC output, punishable on non-cooperation).
   - Local reputation decay on abort.
   - Future zero-knowledge proofs of send (research direction).

### 4.5 Blockchain Interaction Layer
Bitcoin side:
- Full node or Electrs instance routed over Tor.
- PSBT-based partial signing workflow.
- Replace-by-fee (RBF) support for dynamic fee adjustment.
- Reorg monitoring with minimum depth checks.

Monero side:
- Local daemon + wallet RPC over Tor.
- Enforced minimum ring size (≥16).
- One-time stealth address generation per swap.
- Minimal, ephemeral view key sharing only when required for proofs.

### 4.6 Local Ledger & Independent Auditability
- Local storage (conceptual SQLite-like): transaction IDs, adaptor proofs, timestamps.
- Independent verification tool: cross-checks both chains for atomicity.
- Exportable proofs suitable for third-party audits.

### 4.7 Local Monitoring, Risk & Reputation Engine
- Peer scoring: success rate, average latency, abort frequency.
- Risk thresholds: automatic abort on suspicious liquidity or behavior patterns.
- Griefing detection: timeout pattern analysis.
- Reputation system: strictly local (sybil-resistant by design).

## 5. Comparison with Existing Projects (2026 Perspective)

| Criterion                 | Confiaro (Conceptual)       | UnstoppableSwap       | BasicSwap DEX         | Farcaster             | Haveno                |
|---------------------------|-----------------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| Custody                   | None                        | None                  | None                  | None                  | None                  |
| Directions Supported      | Both (asymmetric)           | Primarily BTC→XMR     | Both                  | Multi-chain           | XMR-centric           |
| Discovery Mechanism       | P2P gossip/DHT              | Semi-centralized list | SMSG mixnet           | P2P microservices     | Haveno network        |
| Privacy Network           | Mandatory Tor/I2P           | Optional Tor          | Built-in Tor          | Tor/I2P               | Tor                   |
| Primary Interface         | Modular (CLI/GUI/plugins)   | Desktop GUI           | GUI + CLI             | CLI/microservices     | Desktop GUI           |
| Reputation System         | Local scoring               | Provider list         | Local + hints         | Not specified         | Local                 |
| Maturity (2026)           | Reference design            | Production            | Production            | Advanced prototype    | Beta production       |

## 6. Key Trade-offs and Technical Justifications

- Privacy vs Latency: Mandatory Tor/I2P adds delay → offset by randomized timing obfuscation.
- Usability vs Security: Configurable confirmation depths with strong UI warnings.
- Symmetry vs Reality: XMR → BTC asymmetry stems from Monero limitations → mitigated via economic disincentives.
- Extensibility: Modular layers allow future addition of sidechains (Liquid, Elements) or layer-2 (Lightning for BTC).
- Post-Quantum Readiness: Planned migration path to lattice-based adaptor signatures.

## 7. References and Inspirations

- Gugger, J. (2020). Bitcoin–Monero Cross-chain Atomic Swap. IACR ePrint 2020/1126.
- Lindell, Y. (2020–2021). Adaptor Signatures and Their Applications.
- Erwig et al. (2021). Two-Party Adaptor Signatures from Identification Schemes.
- COMIT Network. xmr-btc-swap repository and protocol documentation.
- UnstoppableSwap. Core library and GUI repositories.
- BasicSwap DEX. Whitepaper and SMSG gossip specification.
- Monero Research Lab. RingCT, Dandelion++, black marble attack analysis.
- Bitcoin Improvement Proposals: BIP-340 (Schnorr signatures), BIP-341 (Taproot), BIP-342 (Tapscript).

This architecture document forms the conceptual foundation for Confiaro — prioritizing technical depth, academic rigor, and transparent discussion of inherent cross-chain privacy and decentralization trade-offs.