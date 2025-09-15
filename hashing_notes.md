# Day 2 - Hashing Basics (Week 2)
*Date:* <Today's Date>  
*Author:* Pavan Teja Kodavati  

---

## What is Hashing?
Hashing is a one-way function that converts any data into a fixed-length string (hash).  

Example:  
- Input: "Blockchain"  
- Hash (SHA-256): a long fixed-length string  

---

## Why SHA-256?
- Secure Hash Algorithm 256-bit
- Used in Bitcoin & most blockchains
- Fast + Collision-resistant

---

## Avalanche Effect
- Tiny change in input → Completely different hash
- Ensures security & data integrity  

Example:  
"Blockchain" → Hash1  
"blockchain" → Hash2 (Totally different!)

---

## Role in Blockchain
- Each block stores data + hash
- Any change in data → hash changes → tampering detected