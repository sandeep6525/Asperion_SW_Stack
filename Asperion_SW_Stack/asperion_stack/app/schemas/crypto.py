"""
Asperion Enterprise OS - Cryptographic Services & Tools Schemas (Pydantic V2)
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class HashRequest(BaseModel):
    data: str
    algorithm: Optional[str] = "SHA-256" # SHA-256, SHA-512, MD5-Disabled

class HashResponse(BaseModel):
    algorithm: str
    digest: str
    length_bits: int
    data_preview: str

class HMACRequest(BaseModel):
    key: str
    message: str

class HMACResponse(BaseModel):
    algorithm: str = "HMAC-SHA256"
    hmac_digest: str

class AESEncryptRequest(BaseModel):
    plaintext: str
    passphrase: str
    associated_data: Optional[str] = None

class AESEncryptResponse(BaseModel):
    algorithm: str = "AES-256-GCM"
    ciphertext_b64: str
    nonce_b64: str
    plaintext_sha256: str
    status: str

class AESDecryptRequest(BaseModel):
    ciphertext_b64: str
    nonce_b64: str
    passphrase: str
    associated_data: Optional[str] = None

class AESDecryptResponse(BaseModel):
    plaintext: str
    status: str

class KeyPairResponse(BaseModel):
    key_type: str
    public_key_pem: str
    private_key_pem: str
    public_key_hex: Optional[str] = None
    fingerprint_sha256: str

class SignRequest(BaseModel):
    message: str
    private_key_pem: str
    algorithm: Optional[str] = "Ed25519" # Ed25519, RSA-PSS

class SignResponse(BaseModel):
    algorithm: str
    signature_b64: str
    message_sha256: str

class VerifySignatureRequest(BaseModel):
    message: str
    signature_b64: str
    public_key_pem: str
    algorithm: Optional[str] = "Ed25519"

class VerifySignatureResponse(BaseModel):
    is_valid: bool
    algorithm: str
    message_sha256: str
    status: str

class MerkleTreeRequest(BaseModel):
    leaf_values: List[str]

class MerkleTreeResponse(BaseModel):
    leaf_count: int
    leaf_hashes: List[str]
    merkle_root: str
    audit_cert: str

class TokenGenerateRequest(BaseModel):
    nbytes: Optional[int] = 32

class TokenGenerateResponse(BaseModel):
    token: str
    entropy_bits: int
    format: str = "URL-Safe Base64"
