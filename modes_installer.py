#!/usr/bin/env python3

import argparse
import json
import logging
import sys
import os
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModesInstaller:
    def __init__(self, target_dir: Path, source_dir: Path = None):
        # Use modes directory relative to script location as default source
        script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.script_dir = script_dir
        
        if source_dir is None:
            source_dir = script_dir / 'modes'
        
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.custom_modes = []

    def find_mode_files(self):
        """Find all JSON files in the source directory"""
        return list(self.source_dir.glob("**/*.json"))

    def copy_roorules(self):
        """Copy roorules files to target project root"""
        try:
            roorules_dir = self.script_dir / 'roorules'
            if not roorules_dir.exists():
                logger.error(f"Roorules directory not found: {roorules_dir}")
                return

            # Copy all .roorules-* files
            for rule_file in roorules_dir.glob('.roorules-*'):
                dest_file = self.target_dir / rule_file.name
                shutil.copy2(rule_file, dest_file)
                logger.info(f"Copied {rule_file.name}")

        except Exception as e:
            logger.error(f"Failed to copy roorules files: {e}")
            sys.exit(1)

    def copy_mcp_config(self):
        """Copy default MCP configuration to target project"""
        try:
            mcp_config_dir = self.target_dir / '.roo'
            mcp_config_dir.mkdir(parents=True, exist_ok=True)
            src_file = self.script_dir / 'mcp-config' / 'default.json'
            dest_file = mcp_config_dir / 'mcp.json'
            shutil.copy2(src_file, dest_file)
            logger.info("Copied MCP configuration file")
        except Exception as e:
            logger.error(f"Failed to copy MCP configuration file: {e}")
            sys.exit(1)
    def update_gitignore(self):
        """Update .gitignore to exclude MCP configuration file"""
        gitignore_path = self.target_dir / '.gitignore'
        mcp_ignore_line = '.roo/mcp.json'

        try:
            # Check if .gitignore exists and if the line is already there
            if gitignore_path.exists():
                with gitignore_path.open('r', encoding='utf-8') as f:
                    lines = f.readlines()
                if not any(line.strip() == mcp_ignore_line for line in lines):
                    # Add newline if file doesn't end with one
                    if lines and not lines[-1].endswith('\n'):
                        lines.append('\n')
                    lines.append(f"{mcp_ignore_line}\n")
                    with gitignore_path.open('w', encoding='utf-8') as f:
                        f.writelines(lines)
                    logger.info("Updated .gitignore")
            else:
                # Create new .gitignore with the line
                with gitignore_path.open('w', encoding='utf-8') as f:
                    f.write(f"{mcp_ignore_line}\n")
                logger.info("Created .gitignore")
        except Exception as e:
            logger.error(f"Failed to update .gitignore: {e}")
            sys.exit(1)


    def create_roomodes_file(self):
        """Create .roomodes file in project root"""
        try:
            config = {
                "customModes": self.custom_modes
            }
            roomodes_file = self.target_dir / '.roomodes'
            with roomodes_file.open('w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            logger.info("Created .roomodes configuration file")
        except Exception as e:
            logger.error(f"Failed to create .roomodes file: {e}")
            sys.exit(1)

    def install_modes(self):
        """Load mode files, create .roomodes configuration, and copy roorules"""
        try:
            # Ensure source directory exists
            if not self.source_dir.exists():
                logger.error(f"Source directory not found: {self.source_dir}")
                sys.exit(1)

            # Create target directory if it doesn't exist
            self.target_dir.mkdir(parents=True, exist_ok=True)

            # Find mode files
            mode_files = self.find_mode_files()
            if not mode_files:
                logger.error(f"No mode files found in {self.source_dir}")
                return

            # Load each mode file
            for src_file in mode_files:
                try:
                    # Read source file
                    with src_file.open('r', encoding='utf-8') as f:
                        mode_data = json.load(f)
                        self.custom_modes.append(mode_data)
                    logger.info(f"Loaded mode: {src_file.name}")
                except Exception as e:
                    logger.error(f"Failed to load {src_file.name}: {e}")

            # Create .roomodes file with all modes
            self.create_roomodes_file()

            # Copy roorules files
            self.copy_roorules()

            # Copy MCP configuration and update gitignore
            self.copy_mcp_config()
            self.update_gitignore()

            logger.info("Mode installation completed successfully")

        except Exception as e:
            logger.error(f"Installation failed: {e}")
            sys.exit(1)

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Install custom modes into a project")
    parser.add_argument("--source", type=Path, help="Source directory containing mode definitions (default: ./modes)")
    parser.add_argument("--target", type=Path, required=True, help="Target project directory")
    args = parser.parse_args()

    # Run installer
    installer = ModesInstaller(target_dir=args.target, source_dir=args.source)
    installer.install_modes()

if __name__ == "__main__":
    main()