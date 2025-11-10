# Meta-Skills Collection

A collection of meta-skills for Claude that enhance skill creation and customization workflows.

## What are Meta-Skills?

Meta-skills are skills that help you create or improve other skills. This collection provides powerful tools for:

- **Creating new skills** from MCP servers with workflow optimizations
- **Customizing existing skills** to match your preferences and requirements
- **Iteratively improving skills** based on real-world usage

## Skills in This Collection

### 🔧 mcp-skill-creator

Transform MCP servers into workflow-optimized skills following [Anthropic's MCP + Code Execution best practices](https://www.anthropic.com/engineering/code-execution-with-mcp).

**Use when you want to:**
- Create a custom skill from one or more MCP servers
- Optimize workflows with parallel execution and data filtering
- Build reusable automation scripts for specific work scenarios
- Capture personal SOPs and preferences into a skill

**Key Features:**
- **Progressive Disclosure**: Load tool definitions on-demand (98.7% token savings)
- **Working Code Generation**: Generates actual working MCP client infrastructure
- **Context Efficiency**: Process data in execution environment
- **Personalization**: Embed user preferences and SOPs into workflow

**Example:**
```
"I search files with priority: Projects → Downloads → Tmp, stop when found"
```
→ Generates a skill with prioritized search workflow and embedded preferences

[See detailed documentation →](mcp-skill-creator/SKILL.md)

---

### ✨ skill-customizer

Fork and iteratively improve existing skills based on your specific preferences and workflows.

**Use when you want to:**
- Customize an existing skill's output format or behavior
- Adapt a skill to company-specific requirements
- Add domain-specific knowledge to an existing skill
- Fine-tune a skill based on real-world usage

**Key Features:**
- **Systematic Forking**: Copy and track skill customizations
- **Structured Feedback**: Capture what works and what doesn't
- **Guided Customization**: Modify behaviors, scripts, and references
- **Version Control**: Timestamped packaging for distribution

**Example:**
```
"I want the pdf skill to always output tables as CSV instead of JSON"
```
→ Forks and customizes the pdf skill with your preferences

[See detailed documentation →](skill-customizer/SKILL.md)

---

## Installation

### Via Claude Code Marketplace

```bash
# Add this repository as a marketplace
/plugin marketplace add https://github.com/nemori-ai/skills.git

# Browse and install plugins
# Then select "Browse and install plugins" → Choose skill → "Install now"
```

### Available Plugins

- **mcp-skill-creator** - Create workflow-optimized skills from MCP servers
- **skill-customizer** - Customize existing skills based on preferences

## Quick Start Examples

### Creating a New MCP-Powered Skill

```bash
# 1. Install MCP SDK
pip3 install mcp --break-system-packages

# 2. Use mcp-skill-creator
"I want to create a skill that searches my Projects, Downloads, and Tmp
directories with priority order, stopping when files are found"
```

### Customizing an Existing Skill

```bash
# Use skill-customizer
"I want to customize the data-analysis skill to always include
confidence intervals and use my company's data visualization standards"
```

## Prerequisites

### For mcp-skill-creator
- Python 3.10+
- MCP SDK: `pip3 install mcp --break-system-packages`
- Node.js (for running MCP servers via npx)

### For skill-customizer
- Python 3.10+

## Documentation

Each skill has detailed documentation in its directory:

- [mcp-skill-creator/SKILL.md](mcp-skill-creator/SKILL.md) - Complete workflow for creating MCP-powered skills
- [mcp-skill-creator/references/](mcp-skill-creator/references/) - MCP best practices and examples
- [skill-customizer/SKILL.md](skill-customizer/SKILL.md) - Complete workflow for customizing skills
- [skill-customizer/references/](skill-customizer/references/) - Customization patterns and examples

## About Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. For more information:

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Equipping agents for the real world with Agent Skills](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contributing

Contributions are welcome! If you have suggestions for improvements or new meta-skills, please feel free to contribute.

## License

This project is open source under the Apache 2.0 license, following the Anthropic Skills repository licensing.

## Credits

Inspired by [Anthropic's Skills repository](https://github.com/anthropics/skills) and [MCP engineering practices](https://www.anthropic.com/engineering/code-execution-with-mcp).
