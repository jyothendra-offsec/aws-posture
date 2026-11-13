"""Review S3 and Lambda configuration from local JSON exports."""
import argparse
import json
from pathlib import Path

S3_CONTROLS = ("BlockPublicAcls", "IgnorePublicAcls",
               "BlockPublicPolicy", "RestrictPublicBuckets")


def audit(snapshot):
    findings = []
    for bucket in snapshot.get("buckets", []):
        for flag in S3_CONTROLS:
            state = bucket.get("public_access_block", {}).get(flag)
            if state is not True:
                findings.append(dict(resource=bucket["name"], check=flag,
                                     status="disabled" if state is False else "unknown",
                                     action="Check effective account and bucket controls"))
    for function in snapshot.get("functions", []):
        if function.get("function_url_auth") == "NONE":
            findings.append(dict(resource=function["name"], check="function-url-auth",
                                 status="unauthenticated-config",
                                 action="Review URL policy and intended exposure"))
        if "environment_keys" not in function:
            continue
        for key in sorted(set(function["environment_keys"])):
            if any(part in key.upper() for part in ("SECRET", "TOKEN", "PASSWORD", "API_KEY")):
                findings.append(dict(resource=function["name"], check="sensitive-key-name",
                                     status="review", key=key,
                                     action="Verify how the value is managed"))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    data = json.loads(args.snapshot.read_text(encoding="utf-8"))
    print(json.dumps(audit(data), indent=2))


if __name__ == "__main__":
    main()
