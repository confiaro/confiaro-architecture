<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/desktop/converter-bitcoin-para-monero-interface.webp"
    alt="Confiaro — Bitcoin to Monero Conversion"
    width="100%"
  />
</p>

<h1 align="center">Confiaro Architecture</h1>

<p align="center">
  <strong>Private, non-custodial Bitcoin ⇄ Monero conversion infrastructure</strong><br>
  Automated · No KYC · No accounts · No email · Privacy by default
</p>

<p align="center">
  <a href="https://crypto.confiaro.com"><strong>Live Platform</strong></a>
</p>

<hr>

## Overview

<strong>Confiaro</strong> is a privacy-first conversion architecture designed to enable
<strong>automatic Bitcoin ⇄ Monero exchanges</strong> without custodial exposure,
identity verification, or account-based tracking.

The system operates as a <strong>non-custodial conversion layer</strong> where users
remain in full control of their funds, keys, and recovery data at all times.

There is no registration.
There is no email.
There is no KYC.

The live production system operates at:

<p align="center">
  <a href="https://crypto.confiaro.com"><strong>https://crypto.confiaro.com</strong></a>
</p>

---

## Automated Conversion Flow

- Fully automated execution
- Typical conversion time: **minutes**
- No manual approval
- No fund locking
- No intermediaries

Funds are credited automatically after blockchain confirmations
and become immediately available for withdrawal.

Users can deposit and withdraw at any time.

---

## Non-Custodial Wallet Architecture

<p align="center">
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/bitcoin.png" width="72" />
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/monero.png" width="72" />
</p>

Confiaro is strictly **non-custodial by design**.

During initialization, the system automatically creates:

- One Bitcoin wallet
- One Monero wallet

Each wallet has its **own independent seed phrase**.

Users are responsible for storing their seeds and can restore
their wallets in **any compatible Bitcoin or Monero wallet**
at any time, without relying on Confiaro.

Confiaro does not store seeds.
Confiaro does not control keys.
Confiaro cannot access user funds.

---

## Network Privacy & Tor

<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/thor.png"
    alt="Tor Network"
    width="96"
  />
</p>

Confiaro is designed to operate over the **Tor network**.

When accessed through Tor:

- IP addresses are not exposed
- Network location is hidden
- ISP-level metadata is mitigated
- Geographic correlation is reduced

Tor is treated as a **first-class transport layer**, not an optional feature.

The platform does not block, fingerprint, or degrade Tor-based access.

Privacy at the network layer is considered as critical as privacy on-chain.

---

## System Architecture

<p align="center">
  <img
    src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/confiaro-architecture/assets/desktop/converter-monero-para-bitcoin-painel.webp"
    alt="Confiaro Conversion Architecture"
    width="92%"
  />
</p>

### Core Components

- <strong>Frontend Interface</strong>  
  Stateless web interface with ephemeral account abstraction,
  dynamic conversion direction and real-time status tracking.

- <strong>Bitcoin Service</strong>  
  Invoice-based deposits, on-chain verification and webhook-driven settlement.

- <strong>Monero Service</strong>  
  Dedicated wallet RPC, subaddress-per-deposit model and confirmation-based crediting.

- <strong>Coordinator Core</strong>  
  Deterministic conversion orchestration, balance accounting
  and auditable state transitions.

All services are logically and physically isolated.

---

## Security Model

Confiaro operates under a <strong>minimal-trust, adversarial threat model</strong>.

- No private keys are requested
- No identity data is collected
- No accounts or credentials exist
- No tracking or analytics are used

The system assumes untrusted clients and hostile networks by default.

No part of this repository enables custody of user funds.

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

## Disclaimer

This repository documents architectural and protocol concepts only.
It does not constitute financial advice or custodial services.

---

<p align="center">
  <em>Privacy is not a feature. It is a requirement.</em>
</p>
