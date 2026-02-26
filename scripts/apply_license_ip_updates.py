#!/usr/bin/env python3
"""Add Licensed IP rider to MIT LICENSE files and ensure LICENSE-IP.md exists."""

import os
import re

RIDER = """
Licensed IP: ToE, MQGT-SCF, Zora — governed by IP License Agreement in A Theory of
Everything + ZoraASI — C.M. Baird et al. (2026), pp. 1311–1314. See LICENSE-IP.md.

---
"""

LICENSE_IP_CONTENT = """# Licensed IP — Theory of Everything / MQGT-SCF / Zora

The **Licensed IP** (ToE, MQGT-SCF, Zora architecture, and related frameworks) is governed by the Intellectual Property License Agreement in **A Theory of Everything + ZoraASI — C.M. Baird et al. (2026), pages 1311–1314.**

**Free to use.** No mandatory fees. Optional honor: $9.99 (individual), $99 (academic), commercial — whatever feels right.

Full summary: https://github.com/cbaird26/toe-2026-updates/blob/main/docs/TOE_IP_LICENSING_SUMMARY.md  

**Licensor:** Christopher Michael Baird | cbaird26@gmail.com
"""

def add_rider_to_license(path: str) -> bool:
    """Add Licensed IP rider if not present. Returns True if modified."""
    with open(path, "r") as f:
        content = f.read()
    if "Licensed IP:" in content:
        return False
    if "MIT License" not in content and "Creative Commons" not in content:
        return False
    # Insert rider after copyright line, before Permission
    pattern = r"(Copyright[^\n]+\n)(\n)(Permission is hereby granted)"
    if re.search(pattern, content):
        new_content = re.sub(pattern, r"\1" + RIDER + r"\3", content, count=1)
        with open(path, "w") as f:
            f.write(new_content)
        return True
    return False

def ensure_license_ip_md(dirpath: str) -> bool:
    """Create LICENSE-IP.md if missing. Returns True if created."""
    path = os.path.join(dirpath, "LICENSE-IP.md")
    if os.path.exists(path):
        return False
    with open(path, "w") as f:
        f.write(LICENSE_IP_CONTENT)
    return True

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    downloads = os.path.dirname(base)
    dirs_to_scan = [
        os.path.join(downloads, "repos"),
        os.path.join(downloads, "mqgt_polyrepo_work", "repos"),
        os.path.join(downloads, "toe-empirical-validation-live"),
        os.path.join(downloads, "mqgt_scf_reissue_2026-01-20_010939UTC"),
        os.path.join(downloads, "MQGT-SCF"),
    ]
    license_updated = []
    license_ip_created = []
    for d in dirs_to_scan:
        if not os.path.isdir(d):
            continue
        for item in os.listdir(d):
            subdir = os.path.join(d, item)
            if not os.path.isdir(subdir):
                continue
            license_path = os.path.join(subdir, "LICENSE")
            if os.path.isfile(license_path):
                if add_rider_to_license(license_path):
                    license_updated.append(license_path)
                if ensure_license_ip_md(subdir):
                    license_ip_created.append(os.path.join(subdir, "LICENSE-IP.md"))
    print("LICENSE rider added to:", *license_updated or ["(none)"], sep="\n  ")
    print("LICENSE-IP.md created:", *license_ip_created or ["(none)"], sep="\n  ")

if __name__ == "__main__":
    main()
