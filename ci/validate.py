"""Validate repository metadata and dependency changes from the checkout root."""
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml


def changed_paths(base, head):
    output = subprocess.check_output(
        ["git", "diff", "--no-renames", "--name-only", "-z", base, head, "--"]
    )
    return set(os.fsdecode(output).split("\0")) - {""}


def validate(base=None, head=None):
    errors = []
    metadata = yaml.safe_load(Path("project.yaml").read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        return ["project.yaml must contain a mapping"]

    for field in ("project_id", "project_name", "owner", "groupshare_location"):
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")

    version = metadata.get("python_version")
    if not isinstance(version, str) or not re.fullmatch(r"3\.\d+", version):
        errors.append('python_version must be a quoted major.minor string, e.g. "3.12"')

    rights = metadata.get("required_access")
    if not isinstance(rights, list):
        errors.append("required_access must be a list (use [] if no access is required)")
    else:
        for index, name in enumerate(rights, start=1):
            if not isinstance(name, str) or not name.strip():
                errors.append(f"Access entry {index} must be a non-empty name")

    if not Path("requirements.txt").is_file():
        errors.append("requirements.txt is required")
    if base and head:
        changed = changed_paths(base, head)
        dependency_files = {"pyproject.toml", "setup.py", "setup.cfg"}
        if changed & dependency_files and "requirements.txt" not in changed:
            errors.append("Update requirements.txt when changing a dependency manifest")
        print("requirements.txt:", "updated" if "requirements.txt" in changed else "unchanged")
    return errors


if __name__ == "__main__":
    if len(sys.argv) not in (1, 3):
        sys.exit("Usage: python ci/validate.py [BASE_SHA HEAD_SHA]")
    try:
        problems = validate(*sys.argv[1:])
    except (OSError, UnicodeError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        sys.exit(f"Validation could not run: {error}")
    if problems:
        sys.exit("\n".join(problems))
    print("Repository checks passed")
