## structure of block
1.Block:
      --> A block stores:
          index:block number
          timestamp:when block created
          transactions:data stored 
          previous hash:link of the previous hash
          hash:unique fingerprint of the block
2.Blockchain:
   a chain of blocks where each block links to the previous one using previous_hash.
    if one block changes,its hash changes then entire chain breaks ,ensures security.
3.Hashing:
   converts block data to fixed-length unique string ussing SHA-256.
why this structure is important:
  immutability:data cant be changed without detection.
  security
 transparancy:anyone can verify the data integrity.
