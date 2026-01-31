# Threat Model – Confiaro  
Fully Decentralized, Non-Custodial, Trustless Atomic Conversion Protocol for BTC ↔ XMR  
Version: Conceptual Reference v0.3 – Early 2026  
Status: Comprehensive high-level threat analysis (non-operational, no implementation-specific bugs or CVEs)

## 1. Introduction and Scope

### 1.1 Purpose of This Document
This threat model provides a systematic, exhaustive analysis of potential security and privacy threats to Confiaro — a peer-to-peer protocol for atomic swaps between Bitcoin (BTC) and Monero (XMR).  
It serves as a foundational reference for developers, auditors, users, and researchers to understand assumptions, adversary capabilities, attack vectors, mitigations, and residual risks in a fully decentralized, non-custodial system.

### 1.2 Assets Protected
- **Primary Assets**  
  - BTC UTXOs locked during swaps  
  - XMR outputs sent during fulfillment  
- **Secondary Assets**  
  - Privacy of transaction graph (unlinkability between BTC and XMR activities)  
  - User identity metadata (IP, timing patterns, session correlations)  
  - Protocol availability (resistance to griefing and DoS)  
  - Atomicity integrity (guarantee that swaps are all-or-nothing)  
- **Tertiary Assets**  
  - Local reputation scores (if implemented)  
  - Adaptor signature secrets and preimages  

### 1.3 Out-of-Scope Threats (Explicitly Not Mitigated by Protocol)
- Compromise of user endpoint (malware, keyloggers, phishing of private keys)  
- Gross user misconfiguration (sending funds to wrong address, disabling Tor)  
- Catastrophic blockchain attacks (51% hashpower takeover on BTC or XMR)  
- Advanced persistent threats targeting individual users (nation-state level)  
- Quantum computing attacks breaking ECC (migration path planned for future)  
- Legal/regulatory coercion (protocol provides no built-in compliance hooks)  

### 1.4 Threat Modeling Framework
- **STRIDE per component** (adapted for cross-chain P2P)  
- **Adversary profiling** (capability tiers)  
- **Risk scoring**: Likelihood × Impact matrix  
  - Likelihood: Rare (<1%), Low (1–10%), Medium (10–40%), High (>40%)  
  - Impact: Negligible, Low, Medium, High, Critical  
- **Residual risk acceptance criteria**: Medium or lower after mitigations (user bears some risk in decentralized design)

## 2. Adversary Models (Detailed Profiles)

### 2.1 Computational Adversary (Tier 1 – Cryptographic)
- Capabilities: Polynomial-time computation, access to known attacks on weak curves  
- Limitations: Cannot solve DLP on secp256k1/ed25519 in feasible time  
- Goal: Forge adaptor signatures, recover preimages, break ECDH session keys  
- Probability in practice: Extremely low under current assumptions  

### 2.2 Network Adversary (Tier 2 – Global Passive + Active)
- Capabilities:  
  - Passive observation of all clearnet traffic  
  - Active: delay/drop/reorder/inject packets  
  - Traffic analysis (volume, timing, packet sizes)  
  - Sybil nodes in gossip/DHT/rendezvous networks  
- Limitations: Cannot break properly implemented Tor/I2P onion routing or E2E encryption (Noise + ECDH)  

### 2.3 Blockchain Adversary (Tier 3 – Miner/Validator Level)
- Capabilities:  
  - 10–30% hashpower (selfish mining, reorgs up to depth 6–10)  
  - MEV extraction (front-running, censoring)  
  - Double-spend low-confirmation txs  
- Limitations: Cannot sustain 51% attack indefinitely on BTC/XMR  

### 2.4 Malicious Participant (Tier 4 – Peer-Level)
- Roles: Dishonest Maker (provides liquidity) or Taker (initiates swap)  
- Behaviors:  
  - Abort mid-protocol  
  - Provide invalid proofs  
  - Delay responses indefinitely  
  - Attempt to link identities across swaps  
  - Run honeypot offers to trace users  

### 2.5 External Chain Analysis Adversary (Tier 5 – Surveillance Firm / Government)
- Capabilities:  
  - Full BTC blockchain access + heuristics (cluster analysis, common-input, change detection)  
  - Partial Monero analysis if view keys leaked or timing correlated  
  - Off-chain correlation (exchange KYC leaks, IP if Tor bypassed)  

## 3. Threat Catalog by STRIDE Category

### 3.1 Spoofing
- Fake peer identity in discovery layer  
- Impersonate legitimate maker/taker  
- Mitigation: Signed offers (ECDSA/Schnorr), local reputation, no global PKI  

### 3.2 Tampering
- Alter negotiation messages (rate, timeouts)  
- Forge adaptor pre-signature  
- Mitigation: HMAC-SHA256 on all messages, adaptor unforgeability  

### 3.3 Repudiation
- Deny participation in swap after completion  
- Mitigation: On-chain evidence (txids + adaptor proofs), local logging  

### 3.4 Information Disclosure
- Leak adaptor preimage publicly  
- Expose Monero view key beyond necessary  
- Mitigation: Ephemeral channels, minimal revelation, stealth addresses  

### 3.5 Denial of Service
- Flood discovery with fake offers  
- Repeated griefing (low-value aborts)  
- Mitigation: Local rate-limiting, min swap amount, reputation decay  

### 3.6 Elevation of Privilege
- Gain control over victim's funds via social engineering  
- Mitigation: No custody, hardware wallet compatibility, UI warnings  

## 4. Direction-Specific Threat Analysis

### 4.1 BTC → XMR (Primary Flow – Lower Risk)

Threat ID | Description | Likelihood | Impact | Mitigation | Residual Risk
---|---|---|---|---|---
BTC-XMR-01 | Adaptor signature forgery | Rare | Critical | OMDL assumption + sound construction | Low
BTC-XMR-02 | Maker withholds preimage after XMR send | Low | Medium | BTC timeout refund path | Low
BTC-XMR-03 | Timing correlation (lock → send) | Medium | High | Randomized delays (120–300s) + variable amounts | Medium
BTC-XMR-04 | BTC reorg after XMR sent | Low | Medium | Require 6+ BTC confs | Low
BTC-XMR-05 | Dust attack on Monero receipt | Medium | Low | Minimum XMR amount check | Low

### 4.2 XMR → BTC (Reverse Flow – Higher Risk)

Threat ID | Description | Likelihood | Impact | Mitigation | Residual Risk
---|---|---|---|---|---
XMR-BTC-01 | Taker sends invalid/dust XMR | Medium | High | Maker verifies tx before s reveal | Medium
XMR-BTC-02 | Griefing via non-claim after XMR send | High | High | Extended BTC timeout (48–72h) + collateral | Medium
XMR-BTC-03 | No native Monero refund → locked funds | Medium | Critical | Cooperative abort + reputation punish | Medium-High
XMR-BTC-04 | Fake send proof | Low | Critical | Partial view key + local scan verification | Low
XMR-BTC-05 | Maker refuses to reveal s | Low | High | Collateral slashing path (future) | Medium

## 5. Privacy Threat Vectors (Detailed)

### 5.1 Cross-Chain Linkage Vectors
- Adaptor preimage revealed in BTC claim tx → temporal correlation with Monero tx  
- Amount heuristics (if same approximate value)  
- Address reuse patterns on BTC side  

### 5.2 Timing & Volume Attacks
- Predictable delay between lock and fulfillment  
- Packet size correlation in Tor circuit  

### 5.3 Metadata Exposure
- IP leak if Tor/I2P misconfigured  
- Session key reuse across swaps  

### 5.4 Bitcoin-Specific Privacy Weaknesses
- UTXO linkage via common inputs  
- Change address detection  
- Cluster analysis by firms like Chainalysis  

### 5.5 Monero-Specific Privacy Strengths & Residual Risks
- Ring signatures + RingCT → excellent default unlinkability  
- Risk only if view key over-shared or timing perfectly correlated  

## 6. Expanded Risk Quantification Matrix

Category | Threat | Likelihood | Impact | Pre-Mitigation Risk | Post-Mitigation Risk | Notes
---|---|---|---|---|---|---
Crypto | Adaptor forgery | Rare | Critical | High | Low | Relies on ECC security
Network | Timing correlation | Medium | High | High | Medium | Delays help but not perfect
Blockchain | Reorg double-spend | Low | Medium | Medium | Low | Deep confs effective
Participant | Griefing/abort | High | Medium | High | Medium | Economic disincentives
Privacy | Cross-chain linkage | Medium | High | High | Medium | Strongest remaining concern
DoS | Discovery flooding | High | Low | Medium | Low | Local filtering
Sybil | Honeypot offers | Medium | Medium | Medium | Low-Med | Reputation local only

## 7. References (Expanded)

- Lindell, Y. (2020). Adaptor Signatures and Their Applications.  
- Erwig, L. et al. (2021). Two-Party Adaptor Signatures from Identification Schemes.  
- Gugger, J. (2020). Bitcoin–Monero Cross-chain Atomic Swap. IACR ePrint 2020/1126.  
- Monero Research Lab:  
  - RingCT security analysis  
  - Dandelion++ anonymity set  
  - Black marble attack vectors  
- COMIT Network: xmr-btc-swap griefing & timeout analysis  
- UnstoppableSwap: practical mainnet observations  
- BasicSwap DEX: SMSG mixnet DoS resistance  
- Bitcoin BIPs: 340 (Schnorr), 341 (Taproot privacy), 342 (Tapscript)  

## 8. Appendices

### 8.1 Glossary (Expanded)
- Adaptor Signature: Signature variant that reveals secret upon correct adaptation  
- Griefing: Attack aiming to waste resources without direct profit  
- OMDL: One-More Discrete Log assumption (basis for adaptor security)  
- Stealth Address: One-time Monero address preventing reuse linkage  
- View Tag: Monero optimization for scanning without full view key  

### 8.2 Hypothetical Attack Scenarios (Conceptual)
- Scenario 1: Malicious Maker runs 100 honeypot offers → traces Takers via timing patterns  
- Scenario 2: Network adversary delays BTC lock confirmation → forces timeout grief  
- Scenario 3: Chain analysis firm clusters BTC change addresses → correlates with known exchange deposits  

### 8.3 Future Threat Evolution
- Quantum threat timeline: 2030+ → migrate to lattice-based adaptors  
- Monero Seraphis/Jamtis upgrades → potential for symmetric timelocks  
- Increased chain surveillance → need for better metadata obfuscation  

This threat model is intentionally exhaustive to reflect the high-stakes nature of cross-chain private swaps. Residual risks remain medium in privacy and griefing categories — inherent to decentralized, trustless design — and are ultimately user-managed.