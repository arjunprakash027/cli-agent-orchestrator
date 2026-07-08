import os
import subprocess
import sys
import shutil
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class WebUIBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # We only want to compile the frontend when building a wheel (distribution)
        if self.target_name != "wheel":
            return

        root_dir = Path(__file__).parent.resolve()
        web_dir = root_dir / "web"
        
        # 1. Check if npm is available
        npm_path = shutil.which("npm")
        if not npm_path:
            # Optionally: Code to download a portable node binary for the OS/Arch,
            # or raise an error instructing the user.
            print("ERROR: Node.js and npm are required to build the Web UI.", file=sys.stderr)
            sys.exit(1)

        print("--- Building Web UI Assets ---")
        try:
            # 2. Install dependencies and build
            subprocess.run([npm_path, "install"], cwd=web_dir, check=True)
            subprocess.run([npm_path, "run", "build"], cwd=web_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Web UI build failed: {e}", file=sys.stderr)
            sys.exit(1)
        print("--- Web UI Built Successfully ---")
