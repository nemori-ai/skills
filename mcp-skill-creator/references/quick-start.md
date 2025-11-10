# Quick Start Guide

This guide will help you create your first MCP-powered skill using the mcp-skill-creator meta-skill.

## Prerequisites

1. Python 3.10 or higher
2. MCP SDK installed:
   ```bash
   pip install mcp --break-system-packages
   ```
3. Node.js (for running MCP servers via npx)

## Overview

Creating an MCP-powered skill is a two-phase process:

**Phase 1 (Programmatic)**: Generate MCP infrastructure using provided scripts
- Introspect MCP servers to discover tools
- Generate type-safe Python wrappers

**Phase 2 (LLM-Driven)**: Create the skill following skill-creator principles
- Analyze workflow and identify optimization opportunities
- Write workflow scripts combining MCP tools
- Embed user preferences and SOPs into SKILL.md
- Package the final skill

## Step-by-Step Process

### Step 1: Gather Input from User

Collect the following information:

**MCP Servers** (required):
```json
{
  "mcp_servers": [
    {
      "name": "puppeteer",
      "command": ["npx", "-y", "@modelcontextprotocol/server-puppeteer"]
    },
    {
      "name": "twitter",
      "command": ["npx", "-y", "@modelcontextprotocol/server-twitter"]
    }
  ]
}
```

**Workflow Description** (required):
- User's step-by-step workflow
- Can be natural language, numbered list, or sequential narrative
- Example: "First I visit the official website, then check Twitter and Reddit, finally create a report"

**Preferences** (optional):
- "I prefer quantitative metrics over qualitative descriptions"
- "Recent information is more valuable than old"
- "Always cross-reference claims"

**SOPs** (optional):
- "Start with official sources before checking community feedback"
- "Cite all sources in the final report"
- "Highlight contradictions between official and community perspectives"

### Step 2: Generate MCP Infrastructure (Programmatic)

#### 2.1 Create MCP Configuration File

```bash
# Save MCP server config
cat > mcp_config.json << EOF
{
  "servers": [
    {
      "name": "puppeteer",
      "command": ["npx", "-y", "@modelcontextprotocol/server-puppeteer"]
    },
    {
      "name": "twitter",  
      "command": ["npx", "-y", "@modelcontextprotocol/server-twitter"]
    }
  ]
}
EOF
```

#### 2.2 Introspect MCP Servers

```bash
python scripts/mcp_introspector.py mcp_config.json introspection.json
```

This discovers all available tools from the MCP servers and saves them to `introspection.json`.

#### 2.3 Generate Tool Wrappers

```bash
mkdir -p my-skill/scripts
python scripts/generate_mcp_wrappers.py introspection.json my-skill
```

This creates:
- `my-skill/scripts/mcp_client.py` - Base MCP client
- `my-skill/scripts/tools/<server>/<tool>.py` - Type-safe wrappers for each tool
- `my-skill/scripts/tools/<server>/__init__.py` - Package initialization

**Generated structure**:
```
my-skill/
└── scripts/
    ├── mcp_client.py
    └── tools/
        ├── puppeteer/
        │   ├── __init__.py
        │   ├── fetch_page.py
        │   └── screenshot.py
        └── twitter/
            ├── __init__.py
            └── search_tweets.py
```

### Step 3: Analyze Workflow (LLM-Driven)

Now use Claude to analyze the user's workflow description:

**Ask yourself**:
- What are the distinct workflow steps?
- Which steps are data fetching (candidates for parallelization)?
- Which steps are data processing (candidates for execution environment filtering)?
- Are there any loops, conditionals, or polling patterns?
- What intermediate state needs to be preserved?

**Example Analysis**:

User workflow: "Research products by checking official site, Twitter, Reddit, then create report"

Analysis:
- **Step 1**: Fetch official website (data fetch)
- **Step 2**: Search Twitter (data fetch - can parallelize with step 3)
- **Step 3**: Search Reddit (data fetch - can parallelize with step 2)
- **Step 4**: Aggregate data (data processing - filter in execution env)
- **Step 5**: Generate report (output)

Optimization opportunities:
- Parallel execution: Steps 2-3
- Data filtering: Step 4 (process 1000s of posts, return top 10)
- Context efficiency: Return summary, not raw data

### Step 4: Plan Skill Contents (LLM-Driven)

Based on the workflow analysis, decide what to include:

**Should you create a script?**
- ✅ Yes: Multi-step workflow, parallel execution opportunities, data filtering needed
- ❌ No: Single tool call, high variability, exploratory task

**For each script, plan**:
- Purpose and scope
- Which MCP tools it uses
- Optimization patterns (parallel, filtering, control flow)
- Parameters and return value

**Example Plan**:

Script: `scripts/workflows/product_research_pipeline.py`
- Purpose: Complete product research workflow
- MCP tools: puppeteer.fetch_page, twitter.search_tweets, reddit.search_discussions
- Optimizations: 
  - Parallel execution of Twitter + Reddit searches
  - Data filtering: Extract top 10 insights from 1000+ posts
  - Return summary, not raw data
- Parameters: product_url, product_name
- Returns: {features, sentiment, highlights}

### Step 5: Implement the Skill (LLM-Driven)

#### 5.1 Create Workflow Scripts

Write `my-skill/scripts/workflows/product_research_pipeline.py`:

```python
import asyncio
from scripts.tools import puppeteer, twitter, reddit

async def product_research_pipeline(product_url: str, product_name: str):
    """
    Complete product research workflow
    
    Optimizations:
    - Parallel Twitter + Reddit searches (2x faster)
    - Data filtering in execution environment
    - Returns summary, not raw data
    """
    
    # Fetch official website
    official = await puppeteer.fetch_page(product_url)
    
    # Parallel social media research
    twitter_data, reddit_data = await asyncio.gather(
        twitter.search_tweets(f'"{product_name}"'),
        reddit.search_discussions(product_name, subreddits=['SaaS'])
    )
    
    # Process in execution environment (not in context)
    key_features = extract_features(official, top_n=10)
    sentiment = analyze_sentiment([twitter_data, reddit_data])
    highlights = extract_highlights(twitter_data + reddit_data, top_n=5)
    
    # Return summary only
    return {
        'key_features': key_features,
        'sentiment': sentiment,
        'highlights': highlights,
        'mention_count': len(twitter_data) + len(reddit_data)
    }


def extract_features(html: str, top_n: int) -> list:
    """Extract key features from website HTML"""
    # TODO: Implement feature extraction logic
    return []

def analyze_sentiment(social_data: list) -> dict:
    """Analyze sentiment from social media posts"""
    # TODO: Implement sentiment analysis
    return {'score': 0, 'summary': ''}

def extract_highlights(posts: list, top_n: int) -> list:
    """Extract most relevant highlights from posts"""
    # TODO: Implement highlight extraction
    return []
```

**Key principles**:
- Use `async`/`await` for IO-bound operations
- Combine related MCP calls into single scripts
- Filter/aggregate data in execution environment
- Return summaries, not raw data
- Include helper functions for data processing

#### 5.2 Write SKILL.md

Create `my-skill/SKILL.md` embedding user preferences and SOPs:

```markdown
---
name: product-research-workflow
description: Automated product research integrating official sources and social platforms with emphasis on quantitative metrics and recent information
---

# Product Research Workflow

Efficiently research internet products by gathering data from official sources 
and social platforms, following your standard research methodology.

## Workflow Overview

This skill implements your research process with built-in optimizations:

1. **Official Source Analysis**: Visit product website to extract key features 
   and positioning (your SOP: always start with official sources)

2. **Social Intelligence Gathering**: Search Twitter and Reddit in parallel 
   for community feedback (optimized: 2x faster than sequential)

3. **Cross-Reference Analysis**: Identify contradictions between official claims 
   and community feedback (your preference: highlight discrepancies)

4. **Report Generation**: Create comprehensive report emphasizing quantitative 
   metrics like ratings and user counts (your preference: quant > qual)

## Quick Start

```python
from scripts.workflows import product_research_pipeline

report = await product_research_pipeline(
    product_url='https://example.com',
    product_name='ExampleApp'
)
```

## Available Workflows

### product_research_pipeline

**Use when**: Researching any new internet product or SaaS tool

**Location**: `scripts/workflows/product_research_pipeline.py`

**Optimizations**:
- 2x faster via parallel social media gathering
- Context-efficient: processes 1000s of posts, returns top 10 insights
- Recent info prioritized (aligns with your preference)

**Usage**:
```python
from scripts.workflows import product_research_pipeline

result = await product_research_pipeline(
    product_url='https://product.com',
    product_name='ProductName'
)

# Result structure:
# {
#   'key_features': ['Feature 1', 'Feature 2', ...],
#   'sentiment': {'score': 0.75, 'summary': '...'},
#   'highlights': ['Highlight 1', ...],
#   'mention_count': 247
# }
```

## MCP Tools Available

### puppeteer

**Tools**: 5 available

**Location**: `scripts/tools/puppeteer/`

**Key tools**: fetch_page, screenshot, pdf_export

**Discovery**: Use `ls scripts/tools/puppeteer/` to see all tools

### twitter

**Tools**: 3 available  

**Location**: `scripts/tools/twitter/`

**Key tools**: search_tweets, get_user_timeline

**Discovery**: Use `ls scripts/tools/twitter/` to see all tools

## Performance Notes

- **Token reduction**: 98.7% fewer tokens vs loading all tools upfront
- **Speed**: 2x faster via parallel execution  
- **Context efficiency**: Processes large datasets, returns summaries

## Advanced Usage

For custom workflows, combine individual MCP tools:

```python
from scripts.tools import puppeteer, twitter

# Custom combination
official_data = await puppeteer.fetch_page(url)
tweets = await twitter.search_tweets(query)

# Your own processing logic...
```
```

**Critical**: Notice how preferences and SOPs are embedded into the workflow description, not as separate sections.

### Step 6: Package and Deliver

Once the skill is complete:

```bash
python /mnt/skills/public/skill-creator/scripts/package_skill.py my-skill
```

This creates `my-skill.skill` file ready for distribution.

## Complete Example

Let's create a product research skill from start to finish:

### 1. Gather Input

User provides:
```
MCP Servers: puppeteer, twitter
Workflow: "Visit official site, check Twitter, create report"
Preferences: "Quantitative metrics preferred, recent info valued"
SOPs: "Always start with official sources"
```

### 2. Generate Infrastructure

```bash
# Create config
cat > mcp_config.json << 'EOF'
{
  "servers": [
    {"name": "puppeteer", "command": ["npx", "-y", "@modelcontextprotocol/server-puppeteer"]},
    {"name": "twitter", "command": ["npx", "-y", "@modelcontextprotocol/server-twitter"]}
  ]
}
EOF

# Introspect
python scripts/mcp_introspector.py mcp_config.json introspection.json

# Generate wrappers
mkdir -p product-research-skill
python scripts/generate_mcp_wrappers.py introspection.json product-research-skill
```

### 3-5. Create Skill (LLM)

Claude analyzes workflow, creates workflow script, writes SKILL.md with embedded preferences.

### 6. Package

```bash
python /mnt/skills/public/skill-creator/scripts/package_skill.py product-research-skill
```

Done! You now have `product-research-skill.skill`.

## Tips for Success

### Writing Good Workflow Descriptions

✅ **Good**:
- "First I visit the official website, then check Twitter and Reddit, finally create a report"
- Numbered steps with clear actions
- Mentions data sources explicitly

❌ **Bad**:
- "I research products" (too vague)
- No clear sequence
- Missing data sources

### Embedding Preferences Effectively

✅ **Good**: Weave into workflow guidance
```markdown
This skill gathers quantitative metrics (ratings, user counts) from multiple 
sources, prioritizing recent information over older reviews.
```

❌ **Bad**: Separate section
```markdown
## User Preferences
- Likes quantitative metrics
- Prefers recent info
```

### When to Create Scripts vs Guidance

**Create Scripts**:
- 3+ step workflows
- Parallel execution opportunities
- Data filtering needs
- Repeated code patterns

**Use Text Guidance**:
- Ad-hoc exploration
- High variability
- Simple tool usage
- Flexibility needed

## Troubleshooting

### MCP Connection Errors

```bash
# Test MCP server manually
npx -y @modelcontextprotocol/server-puppeteer

# Check output for errors
```

### Import Errors

```bash
# Ensure MCP SDK installed
pip install mcp --break-system-packages

# Verify Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/my-skill"
```

### Generated Code Issues

- Review generated wrappers in `scripts/tools/`
- Customize as needed (they're templates)
- Test scripts before packaging

## Next Steps

- Read `references/mcp-best-practices.md` for advanced patterns
- Explore `references/example-config.json` for complete examples
- Customize generated scripts for your specific needs
- Build a library of workflow skills!

## Getting Help

- MCP best practices: `references/mcp-best-practices.md`
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Anthropic's MCP Blog](https://www.anthropic.com/engineering/code-execution-with-mcp)
