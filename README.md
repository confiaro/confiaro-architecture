<p align="center">
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/desktop/converter-bitcoin-para-monero-interface.webp"
       alt="Confiaro BTC to XMR Interface"
       width="100%" />
</p>

<h1 align="center">Confiaro Architecture</h1>

<p align="center">
  <strong>Privacy-first Bitcoin ↔ Monero conversion architecture</strong><br>
  Non-custodial · Protocol-driven · No KYC · Infrastructure-oriented
</p>

<p align="center">
  <a href="https://crypto.confiaro.com"><strong>Live Platform</strong></a> ·
  <a href="#overview">Overview</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#security">Security</a> ·
  <a href="#interface">Interface</a> ·
  <a href="#roadmap">Roadmap</a>
</p>

<hr>

<h2 id="overview">Overview</h2>

<p>
<strong>Confiaro</strong> is a privacy-focused system architecture and protocol design
for converting <strong>Bitcoin (BTC)</strong> to <strong>Monero (XMR)</strong> — and vice-versa —
without custodial exposure, identity tracking, or account-based surveillance.
</p>

<p>
This repository documents the <strong>technical architecture</strong>,
<strong>design principles</strong>, and <strong>protocol flow</strong> behind the production system
running at:
</p>

<p align="center">
  <a href="https://crypto.confiaro.com"><strong>https://crypto.confiaro.com</strong></a>
</p>

<p>
Confiaro is not a generic “swap UI”.
It is an <strong>infrastructure-level conversion system</strong> built with strict service
separation, blockchain-verifiable accounting, and privacy as a non-negotiable
requirement.
</p>

<hr>

<h2 id="architecture">System Architecture</h2>

<p align="center">
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/desktop/converter-monero-para-bitcoin-painel.webp"
       alt="Conversion Panel Architecture"
       width="92%" />
</p>

<h3>Core Components</h3>

<ul>
  <li>
    <strong>Frontend Interface</strong><br>
    Stateless web interface with account abstraction via short <code>account_id</code>,
    dynamic conversion direction, QR-based deposits and real-time status tracking.
  </li>

  <li>
    <strong>Bitcoin Service</strong><br>
    Integrated with <strong>BTCPay Server</strong>, invoice-based deposits,
    signed webhooks and on-chain verification.
  </li>

  <li>
    <strong>Monero Service</strong><br>
    Dedicated Monero Wallet RPC, subaddress-per-deposit model,
    confirmation-based crediting and isolated infrastructure.
  </li>

  <li>
    <strong>Coordinator Core</strong><br>
    Conversion orchestration, balance accounting, deterministic state transitions
    and full historical event tracking.
  </li>
</ul>

<hr>

<h2 id="security">Security Model</h2>

<p>
Confiaro follows a <strong>minimal-trust, adversarial-network model</strong>.
The system assumes untrusted clients, hostile networks and zero reliance on
user honesty.
</p>

<ul>
  <li>No private keys are ever requested or stored</li>
  <li>BTC and XMR services are physically and logically isolated</li>
  <li>All inbound events are webhook-verified and signature-checked</li>
  <li>State transitions are deterministic and auditable</li>
  <li>No personal data is collected, stored or correlated</li>
</ul>

<p>
Every balance change can be explained, traced and verified on-chain.
</p>

<hr>

<h2 id="interface">User Interface (Real Screens)</h2>

<h3>Desktop</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/desktop/endereco-deposito-bitcoin-monero.webp"
       width="45%" />
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/desktop/historico-conversao-btc-xmr.webp"
       width="45%" />
</p>

<h3>Mobile</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/mobile/converter-bitcoin-para-monero-interface.webp"
       width="24%" />
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/mobile/endereco-deposito-bitcoin-monero.webp"
       width="24%" />
  <img src="https://raw.githubusercontent.com/confiaro/confiaro-architecture/main/assets/mobile/historico-conversao-btc-xmr.webp"
       width="24%" />
</p>

<p>
All screenshots above are from the production system.
No mockups. No placeholders.
</p>

<hr>

<h2>Design Principles</h2>

<ul>
  <li>Protocol first, interface second</li>
  <li>No hidden custodial logic</li>
  <li>No opaque balance manipulation</li>
  <li>Everything explainable, traceable and observable</li>
  <li>User experience must never compromise privacy</li>
</ul>

<hr>

<h2 id="roadmap">Roadmap</h2>

<ul>
  <li>[ ] Formal protocol specification (RFC-style)</li>
  <li>[ ] Tor / I2P native routing</li>
  <li>[ ] Deterministic rate-locking engine</li>
  <li>[ ] Proof-of-reserves transparency endpoint</li>
  <li>[ ] Public architecture whitepaper</li>
</ul>

<hr>

<h2>Disclaimer</h2>

<p>
This repository documents architectural and protocol concepts only.
It does not constitute financial advice or custodial services.
</p>

<hr>

<p align="center">
  <em>Privacy is not a feature. It is a requirement.</em>
</p>
