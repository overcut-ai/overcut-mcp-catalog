#!/usr/bin/env python3
"""Validate catalog entries in the overcut-mcp-catalog repository.

Usage:
    python3 scripts/validate-catalog.py              # Validate all entries
    python3 scripts/validate-catalog.py sentry       # Validate a single entry
    python3 scripts/validate-catalog.py sentry slack  # Validate multiple entries
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALID_CATEGORIES = {
    "developer-tools",
    "productivity",
    "data",
    "monitoring",
    "communication",
    "design",
    "documentation",
    "incident-management",
    "it-service-management",
    "ai",
    "other",
}

KEBAB_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
VAR_PLACEHOLDER_RE = re.compile(r"\$\{([^}]+)\}")


def find_vars_recursive(obj):
    """Find all ${VAR} placeholders in a nested structure."""
    found = set()
    if isinstance(obj, str):
        found.update(VAR_PLACEHOLDER_RE.findall(obj))
    elif isinstance(obj, list):
        for item in obj:
            found.update(find_vars_recursive(item))
    elif isinstance(obj, dict):
        for value in obj.values():
            found.update(find_vars_recursive(value))
    return found


def validate_entry(entry_dir):
    """Validate a single catalog entry. Returns list of error strings."""
    errors = []
    dir_name = os.path.basename(entry_dir)

    # 1. Directory name is kebab-case
    if not KEBAB_CASE_RE.match(dir_name):
        errors.append(f"Directory name '{dir_name}' is not valid kebab-case")

    # 2. catalog.json exists and is valid JSON
    catalog_path = os.path.join(entry_dir, "catalog.json")
    if not os.path.isfile(catalog_path):
        errors.append("catalog.json not found")
        return errors

    try:
        with open(catalog_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return errors

    # 3. Required fields present
    for field in ("name", "description", "category", "serverConfig"):
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # 4. Category is valid
    category = data.get("category")
    if category and category not in VALID_CATEGORIES:
        errors.append(
            f"Invalid category '{category}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    # 5. Every ${VAR} in serverConfig has matching requiredSecrets entry and vice versa
    server_config = data.get("serverConfig", {})
    config_vars = find_vars_recursive(server_config)
    secret_vars = {s["envVar"] for s in data.get("requiredSecrets", []) if "envVar" in s}

    missing_secrets = config_vars - secret_vars
    extra_secrets = secret_vars - config_vars
    if missing_secrets:
        errors.append(
            f"Variables in serverConfig without requiredSecrets entry: {', '.join(sorted(missing_secrets))}"
        )
    if extra_secrets:
        errors.append(
            f"requiredSecrets entries without matching serverConfig variable: {', '.join(sorted(extra_secrets))}"
        )

    # 6. recommendedTools is a subset of allTools
    recommended = data.get("recommendedTools", [])
    all_tools = data.get("allTools", [])
    if recommended and all_tools:
        recommended_set = set(recommended)
        all_tools_set = set(all_tools)
        not_in_all = recommended_set - all_tools_set
        if not_in_all:
            errors.append(
                f"recommendedTools not in allTools: {', '.join(sorted(not_in_all))}"
            )

    # 7. No duplicate tool names
    if len(recommended) != len(set(recommended)):
        dupes = [t for t in recommended if recommended.count(t) > 1]
        errors.append(f"Duplicate recommendedTools: {', '.join(set(dupes))}")
    if len(all_tools) != len(set(all_tools)):
        dupes = [t for t in all_tools if all_tools.count(t) > 1]
        errors.append(f"Duplicate allTools: {', '.join(set(dupes))}")

    # 8. If iconUrl references local repo path, icon file exists
    icon_url = data.get("iconUrl", "")
    repo_prefix = "https://raw.githubusercontent.com/overcut-ai/overcut-mcp-catalog/main/"
    if icon_url.startswith(repo_prefix):
        relative_path = icon_url[len(repo_prefix):]
        icon_file = os.path.join(REPO_ROOT, relative_path)
        if not os.path.isfile(icon_file):
            errors.append(f"Icon file not found: {relative_path}")

        # 9. iconUrl directory segment matches entry directory name
        url_dir = relative_path.split("/")[0] if "/" in relative_path else ""
        if url_dir and url_dir != dir_name:
            errors.append(
                f"iconUrl directory '{url_dir}' does not match entry directory '{dir_name}'"
            )

    return errors


def main():
    args = sys.argv[1:]

    if args:
        entry_names = args
    else:
        # Find all directories containing catalog.json
        entry_names = sorted(
            d
            for d in os.listdir(REPO_ROOT)
            if os.path.isfile(os.path.join(REPO_ROOT, d, "catalog.json"))
        )

    if not entry_names:
        print("No catalog entries found.")
        sys.exit(1)

    total = 0
    failed = 0

    for name in entry_names:
        entry_dir = os.path.join(REPO_ROOT, name)
        if not os.path.isdir(entry_dir):
            print(f"SKIP  {name} (directory not found)")
            continue

        total += 1
        errors = validate_entry(entry_dir)

        if errors:
            failed += 1
            print(f"FAIL  {name}")
            for error in errors:
                print(f"      - {error}")
        else:
            print(f"PASS  {name}")

    print(f"\n{'='*40}")
    print(f"Total: {total}  Passed: {total - failed}  Failed: {failed}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
