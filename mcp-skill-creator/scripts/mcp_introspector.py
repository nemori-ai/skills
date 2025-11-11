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
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

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


def check_command_available(command: str) -> bool:
    """Check if a command is available in PATH"""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False


def extract_npm_package(server_command: list[str]) -> Optional[str]:
    """
    Extract npm package name from MCP server command.

    Examples:
        ["npx", "-y", "@modelcontextprotocol/server-filesystem", ...]
        -> "@modelcontextprotocol/server-filesystem"
    """
    if not server_command or server_command[0] not in ["npx", "npm"]:
        return None

    # Find the package name (first argument that starts with @ or is not a flag)
    for arg in server_command[1:]:
        if not arg.startswith("-"):
            return arg

    return None


def install_npm_package(package_name: str) -> bool:
    """
    Install npm package globally.

    Args:
        package_name: npm package to install (e.g., "@modelcontextprotocol/server-filesystem")

    Returns:
        True if installation succeeded
    """
    print(f"📦 Installing MCP server: {package_name}")

    try:
        # Try global install first
        result = subprocess.run(
            ["npm", "install", "-g", package_name],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print(f"  ✓ Installed {package_name} globally")
            return True
        else:
            # If global install fails, try local install
            print(f"  ⚠️ Global install failed, trying local install...")
            result = subprocess.run(
                ["npm", "install", package_name],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print(f"  ✓ Installed {package_name} locally")
                return True
            else:
                print(f"  ✗ Failed to install {package_name}")
                print(f"     Error: {result.stderr}")
                return False

    except subprocess.TimeoutExpired:
        print(f"  ✗ Installation timed out (>120s)")
        return False
    except Exception as e:
        print(f"  ✗ Installation error: {e}")
        return False


def ensure_mcp_server_installed(server_name: str, server_command: list[str]) -> bool:
    """
    Ensure MCP server is installed before introspection.

    Returns:
        True if server is ready (already installed or successfully installed)
    """
    # Check if npm/npx is available
    if not check_command_available("npm"):
        print("⚠️ npm not found. Skipping automatic installation.")
        print("   The server command will be tried as-is.")
        return True  # Continue anyway, might work

    # Extract package name
    package_name = extract_npm_package(server_command)
    if not package_name:
        # Not an npm-based server, skip
        return True

    print(f"Checking MCP server: {package_name}")

    # Check if already installed globally
    try:
        result = subprocess.run(
            ["npm", "list", "-g", package_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"  ✓ Already installed globally")
            return True
    except:
        pass

    # Check if installed locally
    try:
        result = subprocess.run(
            ["npm", "list", package_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"  ✓ Already installed locally")
            return True
    except:
        pass

    # Not installed, attempt installation
    print(f"  ⚠️ Not installed, installing now...")
    return install_npm_package(package_name)


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
        error_msg = str(e)
        print(f"  ✗ Error introspecting {server_name}: {error_msg}")

        # Provide helpful hints for common errors
        if "npm" in error_msg.lower() or "npx" in error_msg.lower():
            print("\n💡 Troubleshooting npm/npx errors:")
            print("  1. Check network connection (can you access npmjs.org?)")
            print("  2. Try running the MCP server command manually:")
            print(f"     {' '.join(server_command)}")
            print("  3. Check npm configuration: cat ~/.npmrc")
            print("  4. If behind a proxy, configure npm proxy settings")
            print("  5. Try clearing npm cache: npm cache clean --force")
        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            print("\n💡 Connection issue - the MCP server may not be responding.")
            print("  1. Verify the server command is correct")
            print("  2. Check if the server requires authentication or additional setup")
            print("  3. Try running the command manually to see detailed error")

        return {
            'server_name': server_name,
            'server_command': server_command,
            'status': 'error',
            'error': error_msg
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

        # Ensure MCP server is installed before introspection
        if not ensure_mcp_server_installed(name, command):
            print(f"  ⚠️ Skipping {name} - installation failed")
            results[name] = {
                'server_name': name,
                'server_command': command,
                'status': 'error',
                'error': 'Failed to install MCP server'
            }
            continue

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
