# Lamport-Merkle Tree Based Post-Quantum Digital Signature System

## 🔐 Project Overview
The rise of quantum computing poses a threat to traditional public-key cryptographic algorithms (e.g., RSA, ElGamal) that rely on mathematical hardness assumptions. This project implements a **hash-based quantum-resistant digital signature scheme** by combining the **Lamport Signature** with a **Merkle Tree**. The system is implemented in Python and features a client-server communication model using sockets to exchange and verify messages.

## 📁 Project Structure
```
├── client.py         # Implements Lamport signature generation, Merkle tree, and client socket communication
├── Server.py         # Handles server-side socket communication and echo response
└──  README.md         # Documentation
```

## 🧠 Core Technologies
### 1. Lamport Signature
- A one-time digital signature scheme based on hash functions
- **Advantages**:
  - Secure against quantum attacks (no number theory involved)
  - Simple structure
- **Disadvantages**:
  - One-time use only
  - Large key sizes (2 x 256 values)

**Signature Generation Process:**
1. Generate two sets of 256 random 256-bit values as the private key.
2. Hash each to form the public key.
3. Hash the message and select private key values based on each bit (0 → set A, 1 → set B).

**Verification Process:**
- Hash the message again.
- Hash the signature values and compare them with the corresponding public key values.

### 2. Merkle Tree
- Used to compress multiple Lamport public keys into a single root hash
- Allows reusability of one-time signatures by verifying a public key through a Merkle proof

### 3. Socket Communication
- Built using Python’s `socket` module
- Client sends user-input message to server
- Server echoes back the message
- Lamport signature and Merkle Tree root hash are computed on the client

## 🛠 How to Run
### 1. Run the server
```bash
python Server.py
```

### 2. Run the client (in a separate terminal)
```bash
python client.py
```

### Example Workflow
- User inputs a message in the client terminal
- The message is sent to the server and echoed back
- A Lamport signature is generated for the message
- A Merkle Tree is constructed from public keys
- The root hash is printed and the signature is verified

## 🧾 Key Functions Summary
| Function | Description |
|----------|-------------|
| `generate_private_key()` | Creates two sets of 256-bit random values as private key |
| `generate_public_key(private_key)` | Hashes private key values to form the public key |
| `generate_signature(message, private_key)` | Signs a message by selecting appropriate private key values based on hash bits |
| `verify_signature(message, signature, public_key)` | Validates the signature using the public key and message hash |
| `MerkleTree(leaf_values)` | Constructs a Merkle Tree from public keys and computes the root hash |

## ⚖️ Pros and Cons
**Pros:**
- Post-quantum secure
- Simple and efficient with basic hash operations

**Cons:**
- Large key sizes
- One-time use constraint (partially addressed via Merkle Tree)
- Requires key pair pre-generation

## 💡 Extensibility
- The Merkle Tree module is designed for modularity: any key algorithm (not only Lamport) can be used as leaf values.
- The number of leaf nodes (signable messages) is adjustable via `leaf_node_count`.

## 📚 References
- [Merkle Tree Explained](https://www.lesstif.com/security/merkle-tree-125305097.html)
- [Understanding Digital Signatures](https://m.blog.naver.com/jvioonpe/221384924295)
- [Quantum Computing Impact](https://www.lgcns.com/blog/it-trend/38169/)
- [Python Socket Tutorial](https://duri1994.github.io/python/python-socket-network/)

## 👥 Team Notes
This project was developed as a part of a cryptography challenge contest. It demonstrates an end-to-end implementation of a quantum-resistant signature scheme and secure communication using Python.

---

> ⚠️ Disclaimer: This system is intended for educational and research purposes only. For real-world applications, use NIST PQC-standardized cryptographic libraries.
