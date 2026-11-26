# Module 23: Enterprise Cryptography, PKI & Digital Attestation Tools Architecture

## 1. Executive Summary & Legal Framework
This subsystem provides the cryptographic foundation for **ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED** (CIN: `U85500KA2026OPC222069`).

Engineered in strict accordance with:
- **FIPS 140-3** (Security Requirements for Cryptographic Modules)
- **ISO/IEC 27001:2022 Control A.10** (Cryptography: Policy on the Use of Cryptographic Controls & Key Management)
- **SOC 2 Type II CC6.1 & CC6.7** (Encryption in Transit, at Rest, and Non-Repudiation)
- **NIST SP 800-38D & NIST SP 800-56A** (AES-GCM Authenticated Encryption & Key Derivation)
- **RFC 8032** (Edwards-Curve Digital Signature Algorithm: Ed25519)
- **India IT Act 2000 (Section 3A)** (Electronic & Digital Signatures)

---

## 2. Cryptographic Core Primitives (`app/engines/crypto_engine.py`)

### Pillar A: Authenticated Symmetric Encryption (AES-256-GCM AEAD)
- **Cipher:** AES-256 in Galois/Counter Mode (GCM).
- **Nonce/IV:** 96-bit (12-byte) cryptographically secure random nonce (`os.urandom(12)`).
- **Key Derivation:** PBKDF2-HMAC-SHA256 with 100,000 iterations and enterprise root salt (`ENTERPRISE_ROOT_SALT`).
- **Integrity Guarantee:** AEAD 128-bit authentication tag guarantees detection of any ciphertext tampering or bit-flipping.

### Pillar B: Asymmetric Cryptography & Digital Signatures (PKI)
- **Ed25519 (RFC 8032):** High-speed, high-security Edwards-curve digital signatures for board resolutions, legal contracts, and event ledger attestations.
- **RSA-PSS (RFC 8017 / PKCS #1 v2.2):** 2048-bit and 4096-bit RSA keys with Probabilistic Signature Scheme (PSS) and MGF1-SHA256 for backward statutory interoperability.
- **Key Serialization:** PKCS#8 PEM private keys and SubjectPublicKeyInfo PEM public keys.

### Pillar C: Hashing, Message Authentication & Merkle Trees
- **Secure Digests:** FIPS-compliant SHA-256 (256-bit) and SHA-512 (512-bit).
- **HMAC Authentication:** RFC 2104 HMAC-SHA256 for API authentication and webhook validation.
- **Merkle Tree Root Engine:** Computes binary Merkle tree root hashes across arbitrary transaction lists to provide batch audit attestations for SOC 2 Type II auditors.

### Pillar D: High-Entropy CSPRNG Token Generation
- Cryptographically secure pseudo-random number generation via Python `secrets.token_urlsafe` yielding 256 bits of entropy.

---

## 3. API Surface (`/api/v1/crypto`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/hash` | Computes SHA-256 or SHA-512 cryptographic digests |
| `POST` | `/hmac` | Computes HMAC-SHA256 authenticated message digests |
| `POST` | `/encrypt/aes-gcm` | Encrypts payload with AES-256-GCM and PBKDF2 key derivation |
| `POST` | `/decrypt/aes-gcm` | Decrypts and authenticates AES-256-GCM ciphertext |
| `POST` | `/keys/generate/ed25519` | Generates a new Ed25519 keypair in PEM format with SHA-256 fingerprint |
| `POST` | `/keys/generate/rsa` | Generates an RSA keypair (2048 or 4096 bits) with PEM serialization |
| `POST` | `/sign` | Signs messages with Ed25519 or RSA-PSS |
| `POST` | `/verify` | Cryptographically verifies digital signatures; returns genuine/forged status |
| `POST` | `/merkle-tree` | Computes cryptographic Merkle Tree Root across a list of audit leaves |
| `POST` | `/token/generate` | Generates high-entropy (256-bit) CSPRNG session tokens or secrets |

---

## 4. UI Workbench (`#view-crypto-tools`)
The Asperion Enterprise OS frontend provides an interactive workbench with 4 specialized tool suites:
1. **Hashing & HMAC:** Real-time hash calculation and HMAC verification.
2. **AES-256-GCM AEAD:** In-browser encryption/decryption with auto-fill testing.
3. **Digital Signatures:** Keypair generation, one-click document signing, and cryptographic non-repudiation verification.
4. **Merkle Tree Audit Root:** Interactive tree generator with visual leaf node tracking and certificate generation.
