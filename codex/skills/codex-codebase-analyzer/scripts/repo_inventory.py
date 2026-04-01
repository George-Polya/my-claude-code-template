#!/usr/bin/env python3
"""
Generate a structural inventory for a codebase or a specific folder.

Purpose:
    Capture directory layout, extension counts, notable files, and
    a tree summary before starting deeper code analysis.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path

IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

NOTABLE_FILE_NAMES = {
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
    "makefile",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "pdm.lock",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "go.mod",
    "go.sum",
    "cargo.toml",
    "cargo.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "gradle.properties",
    "settings.gradle",
    "settings.gradle.kts",
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "conftest.py",
    "pytest.ini",
    "tox.ini",
    ".env",
    ".env.example",
    ".env.test",
    "readme.md",
}

NOTABLE_STEMS = {
    "main",
    "app",
    "server",
    "index",
    "routes",
    "router",
    "controllers",
    "controller",
    "service",
    "services",
    "domain",
    "schema",
    "schemas",
    "config",
    "settings",
    "dependency",
    "dependencies",
    "middleware",
    "models",
    "repository",
    "repositories",
    "conftest",
}


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed options for target path, output format, and depth limits
    """

    parser = argparse.ArgumentParser(
        description="Print a codebase inventory as JSON or Markdown.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory or file to inspect. Defaults to the current directory.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum depth for the rendered tree. Default is 3.",
    )
    parser.add_argument(
        "--max-tree-entries",
        type=int,
        default=200,
        help="Maximum number of entries to include in the tree. Default is 200.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format. Default is markdown.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories.",
    )
    return parser.parse_args()


def should_skip_name(name: str, include_hidden: bool) -> bool:
    """
    Decide whether a file or directory should be skipped.

    Parameters
    ----------
    name : str
        File or directory name
    include_hidden : bool
        Whether hidden items should be included

    Returns
    -------
    bool
        True when the item should be excluded
    """

    if not include_hidden and name.startswith("."):
        return True
    return name in IGNORED_DIR_NAMES


def relative_path(path: Path, root: Path) -> str:
    """
    Return a POSIX-style path relative to the root.
    """

    try:
        return path.relative_to(root).as_posix() or "."
    except ValueError:
        return path.as_posix()


def is_notable_file(path: Path) -> bool:
    """
    Decide whether a file is likely to be an entrypoint or critical config.

    Parameters
    ----------
    path : Path
        File path to inspect

    Returns
    -------
    bool
        True when the file deserves early attention
    """

    lowered_name = path.name.lower()
    if lowered_name in NOTABLE_FILE_NAMES:
        return True
    if lowered_name.startswith("readme"):
        return True
    return path.stem.lower() in NOTABLE_STEMS


def list_root_entries(root: Path, include_hidden: bool) -> list[str]:
    """
    Return sorted direct children of the root path.
    """

    entries: list[str] = []
    for entry in sorted(root.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        if should_skip_name(entry.name, include_hidden):
            continue
        suffix = "/" if entry.is_dir() else ""
        entries.append(f"{entry.name}{suffix}")
    return entries


def build_tree_lines(
    root: Path,
    max_depth: int,
    max_tree_entries: int,
    include_hidden: bool,
) -> tuple[list[str], bool]:
    """
    Build a human-readable directory tree.

    Parameters
    ----------
    root : Path
        Root path to render
    max_depth : int
        Maximum traversal depth
    max_tree_entries : int
        Maximum number of entries to render
    include_hidden : bool
        Whether hidden items should be included

    Returns
    -------
    tuple[list[str], bool]
        Rendered tree lines and a truncation flag
    """

    if root.is_file():
        return [root.name], False

    lines = ["."]
    emitted_entries = 0
    truncated = False

    def walk(current: Path, prefix: str, depth: int) -> None:
        nonlocal emitted_entries, truncated
        if depth > max_depth or truncated:
            return

        entries = []
        for entry in sorted(current.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
            if should_skip_name(entry.name, include_hidden):
                continue
            entries.append(entry)

        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "
            label = f"{entry.name}/" if entry.is_dir() else entry.name
            lines.append(f"{prefix}{connector}{label}")
            emitted_entries += 1

            if emitted_entries >= max_tree_entries:
                truncated = True
                return

            if entry.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                walk(entry, next_prefix, depth + 1)
                if truncated:
                    return

    walk(root, "", 1)
    return lines, truncated


def scan_path(root: Path, include_hidden: bool) -> dict[str, object]:
    """
    Collect directory counts, file counts, extension stats, and notable files.

    Purpose:
        Capture a broad structural summary for the full scope regardless
        of the rendered tree depth limit.

    Parameters
    ----------
    root : Path
        Inventory root
    include_hidden : bool
        Whether hidden items should be included

    Returns
    -------
    dict[str, object]
        Inventory summary data
    """

    extension_counts: Counter[str] = Counter()
    notable_files: list[str] = []
    directories_scanned = 0
    files_scanned = 0

    if root.is_file():
        files_scanned = 1
        extension_counts[root.suffix.lower() or "[no extension]"] += 1
        if is_notable_file(root):
            notable_files.append(root.name)
        return {
            "directories_scanned": 0,
            "files_scanned": files_scanned,
            "extension_counts": extension_counts,
            "notable_files": notable_files,
        }

    for current_root, dirnames, filenames in os.walk(root, topdown=True):
        current_path = Path(current_root)
        filtered_dirnames = []
        for dirname in sorted(dirnames):
            if should_skip_name(dirname, include_hidden):
                continue
            filtered_dirnames.append(dirname)
        dirnames[:] = filtered_dirnames

        directories_scanned += len(dirnames)

        for filename in sorted(filenames):
            if should_skip_name(filename, include_hidden):
                continue
            file_path = current_path / filename
            files_scanned += 1
            extension_counts[file_path.suffix.lower() or "[no extension]"] += 1
            if is_notable_file(file_path) and len(notable_files) < 50:
                notable_files.append(relative_path(file_path, root))

    return {
        "directories_scanned": directories_scanned,
        "files_scanned": files_scanned,
        "extension_counts": extension_counts,
        "notable_files": notable_files,
    }


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    """
    Assemble the final output payload.

    Raises
    ------
    FileNotFoundError
        Raised when the target path does not exist
    ValueError
        Raised when depth or tree entry limits are invalid
    """

    target = Path(args.path).resolve()
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")
    if args.max_depth < 0:
        raise ValueError("--max-depth must be 0 or greater.")
    if args.max_tree_entries < 1:
        raise ValueError("--max-tree-entries must be 1 or greater.")

    scan_result = scan_path(target, args.include_hidden)
    tree_lines, truncated = build_tree_lines(
        target,
        max_depth=args.max_depth,
        max_tree_entries=args.max_tree_entries,
        include_hidden=args.include_hidden,
    )

    extension_counts = [
        {"extension": extension, "count": count}
        for extension, count in sorted(
            scan_result["extension_counts"].items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]

    payload: dict[str, object] = {
        "target_path": str(target),
        "target_type": "file" if target.is_file() else "directory",
        "max_depth": args.max_depth,
        "max_tree_entries": args.max_tree_entries,
        "include_hidden": args.include_hidden,
        "ignored_directory_names": sorted(IGNORED_DIR_NAMES),
        "directories_scanned": scan_result["directories_scanned"],
        "files_scanned": scan_result["files_scanned"],
        "root_entries": [target.name] if target.is_file() else list_root_entries(target, args.include_hidden),
        "extension_counts": extension_counts,
        "notable_files": scan_result["notable_files"],
        "tree": tree_lines,
        "tree_truncated": truncated,
    }
    return payload


def render_markdown(payload: dict[str, object]) -> str:
    """
    Render the collected inventory as Markdown.

    Parameters
    ----------
    payload : dict[str, object]
        Inventory data

    Returns
    -------
    str
        Human-readable Markdown content
    """

    lines = [
        "# Codebase Inventory",
        "",
        f"- Target path: `{payload['target_path']}`",
        f"- Target type: `{payload['target_type']}`",
        f"- Directories scanned: `{payload['directories_scanned']}`",
        f"- Files scanned: `{payload['files_scanned']}`",
        f"- Tree max depth: `{payload['max_depth']}`",
        f"- Include hidden items: `{payload['include_hidden']}`",
        "",
        "## Root Entries",
    ]

    root_entries = payload["root_entries"]
    if root_entries:
        lines.extend(f"- `{entry}`" for entry in root_entries)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Extension Counts",
            "",
            "| Extension | Count |",
            "| --- | ---: |",
        ]
    )

    for item in payload["extension_counts"]:
        lines.append(f"| `{item['extension']}` | {item['count']} |")

    lines.extend(["", "## Notable Files"])
    notable_files = payload["notable_files"]
    if notable_files:
        lines.extend(f"- `{path}`" for path in notable_files)
    else:
        lines.append("- None")

    lines.extend(["", "## Tree", "", "```text"])
    lines.extend(payload["tree"])
    if payload["tree_truncated"]:
        lines.append("... (tree output was truncated at the configured limit)")
    lines.extend(["```", ""])
    return "\n".join(lines)


def main() -> int:
    """
    Script entrypoint.

    Returns
    -------
    int
        0 on success, 1 on error
    """

    try:
        args = parse_args()
        payload = build_payload(args)
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_markdown(payload))
        return 0
    except (FileNotFoundError, ValueError) as error:
        print(f"[ERROR] {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
