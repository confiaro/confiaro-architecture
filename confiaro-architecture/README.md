# Confiaro — Public Architecture & Protocol Documentation

Confiaro is a privacy-first cryptocurrency conversion platform designed to enable
Bitcoin ⇄ Monero exchanges without identity verification, user accounts,
or personal data collection.

The system is built around a strict separation between public-facing interfaces
and private execution infrastructure, following security and privacy best
practices for financial systems.

This repository documents the **public architecture, protocol concepts,
interface specifications, and reference structures** behind the Confiaro platform.

The live system operates at:

https://crypto.confiaro.com

---

## Privacy Model

Confiaro is designed around a minimal-trust philosophy.

The platform does not require and does not store:

- Email addresses
- Passwords
- Identity documents
- Personal information
- Persistent user profiles
- Tracking identifiers

User interaction is based on ephemeral account identifiers generated locally
by the interface and never tied to real-world identity.

No KYC. No accounts. No surveillance.

---

## Architecture Philosophy

Confiaro is not a typical “swap UI”.

It is an infrastructure-oriented conversion system built to prioritize:

- Privacy by default
- Non-custodial interaction
- Deterministic and auditable state transitions
- Service isolation between BTC and XMR components
- Minimal attack surface

The architecture is designed to operate under the assumption of
untrusted clients and hostile network environments.

---

## Scope of This Repository

This repository intentionally exposes **only what must be public**.

### Included:

- High-level system architecture
- Privacy and security principles
- Interface and protocol specifications
- Frontend structure and interaction flows
- Internationalization framework
- Non-operational example flows

### Explicitly Excluded:

- Conversion execution logic
- Liquidity sourcing and management
- Wallet infrastructure and key handling
- Rate calculation engines
- Anti-abuse and monitoring systems
- Operational automation

This separation is deliberate and necessary to preserve both security
and user privacy.

---

## Security Considerations

Core execution components operate in isolated environments
and are not exposed through this repository.

Public interfaces are designed to be stateless, verifiable,
and resilient to misuse.

No part of this repository enables custody of user funds.

---

## Documentation Structure

Detailed documentation can be found in:

- `/docs` — architectural explanations and design rationale
- `/specs` — protocol and interface specifications
- `/examples` — reference flows and non-operational samples

---

## License

This repository is released under the MIT License.

---

Confiaro is built on the principle that privacy is not a feature,
but a requirement.
