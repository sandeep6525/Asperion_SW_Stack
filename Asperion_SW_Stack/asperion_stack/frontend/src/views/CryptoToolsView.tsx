// @ts-ignore
import { loadCryptoTools, switchCryptoTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';

export const CryptoToolsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('hashing');

  useEffect(() => {
    try {
      loadCryptoTools();
    } catch (e) {
      console.error('Error in loadCryptoTools:', e);
    }
  }, []);

  const handleTabSwitch = (tab: string) => {
    setActiveTab(tab);
    try {
      switchCryptoTab(tab);
    } catch (e) {
      console.error('Error in switchCryptoTab:', e);
    }
  };

  const callGlobal = (fnName: string, ...args: any[]) => {
    const fn = (window as any)[fnName];
    if (typeof fn === 'function') {
      fn(...args);
    } else {
      console.warn(`Function ${fnName} not found on window`);
    }
  };

  return (
    <div className="w-full">
      <section id="view-crypto-tools" className="module-view space-y-6">
        {/* Header Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 p-6 rounded-2xl border border-emerald-800/60 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 font-mono text-xs uppercase tracking-wider mb-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              FIPS 140-3 &bull; ISO/IEC 27001 A.10 &bull; SOC 2 CC6.1 &bull; Module 23
            </div>
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
              <i className="fa-solid fa-key text-emerald-400"></i> Cryptography, PKI &amp; Digital Attestation Tools
            </h2>
            <p className="text-sm text-slate-300 mt-1 max-w-3xl">
              Enterprise-grade cryptographic engine supporting AES-256-GCM authenticated encryption, Ed25519 &amp; RSA-PSS digital signatures, SHA-256/512 digests, HMAC authentication, and Merkle tree audit roots.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => callGlobal('generateNewKeyPair', 'Ed25519')}
              className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold transition shadow-lg flex items-center gap-2"
            >
              <i className="fa-solid fa-plus"></i> Generate Ed25519 Keypair
            </button>
            <button
              onClick={() => callGlobal('generateRandomCSPRNGToken')}
              className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 rounded-xl text-xs font-semibold transition flex items-center gap-1.5"
            >
              <i className="fa-solid fa-dice"></i> CSPRNG Token
            </button>
          </div>
        </div>

        {/* Crypto Navigation Tabs */}
        <div className="border-b border-slate-800 flex items-center justify-between">
          <div className="flex gap-2">
            <button
              onClick={() => handleTabSwitch('hashing')}
              id="btn-crypto-tab-hashing"
              className={`px-4 py-2.5 text-xs font-bold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'hashing'
                  ? 'border-emerald-500 text-emerald-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <i className="fa-solid fa-hashtag"></i> Hashing &amp; HMAC
            </button>
            <button
              onClick={() => handleTabSwitch('aes-gcm')}
              id="btn-crypto-tab-aes-gcm"
              className={`px-4 py-2.5 text-xs font-bold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'aes-gcm'
                  ? 'border-emerald-500 text-emerald-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <i className="fa-solid fa-lock"></i> AES-256-GCM AEAD
            </button>
            <button
              onClick={() => handleTabSwitch('signatures')}
              id="btn-crypto-tab-signatures"
              className={`px-4 py-2.5 text-xs font-bold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'signatures'
                  ? 'border-emerald-500 text-emerald-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <i className="fa-solid fa-signature"></i> Digital Signatures (Ed25519/RSA)
            </button>
            <button
              onClick={() => handleTabSwitch('merkle')}
              id="btn-crypto-tab-merkle"
              className={`px-4 py-2.5 text-xs font-bold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'merkle'
                  ? 'border-emerald-500 text-emerald-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <i className="fa-solid fa-network-wired"></i> Merkle Tree Audit Root
            </button>
          </div>
          <div className="flex items-center gap-2 py-1">
            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-800/80">
              Zero-Knowledge Compliant
            </span>
          </div>
        </div>

        {/* TAB 1: Hashing & HMAC (Side-by-side 2-column Grid) */}
        <div
          id="crypto-tab-hashing"
          className={`grid grid-cols-1 md:grid-cols-2 gap-6 ${activeTab === 'hashing' ? '' : 'hidden'}`}
        >
          {/* SHA Hasher */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-white text-sm flex items-center gap-2">
                <i className="fa-solid fa-fingerprint text-emerald-400"></i> Cryptographic Hash Generator
              </h3>
              <span className="text-[10px] font-mono text-slate-400">FIPS 180-4</span>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-medium text-slate-300 mb-1">Algorithm</label>
                <select id="crypto-hash-algo" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200">
                  <option value="SHA-256">SHA-256 (256-bit / 64 hex chars)</option>
                  <option value="SHA-512">SHA-512 (512-bit / 128 hex chars)</option>
                </select>
              </div>
              <div>
                <label className="block font-medium text-slate-300 mb-1">Input Data / Payload</label>
                <textarea
                  id="crypto-hash-input"
                  rows={3}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono text-xs"
                  placeholder="Type or paste payload string..."
                ></textarea>
              </div>
              <button
                onClick={() => callGlobal('executeCryptoHash')}
                className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fa-solid fa-play"></i> Compute Digest
              </button>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1">
                <span className="text-[10px] uppercase font-bold text-slate-500">Hexadecimal Digest:</span>
                <div id="crypto-hash-output" className="text-emerald-300 font-mono text-xs break-all select-all">
                  --
                </div>
              </div>
            </div>
          </div>

          {/* HMAC Authenticator */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-white text-sm flex items-center gap-2">
                <i className="fa-solid fa-shield-halved text-cyan-400"></i> HMAC-SHA256 Authenticator
              </h3>
              <span className="text-[10px] font-mono text-slate-400">RFC 2104</span>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-medium text-slate-300 mb-1">Secret Key</label>
                <input
                  type="password"
                  id="crypto-hmac-key"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200 font-mono"
                  placeholder="Enter shared secret key..."
                />
              </div>
              <div>
                <label className="block font-medium text-slate-300 mb-1">Message String</label>
                <textarea
                  id="crypto-hmac-msg"
                  rows={3}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono text-xs"
                  placeholder="Message to authenticate..."
                ></textarea>
              </div>
              <button
                onClick={() => callGlobal('executeCryptoHMAC')}
                className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fa-solid fa-play"></i> Compute HMAC
              </button>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1">
                <span className="text-[10px] uppercase font-bold text-slate-500">HMAC-SHA256 Signature:</span>
                <div id="crypto-hmac-output" className="text-cyan-300 font-mono text-xs break-all select-all">
                  --
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* TAB 2: AES-256-GCM AEAD (Side-by-side 2-column Grid) */}
        <div
          id="crypto-tab-aes-gcm"
          className={`grid grid-cols-1 md:grid-cols-2 gap-6 ${activeTab === 'aes-gcm' ? '' : 'hidden'}`}
        >
          {/* Encryption Box */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-white text-sm flex items-center gap-2">
                <i className="fa-solid fa-lock text-indigo-400"></i> Authenticated AES-256-GCM Encryption
              </h3>
              <span className="text-[10px] font-mono text-slate-400">NIST SP 800-38D</span>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-medium text-slate-300 mb-1">Passphrase / Master Secret</label>
                <input
                  type="password"
                  id="crypto-aes-enc-pass"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200 font-mono"
                  placeholder="Enter encryption passphrase..."
                />
              </div>
              <div>
                <label className="block font-medium text-slate-300 mb-1">Plaintext Payload</label>
                <textarea
                  id="crypto-aes-enc-plaintext"
                  rows={3}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono text-xs"
                  placeholder="Confidential payload to encrypt..."
                ></textarea>
              </div>
              <button
                onClick={() => callGlobal('executeAESEncrypt')}
                className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fa-solid fa-shield-virus"></i> Encrypt with AES-GCM
              </button>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-[11px]">
                <div>
                  <span className="text-slate-500 uppercase font-bold">Ciphertext (Base64):</span>
                  <div id="crypto-aes-enc-ct" className="text-indigo-300 font-mono break-all select-all">
                    --
                  </div>
                </div>
                <div>
                  <span className="text-slate-500 uppercase font-bold">96-bit Nonce (Base64):</span>
                  <div id="crypto-aes-enc-nonce" className="text-cyan-400 font-mono break-all select-all">
                    --
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Decryption Box */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-white text-sm flex items-center gap-2">
                <i className="fa-solid fa-lock-open text-amber-400"></i> Authenticated AES-256-GCM Decryption
              </h3>
              <span className="text-[10px] font-mono text-emerald-400">Integrity Verified</span>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-medium text-slate-300 mb-1">Passphrase</label>
                <input
                  type="password"
                  id="crypto-aes-dec-pass"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200 font-mono"
                  placeholder="Matching passphrase..."
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Nonce (Base64)</label>
                  <input
                    type="text"
                    id="crypto-aes-dec-nonce"
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200 font-mono text-xs"
                    placeholder="Paste 96-bit nonce..."
                  />
                </div>
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Ciphertext (Base64)</label>
                  <input
                    type="text"
                    id="crypto-aes-dec-ct"
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200 font-mono text-xs"
                    placeholder="Paste ciphertext..."
                  />
                </div>
              </div>
              <button
                onClick={() => callGlobal('executeAESDecrypt')}
                className="w-full py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fa-solid fa-unlock"></i> Decrypt &amp; Verify Integrity
              </button>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1">
                <span className="text-[10px] uppercase font-bold text-slate-500">Decrypted Plaintext:</span>
                <div id="crypto-aes-dec-output" className="text-emerald-300 font-mono text-xs break-all select-all">
                  --
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* TAB 3: Digital Signatures (Ed25519 & RSA-PSS) */}
        <div
          id="crypto-tab-signatures"
          className={`space-y-6 ${activeTab === 'signatures' ? '' : 'hidden'}`}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Keypair Display & Generation */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="font-bold text-white text-sm flex items-center gap-2">
                  <i className="fa-solid fa-id-card-clip text-emerald-400"></i> Asymmetric Keypair Generator
                </h3>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => callGlobal('generateNewKeyPair', 'Ed25519')}
                    className="px-2.5 py-1 bg-emerald-600/30 text-emerald-300 hover:bg-emerald-600/50 rounded text-xs font-semibold"
                  >
                    Ed25519
                  </button>
                  <button
                    onClick={() => callGlobal('generateNewKeyPair', 'RSA-2048')}
                    className="px-2.5 py-1 bg-indigo-600/30 text-indigo-300 hover:bg-indigo-600/50 rounded text-xs font-semibold"
                  >
                    RSA-2048
                  </button>
                </div>
              </div>
              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-slate-400 uppercase text-[10px] font-bold">Public Key (PEM):</span>
                  <textarea
                    id="crypto-pubkey-display"
                    rows={4}
                    readOnly
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 font-mono text-[11px] text-emerald-400 select-all"
                    placeholder="Generate keypair to view public key..."
                  ></textarea>
                </div>
                <div>
                  <span className="text-slate-400 uppercase text-[10px] font-bold">Private Key (PKCS#8 PEM):</span>
                  <textarea
                    id="crypto-privkey-display"
                    rows={4}
                    readOnly
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 font-mono text-[11px] text-rose-400 select-all"
                    placeholder="Generate keypair to view private key..."
                  ></textarea>
                </div>
              </div>
            </div>

            {/* Sign & Verify Box */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="font-bold text-white text-sm flex items-center gap-2">
                  <i className="fa-solid fa-signature text-purple-400"></i> Sign Document &amp; Verify Attestation
                </h3>
                <span className="text-[10px] font-mono text-purple-400">RFC 8032</span>
              </div>
              <div className="space-y-3 text-xs">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Message / Document to Sign</label>
                  <input
                    type="text"
                    id="crypto-sign-msg"
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-slate-200"
                    placeholder="e.g. Asperion Board Resolution ADT/RES/2026/001 approved"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => callGlobal('executeSignMessage')}
                    className="py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-lg transition flex items-center justify-center gap-1.5"
                  >
                    <i className="fa-solid fa-pen-nib"></i> Sign Message
                  </button>
                  <button
                    onClick={() => callGlobal('executeVerifySignature')}
                    className="py-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-emerald-500/30 font-bold rounded-lg transition flex items-center justify-center gap-1.5"
                  >
                    <i className="fa-solid fa-check-double"></i> Verify Signature
                  </button>
                </div>
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-[11px]">
                  <div>
                    <span className="text-slate-500 uppercase font-bold">Base64 Signature:</span>
                    <div id="crypto-sig-output" className="text-purple-300 font-mono break-all select-all">
                      --
                    </div>
                  </div>
                  <div>
                    <span className="text-slate-500 uppercase font-bold">Verification Verdict:</span>
                    <div id="crypto-verify-verdict" className="font-mono font-bold text-slate-400">
                      Awaiting signature input
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* TAB 4: Merkle Tree Root */}
        <div
          id="crypto-tab-merkle"
          className={`space-y-6 ${activeTab === 'merkle' ? '' : 'hidden'}`}
        >
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-white text-sm flex items-center gap-2">
                <i className="fa-solid fa-network-wired text-cyan-400"></i> Merkle Tree Audit Root Calculator
              </h3>
              <span className="text-[10px] font-mono text-cyan-400">SOC 2 Type II Non-Repudiation</span>
            </div>
            <p className="text-xs text-slate-300">
              Enter comma or newline-separated audit strings, transactions, or leaf records. The cryptographic engine iteratively combines pairs with SHA-256 to calculate an immutable Merkle Root.
            </p>
            <div className="space-y-3 text-xs">
              <textarea
                id="crypto-merkle-input"
                rows={4}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono text-xs"
                placeholder="INVOICE-001&#10;BOARD-RES-001&#10;PAYROLL-MAY-2026&#10;SRE-BACKUP-SNAP-01"
              ></textarea>
              <button
                onClick={() => callGlobal('executeMerkleTree')}
                className="w-full py-2 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white font-bold rounded-lg transition flex items-center justify-center gap-2"
              >
                <i className="fa-solid fa-tree"></i> Generate Cryptographic Merkle Root
              </button>
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-slate-500 uppercase font-bold text-[10px]">Merkle Root Hash:</span>
                  <span id="crypto-merkle-cert" className="text-cyan-400 font-mono text-[11px]">
                    --
                  </span>
                </div>
                <div id="crypto-merkle-root" className="text-cyan-300 font-mono text-xs break-all select-all font-bold">
                  --
                </div>
                <div id="crypto-merkle-leaves" className="text-slate-400 font-mono text-[11px] pt-1 border-t border-slate-800/80"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* OPERATIONS MODAL 3: Event Payload Viewer */}
      <div id="modal-ops-payload-viewer" className="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
        <div className="bg-slate-900 rounded-2xl shadow-2xl border border-slate-700 max-w-xl w-full overflow-hidden">
          <div className="p-4 bg-gradient-to-r from-slate-950 via-slate-900 to-cyan-950 text-white flex items-center justify-between">
            <div className="flex items-center gap-2">
              <i className="fa-solid fa-code text-cyan-400"></i>
              <h3 id="ops-payload-modal-title" className="font-bold text-sm">
                Cryptographic Event Payload
              </h3>
            </div>
            <button
              onClick={() => {
                const el = document.getElementById('modal-ops-payload-viewer');
                if (el) el.classList.add('hidden');
              }}
              className="text-slate-400 hover:text-white p-1"
            >
              <i className="fa-solid fa-xmark text-sm"></i>
            </button>
          </div>
          <div className="p-5 space-y-3">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>
                Event Code: <strong id="ops-payload-event-code" className="text-cyan-300 font-mono">--</strong>
              </span>
              <span>
                Actor: <strong id="ops-payload-actor" className="text-slate-200">--</strong>
              </span>
            </div>
            <pre id="ops-payload-json-content" className="p-4 bg-slate-950 rounded-xl border border-slate-800 text-cyan-300 font-mono text-xs overflow-x-auto max-h-96"></pre>
            <div className="flex justify-end pt-2">
              <button
                onClick={() => {
                  const el = document.getElementById('modal-ops-payload-viewer');
                  if (el) el.classList.add('hidden');
                }}
                className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CryptoToolsView;
