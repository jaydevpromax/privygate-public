import { expect } from "chai";
import { network } from "hardhat";

const { ethers } = await network.create();

const AUTHORITY_ID = ethers.encodeBytes32String("University");
const POLICY_ID = ethers.encodeBytes32String("ResearchPolicy");
const PUBLIC_KEY_HASH = ethers.keccak256(ethers.toUtf8Bytes("university-public-key"));
const POLICY_HASH = ethers.keccak256(ethers.toUtf8Bytes("University:student AND Lab:researcher"));
const CREDENTIAL_HASH = ethers.keccak256(ethers.toUtf8Bytes("Alice:Lab:role:researcher"));
const PROOF_HASH = ethers.keccak256(ethers.toUtf8Bytes("accepted-proof"));

async function deployRegistry() {
  const [owner, other] = await ethers.getSigners();
  const Registry = await ethers.getContractFactory("PrivyGateRegistry");
  const registry = await Registry.deploy();
  await registry.waitForDeployment();
  return { registry, owner, other };
}

describe("PrivyGateRegistry", function () {
  it("registers an authority and returns its public key hash", async function () {
    const { registry, owner } = await deployRegistry();

    await expect(registry.registerAuthority(AUTHORITY_ID, PUBLIC_KEY_HASH))
      .to.emit(registry, "AuthorityRegistered")
      .withArgs(AUTHORITY_ID, PUBLIC_KEY_HASH, owner.address);

    expect(await registry.isAuthorityRegistered(AUTHORITY_ID)).to.equal(true);
    const record = await registry.getAuthority(AUTHORITY_ID);
    expect(record.publicKeyHash).to.equal(PUBLIC_KEY_HASH);
    expect(record.registrar).to.equal(owner.address);
    expect(record.active).to.equal(true);
    expect(record.registeredAt).to.be.greaterThan(0n);
  });

  it("limits authority status changes to the registrar", async function () {
    const { registry, other } = await deployRegistry();
    await registry.registerAuthority(AUTHORITY_ID, PUBLIC_KEY_HASH);

    await expect(registry.connect(other).setAuthorityActive(AUTHORITY_ID, false))
      .to.be.revertedWithCustomError(registry, "NotAuthorityRegistrar")
      .withArgs(AUTHORITY_ID, other.address);

    await expect(registry.setAuthorityActive(AUTHORITY_ID, false))
      .to.emit(registry, "AuthorityStatusChanged")
      .withArgs(AUTHORITY_ID, false);

    const record = await registry.getAuthority(AUTHORITY_ID);
    expect(record.active).to.equal(false);
  });

  it("registers policy hashes", async function () {
    const { registry, owner } = await deployRegistry();

    await expect(registry.registerPolicy(POLICY_ID, POLICY_HASH))
      .to.emit(registry, "PolicyRegistered")
      .withArgs(POLICY_ID, POLICY_HASH, owner.address);

    expect(await registry.getPolicyHash(POLICY_ID)).to.equal(POLICY_HASH);
  });

  it("records credential revocation state", async function () {
    const { registry } = await deployRegistry();

    expect(await registry.isRevoked(CREDENTIAL_HASH)).to.equal(false);
    await expect(registry.setRevoked(CREDENTIAL_HASH, true))
      .to.emit(registry, "CredentialRevocationChanged")
      .withArgs(CREDENTIAL_HASH, true);
    expect(await registry.isRevoked(CREDENTIAL_HASH)).to.equal(true);
  });

  it("emits verification audit events without exposing the full proof", async function () {
    const { registry, owner } = await deployRegistry();

    await expect(registry.recordVerification(POLICY_ID, PROOF_HASH, true))
      .to.emit(registry, "VerificationRecorded")
      .withArgs(POLICY_ID, PROOF_HASH, true, owner.address);
  });

  it("rejects empty identifiers and hashes", async function () {
    const { registry } = await deployRegistry();

    await expect(registry.registerAuthority(ethers.ZeroHash, PUBLIC_KEY_HASH))
      .to.be.revertedWithCustomError(registry, "EmptyId");
    await expect(registry.registerAuthority(AUTHORITY_ID, ethers.ZeroHash))
      .to.be.revertedWithCustomError(registry, "EmptyHash");
    await expect(registry.registerPolicy(POLICY_ID, ethers.ZeroHash))
      .to.be.revertedWithCustomError(registry, "EmptyHash");
    await expect(registry.setRevoked(ethers.ZeroHash, true))
      .to.be.revertedWithCustomError(registry, "EmptyHash");
    await expect(registry.recordVerification(ethers.ZeroHash, PROOF_HASH, true))
      .to.be.revertedWithCustomError(registry, "EmptyId");
    await expect(registry.recordVerification(POLICY_ID, ethers.ZeroHash, true))
      .to.be.revertedWithCustomError(registry, "EmptyHash");
  });
});
