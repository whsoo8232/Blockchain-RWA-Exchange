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


def mint(web3, contract, minter, minter_pk, tokenId, tokenURI):
    To_add = web3.to_checksum_address(minter)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(To_add)
    tx = contract.functions.mint(To_add, tokenId, tokenURI).build_transaction(
        {"from": To_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, minter_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def multiMint(web3, contract, minter, minter_pk, dests, tokenIds, tokenURIs):
    To_add = web3.to_checksum_address(minter)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(minter)
    tx = contract.functions.multiMint(dests, tokenIds, tokenURIs).build_transaction(
        {"from": To_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, minter_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def burn(web3, contract, To, To_pk, tokenId):
    To_add = web3.to_checksum_address(To)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(To_add)
    tx = contract.functions.burn(tokenId).build_transaction(
        {"from": To_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, To_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def NFT_tranferFrom(web3, contract, From, From_pk, To, tokenId):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = contract.functions.transferFrom(From_add, To_add, tokenId).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
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

    # NFT contract setup
    NFTs_contract_address = "0x12e030CCaB2cc841E4b66e89f46D433F8bF6FA8E"
    NFTs_contract_abi = "./contracts/NFTs.abi"
    NFTs_contract = get_contract(web3, NFTs_contract_address, NFTs_contract_abi)
    # tradeNFT contract setup
    tradeNFT_contract_address = "0x96EE75129c7a76107ff204400aFbe71FC122cb00"
    tradeNFT_contract_abi = "./contracts/tradeNFT.abi"
    tradeNFT_contract = get_contract(
        web3, tradeNFT_contract_address, tradeNFT_contract_abi
    )
    # USDT contract setup
    USDT_contract_addr = "0xc0adb3cA9c756D5C12d08CF5FD8168d088A9E46d"
    USDT_contract_abi = "./contracts/payToken.abi"
    USDT_contract = get_contract(web3, USDT_contract_addr, USDT_contract_abi)

    # checksum_addresses
    NFT_buyer = web3.to_checksum_address(MY_TESTTEST)
    NFT_owner = web3.to_checksum_address(MY_TESTMAIN)
    tradeContract = web3.to_checksum_address(tradeNFT_contract_address)

    # # trade setup
    # id = 1
    # tokenId = 1
    # tokenPrice = 0.1
    # # Approve NFT to contract
    # gas_price = web3.eth.gas_price
    # nonce = web3.eth.get_transaction_count(NFT_owner)
    # tx = NFTs_contract.functions.approve(tradeContract, tokenId).build_transaction(
    #     {"from": NFT_owner, "nonce": nonce, "gasPrice": gas_price}
    # )
    # signed_txn = web3.eth.account.sign_transaction(tx, MY_TESTMAIN_PK)
    # txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    # print(tx_receipt)
    # # trade_NFT_with_ETH
    # gas_price = web3.eth.gas_price
    # nonce = web3.eth.get_transaction_count(NFT_buyer)
    # tx = tradeNFT_contract.functions.trade_NFT_with_ETH(
    #     id, tokenId, int(tokenPrice * 1e18)
    # ).build_transaction(
    #     {
    #         "from": NFT_buyer,
    #         "nonce": nonce,
    #         "gasPrice": gas_price,
    #         "value": int(tokenPrice * 1e18),
    #     }
    # )
    # signed_txn = web3.eth.account.sign_transaction(tx, MY_TESTTEST_PK)
    # txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    # print(tx_receipt)

    # trade setup
    id = 2
    tokenId = 3
    tokenPrice = 100
    # Approve NFT to contract
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(NFT_owner)
    tx = NFTs_contract.functions.approve(tradeContract, tokenId).build_transaction(
        {"from": NFT_owner, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, MY_TESTMAIN_PK)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    # Approve msg.senders USDT to contract
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(NFT_buyer)
    tx = USDT_contract.functions.approve(
        tradeContract, int(tokenPrice * 1e18)
    ).build_transaction({"from": NFT_buyer, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, MY_TESTTEST_PK)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    # trade_NFT_with_USDT
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(NFT_buyer)
    tx = tradeNFT_contract.functions.trade_NFT_with_USDT(
        id, tokenId, int(tokenPrice * 1e18)
    ).build_transaction(
        {
            "from": NFT_buyer,
            "nonce": nonce,
            "gasPrice": gas_price,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, MY_TESTTEST_PK)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
