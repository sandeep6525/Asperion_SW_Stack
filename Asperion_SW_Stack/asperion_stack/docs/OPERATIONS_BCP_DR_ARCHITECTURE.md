# Module 22: Enterprise Operations, BCP/DR & Cryptographic Event Ledger Architecture

## 1. Executive Summary & Legal Entity Context
This subsystem establishes the immutable core operations kernel, business continuity/disaster recovery (BCP/DR) engine, and statutory data protection registers for **ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED** (CIN: `U85500KA2026OPC222069`).

All operations are cryptographically chained, auditable, and certified under:
- **ISO/IEC 27001:2022 Control A.12.4** (Event Logging, Log Protection & Clock Synchronization)
- **SOC 2 Type II CC7.2** (Tamper-evident audit trail & non-repudiation)
- **ISO 22301:2019** (Business Continuity Management & DR RTO/RPO SLA)
- **India Digital Personal Data Protection (DPDP) Act 2023** (Sections 5 & 6 Statutory Consent Register)

---

## 2. Core Operational Pillars

### Pillar A: Cryptographic Tamper-Evident Event Ledger
- **Algorithm:** SHA-256 Hash Chaining.
- **Genesis Block:** `0000000000000000000000000000000000000000000000000000000000000000`
- **Hash Derivation:**
  $$\text{Current Hash} = \text{SHA-256}(\text{Prev Hash} \parallel \text{Event Code} \parallel \text{Aggregate Type} \parallel \text{Aggregate ID} \parallel \text{Event Type} \parallel \text{Payload JSON} \parallel \text{Timestamp})$$
- **Non-Repudiation:** Digital ED25519 signature representation and IP origin stamping on every state mutation.
- **Verification Endpoint:** `POST /api/v1/operations/ledger/verify` recalculates hashes across the entire table from Block #1 to head in $< 100\text{ms}$.

### Pillar B: Business Continuity & Disaster Recovery (BCP/DR) Simulator
- **RPO Target:** $\le 15\text{ minutes}$ (continuous hourly WAL log checkpoints and incremental transaction tracking).
- **RTO Target:** $\le 5\text{ minutes}$ (hot SQLite backup mounting and integrity scoring in sandboxed runtime).
- **Integrity Validation:** Real file SHA-256 checksum calculated from binary bytes on disk.
- **Encryption:** AES-256-GCM envelope encryption for off-site cold storage replication.

### Pillar C: India DPDP Act 2023 Statutory Consent Register
- **Legal Scope:** Employee biometrics, contractor KYC, client corporate agreements, and candidate screenings.
- **Data Model:** Records Principal Name, Principal Type, Purpose Category, Notice Reference (`ADT/DPDP/NOTICE/2026/V1`), Affirmative Consent Status, and DPO Officer Attestation (`AGT-COMPLY-01`).
- **Audit Linking:** Each consent creation automatically emits an immutable event to the cryptographic ledger.

### Pillar D: SRE Storage Telemetry & Auto-Maintenance
- **WAL Optimization:** Automated truncation of Write-Ahead Log via `PRAGMA wal_checkpoint(TRUNCATE);`.
- **Zero-Downtime Vacuuming:** Reclaims fragmented SQLite pages with zero thread locking.
- **Telemetry Watchdog:** Real-time query latency (`SELECT 1`), database byte size, WAL buffer size, and host RSS memory tracking.

---

## 3. API Surface (`/api/v1/operations`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/overview` | Executive operational health, ledger status, RPO/RTO metrics, and DPDP consent summary |
| `GET` | `/ledger` | Paginated tamper-evident cryptographic event stream with aggregate filters |
| `POST` | `/ledger/append` | Appends a cryptographically chained event block |
| `POST` | `/ledger/verify` | Recomputes entire SHA-256 chain from Genesis block; certifies zero tampering |
| `GET` | `/bcp-dr/snapshots` | Lists BCP/DR backup archives, file sizes, and checksums |
| `POST` | `/bcp-dr/snapshots/create` | Generates a hot backup snapshot with live SHA-256 binary digest |
| `POST` | `/bcp-dr/snapshots/{id}/test-restore` | Simulates automated DR drill, validating RTO SLA ($< 5\text{ min}$) |
| `GET` | `/dpdp/consents` | Lists statutory DPDP consent records with principal filters |
| `POST` | `/dpdp/consents` | Registers affirmative consent and appends event to ledger |
| `GET` | `/telemetry/live` | Real-time SQLite database, WAL pages, memory RSS, and latency |
| `POST` | `/telemetry/vacuum` | Executes WAL checkpoint truncate and SQLite database vacuum |
