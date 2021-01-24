# Blockchain Implementation

### Dependencies

1. Flask (for Web App)
2. hashlib (for hashing blocks)
3. datetime (for timestamping blocks)

### Usage

1. install dependencies
2. run blockchain.py with `py blockchain.py`
3. To Mine new block:
   - create GET request at [localhost:5000/mine](http://localhost:5000/mine)
   - **Note**: wait for a request to give response. Multiple requests creates blocks with same previous blocks and fails sanity check
4. To get complete chain:
   1. create GET request at [localhost:5000/chain](http://localhost/chain)
5. To check sanity:
   1. create GET request at [localhost/chain](http://localhost/chain)

**Note:**

- Use postman to create requests
- By replace localhost with IPv4 Address to access it via other systems on same network

### TODO:

- [x] Implement basic blockchain
- [ ] Incorporate custom data in blocks
- [ ] Create custom cryptocurrency
- [ ] Create smart contracts
