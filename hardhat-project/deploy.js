const hardhat = require("hardhat");

async function main() {
    const Cha_Dao_Sheng_Cha = await hardhat.ethers.getContractFactory("Cha_Dao_Sheng_Cha");

    const contract = await Cha_Dao_Sheng_Cha.deploy();

    console.log(contract.target)
}

main();