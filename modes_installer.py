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
        # Base directory for modes in the target project
        self.roo_dir = self.target_dir / '.roo'
        self.modes_dir = self.roo_dir / 'modes'

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
        """Add .roo/mcp.json to .gitignore"""
        gitignore_path = self.target_dir / '.gitignore'
        pattern = '.roo/mcp.json'

        try:
            if gitignore_path.exists():
                # Append to existing file if pattern not present
                with gitignore_path.open('r+', encoding='utf-8') as f:
                    if pattern not in f.read():
                        f.write(f'\n{pattern}\n')
            else:
                # Create new file with pattern
                with gitignore_path.open('w', encoding='utf-8') as f:
                    f.write(f'{pattern}\n')
        except Exception as e:
            logger.error(f"Failed to update .gitignore: {e}")
            sys.exit(1)


    def install_mode(self, src_file: Path):
        """Install a single mode into its own directory under .roo/modes"""
        try:
            # Read source file
            with src_file.open('r', encoding='utf-8') as f:
                mode_data = json.load(f)
                
            # Create mode directory using slug
            mode_slug = mode_data['slug']
            mode_dir = self.modes_dir / mode_slug
            mode_dir.mkdir(parents=True, exist_ok=True)
            
            # Write mode.json in the mode directory
            mode_file = mode_dir / 'mode.json'
            with mode_file.open('w', encoding='utf-8') as f:
                json.dump(mode_data, f, indent=2)
                
            logger.info(f"Installed mode: {mode_slug}")
            
        except Exception as e:
            logger.error(f"Failed to install mode {src_file.name}: {e}")
            return False
        return True

    def install_modes(self):
        """Install modes into directory structure and copy configuration"""
        try:
            # Ensure source directory exists
            if not self.source_dir.exists():
                logger.error(f"Source directory not found: {self.source_dir}")
                sys.exit(1)

            # Create modes directory structure
            self.modes_dir.mkdir(parents=True, exist_ok=True)

            # Find mode files
            mode_files = self.find_mode_files()
            if not mode_files:
                logger.error(f"No mode files found in {self.source_dir}")
                return

            # Install each mode file
            success = True
            for src_file in mode_files:
                if not self.install_mode(src_file):
                    success = False

            # Copy MCP configuration and update gitignore
            self.copy_mcp_config()
            self.update_gitignore()

            # Copy roorules files (optional as they might be packaged differently)
            self.copy_roorules()

            if success:
                logger.info("Mode installation completed successfully")
            else:
                logger.warning("Mode installation completed with some errors")

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