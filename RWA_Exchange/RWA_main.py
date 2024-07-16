# Essential
from web3 import Web3

# env
import os
from dotenv import load_dotenv


def connect_web3(connect_host, apikey):
    # Mainnet #
    if connect_host == "ethereum":
        rpc_url = "https://mainnet.infura.io/v3/" + apikey
    elif connect_host == "polygon":
        rpc_url = "https://polygon-mainnet.infura.io/v3/" + apikey
    # Testnet #
    elif connect_host == "sepolia":
        rpc_url = "https://sepolia.infura.io/v3/" + apikey
    elif connect_host == "amoy":
        rpc_url = "https://polygon-amoy.infura.io/v3/" + apikey
    else:
        return None
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    return web3


def get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, "r", encoding="utf-8")
    contractAddr = web3.to_checksum_address(contractAddress)
    contract = web3.eth.contract(abi=file.read(), address=contractAddr)

    return contract


def mint(
    web3,
    teaContract,
    minter,
    minter_pk,
    tokenId,
    tokenURI
):
    To_add = web3.to_checksum_address(minter)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(To_add)
    tx = teaContract.functions.mint(
        To_add, tokenId, tokenURI
    ).build_transaction({"from": To_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, minter_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def multiMint(
    web3,
    teaContract,
    minter,
    minter_pk,
    dests,
    tokenIds,
    tokenURIs
):
    To_add = web3.to_checksum_address(minter)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(minter)
    tx = teaContract.functions.multiMint(
        dests, tokenIds, tokenURIs
    ).build_transaction({"from": To_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, minter_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def burn(
    web3,
    teaContract,
    to,
    to_pk,
    tokenId
):
    To_add = web3.to_checksum_address(to)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(To_add)
    tx = teaContract.functions.burn(tokenId).build_transaction({"from": To_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, to_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


if __name__ == "__main__":
    load_dotenv("../.env")
    INFURA_KEY = os.getenv("INFURA_API_KEY")
    MY_TESTMAIN = os.getenv("MY_TESTMAIN")
    MY_TESTMAIN_PK = os.getenv("MY_TESTMAIN_PK")
    MY_TESTTEST = os.getenv("MY_TESTTEST")
    MY_TESTTEST_PK = os.getenv("MY_TESTTEST_PK")

    # WEB3 setup
    network = "amoy"
    web3 = connect_web3(network, INFURA_KEY)

    Token_to_NFT_contract_address = ""

    NFTs_contract_address = "0x12e030CCaB2cc841E4b66e89f46D433F8bF6FA8E"


    ## transaction part
    tokenURI = Cha_Dao_Sheng_Cha_uri
    tokenId = 0
    mint(web3, teaContract, MY_TESTMAIN, MY_TESTMAIN_PK, tokenId, tokenURI)

    