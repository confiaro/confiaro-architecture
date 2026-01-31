<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/desktop/converter-bitcoin-para-monero-interface.webp"
    alt="Confiaro — Bitcoin to Monero Conversion"
    width="100%"
  />
</p>

<h1 align="center">Confiaro — Public Architecture & Protocol Documentation</h1>

<p align="center">
  Privacy-first Bitcoin ⇄ Monero conversion infrastructure<br>
  Non-custodial · No KYC · No accounts · No email · No surveillance
</p>

<p align="center">
  <a href="https://crypto.confiaro.com"><strong>Live Platform</strong></a>
</p>

---

## Overview

**Confiaro** is a privacy-first cryptocurrency conversion system designed to enable
automatic **Bitcoin ⇄ Monero** exchanges without identity verification,
user accounts, email registration, or personal data collection.

The platform operates as a **non-custodial, automated conversion layer**
where users remain in full control of their funds at all times.

There is no fund lock-in.
Users can deposit and withdraw whenever they want.

The production system is live at:

**https://crypto.confiaro.com**

---

## How the Conversion Works

- Conversion is fully automatic
- Typical conversion time: **a few minutes**
- No manual approval
- No intermediaries
- No custody at any stage

Funds are credited as soon as the required blockchain confirmations are met.
Once credited, funds are immediately available for withdrawal.

---

## Non-Custodial by Design

<p align="center">
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/bitcoin.png" width="72" />
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/monero.png" width="72" />
</p>

Confiaro is strictly **non-custodial**.

- Funds are never locked
- Funds are never pooled
- Funds are never frozen

During onboarding, the system **automatically generates two independent wallets**:

- One Bitcoin wallet
- One Monero wallet

Each wallet has its **own seed phrase**.

Users **store their own seeds** and can restore them
in **any compatible Bitcoin or Monero wallet**, at any time,
without relying on Confiaro.

Confiaro does not store, recover, or control user seeds.

---

## Network Privacy (Tor)

<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/tor.png"
    alt="Tor Network"
    width="96"
  />
</p>

Confiaro is designed to operate over **Tor (The Onion Router)**.

When accessed through Tor:

- Real IP address is not exposed
- Network location is hidden
- ISP-level tracking is mitigated
- Geographic correlation is reduced

Tor is treated as a **first-class privacy transport layer**.
Tor access is not restricted, fingerprinted, or degraded.

Network-level privacy is considered as important as on-chain privacy.

---

## Security Model

- No private keys are ever requested
- No identity data is collected
- No email or password system exists
- No persistent user profiles
- No tracking or behavioral analytics

All services operate under the assumption of:
- Untrusted clients
- Hostile networks
- Adversarial environments

---

## Public Scope of This Repository

This repository exposes **only what must be public**.

### Included

- Public architecture
- Protocol concepts
- Interface behavior
- Security and privacy principles
- Reference flows (non-operational)

### Explicitly Excluded

- Conversion execution logic
- Liquidity management
- Wallet infrastructure internals
- Rate engines
- Anti-abuse systems
- Operational automation

This separation is deliberate and essential.

---

## Interface (Production Screens)

### Desktop

<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/desktop/endereco-deposito-bitcoin-monero.webp"
    width="45%"
  />
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/desktop/historico-conversao-btc-xmr.webp"
    width="45%"
  />
</p>

### Mobile

<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/mobile/converter-bitcoin-para-monero-interface.webp"
    width="24%"
  />
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/mobile/endereco-deposito-bitcoin-monero.webp"
    width="24%"
  />
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/mobile/historico-conversao-btc-xmr.webp"
    width="24%"
  />
</p>

All screenshots are from the live production system.

---

## License

This repository is released under the **MIT License**.

---

<p align="center">
  <em>Privacy is not a feature. It is a requirement.</em>
</p>
