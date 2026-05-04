from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

from privygate import Attribute, authority_setup, encode_policy, issue_credential, setup, sign, user_setup, verify


def run_case(authority_count: int, attribute_count: int, threshold: int) -> dict[str, object]:
    params = setup(epoch=1)
    user_secret, user_commitment = user_setup(params, f"user-{authority_count}-{attribute_count}")
    authorities = [authority_setup(params, f"Authority{i}") for i in range(authority_count)]

    attributes = [
        Attribute(f"Authority{i % authority_count}", "role", f"attr{i}")
        for i in range(attribute_count)
    ]

    credentials = []
    keygen_start = time.perf_counter()
    for attribute in attributes:
        sk, pk = authorities[int(attribute.authority_id.replace("Authority", ""))]
        credentials.append(issue_credential(params, sk, pk, user_commitment, attribute, params.epoch))
    keygen_ms = (time.perf_counter() - keygen_start) * 1000

    policy = encode_policy(f"{threshold}-of-{attribute_count}", attributes, threshold=threshold)
    message = f"benchmark:{authority_count}:{attribute_count}:{threshold}".encode("utf-8")

    sign_start = time.perf_counter()
    signature = sign(params, user_secret, credentials, policy, message)
    sign_ms = (time.perf_counter() - sign_start) * 1000

    authority_pks = {pk.authority_id: pk for _, pk in authorities}
    verify_start = time.perf_counter()
    result = verify(params, authority_pks, policy, message, signature)
    verify_ms = (time.perf_counter() - verify_start) * 1000

    return {
        "authority_count": authority_count,
        "attribute_count": attribute_count,
        "threshold": threshold,
        "keygen_time_ms": round(keygen_ms, 4),
        "sign_time_ms": round(sign_ms, 4),
        "verify_time_ms": round(verify_ms, 4),
        "signature_components": len(signature.sigma_components),
        "signature_size_bytes": len(str(signature).encode("utf-8")),
        "accepted": result.accepted,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark the PrivyGate core prototype.")
    parser.add_argument("--output", default="experiments/results/core_benchmark.csv")
    args = parser.parse_args()

    cases = []
    for authority_count in (2, 4, 8, 16):
        cases.append(run_case(authority_count, attribute_count=authority_count * 2, threshold=authority_count))
    for attribute_count in (5, 10, 20, 40):
        cases.append(run_case(authority_count=4, attribute_count=attribute_count, threshold=max(1, attribute_count // 2)))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(cases[0]))
        writer.writeheader()
        writer.writerows(cases)
    print(output_path)


if __name__ == "__main__":
    main()

