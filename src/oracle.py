from web3 import Web3
import json
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from secret import operator_private_key

# create an account using the private key
account = w3.eth.account.privateKeyToAccount(private_key)

# при наличии большего количества оракулов массив должен быть расширен
oracles_addresses = ["0x6a50a7e7ae42068d8aa60a8e03cb9e446db1d1d5", "0x87e59c295463890a0265ec8527b8559bf6181458", "0xd07348b02e5a6aa5efdb073d6c26ba274f3c7318"]

# localhost hardhat - localhost:8545
# one more sandbox - sepolia testnet
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# load the contract's ABI for iteract
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"system","type":"address"},{"internalType":"uint256[]","name":"resourceIds","type":"uint256[]"},{"internalType":"uint256[]","name":"rates","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"productId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"oldRate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newRate","type":"uint256"}],"name":"RateChange","type":"event"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"}],"name":"getProductRateById","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"uint256","name":"newProductRate","type":"uint256"}],"name":"setProductRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

app = Flask(__name__)

#Russia
resourceIds1 = [1, 3, 4, 5]
prices1 = [20, 30, 10, 5]

#China
resourceIds2 = [1, 2]
prices2 = [50, 100]
  
#India
resourceIds3 = [1, 3, 4]
prices3 = [10, 20, 5]

def execute(address, id, rate):
    # Create a contract instance
    contract = w3.eth.contract(address=address, abi=contract_abi)

    # Send a transaction to a contract function
    transaction = contract.functions.setProductRate(product, rate).buildTransaction({
        'chainId': 31337,  # Chain ID of the network
        # hardhat
        'gas': 2000000,  # Gas limit
        'gasPrice': w3.toWei('101', 'gwei'),  # Gas price in Wei
        'nonce': w3.eth.getTransactionCount(account.address),
    })

    # Sign the transaction
    signed_transaction = account.signTransaction(transaction)

    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print(f"Transaction Hash: {tx_hash.hex()}")

def update_prices():
    #gold rate
    url1 = 'https://api.example.com/data'
    response = requests.get(url1)
    if response.status_code == 200:
        data = response.json()  # Разбор ответа как JSON (если сервер возвращает JSON)
        rate = data["price"]
        print('Actual price:', rate)

        get_rate_from_smart_contract = contract.functions.getProductRateById(resourceIds1[0]).call()

        if get_rate_from_smart_contract != rate:
            #update in smart contract
            execute(oracles_addresses[0], resourceIds1[0], data["price"])
    else:
        print('ERR:', response.status_code)


    #nikel rate
    url2 = 'https://api.example.com/data2'
    response = requests.get(url2)
    if response.status_code == 200:
        data = response.json()  # Разбор ответа как JSON (если сервер возвращает JSON)
        rate = data["price"]
        print('Actual price:', rate)

        get_rate_from_smart_contract = contract.functions.getProductRateById(resourceIds1[0]).call()

        if get_rate_from_smart_contract != rate:
            #update in smart contract
            execute(oracles_addresses[0], resourceIds1[1], data["price"])
    else:
        print('ERR:', response.status_code)


    #neft rate
    url3 = 'https://api.example.com/data3'
    response = requests.get(url3)
    if response.status_code == 200:
        data = response.json()  # Разбор ответа как JSON (если сервер возвращает JSON)
        rate = data["price"]
        print('Actual price:', rate)
        
        get_rate_from_smart_contract = contract.functions.getProductRateById(resourceIds1[0]).call()

        if get_rate_from_smart_contract != rate:
            #update in smart contract
            execute(oracles_addresses[0], resourceIds1[2], data["price"])
    else:
        print('ERR:', response.status_code)


    #gaz
    url4 = 'https://api.example.com/data4'
    response = requests.get(url4)
    if response.status_code == 200:
        data = response.json()  # Разбор ответа как JSON (если сервер возвращает JSON)
        rate = data["price"]
        print('Actual price:', rate)

        get_rate_from_smart_contract = contract.functions.getProductRateById(resourceIds1[0]).call()

        if get_rate_from_smart_contract != rate:
            #update in smart contract
            execute(oracles_addresses[0], resourceIds1[3], data["price"])
    else:
        print('ERR:', response.status_code)


def update():
    print("Update rates executing")
    update_prices()

scheduler = BackgroundScheduler()
# обновление рейтров с интеравалом seconds
# for tests 10 секунд
scheduler.add_job(update, 'interval', seconds=5)

scheduler.start()

@app.route('/')
def index():
    return "Oracle is up!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
