const hardhat = require("hardhat");

async function main() {
    const NFTs = await hardhat.ethers.getContractFactory("NFTs");

    const contract = await NFTs.deploy();

    console.log(contract.target)
}

main();