# MCP Code Execution Best Practices

This reference document provides detailed guidance on implementing efficient MCP integrations using code execution patterns, based on [Anthropic's MCP engineering blog post](https://www.anthropic.com/engineering/code-execution-with-mcp).

## Core Principles

### 1. Progressive Disclosure

**Problem**: Loading all MCP tool definitions upfront wastes context window space.

**Solution**: Present tools as code APIs on a filesystem, allowing models to load only what they need.

```
scripts/
├── tools/
│   ├── google-drive/
│   │   ├── getDocument.ts
│   │   ├── listFiles.ts
│   │   └── index.ts
│   └── salesforce/
│       ├── updateRecord.ts
│       └── index.ts
```

**Benefits**:
- Reduces initial context from 150,000 tokens to 2,000 tokens (98.7% reduction)
- Scales to thousands of tools without overwhelming the model
- Tools loaded on-demand as needed

**Implementation**:
```python
# Agent explores filesystem
tools_available = os.listdir('scripts/tools/google-drive/')

# Agent reads only needed tool definitions
with open('scripts/tools/google-drive/getDocument.py') as f:
    tool_code = f.read()
```

### 2. Context-Efficient Data Handling

**Problem**: Intermediate results flowing through context window consume excessive tokens.

**Bad Example**:
```python
# Without code execution - all data flows through context
TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
→ returns 10,000 rows to model
→ model filters in context
→ passes filtered data to next tool
```

**Good Example**:
```python
# With code execution - filter in execution environment
sheet_data = await gdrive.getSheet({'sheetId': 'abc123'})

# Filter in execution environment (no context cost)
pending_orders = [
    row for row in sheet_data 
    if row['Status'] == 'pending' and row['Amount'] > 1000
]

# Only return summary to model
print(f"Found {len(pending_orders)} high-value pending orders")
print(pending_orders[:5])  # Show first 5 for review
```

**Benefits**:
- Processes 10,000 rows but only sends 5 to model
- Reduces token usage by 99.5%
- Faster execution, lower costs

### 3. Parallel Execution

**Problem**: Sequential tool calls waste time when operations are independent.

**Bad Example**:
```python
# Sequential execution
twitter_data = await x_com.search_tweets(query)
# Wait for Twitter...
reddit_data = await reddit.search_discussions(query)
# Wait for Reddit...
```

**Good Example**:
```python
# Parallel execution with asyncio.gather()
twitter_task = x_com.search_tweets(query)
reddit_task = reddit.search_discussions(query)
producthunt_task = producthunt.search(query)

# Execute all concurrently
results = await asyncio.gather(
    twitter_task,
    reddit_task,
    producthunt_task
)

twitter_data, reddit_data, ph_data = results
```

**Benefits**:
- 3x faster execution (if all APIs take similar time)
- Better user experience
- Efficient resource utilization

### 4. Complex Control Flow

**Problem**: Implementing loops and conditionals via sequential tool calls is inefficient.

**Bad Example**:
```python
# Agent alternates between tool calls and sleep
TOOL CALL: slack.getMessages()
→ no deployment message
SLEEP: 5 seconds
TOOL CALL: slack.getMessages()
→ no deployment message
SLEEP: 5 seconds
# ... repeat many times
```

**Good Example**:
```python
# Implement control flow in code
async def wait_for_deployment(channel: str, timeout: int = 300):
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        messages = await slack.getChannelHistory(channel, limit=10)
        
        if any('deployment complete' in m['text'].lower() for m in messages):
            return {'status': 'success', 'message': messages[0]}
        
        await asyncio.sleep(10)
    
    return {'status': 'timeout'}
```

**Benefits**:
- Single code execution instead of 60+ tool calls
- Faster time to first token
- More reliable error handling

### 5. Privacy-Preserving Operations

**Problem**: Sensitive data flowing through model context raises privacy concerns.

**Solution**: Keep sensitive data in execution environment, only share summaries.

```python
# Load sensitive customer data
customers = await gdrive.getSheet({'sheetId': 'customer_contacts'})

# Process PII in execution environment (never shown to model)
for customer in customers:
    await salesforce.updateRecord({
        'objectType': 'Lead',
        'recordId': customer['salesforce_id'],
        'data': {
            'Email': customer['email'],      # PII stays in execution env
            'Phone': customer['phone'],      # PII stays in execution env
            'Name': customer['name']         # PII stays in execution env
        }
    })

# Only summary goes to model
print(f"Updated {len(customers)} customer records")
print("✓ All contact information synchronized")
```

**Optional Enhancement**: Tokenize PII automatically in MCP client:
```python
# What model sees (if PII is tokenized):
[
  {'email': '[EMAIL_1]', 'phone': '[PHONE_1]', 'name': '[NAME_1]'},
  {'email': '[EMAIL_2]', 'phone': '[PHONE_2]', 'name': '[NAME_2]'}
]

# Real data flows Google Sheets → Salesforce without entering model context
```

### 6. State Persistence and Skills

**Problem**: Agents cannot build on previous work without memory.

**Solution**: Use filesystem to persist intermediate results and reusable functions.

**State Persistence**:
```python
# Save intermediate results
import json

intermediate_data = await fetch_and_process()

with open('./workspace/state.json', 'w') as f:
    json.dump(intermediate_data, f)

# Later execution picks up where it left off
with open('./workspace/state.json') as f:
    state = json.load(f)
```

**Skill Evolution**:
```python
# Save reusable function as a skill
# In ./skills/save-sheet-as-csv.py
import pandas as pd
from scripts.tools import gdrive

async def save_sheet_as_csv(sheet_id: str, output_path: str):
    """
    Reusable function to export Google Sheet as CSV
    """
    data = await gdrive.getSheet({'sheetId': sheet_id})
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    return output_path

# Later, in any workflow:
from skills.save_sheet_as_csv import save_sheet_as_csv

csv_path = await save_sheet_as_csv('abc123', './data/export.csv')
```

**Add SKILL.md** to create structured skill:
```markdown
---
name: sheet-csv-exporter
description: Export Google Sheets to CSV format
---

# Sheet CSV Exporter

Provides a reusable function for exporting Google Sheets to CSV files.

## Usage

```python
from skills.save_sheet_as_csv import save_sheet_as_csv

csv_path = await save_sheet_as_csv(
    sheet_id='your-sheet-id',
    output_path='./output/data.csv'
)
```
```

## Token Usage Comparison

| Approach | Token Usage | Latency | Privacy |
|----------|-------------|---------|---------|
| **Direct Tool Calls** | 150,000+ tokens (all tool definitions loaded) | High (sequential calls) | ⚠️ All data through context |
| **Code Execution with MCP** | 2,000 tokens (load on demand) | Low (parallel execution) | ✅ Data filtered/tokenized |

**Savings**: 98.7% token reduction, 3-5x faster execution

## When to Use Code Execution

✅ **Use code execution when**:
- Working with many MCP tools (>10 tools)
- Processing large datasets (>1000 rows)
- Need parallel API calls
- Workflow involves loops/conditionals
- Privacy concerns with sensitive data
- Building reusable workflows

❌ **Avoid code execution when**:
- Simple single tool call
- Small data amounts
- Quick ad-hoc tasks
- No performance concerns
- Execution environment unavailable

## Implementation Considerations

### Security
- Sandbox execution environment properly
- Limit resource usage (CPU, memory, time)
- Monitor for malicious code patterns
- Validate all inputs

### Error Handling
```python
try:
    result = await mcp_tool(params)
except Exception as e:
    # Log error
    logger.error(f"MCP tool failed: {e}")
    # Return graceful fallback
    return {'error': str(e), 'status': 'failed'}
```

### Testing
- Test scripts in isolation
- Mock MCP tool responses
- Verify error handling
- Check performance gains

## Examples from Production

### Example 1: Document Processing Pipeline
```python
async def process_contracts(folder_id: str):
    """Process all contracts in a folder"""
    # 1. List all files (single MCP call)
    files = await gdrive.listFiles({'folderId': folder_id})
    
    # 2. Filter in execution environment
    pdf_files = [f for f in files if f['type'] == 'pdf']
    
    # 3. Parallel processing
    results = await asyncio.gather(*[
        extract_contract_data(f['id']) 
        for f in pdf_files
    ])
    
    # 4. Aggregate and save
    summary = aggregate_contract_summary(results)
    
    # Only summary to model
    return {
        'total_contracts': len(pdf_files),
        'processed': len(results),
        'summary': summary[:500]  # Truncate for context
    }
```

### Example 2: Social Media Monitoring
```python
async def monitor_brand_mentions(brand: str):
    """Monitor brand across multiple platforms"""
    # Parallel fetch from multiple sources
    twitter_task = x_com.search_tweets(f'"{brand}"')
    reddit_task = reddit.search(brand, subreddits=['technology'])
    hn_task = hackernews.search(brand)
    
    mentions = await asyncio.gather(
        twitter_task, reddit_task, hn_task
    )
    
    # Sentiment analysis in execution environment
    sentiment = analyze_sentiment_batch(mentions)
    
    # Filter and aggregate
    recent_mentions = filter_last_24h(mentions)
    key_insights = extract_key_insights(recent_mentions)
    
    return {
        'mention_count': len(recent_mentions),
        'sentiment': sentiment,
        'key_insights': key_insights,
        'platforms': {
            'twitter': len(mentions[0]),
            'reddit': len(mentions[1]),
            'hackernews': len(mentions[2])
        }
    }
```

## Further Reading

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [Anthropic MCP Engineering Blog](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode/)
