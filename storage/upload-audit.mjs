import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { ethers } from "ethers";
import { Indexer, MemData } from "@0gfoundation/0g-storage-ts-sdk";

const manifestPath = resolve(process.cwd(), process.argv[2] ?? "../docs/hackathon/privygate_0g_storage_audit_manifest.json");
const rpcUrl = process.env.OG_RPC_URL ?? "https://evmrpc.0g.ai";
const indexerRpc = process.env.OG_STORAGE_INDEXER_RPC ?? "https://indexer-storage-turbo.0g.ai";
const privateKey = process.env.OG_PRIVATE_KEY ?? process.env.PRIVATE_KEY;

if (!privateKey) {
  console.error("Missing OG_PRIVATE_KEY or PRIVATE_KEY in the shell environment.");
  process.exit(1);
}

const payload = await readFile(manifestPath);
const provider = new ethers.JsonRpcProvider(rpcUrl);
const signer = new ethers.Wallet(privateKey, provider);
const indexer = new Indexer(indexerRpc);
const data = new MemData(payload);

const [tree, treeErr] = await data.merkleTree();
if (treeErr !== null) {
  throw new Error(`Merkle tree error: ${treeErr}`);
}

const [tx, uploadErr] = await indexer.upload(data, rpcUrl, signer);
if (uploadErr !== null) {
  throw new Error(`0G Storage upload error: ${uploadErr}`);
}

const result = {
  manifestPath,
  rpcUrl,
  indexerRpc,
  rootHash: tx.rootHash ?? tree?.rootHash?.(),
  txHash: tx.txHash,
};

console.log(JSON.stringify(result, null, 2));
