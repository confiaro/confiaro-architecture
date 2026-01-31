# Security Model – Confiaro  
Fully Decentralized, Non-Custodial, Trustless BTC ↔ XMR Atomic Conversion Protocol  
Version: Conceptual Reference v0.4 – Early 2026  
Status: High-level security blueprint (non-operational, no code, no production configurations)

## 1. Guiding Security Principles

Confiaro adopts a rigorous, layered security posture designed for a trustless, privacy-focused cross-chain environment. The following principles govern all design decisions:

### 1.1 Defense in Depth
Multiple independent protection layers are applied at every stage:
- Cryptographic layer: adaptor signatures, ECDH session keys, HMAC message integrity
- Network layer: mandatory Tor/I2P onion routing, randomized timing obfuscation
- Protocol layer: asymmetric timeouts, liquidity proofs, atomicity guarantees
- Local validation layer: independent chain monitoring, receipt verification before claim
- Economic layer: reputation scoring, minimum amounts, collateral bonding (reverse direction)
- User layer: hardware wallet compatibility, explicit warnings, no automatic key exposure

A compromise in one layer does not cascade to others.

### 1.2 Minimal Attack Surface
- No component holds complete context of a swap.
- Public interfaces expose only ephemeral discovery data (signed offers, adaptor pubkeys).
- No hot wallet or long-lived keys are ever present in public-facing code.
- Orchestration and blockchain interaction run locally on user machines.
- No shared state or central ledger exists.

### 1.3 No Hot Wallet Exposure via Public Endpoints
- All private keys remain under user control at all times.
- No daemon, RPC endpoint, or service ever holds spend keys or preimages.
- Adaptor pre-signatures are generated locally and never stored persistently.
- Temporary view key shares (Monero side) are ephemeral and scoped to a single swap.

### 1.4 Rate Limiting and Abuse Detection (Strictly Local / Private)
- All rate limiting, peer scoring, and abuse detection happen client-side.
- No central blacklist or global reputation database.
- Local counters track abort frequency, latency anomalies, liquidity proof failures.
- Automatic temporary peer blacklisting after repeated failures.
- No telemetry sent to any server.

### 1.5 Prioritization: Integrity over Convenience
- Security decisions explicitly sacrifice usability when necessary:
  - Longer default confirmation depths (6 BTC / 10 XMR)
  - Mandatory Tor/I2P (no clearnet fallback)
  - No automatic resumption of failed swaps
  - Explicit user confirmation steps for high-risk directions (XMR → BTC)
  - No "fast mode" shortcuts that weaken atomicity or privacy

## 2. Security Layers in Detail

### 2.1 Cryptographic Security Layer
- Adaptor signatures (ECDSA/Schnorr variants) for conditional claims.
  - Unforgeability under OMDL assumption.
  - Preimage secrecy until legitimate fulfillment.
- Session key establishment: Noise protocol + ECDH over secp256k1.
- Message authentication: HMAC-SHA256 on all P2P messages.
- Hash functions: SHA-256 (BTC commitments), Blake2b/Keccak (cross-chain hashes).
- Monero primitives: RingCT, ring signatures (size ≥16), stealth addresses.
- Future-proofing: migration path to post-quantum lattice-based adaptors.

### 2.2 Network Security Layer
- Mandatory onion routing (Tor v3 or I2P garlic routing).
- No fallback to clearnet (prevents IP leaks even under misconfiguration).
- End-to-end encryption for all negotiation and proof exchange.
- Randomized delays (Gaussian distribution, μ=120–300s) to break timing correlation.
- Ephemeral session identifiers (no persistent peer IDs).

### 2.3 Protocol-Level Security Mechanisms
- Asymmetric execution order: BTC lock first in primary direction.
- Time-bound windows with refund paths (BTC CLTV emulation via adaptors).
- Liquidity proofs: partial PSBT signatures or UTXO commitments before lock.
- Cooperative abort paths: mutual signed abort messages to release resources early.
- Independent receipt verification: Taker scans Monero chain locally before revealing preimage.

### 2.4 Local Validation & Monitoring Layer
- Each participant runs own full/light node (BTC Core / Electrs + Monero daemon).
- Reorg detection: minimum confirmation thresholds enforced locally.
- Fee estimation: dynamic RBF support to avoid stuck transactions.
- Local ledger: transaction IDs, adaptor proofs, timestamps for personal audit.
- Peer scoring engine: success rate, average latency, abort frequency, liquidity reliability.

### 2.5 Economic & Reputation Security Layer
- Minimum swap amounts to deter dust/griefing attacks.
- Local reputation decay on non-cooperative behavior.
- Optional collateral bonding (XMR → BTC direction): separate BTC output slashed on abort.
- No global reputation system (prevents sybil amplification).

### 2.6 User-Facing Security Controls
- Hardware wallet integration (Ledger, Trezor, Coldcard) for BTC PSBT signing.
- Address validation: checksums, format checks, avoid reuse warnings.
- High-risk warnings: prominent UI alerts for XMR → BTC direction.
- Manual confirmation steps: double-check amounts, destinations, timeouts.
- Exportable proofs: allow independent third-party verification of atomicity.

## 3. Security Trade-offs & Justifications

### 3.1 Usability vs Security Trade-offs
- Longer timeouts → higher griefing tolerance but stronger refund guarantees.
- Deep confirmations → increased delay but reduced reorg risk.
- Mandatory Tor/I2P → latency penalty but eliminates IP metadata leaks.
- No automatic recovery → prevents silent failures but requires user awareness.

### 3.2 Privacy vs Performance Trade-offs
- Randomized delays → breaks timing attacks but slows UX.
- Minimal on-chain data (Taproot aggregation) → reduces linkage but increases tx complexity.
- Ephemeral view key sharing → enables proofs but requires careful scoping.

### 3.3 Decentralization vs Resilience Trade-offs
- Pure P2P discovery → no single point of failure but vulnerable to sybil.
- Local reputation only → sybil-resistant but slower trust buildup.

## 4. Security Assumptions

### 4.1 Cryptographic Assumptions
- Discrete Log Problem hardness on secp256k1 and ed25519.
- Adaptor signature soundness (unforgeable under OMDL).
- Collision resistance of SHA-256 / Blake2b.

### 4.2 Network Assumptions
- Tor/I2P provides sufficient anonymity against global passive adversaries.
- No permanent deanonymization of onion services.

### 4.3 Blockchain Assumptions
- BTC and XMR maintain honest-majority consensus.
- Short reorgs possible but not sustained 51% attacks.

### 4.4 Participant Assumptions
- Users follow UI warnings and use secure devices.
- Malicious participants are economically rational (reputation matters).

## 5. Residual Risks & Acceptance Criteria

- Privacy linkage via timing/amount correlation → Residual: Medium (mitigated but not eliminated).
- Griefing in XMR → BTC direction → Residual: Medium (economic disincentives help).
- Sybil attacks on discovery → Residual: Low-Medium (local filtering effective).
- Quantum vulnerability (long-term) → Residual: High (future migration planned).

All residual risks are accepted as inherent to decentralized, cross-chain, privacy-preserving protocols. Users self-assess risk tolerance based on swap value.

## 6. References & Inspirations

- Lindell, Y. (2020). Adaptor Signatures and Applications.
- Erwig et al. (2021). Two-Party Adaptor Signatures.
- Gugger, J. (2020). Bitcoin–Monero Atomic Swap (ePrint 2020/1126).
- Monero Research Lab: RingCT, Dandelion++, timing attack analyses.
- COMIT Network & UnstoppableSwap: practical security observations.
- Bitcoin BIPs 340/341/342: Schnorr & Taproot security enhancements.
- OWASP Threat Modeling Cheat Sheet (adapted for P2P protocols).

This security model emphasizes uncompromising integrity, minimal exposure, and layered protections — prioritizing protocol robustness over user convenience in a trustless environment.