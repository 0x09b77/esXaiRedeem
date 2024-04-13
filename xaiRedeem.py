from web3 import Web3, HTTPProvider
from web3.contract import Contract
from datetime import datetime
import HP_ERC20
import esXai
import time
import sys
import schedule

w3: Web3
token_contract: Contract
account_address: str # = Web3.to_checksum_address('0xdb58d9bb95ae6878078e6451efd3ae4a2f6d1e15')
account_private_key: str
redeemption_time: int

redeemption_address = Web3.to_checksum_address(esXai.esXai_redeemption_contract_address)
token_contract_address = Web3.to_checksum_address(esXai.contract_address)

def redeem(balance):
    tokens_to_redeem = w3.to_wei(balance, 'ether')
    redeem_contract = w3.eth.contract(address=redeemption_address, abi=esXai.esXai_redeemption_contract_abi)
    gas_price = w3.to_wei(20, 'gwei')
    tx = redeem_contract.functions.startRedemption(tokens_to_redeem, redeemption_time).build_transaction({
    'chainId': 42161,
    'gas': 200000,
    'gasPrice': gas_price,
    'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(account_address))
    })
    signed_tx = w3.eth.account.sign_transaction(tx, account_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status:
        print(f"The transaction was successful {balance} esXai send to redeem contract")
    else:
        print("Trx failed. will retry later")

def checkAll():
    token_balance = HP_ERC20.check_token_balance(w3, Web3.to_checksum_address(account_address), token_contract_address, esXai.esXai_contract_abi)
    current_datetime = datetime.now()
    print(f'balance of tokens on acc {account_address}: {token_balance}, time: {current_datetime.strftime("%d.%m.%Y, %H:%M")}')
    balance_in_ethers = w3.from_wei(token_balance, 'ether')
    if balance_in_ethers > 1:
        truncated_balance = int(balance_in_ethers)
        redeem(truncated_balance)

if __name__ == "__main__":
    account_address = input("input your address: ")
    account_private_key = input("input your private key: ")
    redeemption_time = int(input("enter redeemption rate in seconds - 180(15552000), 90(7776000), 15(1296000) : "))
    if not redeemption_time == 15552000 or redeemption_time == 7776000 or redeemption_time == 1296000:
        print("wrong redeemption rate!")
        sys.exit()
    w3 = Web3(HTTPProvider('https://1rpc.io/arb'))
    token_contract = w3.eth.contract(address=token_contract_address, abi=esXai.esXai_contract_abi)
    schedule.every().hour.do(checkAll)
    while True:
        schedule.run_pending()
        time.sleep(1)