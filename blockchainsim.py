import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash, proof):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Generate SHA-256 hash of the block."""
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "proof": self.proof
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()

class Blockchain:
    def __init__(self):
        """Initialize the blockchain with a genesis block."""
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(index=0, transactions=["Genesis Block"], previous_hash="0", proof=1)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """Simple proof-of-work algorithm."""
        new_proof = 1
        while True:
            hash_attempt = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_attempt[:4] == "0000":
                return new_proof
            new_proof += 1

    def add_block(self, transactions):
        """Add a new block with given transactions."""
        last_block = self.get_last_block()
        proof = self.proof_of_work(last_block.proof)
        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=last_block.hash,
            proof=proof
        )
        self.chain.append(new_block)
        print("Block added successfully!")

    def is_chain_valid(self):
        """Check if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def tamper_block(self, index, new_data):
        """Modify a block's transactions to simulate tampering."""
        if 0 < index < len(self.chain):
            self.chain[index].transactions = new_data
            self.chain[index].hash = self.chain[index].calculate_hash()
            print("Block tampered successfully!")
        else:
            print("Invalid block index")

    def print_chain(self):
        """Print the blockchain in a readable format."""
        for block in self.chain:
            print(json.dumps(vars(block), indent=4))

if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block(["Prathamesh pays Raj 1 BTC", "Raj pays Gourav 0.5 BTC"])  # Pre-added block

    while True:
        print("\nMenu:")
        print("1. Add a new block")
        print("2. Print blockchain")
        print("3. Validate blockchain")
        print("4. Tamper with a block")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            transactions = input("Enter transactions (comma-separated): ").split(",")
            blockchain.add_block(transactions)
        elif choice == "2":
            blockchain.print_chain()
        elif choice == "3":
            print("Is blockchain valid?", blockchain.is_chain_valid())
        elif choice == "4":
            index = int(input("Enter block index to tamper: "))
            new_data = input("Enter new transactions (comma-separated): ").split(",")
            blockchain.tamper_block(index, new_data)
        elif choice == "5":
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")
