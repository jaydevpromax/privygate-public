// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title PrivyGateRegistry
/// @notice Minimal on-chain registry for the PrivyGate prototype.
/// @dev Heavy cryptographic verification stays off-chain. This contract records
///      authority keys, policy hashes, revocation status, and verification logs.
contract PrivyGateRegistry {
    struct AuthorityRecord {
        bytes32 publicKeyHash;
        address registrar;
        uint64 registeredAt;
        bool active;
    }

    mapping(bytes32 => AuthorityRecord) private authorities;
    mapping(bytes32 => bytes32) private policyHashes;
    mapping(bytes32 => bool) private revokedCredentials;

    event AuthorityRegistered(bytes32 indexed authorityId, bytes32 publicKeyHash, address indexed registrar);
    event AuthorityStatusChanged(bytes32 indexed authorityId, bool active);
    event PolicyRegistered(bytes32 indexed policyId, bytes32 policyHash, address indexed registrar);
    event CredentialRevocationChanged(bytes32 indexed credentialHash, bool revoked);
    event VerificationRecorded(bytes32 indexed policyId, bytes32 proofHash, bool result, address indexed verifier);

    error EmptyId();
    error EmptyHash();
    error AuthorityNotFound(bytes32 authorityId);
    error NotAuthorityRegistrar(bytes32 authorityId, address caller);

    function registerAuthority(bytes32 authorityId, bytes32 publicKeyHash) external {
        if (authorityId == bytes32(0)) revert EmptyId();
        if (publicKeyHash == bytes32(0)) revert EmptyHash();

        authorities[authorityId] = AuthorityRecord({
            publicKeyHash: publicKeyHash,
            registrar: msg.sender,
            registeredAt: uint64(block.timestamp),
            active: true
        });

        emit AuthorityRegistered(authorityId, publicKeyHash, msg.sender);
    }

    function setAuthorityActive(bytes32 authorityId, bool active) external {
        AuthorityRecord storage record = authorities[authorityId];
        if (record.registrar == address(0)) revert AuthorityNotFound(authorityId);
        if (record.registrar != msg.sender) revert NotAuthorityRegistrar(authorityId, msg.sender);

        record.active = active;
        emit AuthorityStatusChanged(authorityId, active);
    }

    function registerPolicy(bytes32 policyId, bytes32 policyHash) external {
        if (policyId == bytes32(0)) revert EmptyId();
        if (policyHash == bytes32(0)) revert EmptyHash();

        policyHashes[policyId] = policyHash;
        emit PolicyRegistered(policyId, policyHash, msg.sender);
    }

    function setRevoked(bytes32 credentialHash, bool revoked) external {
        if (credentialHash == bytes32(0)) revert EmptyHash();

        revokedCredentials[credentialHash] = revoked;
        emit CredentialRevocationChanged(credentialHash, revoked);
    }

    function recordVerification(bytes32 policyId, bytes32 proofHash, bool result) external {
        if (policyId == bytes32(0)) revert EmptyId();
        if (proofHash == bytes32(0)) revert EmptyHash();

        emit VerificationRecorded(policyId, proofHash, result, msg.sender);
    }

    function isAuthorityRegistered(bytes32 authorityId) external view returns (bool) {
        return authorities[authorityId].registrar != address(0);
    }

    function getAuthority(bytes32 authorityId) external view returns (AuthorityRecord memory) {
        return authorities[authorityId];
    }

    function getPolicyHash(bytes32 policyId) external view returns (bytes32) {
        return policyHashes[policyId];
    }

    function isRevoked(bytes32 credentialHash) external view returns (bool) {
        return revokedCredentials[credentialHash];
    }
}

