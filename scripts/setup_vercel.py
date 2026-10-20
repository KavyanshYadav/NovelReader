#!/usr/bin/env python3
"""Wire the reader up to Vercel: project, GitHub link, and the CI secrets.

Usage:
    python3 scripts/setup_vercel.py

Run `vercel login` first. The script then:

  1. links the repository to a Vercel project called "novel-reader"
  2. connects the GitHub repository so pushes deploy automatically
  3. publishes the repository variables the GitHub Action needs
  4. stores a Vercel token as the VERCEL_TOKEN repository secret
  5. ships a production deployment and prints the live URL

The token is read from the local Vercel credentials and piped straight into
`gh secret set`; it is never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = "novel-reader"
REPO = "KavyanshYadav/NovelReader"
TEAM = os.environ.get("VERCEL_TEAM_ID", "team_a0nxiCStSu0wJ7T3uZRt4fVi")

TOKEN_FILES = [
    Path.home() / ".local/share/com.vercel.cli/auth.json",
    Path.home() / ".vercel/auth.json",
    Path.home() / ".config/vercel/auth.json",
]


def run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    print(f"\n$ {' '.join(args)}")
    return subprocess.run(args, **kwargs)


def find_token() -> str | None:
    for path in TOKEN_FILES:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict):
            token = data.get("token")
            if isinstance(token, str) and token:
                return token
            for value in data.values():
                if isinstance(value, dict) and isinstance(value.get("token"), str):
                    return value["token"]
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-git-connect", action="store_true")
    args = parser.parse_args()

    if shutil.which("vercel") is None:
        raise SystemExit("The Vercel CLI is not installed: npm install -g vercel")
    if shutil.which("gh") is None:
        raise SystemExit("The GitHub CLI is not installed.")

    who = run(["vercel", "whoami"], capture_output=True, text=True)
    if "Logged out" in (who.stdout + who.stderr):
        raise SystemExit(
            "The Vercel CLI is logged out. Run `vercel login` first, then re-run this script."
        )
    print(f"\nVercel CLI is signed in as {who.stdout.strip().splitlines()[-1]}")

    # 1. Link the project
    run(
        [
            "vercel",
            "link",
            "--yes",
            "--project",
            PROJECT,
            "--scope",
            TEAM,
        ],
        cwd=ROOT,
    )
    project_file = ROOT / ".vercel" / "project.json"
    if not project_file.exists():
        raise SystemExit("vercel link did not produce .vercel/project.json")
    project = json.loads(project_file.read_text(encoding="utf-8"))
    org_id = project.get("orgId", "")
    project_id = project.get("projectId", "")
    print(f"\nLinked project {PROJECT} (org {org_id}, project {project_id})")

    # 2. Connect the GitHub repository for automatic deployments
    if not args.skip_git_connect:
        connect = run(
            [
                "vercel",
                "git",
                "connect",
                f"https://github.com/{REPO}",
                "--scope",
                TEAM,
            ],
            capture_output=True,
            text=True,
        )
        output = connect.stdout + connect.stderr
        print(output.strip()[:1200])
        if connect.returncode != 0:
            print(
                "\nCould not connect the repository automatically. Connect it from the "
                f"Vercel dashboard: Project {PROJECT} -> Settings -> Git.\n"
            )

    # 3. Repository variables for the workflow
    for name, value in (("VERCEL_ORG_ID", org_id), ("VERCEL_PROJECT_ID", project_id)):
        run(["gh", "variable", "set", name, "--body", value, "--repo", REPO])

    # 4. The token secret
    token = find_token()
    if token:
        run(
            ["gh", "secret", "set", "VERCEL_TOKEN", "--repo", REPO],
            input=token,
            text=True,
        )
        print("\nStored the Vercel token as the VERCEL_TOKEN repository secret.")
    else:
        print(
            "\nCould not find a local Vercel token. Create one at "
            "https://vercel.com/account/tokens and add it with:\n"
            f"  gh secret set VERCEL_TOKEN --repo {REPO}\n"
        )

    # 5. Production deployment
    deploy = run(
        ["vercel", "deploy", "--prod", "--yes", "--scope", TEAM],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print((deploy.stdout + deploy.stderr)[-1500:])
    if deploy.returncode == 0:
        for line in (deploy.stdout + deploy.stderr).splitlines():
            if "Production URL" in line or "https://" in line and "vercel.app" in line:
                print(f"\nLive at: {line.strip()}")


if __name__ == "__main__":
    main()
