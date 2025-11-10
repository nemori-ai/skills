#!/usr/bin/env python3
"""
MCP Server Introspector

Connects to MCP servers and extracts tool definitions,
generating structured data for skill creation.

Usage:
    python mcp_introspector.py config.json output.json
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# Try to import MCP SDK, provide helpful error if not available
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("\n" + "="*70)
    print("❌ ERROR: MCP SDK not installed")
    print("="*70)
    print("\nThe MCP SDK is required to introspect MCP servers.")
    print("\n📦 Install it with:")
    print("\n    pip3 install mcp --break-system-packages")
    print("\n✓ Verify installation:")
    print("\n    python3 -c \"import mcp; print('MCP SDK ready!')\"")
    print("\n" + "="*70 + "\n")
    sys.exit(1)


async def introspect_mcp_server(server_name: str, server_command: list[str]) -> dict:
    """
    Connect to an MCP server and list all available tools
    
    Args:
        server_name: Name of the MCP server
        server_command: Command to start MCP server (e.g., ['npx', '-y', '@modelcontextprotocol/server-filesystem', '/tmp'])
    
    Returns:
        Dictionary with server capabilities and tool definitions
    """
    print(f"Introspecting MCP server: {server_name}")
    
    try:
        server_params = StdioServerParameters(
            command=server_command[0],
            args=server_command[1:] if len(server_command) > 1 else [],
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # List all tools
                tools_result = await session.list_tools()
                
                tools = []
                for tool in tools_result.tools:
                    tools.append({
                        'name': tool.name,
                        'description': tool.description,
                        'input_schema': tool.inputSchema
                    })
                
                print(f"  ✓ Found {len(tools)} tools in {server_name}")
                
                return {
                    'server_name': server_name,
                    'server_command': server_command,
                    'tool_count': len(tools),
                    'tools': tools,
                    'status': 'success'
                }
    
    except Exception as e:
        print(f"  ✗ Error introspecting {server_name}: {str(e)}")
        return {
            'server_name': server_name,
            'server_command': server_command,
            'status': 'error',
            'error': str(e)
        }


async def introspect_all_servers(server_configs: list[dict]) -> dict:
    """
    Introspect multiple MCP servers
    
    Args:
        server_configs: List of {name, command} dicts
    
    Returns:
        Dictionary mapping server names to their capabilities
    """
    results = {}
    
    for config in server_configs:
        name = config['name']
        command = config['command']
        
        result = await introspect_mcp_server(name, command)
        results[name] = result
    
    return results


def load_config(config_path: str) -> list[dict]:
    """
    Load MCP server configuration from JSON file
    
    Expected format:
    {
        "servers": [
            {
                "name": "filesystem",
                "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            },
            ...
        ]
    }
    """
    with open(config_path) as f:
        config = json.load(f)
    
    return config.get('servers', [])


def main():
    if len(sys.argv) < 3:
        print("Usage: mcp_introspector.py <config.json> <output.json>")
        print("\nConfig format:")
        print(json.dumps({
            "servers": [
                {
                    "name": "example-server",
                    "command": ["npx", "-y", "@modelcontextprotocol/server-example"]
                }
            ]
        }, indent=2))
        sys.exit(1)
    
    config_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Load configuration
    print(f"Loading MCP server configuration from {config_path}")
    server_configs = load_config(config_path)
    print(f"Found {len(server_configs)} servers to introspect\n")
    
    # Introspect all servers
    results = asyncio.run(introspect_all_servers(server_configs))
    
    # Save results
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Introspection results saved to {output_path}")
    
    # Summary
    success_count = sum(1 for r in results.values() if r.get('status') == 'success')
    total_tools = sum(r.get('tool_count', 0) for r in results.values() if r.get('status') == 'success')
    
    print(f"\nSummary:")
    print(f"  Servers successfully introspected: {success_count}/{len(server_configs)}")
    print(f"  Total tools discovered: {total_tools}")


if __name__ == '__main__':
    main()
