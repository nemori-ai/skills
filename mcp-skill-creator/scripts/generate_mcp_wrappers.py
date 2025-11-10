#!/usr/bin/env python3
"""
MCP Wrapper Generator

Creates type-safe Python wrappers for MCP tools based on their JSON Schema definitions.

Usage:
    python generate_mcp_wrappers.py <introspection.json> <output_dir>
"""

import json
import sys
from pathlib import Path
from typing import Any


def json_schema_to_python_type(schema: dict) -> str:
    """Convert JSON Schema type to Python type hint"""
    if not schema or 'type' not in schema:
        return 'Any'
    
    type_map = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'array': 'list',
        'object': 'dict',
    }
    
    schema_type = schema.get('type')
    
    if schema_type in type_map:
        python_type = type_map[schema_type]
        
        # Handle arrays with item types
        if schema_type == 'array' and 'items' in schema:
            item_type = json_schema_to_python_type(schema['items'])
            return f'list[{item_type}]'
        
        return python_type
    
    return 'Any'


def sanitize_name(name: str) -> str:
    """Sanitize tool name for Python function name"""
    # Replace hyphens and dots with underscores
    return name.replace('-', '_').replace('.', '_')


def generate_wrapper_function(tool: dict, server_name: str) -> str:
    """Generate Python wrapper function for a single MCP tool"""
    name = sanitize_name(tool['name'])
    original_name = tool['name']
    description = tool.get('description', 'No description available')
    input_schema = tool.get('input_schema', {})
    
    # Parse parameters
    properties = input_schema.get('properties', {})
    required = input_schema.get('required', [])
    
    # Build parameter list
    params = []
    param_docs = []
    
    for param_name, param_schema in properties.items():
        python_type = json_schema_to_python_type(param_schema)
        param_desc = param_schema.get('description', 'No description')
        
        if param_name in required:
            params.append(f"{param_name}: {python_type}")
        else:
            params.append(f"{param_name}: {python_type} | None = None")
        
        param_docs.append(f"        {param_name}: {param_desc}")
    
    params_str = ', '.join(params)
    param_docs_str = '\n'.join(param_docs) if param_docs else '        No parameters'
    
    # Generate function
    function_code = f'''async def {name}({params_str}) -> dict:
    """
    {description}
    
    Args:
{param_docs_str}
    
    Returns:
        dict: Result from MCP tool call
    """
    from .mcp_client import call_mcp_tool
    
    params = {{}}
'''
    
    # Add parameter packing code
    for param_name in properties.keys():
        function_code += f'''    if {param_name} is not None:
        params['{param_name}'] = {param_name}
'''
    
    function_code += f'''    
    return await call_mcp_tool('{server_name}', '{original_name}', params)
'''
    
    return function_code


def generate_mcp_client(output_dir: Path):
    """Generate the base MCP client module with working implementation"""
    client_code = '''"""
Base MCP Client

Provides foundational infrastructure for calling MCP tools.
Progressive disclosure: Load tool definitions on-demand using list_mcp_tools.py
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# Check for MCP SDK and provide helpful error message
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("\\n" + "="*70)
    print("❌ ERROR: MCP SDK not installed")
    print("="*70)
    print("\\nThis skill requires the MCP SDK to connect to MCP servers.")
    print("\\n📦 Install it with:")
    print("\\n    pip3 install mcp --break-system-packages")
    print("\\n✓ Verify installation:")
    print("\\n    python3 -c \\"import mcp; print('MCP SDK ready!')\\"")
    print("\\n💡 See SKILL.md Prerequisites section for more details.")
    print("\\n" + "="*70 + "\\n")
    sys.exit(1)


def load_mcp_config():
    """Load MCP server configuration from config file"""
    # Look for config in skill directory
    skill_dir = Path(__file__).parent.parent
    config_path = skill_dir / 'mcp_config.json'

    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            return {s['name']: s for s in config.get('servers', [])}

    return {}


MCP_SERVER_CONFIG = load_mcp_config()


async def call_mcp_tool(server_name: str, tool_name: str, params: dict) -> Any:
    """
    Call an MCP tool

    Args:
        server_name: Name of the MCP server
        tool_name: Name of the tool to call
        params: Parameters to pass to the tool

    Returns:
        Result from the MCP tool
    """
    if server_name not in MCP_SERVER_CONFIG:
        raise ValueError(
            f"MCP server '{server_name}' not configured. "
            f"Please add it to mcp_config.json"
        )

    server_config = MCP_SERVER_CONFIG[server_name]
    server_command = server_config['command']

    server_params = StdioServerParameters(
        command=server_command[0],
        args=server_command[1:] if len(server_command) > 1 else [],
    )

    # Use context manager properly - create new connection for each call
    # This is simpler and avoids connection management issues
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, params)

            # Extract content from result
            if hasattr(result, 'content') and result.content:
                # Return the first content item's text
                return result.content[0].text if result.content[0].text else result.content[0]

            return result
'''

    client_path = output_dir / 'scripts' / 'mcp_client.py'
    client_path.parent.mkdir(parents=True, exist_ok=True)
    client_path.write_text(client_code)
    print(f"  Generated: {client_path}")


def generate_server_wrappers(server_name: str, tools: list[dict], output_dir: Path):
    """Generate wrapper files for all tools in a server"""
    server_dir = output_dir / 'scripts' / 'tools' / server_name
    server_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nGenerating wrappers for '{server_name}' ({len(tools)} tools)...")
    
    # Generate __init__.py
    init_imports = []
    for tool in tools:
        func_name = sanitize_name(tool['name'])
        init_imports.append(f"from .{func_name} import {func_name}")
    
    init_code = '\n'.join(init_imports) + '\n\n__all__ = [' + ', '.join(f"'{sanitize_name(t['name'])}'" for t in tools) + ']\n'
    (server_dir / '__init__.py').write_text(init_code)
    
    # Generate individual tool files
    for tool in tools:
        func_name = sanitize_name(tool['name'])
        tool_code = generate_wrapper_function(tool, server_name)
        (server_dir / f"{func_name}.py").write_text(tool_code)
    
    print(f"  ✓ Generated wrappers in: {server_dir}")


def generate_list_tools_script(output_dir: Path):
    """Generate script to list all MCP tools dynamically (Progressive Disclosure)"""
    script_code = '''"""
List all available MCP tools from configured servers

This implements Progressive Disclosure - tools are discovered on-demand
rather than pre-loading all definitions into context.
"""

import asyncio
import json
import sys
from pathlib import Path

# Check for MCP SDK and provide helpful error message
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("\\n" + "="*70)
    print("❌ ERROR: MCP SDK not installed")
    print("="*70)
    print("\\nThis skill requires the MCP SDK to list available tools.")
    print("\\n📦 Install it with:")
    print("\\n    pip3 install mcp --break-system-packages")
    print("\\n✓ Verify installation:")
    print("\\n    python3 -c \\"import mcp; print('MCP SDK ready!')\\"")
    print("\\n💡 See SKILL.md Prerequisites section for more details.")
    print("\\n" + "="*70 + "\\n")
    sys.exit(1)


async def list_server_tools(server_name: str, server_command: list):
    """List all tools from an MCP server"""
    server_params = StdioServerParameters(
        command=server_command[0],
        args=server_command[1:] if len(server_command) > 1 else [],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List all tools
            tools_result = await session.list_tools()

            return [
                {
                    'name': tool.name,
                    'description': tool.description,
                    'input_schema': tool.inputSchema
                }
                for tool in tools_result.tools
            ]


async def main():
    # Load config
    skill_dir = Path(__file__).parent.parent
    config_path = skill_dir / 'mcp_config.json'

    with open(config_path) as f:
        config = json.load(f)

    print("="*70)
    print("MCP TOOLS REFERENCE")
    print("="*70)

    for server in config['servers']:
        server_name = server['name']
        server_command = server['command']

        print(f"\\n📦 Server: {server_name}")
        print("-"*70)

        try:
            tools = await list_server_tools(server_name, server_command)

            print(f"Total tools: {len(tools)}\\n")

            for tool in tools:
                print(f"🔧 {tool['name']}")
                print(f"   Description: {tool['description']}")

                # Show parameters
                schema = tool.get('input_schema', {})
                properties = schema.get('properties', {})
                required = schema.get('required', [])

                if properties:
                    print(f"   Parameters:")
                    for param_name, param_info in properties.items():
                        param_type = param_info.get('type', 'unknown')
                        param_desc = param_info.get('description', 'No description')
                        req = " (required)" if param_name in required else " (optional)"
                        print(f"     - {param_name}: {param_type}{req}")
                        if param_desc != 'No description':
                            print(f"       {param_desc}")
                print()

        except Exception as e:
            print(f"✗ Error: {e}\\n")


if __name__ == '__main__':
    asyncio.run(main())
'''

    script_path = output_dir / 'scripts' / 'list_mcp_tools.py'
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(script_code)
    print(f"  Generated: {script_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_mcp_wrappers.py <introspection.json> <output_dir>")
        print("\nGenerates Python wrapper code for MCP tools based on introspection results.")
        sys.exit(1)
    
    introspection_file = sys.argv[1]
    output_dir = Path(sys.argv[2])
    
    # Load introspection data
    print(f"Loading introspection data from {introspection_file}")
    with open(introspection_file) as f:
        introspection_data = json.load(f)
    
    # Generate base MCP client
    print("\nGenerating base MCP client...")
    generate_mcp_client(output_dir)

    # Generate tool listing script (Progressive Disclosure)
    print("\nGenerating list_mcp_tools.py...")
    generate_list_tools_script(output_dir)

    # Generate wrappers for each server
    for server_name, server_data in introspection_data.items():
        if server_data.get('status') == 'success':
            generate_server_wrappers(
                server_name,
                server_data['tools'],
                output_dir
            )
        else:
            print(f"\n✗ Skipping '{server_name}' (introspection failed)")
    
    print("\n✓ Wrapper generation complete!")
    print(f"\nGenerated files in: {output_dir / 'scripts'}")
    print("  - mcp_client.py: Base client infrastructure (working implementation)")
    print("  - list_mcp_tools.py: Dynamic tool discovery (Progressive Disclosure)")
    print("  - tools/<server>/*.py: Type-safe tool wrappers (optional)")


if __name__ == '__main__':
    main()
