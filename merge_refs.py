#!/usr/bin/env python3
"""Merge references from refs_content_map.json into node frontmatter."""

import json
import os


def main():
    json_path = "/tmp/refs_content_map.json"
    if not os.path.exists(json_path):
        print(f"ERROR: {json_path} not found")
        return 1

    with open(json_path) as f:
        refs_map = json.load(f)

    base_dir = "/mnt/d/00_Hermes/AI_Knowledge_Graph"

    success = 0
    skipped = 0
    errors = []

    for rel_path, ref_data in refs_map.items():
        abs_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(abs_path):
            errors.append(f"{rel_path}: file not found")
            continue

        references = ref_data.get("references", [])
        if not references:
            skipped += 1
            continue

        with open(abs_path) as f:
            content = f.read()

        # Check if frontmatter already has references
        second_sep = content.find("---", 3)
        if second_sep == -1:
            errors.append(f"{rel_path}: no valid frontmatter")
            continue
        frontmatter = content[3:second_sep]
        body = content[second_sep + 3:]

        if "references:" in frontmatter:
            skipped += 1
            continue

        # Build YAML references block
        ref_yaml_lines = ["references:"]
        for ref in references:
            title = ref.get("title", "").replace('"', '\\"')
            ref_yaml_lines.append(f'  - title: "{title}"')
            ref_yaml_lines.append(f"    type: {ref.get('type', 'paper')}")
            author = ref.get("author", "")
            if author:
                author = author.replace('"', '\\"')
                ref_yaml_lines.append(f'    author: "{author}"')
            if ref.get("year"):
                ref_yaml_lines.append(f"    year: {ref['year']}")
            url = ref.get("url", "")
            if url:
                ref_yaml_lines.append(f'    url: "{url}"')

        ref_yaml = "\n".join(ref_yaml_lines)

        # Insert references before the closing --- of frontmatter
        new_content = "---" + frontmatter.rstrip() + "\n" + ref_yaml + "\n---" + body

        with open(abs_path, "w") as f:
            f.write(new_content)

        success += 1

    print(f"Results:")
    print(f"  Updated:   {success}")
    print(f"  Skipped:   {skipped}")
    print(f"  Errors:    {len(errors)}")
    for e in errors:
        print(f"    - {e}")
    print(f"  Total:     {success + skipped + len(errors)}")
    return 0


if __name__ == "__main__":
    exit(main())