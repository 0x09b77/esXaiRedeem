from web3 import Web3

def check_token_balance(w3, account_address, token_contract_address, token_contract_abi):
    token_contract = w3.eth.contract(address=token_contract_address, abi=token_contract_abi)
    balance = token_contract.functions.balanceOf(account_address).call()
    return balance

def check_decimals(w3, account_address, token_contract_address, token_contract_abi):
    token_contract = w3.eth.contract(address=token_contract_address, abi=token_contract_abi)
    decimals = token_contract.functions.decimals.call()
    return decimals