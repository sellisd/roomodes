#!/usr/bin/env python3

import argparse
import json
import os
import shutil
from pathlib import Path
import sys

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def copy_files(src_dir, dest_dir, pattern):
    """Copy files matching pattern from source to destination"""
    src_path = Path(src_dir)
    for file in src_path.glob(pattern):
        shutil.copy2(file, dest_dir)
        print(f"Copied {file.name} to {dest_dir}")

def create_roomodes_file(target_dir, modes_dir):
    """Create .roomodes file with mode configurations"""
    modes = []
    modes_path = Path(modes_dir)
    
    for mode_file in modes_path.glob("*.json"):
        with open(mode_file, 'r') as f:
            mode_config = json.load(f)
            modes.append(mode_config)
    
    roomodes_config = {
        "version": "1.0.0",
        "customModes": modes
    }
    
    roomodes_path = Path(target_dir) / ".roomodes"
    with open(roomodes_path, 'w') as f:
        json.dump(roomodes_config, f, indent=2)
        print(f"Created .roomodes file at {roomodes_path}")

def setup_mcp_config(target_dir):
    """Set up MCP configuration"""
    mcp_dir = Path(target_dir) / ".roo"
    create_directory(mcp_dir)
    
    # Check for existing MCP configuration
    dest_config = mcp_dir / "mcp.json"
    if dest_config.exists():
        print(f"\n⚠️  Notice: Existing MCP configuration found at {dest_config}")
        print("    Preserving existing configuration. If you need to update it, please do so manually.")
        return

    # Copy new MCP configuration only if none exists
    source_config = Path("mcp-config/default.json")
    if source_config.exists():
        shutil.copy2(source_config, dest_config)
        print(f"Copied new MCP configuration to {dest_config}")
    else:
        print("Warning: MCP configuration template not found")

def main():
    parser = argparse.ArgumentParser(description="Install custom Roo modes for agile development")
    parser.add_argument("--target", required=True, help="Target project directory")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    
    if not target_dir.exists():
        print(f"Error: Target directory {target_dir} does not exist")
        sys.exit(1)

    print(f"Setting up custom Roo modes in {target_dir}")

    # Copy mode files
    print("\nInstalling mode configurations...")
    create_directory(target_dir)
    create_roomodes_file(target_dir, "modes")

    # Copy roorules
    print("\nInstalling mode rules...")
    copy_files("roorules", target_dir, ".roorules-*")

    # Set up MCP configuration
    print("\nSetting up MCP configuration...")
    setup_mcp_config(target_dir)

    print("\nInstallation complete!")
    print("\nAvailable modes:")
    print("- Product Owner (product-owner)")
    print("- Scrum Master (scrum-master)")
    print("- Tech Lead (tech-lead)")
    print("- Developer (developer)")
    print("- QA Engineer (qa)")

if __name__ == "__main__":
    main()