import { network } from "hardhat";

const connection = await network.create();
const { ethers } = connection;

async function main() {
  const chain = await ethers.provider.getNetwork();
  const [signer] = await ethers.getSigners();
  const address = await signer.getAddress();
  const balance = await ethers.provider.getBalance(address);

  console.log(`Network: ${connection.networkName}`);
  console.log(`Chain ID: ${chain.chainId}`);
  console.log(`Signer: ${address}`);
  console.log(`Balance: ${ethers.formatEther(balance)} OG`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
