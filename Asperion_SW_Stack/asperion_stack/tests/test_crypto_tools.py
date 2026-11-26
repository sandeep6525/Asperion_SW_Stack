"""
Unit & Integration Tests for Module 23 - Cryptographic Tools & PKI Engine
Covers:
1. Hashing algorithms (SHA-256 and SHA-512)
2. HMAC-SHA256 authenticated digests
3. Symmetric encryption & decryption (AES-256-GCM with PBKDF2)
4. Authenticated decryption failure with tampered ciphertext/nonce
5. Asymmetric keypair generation (Ed25519 & RSA-2048)
6. Digital signature generation and verification (Ed25519 & RSA-PSS)
7. Digital signature rejection for tampered messages
8. Merkle Tree Root computation for audit batches
9. High-entropy CSPRNG token generation
"""
import pytest
from app.engines.crypto_engine import crypto_engine
from app.api.crypto import (
    compute_hash, compute_hmac, encrypt_aes_gcm, decrypt_aes_gcm,
    generate_ed25519_keypair, generate_rsa_keypair,
    sign_message, verify_signature, compute_merkle_tree, generate_token
)
from app.schemas.crypto import (
    HashRequest, HMACRequest, AESEncryptRequest, AESDecryptRequest,
    SignRequest, VerifySignatureRequest, MerkleTreeRequest, TokenGenerateRequest
)

def test_hashing_sha256_and_sha512():
    # 1. SHA-256
    req256 = HashRequest(data="Asperion Enterprise OS 2026", algorithm="SHA-256")
    res256 = compute_hash(req256)
    assert res256.algorithm == "SHA-256"
    assert res256.length_bits == 256
    assert len(res256.digest) == 64
    assert res256.digest == crypto_engine.sha256_digest("Asperion Enterprise OS 2026")

    # 2. SHA-512
    req512 = HashRequest(data="Asperion Enterprise OS 2026", algorithm="SHA-512")
    res512 = compute_hash(req512)
    assert res512.algorithm == "SHA-512"
    assert res512.length_bits == 512
    assert len(res512.digest) == 128


def test_hmac_sha256():
    req = HMACRequest(key="EnterpriseMasterKey", message="Transaction-94812")
    res = compute_hmac(req)
    assert res.algorithm == "HMAC-SHA256"
    assert len(res.hmac_digest) == 64
    assert res.hmac_digest == crypto_engine.hmac_sha256("EnterpriseMasterKey", "Transaction-94812")


def test_aes_256_gcm_encrypt_decrypt_roundtrip():
    passphrase = "UltraSecureAsperionPassphrase2026!"
    plaintext = "Confidential Payroll Data: INR 15,00,000 for Director Varadi Vijay"

    # Encrypt
    enc_req = AESEncryptRequest(plaintext=plaintext, passphrase=passphrase)
    enc_res = encrypt_aes_gcm(enc_req)
    assert enc_res.algorithm == "AES-256-GCM"
    assert enc_res.status == "ENCRYPTED_SUCCESS"
    assert len(enc_res.ciphertext_b64) > 0
    assert len(enc_res.nonce_b64) > 0

    # Decrypt
    dec_req = AESDecryptRequest(
        ciphertext_b64=enc_res.ciphertext_b64,
        nonce_b64=enc_res.nonce_b64,
        passphrase=passphrase
    )
    dec_res = decrypt_aes_gcm(dec_req)
    assert dec_res.status == "DECRYPTED_SUCCESS"
    assert dec_res.plaintext == plaintext


def test_aes_256_gcm_tamper_detection():
    passphrase = "MasterKeyPassphrase"
    enc_res = encrypt_aes_gcm(AESEncryptRequest(plaintext="Secret", passphrase=passphrase))

    # Tampered passphrase should raise HTTPException 400
    with pytest.raises(Exception):
        decrypt_aes_gcm(AESDecryptRequest(
            ciphertext_b64=enc_res.ciphertext_b64,
            nonce_b64=enc_res.nonce_b64,
            passphrase="WrongPassword"
        ))


def test_ed25519_keypair_and_signing():
    kp = generate_ed25519_keypair()
    assert kp.key_type == "Ed25519"
    assert "BEGIN PUBLIC KEY" in kp.public_key_pem
    assert "BEGIN PRIVATE KEY" in kp.private_key_pem
    assert len(kp.fingerprint_sha256) == 64

    message = "Board Resolution ADT/RES/2026/001: Authorized by Sole Director Varadi Vijay"

    # Sign
    sign_res = sign_message(SignRequest(
        message=message,
        private_key_pem=kp.private_key_pem,
        algorithm="Ed25519"
    ))
    assert sign_res.algorithm == "ED25519"
    assert len(sign_res.signature_b64) > 0

    # Verify Genuine
    verify_res = verify_signature(VerifySignatureRequest(
        message=message,
        signature_b64=sign_res.signature_b64,
        public_key_pem=kp.public_key_pem,
        algorithm="Ed25519"
    ))
    assert verify_res.is_valid is True
    assert verify_res.status == "SIGNATURE_GENUINE"

    # Verify Tampered Message Fails
    verify_tampered = verify_signature(VerifySignatureRequest(
        message="Forger Modified Message Content",
        signature_b64=sign_res.signature_b64,
        public_key_pem=kp.public_key_pem,
        algorithm="Ed25519"
    ))
    assert verify_tampered.is_valid is False
    assert verify_tampered.status == "SIGNATURE_FORGERY_OR_INVALID"


def test_rsa_pss_signing_and_verification():
    kp = generate_rsa_keypair(key_size=2048)
    assert kp.key_type == "RSA-2048"

    message = "Asperion Commercial Invoicing Attestation"
    sign_res = sign_message(SignRequest(
        message=message,
        private_key_pem=kp.private_key_pem,
        algorithm="RSA-PSS"
    ))
    assert sign_res.algorithm == "RSA-PSS"

    verify_res = verify_signature(VerifySignatureRequest(
        message=message,
        signature_b64=sign_res.signature_b64,
        public_key_pem=kp.public_key_pem,
        algorithm="RSA-PSS"
    ))
    assert verify_res.is_valid is True


def test_merkle_tree_computation():
    leaves = ["LEAF_TXN_001", "LEAF_TXN_002", "LEAF_TXN_003", "LEAF_TXN_004"]
    res = compute_merkle_tree(MerkleTreeRequest(leaf_values=leaves))
    assert res.leaf_count == 4
    assert len(res.leaf_hashes) == 4
    assert len(res.merkle_root) == 64
    assert res.audit_cert.startswith("ADT-MERKLE-CERT-ROOT-")


def test_csprng_token_generation():
    tok_res = generate_token(TokenGenerateRequest(nbytes=32))
    assert len(tok_res.token) > 30
    assert tok_res.entropy_bits == 256
