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

    # tea contracnt addresses
    Cha_Dao_Sheng_Cha = "0x895d95aBFf11C594F3E73eFC2023AA1cB5dEA2E3"
    Dashu_Sheng_Xiaobing = "0x2BeF9A0B45Fd9f9a52198FbFa1c39472A84A1106"
    Menghai = "0xdb890A8f2Ee01Ce58A69B7a1d8E80bd4D28Bf034"
    Purple_Sheng = "0x2BA062A4DBDD376D36bc3D3a075833b102EbB58f"
    Ye_Sheng_Qiao_Mu_Sheng_Bing = "0x5D4B2d9e5c05783C7d29f17c5cDf00bfE1d0285E"
    Yunhai_Sheng_Cha = "0xbFB86EbD5eF3660eD1F56B09661D016841727A5F"
    
    #tea tokenURI
    Cha_Dao_Sheng_Cha_uri = "https://956d334ec241ad80399eb1fcfc13d462.ipfscdn.io/ipfs/QmRutGgkRwpC1EzahGXkC3UGuywLonkuoNCRHhtgzbAMbD"
    Dashu_Sheng_Xiaobing_uri = "https://956d334ec241ad80399eb1fcfc13d462.ipfscdn.io/ipfs/QmQCgeEzxEnYLkNKj9KYsanVFVy6fgzN97Jjq1SkLkTycj"
    Menghai_uri = "https://956d334ec241ad80399eb1fcfc13d462.ipfscdn.io/ipfs/QmQsZw4dhPaMJfVtn8vBVpi2RuhDLoTrjdkwwhWMjmCHQV"
    Purple_Sheng_uri = "https://956d334ec241ad80399eb1fcfc13d462.ipfscdn.io/ipfs/QmSJ7mcProY8Q3JYiP3iGEd2Kb9ZEiexLHPdEN3Xznh1a4"
    Ye_Sheng_Qiao_Mu_Sheng_Bing_uri = "https://956d334ec241ad80399eb1fcfc13d462.ipfscdn.io/ipfs/QmU6iAHqXBMnVrjh35ywukoq6qgj1eUFdJZdsV7iksbeoV"
    Yunhai_Sheng_Cha_uri = "https://956d334ec241ad80399eb1fcfc13d462.ipfscdn.io/ipfs/QmX71qPMg9rfmBZEjccrwXKG6sHFif5DcBz57QXpRnJ8UP"

    # ETH Funding Contract
    teaContract_addr = Cha_Dao_Sheng_Cha
    teaContract_abi = "./contract/TEA_Exchange.abi"
    teaContract = get_contract(web3, teaContract_addr, teaContract_abi)
    teaContract_owner = teaContract.functions.owner().call()


    # ## transaction part
    # tokenURI = Cha_Dao_Sheng_Cha_uri
    # tokenId = 0
    # mint(web3, teaContract, MY_TESTMAIN, MY_TESTMAIN_PK, tokenId, tokenURI)
    dests = []
    tokenIds = []
    tokenURIs = []
    for i in range(20):
        dests.append(MY_TESTMAIN)
        tokenId = i+1
        tokenIds.append(tokenId)
        tokenURIs.append(Cha_Dao_Sheng_Cha_uri)
    
    multiMint(web3, teaContract, MY_TESTMAIN, MY_TESTMAIN_PK, dests, tokenIds, tokenURIs)

