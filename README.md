# Skill Customizer

A skill for Claude that enables you to fork and iteratively improve existing skills based on your specific preferences and workflows.

This repository is inspired by [Anthropic's official Skills repository](https://github.com/anthropics/skills) and focuses on making skill customization accessible and systematic.

## What is skill-customizer?

Instead of creating skills from scratch or making one-time modifications, **skill-customizer** provides a structured workflow for:

- **Forking** existing skills as a starting point
- **Testing** them on real tasks to identify gaps
- **Gathering feedback** through structured collection
- **Customizing** through iterative improvements
- **Packaging** with timestamped versions for distribution

## When to Use skill-customizer

Use this skill when you:
- Find an existing skill useful but want specific modifications
- Have personal preferences about output format, verbosity, or style
- Need to adapt a skill to company-specific requirements or workflows
- Want to add domain-specific knowledge to an existing skill
- Discover gaps after trying a skill on real tasks

**Perfect for:**
- Adjusting output formats (e.g., JSON → Markdown, verbose → concise)
- Adding company-specific guidelines or templates
- Incorporating domain-specific knowledge or terminology
- Matching your personal workflow preferences

## Quick Start

### Installation via Claude Code Marketplace

```bash
# Add this repository as a marketplace
/plugin marketplace add https://github.com/nemori-ai/skill-customizer.git

# Browse and install
# Then select "Browse and install plugins" → "skill-customizer" → "Install now"
```

### Using the Skill

After installation, Claude will proactively suggest using skill-customizer when it detects you're customizing a skill during a session. You can also invoke it directly:

```
"I want to customize the pdf skill to always output tables as CSV instead of JSON"
```

Claude will guide you through:
1. Forking the base skill
2. Testing and gathering your feedback
3. Applying targeted improvements
4. Iterating until you're satisfied
5. Packaging the final version with a timestamp

## Features

### 1. Systematic Forking
- Automatically copies the entire skill structure
- Updates metadata with customization tracking
- Creates a `CUSTOMIZATION_LOG.md` for documenting changes
- Preserves original skill organization

### 2. Structured Feedback Collection
Interactive feedback tracking helps you:
- Document what worked well
- Identify what didn't match expectations
- Capture specific preferences
- Prioritize improvements

### 3. Guided Customization
Modify different aspects of skills:
- **SKILL.md**: Change behaviors, workflows, output formats
- **Scripts**: Adjust parameters, add processing steps
- **References**: Add company guidelines, domain schemas
- **Assets**: Include templates, brand assets

### 4. Version Control
- Timestamped packaging: `my-skill-20251021-143022.zip`
- Track iterations and improvements over time
- Easy to share and install across Claude environments

## Project Structure

```
skill-customizer/
├── SKILL.md                      # Main skill instructions
├── scripts/
│   ├── fork_skill.py            # Fork existing skills
│   ├── track_feedback.py        # Collect structured feedback
│   ├── finalize_skill.py        # Package with timestamp
│   └── quick_validate.py        # Validate skill structure
└── references/
    └── customization_patterns.md # Detailed patterns and examples
```

## Examples

**Example 1: Output Format Customization**
```
User: "I use the pdf skill a lot, but I always want tables as CSV, not JSON"

Claude: "I can help you create a customized version of the pdf skill. Let me fork it
and customize it to always output tables as CSV..."

[Creates my-pdf-csv skill with modified output format]
```

**Example 2: Company-Specific Adaptation**
```
User: "I want the internal-comms skill to follow our company's style guide"

Claude: "Great! I'll customize the internal-comms skill for your company. First,
can you share your style guide?"

[Adds style guide to references/, updates SKILL.md examples]
```

**Example 3: Domain Specialization**
```
User: "The data-analysis skill is good but needs medical terminology"

Claude: "I'll create a specialized version for medical data analysis..."

[Adds medical terminology reference, updates examples with healthcare use cases]
```

## Documentation

For detailed information, see:
- **SKILL.md** - Complete workflow and best practices
- **references/customization_patterns.md** - Detailed patterns, examples, and troubleshooting

## About Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. For more information about the skills system:

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Equipping agents for the real world with Agent Skills](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contributing

This skill was created to make skill customization more accessible. If you have suggestions for improvements or find issues, please feel free to contribute.

## License

This project is open source under the Apache 2.0 license, following the original Anthropic Skills repository licensing.

## Credits

Inspired by and based on [Anthropic's Skills repository](https://github.com/anthropics/skills), which provides the foundation for understanding and working with Claude's skills system.
