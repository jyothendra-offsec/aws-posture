# AWS Posture

Review exported S3 and Lambda configuration for follow-up.

## Quick start

Use Python 3.10 or newer. The CLI runs locally with the standard library. From the repository root, run:

```sh
python3 main.py example.json
```

The sample flags one disabled bucket control, one missing control, one function URL configured with `NONE`, and one environment key name for review.

## Input and output

| Input | Format | Output or purpose |
| --- | --- | --- |
| `buckets[]` | `name`, optional `public_access_block` with AWS boolean flags | `disabled` or `unknown` per control |
| `functions[]` | `name`, optional `function_url_auth` and `environment_keys` | URL auth and sensitive-name review leads |

Results are JSON on stdout. Redirect to a file when you want to save the review.

## Interpreting results

A bucket-level flag alone does not establish effective public access. Review account-level controls and resource policy. Supply environment key names only. The tool neither retrieves values nor connects to AWS.

## Troubleshooting

- Use the included fixture first to confirm the command and working directory.
- Check the input path and required fields if the CLI exits with status 2.
- Keep real assessment exports and generated reports in your private workspace.

## Verify locally

```sh
python3 -m unittest discover -s tests -v
```

## Review workflow

Start with resources reported as unknown. Collect missing configuration before treating an empty findings array as evidence of coverage. Keep the inventory scope and timestamp with the output.

## Usage terms

Original material in this revision requires the owner's written permission for modification or redistribution. Earlier MIT releases and third-party licenses retain their terms. See [LICENSE](LICENSE).
