import { network } from "hardhat";

const connection = await network.create();
const { ethers } = connection;

function explorerBase() {
  if (connection.networkName === "ogGalileo") {
    return process.env.OG_GALILEO_EXPLORER_URL || "https://chainscan-galileo.0g.ai";
  }
  return process.env.OG_EXPLORER_URL || "https://chainscan.0g.ai";
}

function explorerTxUrl(hash) {
  return `${explorerBase().replace(/\/$/, "")}/tx/${hash}`;
}

function explorerAddressUrl(address) {
  return `${explorerBase().replace(/\/$/, "")}/address/${address}`;
}

async function main() {
  const chain = await ethers.provider.getNetwork();
  const Registry = await ethers.getContractFactory("PrivyGateRegistry");
  const registry = await Registry.deploy();
  await registry.waitForDeployment();

  const address = await registry.getAddress();
  const deploymentTx = registry.deploymentTransaction();

  console.log(`Network: ${connection.networkName}`);
  console.log(`Chain ID: ${chain.chainId}`);
  console.log(`PrivyGateRegistry deployed at: ${address}`);
  console.log(`Explorer contract: ${explorerAddressUrl(address)}`);
  if (deploymentTx?.hash) {
    console.log(`Deployment tx: ${deploymentTx.hash}`);
    console.log(`Explorer tx: ${explorerTxUrl(deploymentTx.hash)}`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
