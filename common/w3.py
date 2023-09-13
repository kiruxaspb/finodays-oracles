# create an account using the private key
account = w3.eth.account.privateKeyToAccount(private_key)

# при наличии большего количества оракулов массив должен быть расширен
oracles_addresses = ["0x6a50a7e7ae42068d8aa60a8e03cb9e446db1d1d5", "0x87e59c295463890a0265ec8527b8559bf6181458", "0xd07348b02e5a6aa5efdb073d6c26ba274f3c7318"]

# sepolia - https://sepolia.infura.io/v3/92a117f286914f259e30d3338aad054d
# localhost hardhat - localhost:8545
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/92a117f286914f259e30d3338aad054d'))

# load the contract's ABI for iteract
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"system","type":"address"},{"internalType":"uint256[]","name":"resourceIds","type":"uint256[]"},{"internalType":"uint256[]","name":"rates","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"productId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"oldRate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newRate","type":"uint256"}],"name":"RateChange","type":"event"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"}],"name":"getProductRateById","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"uint256","name":"newProductRate","type":"uint256"}],"name":"setProductRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# Replace with the contract address
contract_address = 'CONTRACT_ADDRESS'

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Send a transaction to a contract function
transaction = contract.functions.setProductRate(product, rate).buildTransaction({
    'chainId': 1,  # Chain ID of the network
    'gas': 2000000,  # Gas limit
    'gasPrice': w3.toWei('101', 'gwei'),  # Gas price in Wei
    'nonce': w3.eth.getTransactionCount(account.address),
})

# Sign the transaction
signed_transaction = account.signTransaction(transaction)

# Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
print(f"Transaction Hash: {tx_hash.hex()}")