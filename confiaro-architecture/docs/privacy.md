# Privacy Model – Confiaro  
Fully Decentralized, Non-Custodial, Trustless BTC ↔ XMR Atomic Conversion Protocol  
Version: Conceptual Reference v0.5 – Early 2026  
Status: Comprehensive high-level privacy blueprint (non-operational, no telemetry, no logging mechanisms described)

## 1. Core Philosophy: Privacy as the Foundation

Privacy is not a feature — it is the foundation.

Every design decision in Confiaro is evaluated first and foremost through the lens of privacy preservation. Usability, performance, and liquidity are secondary considerations that are only accepted when they do not introduce identifiable metadata, correlation vectors, or linkage risks.

The protocol is engineered to ensure that no entity — not the developers, not liquidity providers, not network observers, and not chain analysis firms — can reliably link a user's real-world identity to their transaction history, swap patterns, or on-chain activities.

## 2. Fundamental Privacy Principles (Expanded)

Confiaro strictly adheres to the following principles, with no exceptions or optional modes that weaken them.

### 2.1 No Personal Data Storage
- Absolutely no collection, processing, or storage of any personally identifiable information (PII).
- No usernames, email addresses, phone numbers, biometric data, or government IDs.
- No wallet addresses are stored beyond the duration of a single ephemeral swap session.
- No local history is shared or synchronized across devices.
- No backup or cloud sync features that could expose transaction metadata.
- Even optional debug logs are stored only locally and never transmitted.
- Principle justification: Any persistent data creates a target for subpoenas, breaches, or accidental leaks.

### 2.2 No IP Correlation
- All network communication is forced through anonymity networks (Tor v3 onion services primary, I2P garlic routing secondary).
- No clearnet connections are permitted under any circumstances — the software refuses to function without a valid anonymity layer.
- No DNS lookups that could leak intent (all rendezvous points use hardcoded or DHT-resolved onion addresses).
- Circuit rotation follows Tor best practices (new circuit per session, guard node persistence disabled for maximum churn).
- No fallback to proxies or VPNs that could introduce trusted third parties.
- Randomized padding traffic is injected to normalize packet sizes and resist volume analysis.
- Principle justification: IP addresses are one of the strongest real-world identity correlators in cryptocurrency usage.

### 2.3 No Behavioral Profiling
- No tracking of swap frequency, preferred rates, typical amounts, or direction preferences.
- No client-side analytics that could build a local profile (even anonymized).
- Offer browsing is performed without sending queries to centralized servers — all discovery is gossip-based or DHT.
- No recommendation engines or "suggested peers" that could fingerprint user preferences.
- Randomized response ordering and delay patterns prevent inference of user intent from interaction timing.
- No machine learning or heuristic models that could infer user behavior from local data.
- Principle justification: Behavioral patterns are increasingly used by chain analysis firms to de-anonymize users even when direct metadata is absent.

### 2.4 No Account Recovery Mechanisms
- No seed phrase backup prompts that encourage cloud storage.
- No social recovery, multi-sig recovery, or trusted contacts.
- No support tickets or helpdesk that would require identity disclosure for "recovery assistance".
- Loss of private keys results in permanent loss of access — this is explicitly communicated as a feature, not a bug.
- No "emergency access" or developer backdoors.
- Principle justification: Recovery mechanisms are the primary vector for identity linkage in most wallet applications.

### 2.5 No External Analytics or Telemetry
- Zero telemetry of any kind — no crash reports, usage statistics, or error logging sent to any endpoint.
- No integration with third-party services (Sentry, Google Analytics, Mixpanel, etc.).
- No optional "send diagnostics" feature — telemetry is structurally impossible.
- Verbose logging is local-only and requires manual user activation with a clear privacy warning.
- No update server that phones home with device identifiers.
- Principle justification: Even anonymized telemetry has been shown to enable re-identification attacks at scale.

### 2.6 All Conversions Executed Without Linking Identity to Transaction History
- Each swap is a completely isolated, stateless event.
- No cross-swap identifiers (no persistent adaptor keys, no chained preimages).
- No session tokens or cookies.
- On-chain footprints are minimized and obfuscated (detailed below).
- Principle justification: The ultimate goal is to ensure that even a global adversary with full blockchain access cannot link a user's swaps to their identity.

## 3. Privacy by Layer (Detailed Breakdown)

### 3.1 Network-Layer Privacy
- Mandatory Tor/I2P routing for all P2P traffic.
- End-to-end encryption (Noise protocol + ECDH) on top of onion routing.
- Ephemeral session keys — new key pair per negotiation.
- Randomized circuit lifetimes and stream isolation.
- Cover traffic generation to mask real negotiation packets.
- No direct peer connections — all traffic through anonymity network.

### 3.2 Discovery-Layer Privacy
- Gossip protocol and DHT use only ephemeral identifiers.
- Offers are signed but not linked to persistent identities.
- No centralized order book or relay server that could log queries.
- Client-side filtering — no feedback to the network about which offers were viewed or accepted.

### 3.3 Negotiation-Layer Privacy
- All messages encrypted end-to-end.
- No plaintext metadata (amounts, rates) visible on the wire.
- Randomized message ordering and delays to prevent timing-based inference.
- No persistent channel IDs.

### 3.4 On-Chain Privacy (Monero Side)
- Full RingCT: amounts completely confidential.
- Ring signatures with minimum size 16 (configurable higher).
- One-time stealth addresses generated per swap.
- No address reuse across swaps.
- View tags for efficient scanning without exposing full view key.

### 3.5 On-Chain Privacy (Bitcoin Side)
- Taproot (BIP-341) key-path spends to hide script complexity.
- Single-output lock transactions where possible (no change address leakage).
- Encouraged pre-swap CoinJoin or collaborative transactions.
- Variable amount selection to avoid round-number heuristics.
- Adaptor preimage revelation minimized and obfuscated.

### 3.6 Cross-Chain Privacy (Linkage Prevention)
- No forced amount equivalence between BTC lock and XMR send.
- Timing decoupling via mandatory randomized delays (120–600 seconds configurable).
- Adaptor preimage shared only via encrypted channel (never on-chain in identifiable way).
- No shared identifiers or deterministic derivations between chains.

### 3.7 Metadata & Off-Chain Privacy
- No local storage of peer onion addresses beyond session.
- No logging of negotiation details by default.
- Exportable proofs are anonymized (no timestamps or peer info).

## 4. Privacy Threat Analysis & Mitigations

### 4.1 Timing Correlation Threats
- Threat: Observer correlates BTC lock time with XMR send time.
- Mitigation: Enforced Gaussian delays + variable confirmation waiting.
- Residual risk: Low-Medium (global adversary may attempt statistical correlation).

### 4.2 Amount Correlation Threats
- Threat: Approximate amount matching across chains.
- Mitigation: No protocol-enforced amount parity + user guidance on variable amounts.
- Residual risk: Low (Monero amounts hidden entirely).

### 4.3 Traffic Analysis Threats
- Threat: Packet size/volume reveals negotiation phase.
- Mitigation: Constant padding + cover traffic.
- Residual risk: Low (Tor/I2P resistant to known attacks).

### 4.4 Sybil & Honeypot Threats
- Threat: Malicious peers offer swaps to collect metadata.
- Mitigation: Local reputation + liquidity proofs + no persistent identifiers.
- Residual risk: Medium (sophisticated actors possible).

### 4.5 Chain Analysis Threats (BTC Side)
- Threat: Clustering via common-input or change heuristics.
- Mitigation: Taproot + pre-mix guidance + single-output design.
- Residual risk: Medium (inherent to transparent ledger).

## 5. Privacy Trade-offs & Justifications

- Latency vs Unlinkability: Tor/I2P adds seconds to minutes — accepted.
- Discovery Speed vs Metadata Leakage: Pure gossip/DHT is slower than centralized relays — accepted.
- Proof Efficiency vs Minimal Revelation: Partial view key shares are tightly scoped — ZK alternatives planned.
- Liquidity vs Profiling Risk: No global order book — accepted for privacy.

## 6. Privacy Assumptions

- Tor/I2P networks remain robust against nation-state traffic analysis.
- Monero ring selection and decoy sampling resist statistical de-anonymization.
- Users follow best practices (no address reuse, variable amounts, secure devices).
- No catastrophic ECC breaks or Tor compromise in the near term.

## 7. Residual Privacy Risks Summary

- Cross-chain timing/volume correlation → Medium
- Bitcoin clustering heuristics → Medium
- User-induced leaks (misconfiguration, reuse) → Medium-High
- Malicious peer tracing → Low-Medium

These risks are inherent to any protocol bridging a transparent (BTC) and private (XMR) chain and are minimized to the greatest extent possible without sacrificing decentralization.

## 8. References & Inspirations

- Monero Research Lab papers: RingCT security, decoy selection analysis, Dandelion++.
- van Saberhagen (2013): CryptoNote v2.0 (Monero privacy foundation).
- Tor Project documentation: Onion service v3 specification, traffic obfuscation.
- Bitcoin BIPs 340/341/342: Schnorr and Taproot privacy properties.
- BasicSwap DEX: Metadata minimization in SMSG gossip.
- UnstoppableSwap & COMIT: Practical cross-chain privacy observations.

Confiaro embodies the cypherpunk ethos: privacy by design, privacy by default, and privacy without compromise.