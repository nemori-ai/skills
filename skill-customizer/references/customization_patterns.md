# Customization Patterns Reference

This comprehensive guide provides detailed examples, patterns, and best practices for customizing skills effectively.

## Table of Contents

1. [Modification Patterns by Type](#modification-patterns-by-type)
2. [Before/After Examples](#beforeafter-examples)
3. [Common Challenges and Solutions](#common-challenges-and-solutions)
4. [Advanced Techniques](#advanced-techniques)
5. [Maintenance Best Practices](#maintenance-best-practices)

---

## Modification Patterns by Type

### Pattern 1: Output Format Customization

**Use case:** User prefers a different output format than the skill's default

**Common scenarios:**
- JSON → Markdown conversion
- Adding/removing metadata fields
- Changing table formats
- Customizing citations or references

**Implementation approach:**

1. **Simple format preference** (Markdown vs JSON):
   - Modify SKILL.md to specify new default format
   - Update examples to show new format
   - If script-based, add format parameter to scripts

2. **Complex formatting requirements** (company style guide):
   - Create `scripts/custom_formatter.py` with formatting functions
   - Add `references/format_guide.md` with detailed specifications
   - Update SKILL.md to reference custom formatter
   - Provide examples of correctly formatted output

**Example modification:**

```markdown
# Before (in SKILL.md):
## Output Format
Return results as JSON with the following structure:
{
  "title": "...",
  "content": "..."
}

# After (customized for Markdown preference):
## Output Format
Return results as Markdown with the following structure:

# [Title]

[Content]

Source: [Document name, page X]
```

### Pattern 2: Workflow Simplification

**Use case:** User only uses a subset of the skill's features

**Common scenarios:**
- Removing unused sections from decision trees
- Focusing on a single primary workflow
- Eliminating optional features
- Streamlining for repetitive tasks

**Implementation approach:**

1. **Identify core workflow:**
   - Review user's actual usage patterns
   - Determine which features are never used
   - Identify the 80/20 of user's needs

2. **Restructure SKILL.md:**
   - Move primary workflow to the top
   - Simplify or remove unused sections
   - Update decision trees to reflect focused use case
   - Consolidate related operations

3. **Update examples:**
   - Replace generic examples with user-specific scenarios
   - Focus on most common tasks
   - Remove examples for unused features

**Example modification:**

```markdown
# Before: Generic PDF skill with many capabilities
## Capabilities
1. Extract text
2. Extract tables
3. Extract images
4. Merge PDFs
5. Split PDFs
6. Rotate pages
7. Add watermarks
8. Fill forms

# After: Streamlined for table extraction use case
## Primary Workflow: Table Extraction

Extract tables from PDF documents and output as CSV.

### Quick Start
[Focused table extraction workflow]

### Advanced Options
- Multi-page table handling
- Custom column mapping
- Header detection

(Other capabilities removed or moved to appendix)
```

### Pattern 3: Domain Context Addition

**Use case:** User works in a specialized domain requiring specific knowledge

**Common scenarios:**
- Adding industry terminology
- Including domain-specific schemas
- Incorporating regulatory requirements
- Adding company-specific processes

**Implementation approach:**

1. **Create domain reference files:**
   - `references/domain_glossary.md` - Terminology and definitions
   - `references/domain_schemas.md` - Data structures and standards
   - `references/domain_workflows.md` - Industry-specific processes

2. **Update SKILL.md:**
   - Add domain context to overview
   - Reference domain files in relevant sections
   - Include domain-specific examples
   - Adjust language for domain audience

3. **Add domain assets:**
   - Templates specific to the domain
   - Sample documents from the domain
   - Domain-specific boilerplate

**Example modification:**

```markdown
# Before: Generic document processing
## Overview
Process documents to extract and analyze content.

# After: Healthcare-specific document processing
## Overview
Process healthcare documents (clinical notes, lab reports, discharge summaries)
according to HL7 and HIPAA standards. Extract structured medical information
while maintaining compliance with healthcare regulations.

## Domain Context
Load `references/medical_terminology.md` for standardized medical terms and codes.
Load `references/hipaa_compliance.md` for data handling requirements.

## Workflows
[Updated with healthcare-specific examples and terminology]
```

### Pattern 4: Parameter Default Adjustment

**Use case:** User consistently uses different parameters than skill defaults

**Common scenarios:**
- Changing verbosity levels
- Adjusting processing thresholds
- Modifying timeout or retry settings
- Updating file format preferences

**Implementation approach:**

1. **In SKILL.md:**
   - Update default values in workflow descriptions
   - Modify examples to use new defaults
   - Document when non-default values might be appropriate

2. **In scripts:**
   - Change default parameter values in function signatures
   - Update configuration constants
   - Maintain backward compatibility if needed

**Example modification:**

```python
# Before: scripts/extractor.py
def extract_text(pdf_path, verbosity='verbose'):
    """Extract text with verbose output by default"""
    if verbosity == 'verbose':
        # Include metadata, page numbers, formatting
        pass
    else:
        # Concise output
        pass

# After: Customized for concise preference
def extract_text(pdf_path, verbosity='concise'):
    """Extract text with concise output by default (customized)"""
    if verbosity == 'concise':
        # Clean text only
        pass
    else:
        # Include additional details
        pass
```

### Pattern 5: Tool Integration

**Use case:** User wants to integrate with specific tools or services

**Common scenarios:**
- Adding API integrations
- Connecting to company databases
- Integrating with project management tools
- Automating with company workflows

**Implementation approach:**

1. **Create integration scripts:**
   - `scripts/api_connector.py` - Handle API authentication and calls
   - `scripts/data_transformer.py` - Convert between formats

2. **Add integration documentation:**
   - `references/api_setup.md` - Configuration instructions
   - `references/authentication.md` - Credential management

3. **Update SKILL.md:**
   - Add integration setup steps
   - Document new workflows enabled by integration
   - Provide troubleshooting guidance

**Example modification:**

```markdown
# Added to SKILL.md:

## Notion Integration

This customized version integrates with Notion to automatically save processed
documents to your Notion workspace.

### Setup
1. Generate Notion API token (see references/notion_setup.md)
2. Set NOTION_TOKEN environment variable
3. Configure target database ID

### Workflow
After processing a document:
1. Extract content using standard workflow
2. Format for Notion (using scripts/notion_formatter.py)
3. Upload to specified Notion database
4. Return Notion page URL

### Scripts
- scripts/notion_connector.py - Handle Notion API calls
- scripts/notion_formatter.py - Convert to Notion blocks
```

---

## Before/After Examples

### Example 1: PDF Skill → My PDF Tables

**Original use case:** General PDF processing
**Customized use case:** Quick table extraction for financial reports

#### Before: Generic PDF skill excerpt

```markdown
## Capabilities

### Extract Text
Use pypdf or pdfplumber to extract text content...

### Extract Tables
Use pdfplumber to extract tables...
[Detailed multi-option workflow]

### Merge PDFs
Combine multiple PDF files...

### Split PDFs
Separate PDF into individual pages...
```

#### After: Streamlined for table extraction

```markdown
## Primary Workflow: Financial Report Table Extraction

Extract tables from financial PDF reports and output as CSV files with
proper numeric formatting.

### Quick Workflow
1. Load PDF using pdfplumber
2. Detect tables on each page
3. Extract with financial number formatting preserved
4. Output as CSV with headers
5. Include source page reference

### Default Settings (Customized)
- Output format: CSV (not JSON)
- Number format: Preserve commas and decimal points
- Headers: Auto-detect from first row
- Multiple tables: Separate files with page suffix

### Example
Input: quarterly_report.pdf
Output: quarterly_report_p3_table1.csv, quarterly_report_p3_table2.csv

[Detailed table extraction code with financial formatting]

---
Note: Other PDF capabilities (merge, split, etc.) removed for focus.
Refer to base 'pdf' skill if needed.
```

### Example 2: Internal Comms → Company X Communications

**Original use case:** General internal communications
**Customized use case:** Company X-specific communication standards

#### Before: Generic internal comms

```markdown
## Writing Status Updates

Write clear status updates for internal teams.

### Structure
- Summary
- Progress
- Blockers
- Next steps

### Tone
Professional and clear.
```

#### After: Company X customized

```markdown
## Writing Status Updates (Company X Standard)

Follow Company X communication guidelines (references/company_style_guide.md).

### Structure (Company X Template)
1. **TL;DR** - One-sentence summary
2. **Highlights** - 3-5 bullet points (emoji required per style guide)
3. **Metrics** - Include OKR alignment
4. **Blockers** - Use RAG status (Red/Amber/Green)
5. **Next Steps** - Include owner and due date
6. **Links** - Notion doc, Jira tickets, Slack thread

### Tone
Match Company X voice:
- Casual but professional
- Use "we" not "I"
- Default to transparent/public sharing
- Include memes/GIFs when appropriate

### Template
Use assets/company_x_status_template.md as starting point.

### Example Output
[Shows Company X-specific format with emojis, RAG status, etc.]
```

### Example 3: Canvas Design → Medical Infographic Designer

**Original use case:** General visual design
**Customized use case:** Medical education infographics

#### Before: Generic design instructions

```markdown
## Design Principles
- Use color theory for visual hierarchy
- Balance composition
- Choose appropriate typography
- Create clear focal points
```

#### After: Medical infographic specific

```markdown
## Medical Infographic Design Principles

Follow medical education best practices and accessibility standards.

### Color Requirements
- Use colorblind-safe palette (references/medical_colors.md)
- Avoid red/green for critical distinctions
- High contrast ratios (WCAG AAA)
- Use color + pattern for differentiation

### Typography
- Sans-serif for body (Arial, Helvetica)
- Minimum 14pt for body text (readability for all ages)
- Medical terms in bold on first use
- Include pronunciation guides for complex terms

### Medical Content Standards
- Cite sources (AMA format)
- Include disclaimer for educational use
- Use anatomically correct illustrations from assets/medical_images/
- Follow HIPAA guidelines for any patient data

### Layout
- Clear information hierarchy (diagnosis → symptoms → treatment)
- Use flowcharts for decision trees
- Include legend for all symbols
- Mobile-friendly formatting (many clinicians use tablets)

### Assets
- assets/anatomical_illustrations/ - Approved medical illustrations
- assets/medical_icons/ - Standard medical symbol set
- assets/citation_template.txt - AMA citation format
```

---

## Common Challenges and Solutions

### Challenge 1: Balancing Customization vs. Reusability

**Problem:** Over-customizing for a single task makes the skill too narrow

**Solutions:**
1. **Parameterize instead of hardcode:**
   - Use configuration files for user-specific values
   - Make customizations optional/togglable
   - Provide defaults but allow overrides

2. **Document the scope:**
   - Clearly state what the customized skill is for
   - List related use cases it still supports
   - Note when to use base skill vs. customized version

3. **Version thoughtfully:**
   - Keep base fork for general use
   - Create specialized forks for very specific needs
   - Document fork relationships

**Example:**
```markdown
# In SKILL.md metadata:
metadata:
  customized-from: pdf
  customization-scope: Financial report table extraction
  also-works-for: Quarterly reports, balance sheets, income statements
  not-suitable-for: Image extraction, form filling, general PDFs
```

### Challenge 2: Keeping Customizations Maintainable

**Problem:** Hard to remember what was changed and why after time passes

**Solutions:**
1. **Comprehensive CUSTOMIZATION_LOG.md:**
   - Document every change with rationale
   - Include "why" not just "what"
   - Note testing procedures

2. **Inline comments in modified scripts:**
   ```python
   # CUSTOMIZED: Changed default from 'verbose' to 'concise'
   # Reason: User preference for minimal output (see CUSTOMIZATION_LOG v1.1)
   def process(verbosity='concise'):
       pass
   ```

3. **Version number in SKILL.md:**
   ```yaml
   metadata:
     customization-version: 2.3
     last-updated: 2025-10-21
   ```

### Challenge 3: Merging Updates from Base Skill

**Problem:** Base skill gets updates/improvements that you want in customized version

**Solutions:**
1. **Track base skill version:**
   ```yaml
   metadata:
     customized-from: pdf
     base-skill-version: 1.0
     last-sync-date: 2025-10-21
   ```

2. **Manual merge process:**
   - Review base skill changelog
   - Identify relevant updates
   - Apply updates manually to customized version
   - Test thoroughly
   - Update metadata

3. **Minimize deep modifications:**
   - Prefer additions over modifications when possible
   - Use wrapper scripts instead of editing base scripts
   - Keep modifications isolated and documented

### Challenge 4: Multiple Users with Different Preferences

**Problem:** Team wants shared skill but members have different preferences

**Solutions:**
1. **Configuration-driven approach:**
   - Create `config.yaml` for user preferences
   - Each user maintains their own config
   - Skill reads config at runtime

   ```python
   # scripts/config.py
   import yaml

   def load_user_config():
       config_path = Path.home() / '.skill-config' / 'pdf-config.yaml'
       if config_path.exists():
           return yaml.safe_load(config_path.read_text())
       return default_config()
   ```

2. **Profile-based customization:**
   - Create named profiles (analyst, researcher, designer)
   - User selects profile at runtime
   - Skill applies profile-specific settings

3. **Fork per user or team:**
   - Maintain individual forks for strongly divergent needs
   - Share common base scripts as library
   - Document fork relationships

### Challenge 5: Testing Customized Skills

**Problem:** Ensuring customizations work as intended without breaking functionality

**Solutions:**
1. **Maintain test cases:**
   - Document specific test scenarios in CUSTOMIZATION_LOG.md
   - Keep sample input files in `tests/` directory
   - Define expected outputs for each customization

2. **Before/after comparison:**
   - Run same task on base skill and customized skill
   - Compare outputs
   - Verify customizations took effect
   - Check for unintended side effects

3. **Regression testing:**
   - Test previous use cases when adding new customizations
   - Ensure new changes don't break earlier improvements
   - Maintain a test checklist

**Example test checklist:**
```markdown
# Test Checklist for my-pdf-tables v2.1

- [ ] Basic table extraction works
- [ ] Financial numbers preserve formatting
- [ ] Multi-page tables handled correctly
- [ ] CSV output has correct headers
- [ ] Page numbers included in filename
- [ ] Previous customizations still work:
  - [ ] v1.1: Concise output format
  - [ ] v1.5: Auto-header detection
  - [ ] v2.0: Multiple table separation
```

---

## Advanced Techniques

### Technique 1: Layered Customization

Create a hierarchy of customizations for progressive specialization:

```
pdf (base skill)
  └── my-pdf-workflow (general personal customizations)
      ├── financial-pdf (financial reports)
      └── research-pdf (academic papers)
```

**Implementation:**
1. First fork: Personal preferences (output format, defaults)
2. Second fork: Domain-specific (financial vs. research)
3. Document fork hierarchy in metadata

**Benefits:**
- Share common customizations
- Specialize without duplication
- Easy to maintain related forks

### Technique 2: Plugin/Extension Pattern

Design customizations as plugins that extend base skill without modifying it:

**Structure:**
```
my-pdf/
  ├── SKILL.md (references base + extensions)
  ├── scripts/
  │   ├── extensions/
  │   │   ├── financial_formatter.py
  │   │   └── auto_namer.py
  └── references/
      └── base_skill.md (copy of original for reference)
```

**In SKILL.md:**
```markdown
## Base Capabilities
Refer to references/base_skill.md for standard PDF operations.

## Extensions
This customized version adds:
- Financial number formatting (scripts/extensions/financial_formatter.py)
- Smart file naming (scripts/extensions/auto_namer.py)

Use base capabilities as documented, then apply extensions as needed.
```

**Benefits:**
- Clear separation of base vs. custom
- Easier to maintain
- Simple to add/remove extensions

### Technique 3: Template-Based Customization

For skills that generate content, use templates to customize output:

**Structure:**
```
my-comms/
  ├── SKILL.md
  ├── scripts/
  │   └── template_renderer.py
  └── assets/
      ├── templates/
      │   ├── status_update.md
      │   ├── project_brief.md
      │   └── incident_report.md
```

**Usage:**
```python
# scripts/template_renderer.py
from jinja2 import Template

def render_status_update(data):
    template_path = Path('assets/templates/status_update.md')
    template = Template(template_path.read_text())
    return template.render(**data)
```

**Benefits:**
- Easy to customize without code changes
- Non-technical users can update templates
- Consistent formatting across outputs

### Technique 4: Conditional Behavior Based on Context

Adapt skill behavior based on detected context:

```python
# scripts/context_detector.py

def detect_context(document_path):
    """Detect document type/context to apply appropriate customizations"""
    content = read_document(document_path)

    if 'QUARTERLY REPORT' in content[:1000]:
        return 'financial_quarterly'
    elif 'BALANCE SHEET' in content[:1000]:
        return 'financial_balance'
    elif 'CLINICAL NOTES' in content[:500]:
        return 'medical_clinical'
    else:
        return 'general'

def process_with_context(document_path):
    context = detect_context(document_path)

    if context == 'financial_quarterly':
        return process_financial_quarterly(document_path)
    elif context == 'medical_clinical':
        return process_medical_clinical(document_path)
    else:
        return process_general(document_path)
```

**Benefits:**
- Single skill handles multiple specialized scenarios
- Automatic context adaptation
- User doesn't need to specify type

### Technique 5: Feedback-Driven Auto-Refinement

Build in feedback collection and analysis:

```python
# scripts/track_usage.py

def log_usage(task_type, user_satisfaction, notes):
    """Log usage to identify improvement opportunities"""
    usage_log = Path('USAGE_LOG.jsonl')

    entry = {
        'timestamp': datetime.now().isoformat(),
        'task_type': task_type,
        'satisfaction': user_satisfaction,  # 1-5
        'notes': notes
    }

    with open(usage_log, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def analyze_usage_patterns():
    """Analyze usage log to identify customization opportunities"""
    # Find low-satisfaction tasks
    # Identify common pain points
    # Suggest targeted improvements
    pass
```

**Benefits:**
- Data-driven customization decisions
- Identify patterns over time
- Prioritize highest-impact improvements

---

## Maintenance Best Practices

### Best Practice 1: Regular Review Cycles

**Schedule:** Review customized skills quarterly or after major projects

**Review checklist:**
- Are customizations still relevant?
- Any new pain points to address?
- Can any customizations be generalized?
- Are there unused customizations to remove?
- Does documentation need updates?

### Best Practice 2: Version Control

Use git or similar for tracking changes:

```bash
cd my-customized-skill/
git init
git add .
git commit -m "Initial fork from base skill"

# After each customization iteration
git add .
git commit -m "v1.1: Changed default output format to Markdown

- Modified SKILL.md output section
- Updated examples
- Tested on sample documents

Addresses feedback from 2025-10-15"
```

**Benefits:**
- Track change history
- Easy to revert problematic changes
- Collaborate with others
- Maintain multiple versions

### Best Practice 3: Documentation as Code

Keep documentation close to implementation:

```python
# scripts/financial_formatter.py
"""
Financial number formatter for PDF table extraction

Customization History:
- v1.1 (2025-10-15): Added comma preservation
- v1.2 (2025-10-18): Added currency symbol detection
- v2.0 (2025-10-20): Support for European number formats

Related customization log entries: v1.1, v1.2, v2.0
"""

def format_financial_number(value, preserve_commas=True):
    """
    Format extracted number for financial reports

    Args:
        value: Extracted number string
        preserve_commas: Keep thousand separators (default: True per v1.1)

    Returns:
        Formatted number string

    Examples:
        >>> format_financial_number("1,234.56")
        "1,234.56"

        >>> format_financial_number("1.234,56")  # European format, v2.0
        "1.234,56"
    """
    pass
```

### Best Practice 4: Maintain a CHANGELOG

Separate from CUSTOMIZATION_LOG.md, maintain a user-facing changelog:

```markdown
# Changelog: my-pdf-tables

## [2.0.0] - 2025-10-20
### Added
- Support for European number formats (commas/periods swapped)
- Auto-detection of number format from document locale

### Changed
- Default output includes source page numbers
- Table headers now auto-detected (previously manual)

### Fixed
- Multi-page tables no longer split incorrectly

## [1.2.0] - 2025-10-18
### Added
- Currency symbol detection and preservation
- Support for parenthetical negative numbers (accounting format)

## [1.1.0] - 2025-10-15
### Changed
- Default output format: CSV (was JSON)
- Preserve comma thousand separators (was stripping)

### Removed
- Unused image extraction code from base skill

## [1.0.0] - 2025-10-10
### Added
- Initial fork from 'pdf' base skill
- Focus on table extraction workflow
```

### Best Practice 5: Share and Learn

**Within teams:**
- Share successful customization patterns
- Document what worked and what didn't
- Create organization-wide customization library
- Hold periodic skill review sessions

**With community:**
- Contribute useful patterns back to base skills
- Share generalized customizations
- Learn from others' customization approaches

**Documentation:**
- Maintain README.md for customized skill
- Include setup instructions
- Document prerequisites
- Provide troubleshooting guide

---

## Quick Reference: When to Use Each Pattern

| Scenario | Recommended Pattern | Key Resources |
|----------|-------------------|---------------|
| Different output format | Output Format Customization | Modify SKILL.md, add formatter script |
| Only use subset of features | Workflow Simplification | Restructure SKILL.md, remove unused sections |
| Specialized domain/industry | Domain Context Addition | Add references/, update examples |
| Different default settings | Parameter Default Adjustment | Update SKILL.md, modify script defaults |
| Need to connect to other tools | Tool Integration | Add scripts/, integration docs |
| Team with varying preferences | Configuration-driven | Add config.yaml, profile system |
| Progressive specialization | Layered Customization | Multiple forks in hierarchy |
| Extend without modifying | Plugin/Extension Pattern | Extension scripts, modular design |
| Content generation | Template-Based | Templates in assets/, renderer script |
| Handle multiple scenarios | Conditional Behavior | Context detector, branching logic |

---

## Conclusion

Effective skill customization is an iterative process that balances specificity with reusability. Use these patterns as starting points, adapt them to your needs, and always document your customizations thoroughly for future reference.

Remember:
- Start small with targeted improvements
- Test each customization thoroughly
- Document rationale, not just changes
- Review and refine regularly
- Share learnings with others
