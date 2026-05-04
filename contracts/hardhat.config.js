import { existsSync, readFileSync } from "node:fs";
import hardhatToolboxMochaEthers from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import { configVariable, defineConfig } from "hardhat/config";

function loadLocalEnv() {
  const envUrl = new URL(".env", import.meta.url);
  if (!existsSync(envUrl)) {
    return;
  }

  for (const rawLine of readFileSync(envUrl, "utf8").split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }
    const match = /^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/.exec(line);
    if (!match) {
      continue;
    }
    const [, key, rawValue] = match;
    let value = rawValue.trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
}

loadLocalEnv();

const solcSettings = {
  evmVersion: "cancun"
};

export default defineConfig({
  plugins: [hardhatToolboxMochaEthers],
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  solidity: {
    profiles: {
      default: {
        version: "0.8.24",
        settings: solcSettings
      },
      production: {
        version: "0.8.24",
        settings: {
          ...solcSettings,
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      }
    }
  },
  networks: {
    hardhatMainnet: {
      type: "edr-simulated",
      chainType: "l1"
    },
    og: {
      type: "http",
      chainType: "l1",
      chainId: 16661,
      url: configVariable("OG_RPC_URL"),
      accounts: [configVariable("OG_PRIVATE_KEY")]
    },
    ogGalileo: {
      type: "http",
      chainType: "l1",
      chainId: 16602,
      url: configVariable("OG_GALILEO_RPC_URL"),
      accounts: [configVariable("OG_GALILEO_PRIVATE_KEY")]
    }
  }
});
