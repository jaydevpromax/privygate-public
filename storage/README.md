# PrivyGate 0G Storage Helper

This optional helper uploads the generated PrivyGate audit manifest to 0G Storage.

Generate the manifest first from the repository root:

```powershell
python .\scripts\generate_storage_audit_manifest.py
```

Install the helper dependencies:

```powershell
cd storage
npm.cmd install
```

Upload after setting your private key in the current shell. Do not write private keys into this repository.

```powershell
$env:OG_PRIVATE_KEY='0x...'
npm.cmd run upload:audit
```

The script prints the 0G Storage root hash and transaction hash. Record those values in README and submission materials. Do not write them back into the uploaded manifest file, because that would change the file content and invalidate the content-addressed root.

Keep secret material out of Git. The manifest itself contains only public demo hashes, policy names, public chain evidence, and redacted authorization metadata.

## Dependency Audit Note

`npm audit` currently reports high-severity issues through the 0G Storage SDK dependency chain:

```text
@0gfoundation/0g-storage-ts-sdk -> open-jsonrpc-provider -> axios
```

This helper is a local, one-shot upload tool for a public redacted manifest, not a production service. Use it only from a trusted local shell, never commit or display private keys, and remove `OG_PRIVATE_KEY` from the environment after uploading.
