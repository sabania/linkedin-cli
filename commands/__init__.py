import json
import sys


def output_json(data) -> None:
    """Write data as JSON to stdout. Used by --json flag across commands."""
    sys.stdout.write(json.dumps(data, indent=2, ensure_ascii=False, default=str) + "\n")
