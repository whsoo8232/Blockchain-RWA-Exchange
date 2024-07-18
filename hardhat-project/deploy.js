const hardhat = require("hardhat");

async function main() {
    const tradeNFT = await hardhat.ethers.getContractFactory("tradeNFT");

    const contract = await tradeNFT.deploy();

    console.log(contract.target)
}

main();