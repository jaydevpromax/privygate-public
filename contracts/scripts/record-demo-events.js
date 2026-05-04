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

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`${name} is required`);
  }
  return value;
}

function bytes32Label(label) {
  return ethers.encodeBytes32String(label);
}

function hashLabel(label) {
  return ethers.keccak256(ethers.toUtf8Bytes(label));
}

async function waitAndLog(label, txPromise) {
  const tx = await txPromise;
  const receipt = await tx.wait();
  console.log(`${label}: ${receipt.hash}`);
  console.log(`${label} explorer: ${explorerTxUrl(receipt.hash)}`);
  return receipt;
}

async function main() {
  const chain = await ethers.provider.getNetwork();
  const address = requireEnv("PRIVYGATE_REGISTRY_ADDRESS");
  const registry = await ethers.getContractAt("PrivyGateRegistry", address);

  console.log(`Network: ${connection.networkName}`);
  console.log(`Chain ID: ${chain.chainId}`);
  console.log(`Registry: ${address}`);

  const universityId = bytes32Label("University");
  const labId = bytes32Label("Lab");
  const policyId = bytes32Label("ResearchPolicy");
  const credentialHash = hashLabel("Alice:Lab:role:researcher");

  await waitAndLog(
    "registerAuthority(University)",
    registry.registerAuthority(universityId, hashLabel("University public key"))
  );
  await waitAndLog(
    "registerAuthority(Lab)",
    registry.registerAuthority(labId, hashLabel("Lab public key"))
  );
  await waitAndLog(
    "registerPolicy(ResearchPolicy)",
    registry.registerPolicy(policyId, hashLabel("University:student AND Lab:researcher"))
  );
  await waitAndLog(
    "recordVerification(success)",
    registry.recordVerification(policyId, hashLabel("Alice proof accepted"), true)
  );
  await waitAndLog("setRevoked(Alice researcher)", registry.setRevoked(credentialHash, true));
  await waitAndLog(
    "recordVerification(after revocation)",
    registry.recordVerification(policyId, hashLabel("Alice proof rejected after revocation"), false)
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
