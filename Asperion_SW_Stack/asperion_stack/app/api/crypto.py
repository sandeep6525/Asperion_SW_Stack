"""
Asperion Enterprise OS - Cryptographic Services & Tools API Router
Endpoint prefix: /api/v1/crypto
Complies with FIPS 140-3, ISO/IEC 27001 Control A.10, and SOC 2 CC6.1/CC6.7.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.engines.crypto_engine import crypto_engine
from app.schemas.crypto import (
    HashRequest, HashResponse,
    HMACRequest, HMACResponse,
    AESEncryptRequest, AESEncryptResponse,
    AESDecryptRequest, AESDecryptResponse,
    KeyPairResponse,
    SignRequest, SignResponse,
    VerifySignatureRequest, VerifySignatureResponse,
    MerkleTreeRequest, MerkleTreeResponse,
    TokenGenerateRequest, TokenGenerateResponse
)

router = APIRouter(prefix="/crypto", tags=["Enterprise Cryptographic Tools"])

@router.post("/hash", response_model=HashResponse)
def compute_hash(payload: HashRequest):
    """
    Computes cryptographic digest (SHA-256 or SHA-512) for inputs.
    """
    algo = payload.algorithm.upper() if payload.algorithm else "SHA-256"
    if algo == "SHA-512":
        digest = crypto_engine.sha512_digest(payload.data)
        bits = 512
    elif algo == "SHA-256":
        digest = crypto_engine.sha256_digest(payload.data)
        bits = 256
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported hash algorithm '{payload.algorithm}'. Only SHA-256 and SHA-512 are permitted."
        )

    preview = payload.data[:40] + "..." if len(payload.data) > 40 else payload.data
    return HashResponse(
        algorithm=algo,
        digest=digest,
        length_bits=bits,
        data_preview=preview
    )

@router.post("/hmac", response_model=HMACResponse)
def compute_hmac(payload: HMACRequest):
    """
    Computes HMAC-SHA256 authenticated message digest.
    """
    digest = crypto_engine.hmac_sha256(payload.key, payload.message)
    return HMACResponse(
        algorithm="HMAC-SHA256",
        hmac_digest=digest
    )

@router.post("/encrypt/aes-gcm", response_model=AESEncryptResponse)
def encrypt_aes_gcm(payload: AESEncryptRequest):
    """
    Encrypts payload using authenticated AES-256-GCM with PBKDF2 key derivation.
    """
    try:
        ad = payload.associated_data.encode("utf-8") if payload.associated_data else None
        res = crypto_engine.encrypt_aes_gcm(payload.plaintext, payload.passphrase, ad)
        return AESEncryptResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AES Encryption failed: {str(e)}")

@router.post("/decrypt/aes-gcm", response_model=AESDecryptResponse)
def decrypt_aes_gcm(payload: AESDecryptRequest):
    """
    Decrypts AES-256-GCM ciphertext. Fails if ciphertext or nonce was tampered with.
    """
    try:
        ad = payload.associated_data.encode("utf-8") if payload.associated_data else None
        decrypted = crypto_engine.decrypt_aes_gcm(payload.ciphertext_b64, payload.nonce_b64, payload.passphrase, ad)
        return AESDecryptResponse(plaintext=decrypted, status="DECRYPTED_SUCCESS")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Decryption authentication failed. Bad passphrase or corrupted ciphertext: {str(e)}"
        )

@router.post("/keys/generate/ed25519", response_model=KeyPairResponse)
def generate_ed25519_keypair():
    """
    Generates an Ed25519 asymmetric cryptographic keypair.
    """
    kp = crypto_engine.generate_ed25519_keypair()
    fp = crypto_engine.sha256_digest(kp["public_key_pem"])
    return KeyPairResponse(
        key_type=kp["key_type"],
        public_key_pem=kp["public_key_pem"],
        private_key_pem=kp["private_key_pem"],
        public_key_hex=kp.get("public_key_hex"),
        fingerprint_sha256=fp
    )

@router.post("/keys/generate/rsa", response_model=KeyPairResponse)
def generate_rsa_keypair(key_size: int = 2048):
    """
    Generates an RSA asymmetric cryptographic keypair (2048 or 4096 bits).
    """
    if key_size not in (2048, 4096):
        key_size = 2048
    kp = crypto_engine.generate_rsa_keypair(key_size=key_size)
    fp = crypto_engine.sha256_digest(kp["public_key_pem"])
    return KeyPairResponse(
        key_type=kp["key_type"],
        public_key_pem=kp["public_key_pem"],
        private_key_pem=kp["private_key_pem"],
        fingerprint_sha256=fp
    )

@router.post("/sign", response_model=SignResponse)
def sign_message(payload: SignRequest):
    """
    Generates digital signature for a message using Ed25519 or RSA-PSS.
    """
    algo = payload.algorithm.upper() if payload.algorithm else "ED25519"
    try:
        if algo == "ED25519":
            sig = crypto_engine.sign_ed25519(payload.message, payload.private_key_pem)
        elif algo in ("RSA", "RSA-PSS"):
            sig = crypto_engine.sign_rsa_pss(payload.message, payload.private_key_pem)
        else:
            raise HTTPException(status_code=400, detail="Unsupported signing algorithm. Use Ed25519 or RSA-PSS.")

        msg_hash = crypto_engine.sha256_digest(payload.message)
        return SignResponse(
            algorithm=algo,
            signature_b64=sig,
            message_sha256=msg_hash
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Digital signing failed: {str(e)}")

@router.post("/verify", response_model=VerifySignatureResponse)
def verify_signature(payload: VerifySignatureRequest):
    """
    Cryptographically verifies an Ed25519 or RSA-PSS digital signature.
    """
    algo = payload.algorithm.upper() if payload.algorithm else "ED25519"
    try:
        if algo == "ED25519":
            valid = crypto_engine.verify_ed25519(payload.message, payload.signature_b64, payload.public_key_pem)
        elif algo in ("RSA", "RSA-PSS"):
            valid = crypto_engine.verify_rsa_pss(payload.message, payload.signature_b64, payload.public_key_pem)
        else:
            raise HTTPException(status_code=400, detail="Unsupported signature verification algorithm.")

        msg_hash = crypto_engine.sha256_digest(payload.message)
        return VerifySignatureResponse(
            is_valid=valid,
            algorithm=algo,
            message_sha256=msg_hash,
            status="SIGNATURE_GENUINE" if valid else "SIGNATURE_FORGERY_OR_INVALID"
        )
    except Exception as e:
        return VerifySignatureResponse(
            is_valid=False,
            algorithm=algo,
            message_sha256=crypto_engine.sha256_digest(payload.message),
            status=f"VERIFICATION_ERROR: {str(e)}"
        )

@router.post("/merkle-tree", response_model=MerkleTreeResponse)
def compute_merkle_tree(payload: MerkleTreeRequest):
    """
    Computes cryptographic Merkle Tree Root for a series of ledger leaves/hashes.
    """
    leaves = [crypto_engine.sha256_digest(v) for v in payload.leaf_values]
    root = crypto_engine.compute_merkle_root(leaves)
    cert = f"ADT-MERKLE-CERT-ROOT-{root[:16].upper()}"
    return MerkleTreeResponse(
        leaf_count=len(leaves),
        leaf_hashes=leaves,
        merkle_root=root,
        audit_cert=cert
    )

@router.post("/token/generate", response_model=TokenGenerateResponse)
def generate_token(payload: TokenGenerateRequest):
    """
    Generates high-entropy CSPRNG tokens for session keys, salts, or API secrets.
    """
    nbytes = payload.nbytes if payload.nbytes and 16 <= payload.nbytes <= 256 else 32
    tok = crypto_engine.generate_secure_token(nbytes=nbytes)
    return TokenGenerateResponse(
        token=tok,
        entropy_bits=nbytes * 8,
        format="URL-Safe Base64"
    )
