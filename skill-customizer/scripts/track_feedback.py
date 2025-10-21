#!/usr/bin/env python3
"""
Feedback Tracker - Captures and organizes user feedback for skill customization

This script helps structure user feedback about skill performance, making it
easier to identify specific areas for improvement and track customization needs.

Usage:
    track_feedback.py <skill-directory>

Interactive mode:
    The script will guide you through collecting structured feedback about:
    - What task was attempted
    - What worked well
    - What didn't match expectations
    - Specific preferences or requirements
    - Suggested improvements

Output:
    Creates/appends to FEEDBACK.md in the skill directory with structured feedback entries
"""

import sys
from pathlib import Path
from datetime import datetime


FEEDBACK_TEMPLATE = """# Skill Feedback Log

This file tracks user feedback and customization needs for iterative skill improvement.

---
"""


FEEDBACK_ENTRY_TEMPLATE = """
## Feedback Entry #{entry_num} - {date}

### Task Context
**What were you trying to accomplish?**
{task_description}

### What Worked Well
{what_worked}

### What Didn't Match Expectations
{what_didnt_work}

### Specific Preferences/Requirements
{preferences}

### Suggested Improvements
{improvements}

### Priority
{priority}

---
"""


def collect_feedback_interactive():
    """
    Interactively collect structured feedback from user.

    Returns:
        Dictionary with feedback components
    """
    print("\n📝 Skill Feedback Collection")
    print("=" * 60)
    print("Please provide detailed feedback to help customize this skill.\n")

    feedback = {}

    # Task context
    print("1️⃣  What task were you trying to accomplish?")
    print("   (Be specific: e.g., 'Extract tables from a 20-page PDF report')")
    feedback['task_description'] = input("   > ").strip()
    print()

    # What worked
    print("2️⃣  What aspects of the skill worked well?")
    print("   (e.g., 'Text extraction was accurate', 'Fast processing')")
    feedback['what_worked'] = input("   > ").strip()
    if not feedback['what_worked']:
        feedback['what_worked'] = "N/A"
    print()

    # What didn't work
    print("3️⃣  What didn't match your expectations?")
    print("   (e.g., 'Output format was JSON, I needed Markdown', 'Too verbose')")
    feedback['what_didnt_work'] = input("   > ").strip()
    if not feedback['what_didnt_work']:
        feedback['what_didnt_work'] = "N/A"
    print()

    # Preferences
    print("4️⃣  What are your specific preferences or requirements?")
    print("   (e.g., 'Always output in Markdown', 'Include source page numbers')")
    feedback['preferences'] = input("   > ").strip()
    if not feedback['preferences']:
        feedback['preferences'] = "N/A"
    print()

    # Improvements
    print("5️⃣  What specific improvements would help?")
    print("   (e.g., 'Add option to filter by date range', 'Default to concise output')")
    feedback['improvements'] = input("   > ").strip()
    if not feedback['improvements']:
        feedback['improvements'] = "N/A"
    print()

    # Priority
    print("6️⃣  How important is this customization?")
    print("   Options: critical, high, medium, low")
    priority = input("   > ").strip().lower()
    if priority not in ['critical', 'high', 'medium', 'low']:
        priority = 'medium'
    feedback['priority'] = priority.capitalize()
    print()

    return feedback


def save_feedback(skill_dir, feedback):
    """
    Save feedback to FEEDBACK.md file.

    Args:
        skill_dir: Path to skill directory
        feedback: Dictionary with feedback components

    Returns:
        Path to feedback file
    """
    feedback_path = skill_dir / 'FEEDBACK.md'

    # Create feedback file if it doesn't exist
    if not feedback_path.exists():
        feedback_path.write_text(FEEDBACK_TEMPLATE)
        entry_num = 1
    else:
        # Count existing entries
        content = feedback_path.read_text()
        entry_num = content.count('## Feedback Entry #') + 1

    # Format feedback entry
    entry = FEEDBACK_ENTRY_TEMPLATE.format(
        entry_num=entry_num,
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        task_description=feedback['task_description'],
        what_worked=feedback['what_worked'],
        what_didnt_work=feedback['what_didnt_work'],
        preferences=feedback['preferences'],
        improvements=feedback['improvements'],
        priority=feedback['priority']
    )

    # Append to file
    with open(feedback_path, 'a') as f:
        f.write(entry)

    return feedback_path


def analyze_feedback_patterns(feedback_path):
    """
    Analyze feedback file for common patterns.

    Args:
        feedback_path: Path to feedback file

    Returns:
        Dictionary with analysis results
    """
    if not feedback_path.exists():
        return None

    content = feedback_path.read_text()

    analysis = {
        'total_entries': content.count('## Feedback Entry #'),
        'critical_priority': content.count('Priority\nCritical'),
        'high_priority': content.count('Priority\nHigh'),
        'common_themes': []
    }

    # Simple keyword analysis for common themes
    keywords = {
        'output format': ['format', 'markdown', 'json', 'output'],
        'verbosity': ['verbose', 'concise', 'too much', 'too little'],
        'performance': ['slow', 'fast', 'speed', 'performance'],
        'accuracy': ['accurate', 'wrong', 'incorrect', 'missing'],
    }

    for theme, words in keywords.items():
        if any(word.lower() in content.lower() for word in words):
            analysis['common_themes'].append(theme)

    return analysis


def main():
    if len(sys.argv) < 2:
        print("Usage: track_feedback.py <skill-directory>")
        print("\nThis script helps collect structured feedback for skill customization.")
        print("Run it after using a skill to capture what needs to be improved.")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    # Validate skill directory
    if not skill_path.exists():
        print(f"❌ Error: Skill directory not found: {skill_path}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        sys.exit(1)

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        print(f"❌ Error: Not a valid skill directory (SKILL.md not found): {skill_path}")
        sys.exit(1)

    print(f"📂 Skill: {skill_path.name}")

    # Collect feedback
    feedback = collect_feedback_interactive()

    # Save feedback
    try:
        feedback_path = save_feedback(skill_path, feedback)
        print(f"\n✅ Feedback saved to: {feedback_path.name}")
    except Exception as e:
        print(f"\n❌ Error saving feedback: {e}")
        sys.exit(1)

    # Analyze patterns
    analysis = analyze_feedback_patterns(feedback_path)
    if analysis and analysis['total_entries'] > 1:
        print(f"\n📊 Feedback Summary:")
        print(f"   Total entries: {analysis['total_entries']}")
        print(f"   Critical priority: {analysis['critical_priority']}")
        print(f"   High priority: {analysis['high_priority']}")
        if analysis['common_themes']:
            print(f"   Common themes: {', '.join(analysis['common_themes'])}")

    print(f"\n💡 Next steps:")
    print(f"   1. Review feedback in {feedback_path.name}")
    print(f"   2. Identify specific changes to make in SKILL.md or scripts")
    print(f"   3. Apply improvements and test")
    print(f"   4. Document changes in CUSTOMIZATION_LOG.md")


if __name__ == "__main__":
    main()
