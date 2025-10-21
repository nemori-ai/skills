#!/usr/bin/env python3
"""
Skill Forker - Creates a customized copy of an existing skill

This script copies an existing skill to a new location with a new name,
preserving all structure and resources while updating metadata to reflect
the customization.

Usage:
    fork_skill.py <source-skill-path> <new-skill-name> --path <output-directory>

Examples:
    fork_skill.py ./pdf my-pdf-workflow --path ./custom-skills
    fork_skill.py ../skills/canvas-design my-design-style --path .
    fork_skill.py ./internal-comms company-comms --path ~/my-skills

The script will:
- Copy all files and directories from the source skill
- Update the skill name in SKILL.md frontmatter
- Append customization metadata
- Preserve all scripts, references, and assets
- Create a customization log for tracking changes
"""

import sys
import shutil
import re
from pathlib import Path
from datetime import datetime


def update_skill_metadata(skill_md_path, new_name, source_skill_name):
    """
    Update the SKILL.md file with new name and customization metadata.

    Args:
        skill_md_path: Path to the SKILL.md file
        new_name: New skill name
        source_skill_name: Original skill name for reference
    """
    content = skill_md_path.read_text()

    # Update the name in frontmatter
    content = re.sub(
        r'(name:\s*)([^\n]+)',
        f'\\1{new_name}',
        content,
        count=1
    )

    # Add or update metadata section in frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)

        # Check if metadata already exists
        if 'metadata:' not in frontmatter:
            # Add metadata before the closing ---
            new_frontmatter = frontmatter + f'\nmetadata:\n  customized-from: {source_skill_name}\n  customization-date: {datetime.now().strftime("%Y-%m-%d")}'
            content = content.replace(
                f'---\n{frontmatter}\n---',
                f'---\n{new_frontmatter}\n---'
            )
        else:
            # Update existing metadata
            if 'customized-from:' not in frontmatter:
                # Add to existing metadata section
                content = re.sub(
                    r'(metadata:)',
                    f'\\1\n  customized-from: {source_skill_name}\n  customization-date: {datetime.now().strftime("%Y-%m-%d")}',
                    content,
                    count=1
                )

    skill_md_path.write_text(content)


def create_customization_log(target_dir, source_skill_name, new_name):
    """
    Create a customization log to track changes.

    Args:
        target_dir: Target skill directory
        source_skill_name: Original skill name
        new_name: New skill name
    """
    log_content = f"""# Customization Log: {new_name}

## Base Skill
- **Source**: {source_skill_name}
- **Forked on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Customization History

### Version 1.0 - Initial Fork
- Created customized version from `{source_skill_name}`
- Ready for iterative improvements based on user feedback

---

## How to Track Changes

Document each customization iteration below with:
1. Date and version number
2. What was changed (SKILL.md, scripts, references, assets)
3. Why it was changed (user feedback, preference, workflow improvement)
4. How to test the change

### Example Entry:

### Version 1.1 - [Date]
**Changes:**
- Modified SKILL.md: Updated default output format from JSON to Markdown
- Added script: custom_formatter.py for company-specific formatting

**Reason:**
- User prefers Markdown output for easier sharing with team
- Company style guide requires specific heading formats

**Testing:**
- Run the skill on sample document
- Verify output matches company style guide

---

## Modification Notes

Add your customization notes here as you iterate...
"""

    log_path = target_dir / 'CUSTOMIZATION_LOG.md'
    log_path.write_text(log_content)
    return log_path


def fork_skill(source_path, new_name, output_path):
    """
    Fork an existing skill to create a customized version.

    Args:
        source_path: Path to the source skill directory
        new_name: Name for the new customized skill
        output_path: Directory where the new skill should be created

    Returns:
        Path to the created skill directory, or None if error
    """
    source_path = Path(source_path).resolve()
    output_path = Path(output_path).resolve()

    # Validate source skill exists
    if not source_path.exists():
        print(f"❌ Error: Source skill not found: {source_path}")
        return None

    if not source_path.is_dir():
        print(f"❌ Error: Source path is not a directory: {source_path}")
        return None

    # Validate SKILL.md exists in source
    source_skill_md = source_path / 'SKILL.md'
    if not source_skill_md.exists():
        print(f"❌ Error: SKILL.md not found in source skill: {source_path}")
        return None

    # Extract source skill name from directory or SKILL.md
    source_skill_name = source_path.name

    # Create target directory
    target_dir = output_path / new_name

    if target_dir.exists():
        print(f"❌ Error: Target directory already exists: {target_dir}")
        return None

    # Copy the entire skill directory
    try:
        print(f"📋 Copying skill from {source_path} to {target_dir}...")
        shutil.copytree(source_path, target_dir)
        print(f"✅ Copied all files and directories")
    except Exception as e:
        print(f"❌ Error copying skill directory: {e}")
        return None

    # Update SKILL.md metadata
    try:
        target_skill_md = target_dir / 'SKILL.md'
        update_skill_metadata(target_skill_md, new_name, source_skill_name)
        print(f"✅ Updated SKILL.md metadata")
    except Exception as e:
        print(f"❌ Error updating SKILL.md: {e}")
        return None

    # Create customization log
    try:
        log_path = create_customization_log(target_dir, source_skill_name, new_name)
        print(f"✅ Created customization log: {log_path.name}")
    except Exception as e:
        print(f"⚠️  Warning: Could not create customization log: {e}")

    print(f"\n✅ Successfully forked '{source_skill_name}' to '{new_name}'")
    print(f"   Location: {target_dir}")
    print(f"\n📝 Next steps:")
    print(f"   1. Review SKILL.md and identify customization needs")
    print(f"   2. Use the skill on real tasks to gather feedback")
    print(f"   3. Make iterative improvements based on user preferences")
    print(f"   4. Document changes in CUSTOMIZATION_LOG.md")

    return target_dir


def main():
    if len(sys.argv) < 4 or '--path' not in sys.argv:
        print("Usage: fork_skill.py <source-skill-path> <new-skill-name> --path <output-directory>")
        print("\nExamples:")
        print("  fork_skill.py ./pdf my-pdf-workflow --path ./custom-skills")
        print("  fork_skill.py ../skills/canvas-design my-design-style --path .")
        print("  fork_skill.py ./internal-comms company-comms --path ~/my-skills")
        print("\nSkill name requirements:")
        print("  - Hyphen-case (lowercase with hyphens)")
        print("  - Alphanumeric characters and hyphens only")
        print("  - Must match directory name")
        sys.exit(1)

    # Parse arguments
    source_path = sys.argv[1]
    new_name = sys.argv[2]

    try:
        path_index = sys.argv.index('--path')
        output_path = sys.argv[path_index + 1]
    except (ValueError, IndexError):
        print("❌ Error: --path flag requires an output directory")
        sys.exit(1)

    # Validate new skill name format
    if not re.match(r'^[a-z0-9-]+$', new_name):
        print(f"❌ Error: Skill name '{new_name}' must be hyphen-case (lowercase, hyphens only)")
        sys.exit(1)

    if new_name.startswith('-') or new_name.endswith('-') or '--' in new_name:
        print(f"❌ Error: Skill name '{new_name}' cannot start/end with hyphen or contain consecutive hyphens")
        sys.exit(1)

    print(f"🔀 Forking skill...")
    print(f"   Source: {source_path}")
    print(f"   New name: {new_name}")
    print(f"   Output: {output_path}")
    print()

    result = fork_skill(source_path, new_name, output_path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
