#!/data/data/com.termux/files/usr/bin/python3
"""
OMEGA-7 ROOT BRIDGE
Advanced environment preservation between Termux and Root
Deploy: python root-bridge.py --install
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path

class RootBridge:
    def __init__(self):
        self.termux_prefix = "/data/data/com.termux/files/usr"
        self.termux_home = "/data/data/com.termux/files/home"
        self.bin_dir = f"{self.termux_prefix}/bin"
        self.essential_vars = {
            'PREFIX': self.termux_prefix,
            'PATH': f"{self.termux_prefix}/bin:/system/bin:/system/xbin",
            'LD_LIBRARY_PATH': f"{self.termux_prefix}/lib",
            'TMPDIR': f"{self.termux_prefix}/tmp", 
            'SHELL': f"{self.termux_prefix}/bin/bash",
            'TERM': 'xterm-256color',
            'HOME': self.termux_home
        }
    
    def create_smart_root(self):
        """Create intelligent root bridge script"""
        smart_root = f'''#!/system/bin/sh
# SMART ROOT BRIDGE - OMEGA-7
# Preserves Termux environment in root context

export PREFIX={self.termux_prefix}
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib
export TMPDIR=$PREFIX/tmp
export SHELL=$PREFIX/bin/bash
export TERM=xterm-256color
export HOME={self.termux_home}

# Store current directory
CURRENT_DIR="$PWD"

# Smart environment detection
if [ -z "$1" ]; then
    # Interactive root shell with full Termux environment
    exec /system/bin/su -p -c "cd \\"$CURRENT_DIR\\"; export USER=root; exec $SHELL -l"
else
    # Single command execution
    exec /system/bin/su -p -c "cd \\"$CURRENT_DIR\\"; export USER=root; $@"
fi
'''
        
        script_path = f"{self.bin_dir}/root"
        with open(script_path, 'w') as f:
            f.write(smart_root)
        os.chmod(script_path, 0o755)
        print(f"[+] Smart root bridge installed: {script_path}")
    
    def create_root_pkg(self):
        """Create root-pkg for package management in root"""
        root_pkg = '''#!/system/bin/sh
# ROOT-PKG - Package management in root context

export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib
export TMPDIR=$PREFIX/tmp

# Execute pkg with root privileges
exec /system/bin/su -p -c "cd /data/data/com.termux/files/home; pkg $@"
'''
        
        script_path = f"{self.bin_dir}/root-pkg"
        with open(script_path, 'w') as f:
            f.write(root_pkg)
        os.chmod(script_path, 0o755)
        print(f"[+] root-pkg installed: {script_path}")
    
    def create_env_sync(self):
        """Create environment synchronization"""
        env_sync = '''#!/data/data/com.termux/files/usr/bin/bash
# ENVIRONMENT SYNCHRONIZATION SCRIPT

sync_root_env() {{
    # Sync important files to root environment
    cp ~/.bashrc /root/.bashrc 2>/dev/null
    cp ~/.profile /root/.profile 2>/dev/null
    mkdir -p /root/.termux
    echo "Environment synchronized"
}}

sync_termux_env() {{
    # Sync root environment back to Termux  
    cp /root/.bashrc ~/.bashrc 2>/dev/null
    cp /root/.profile ~/.profile 2>/dev/null
    echo "Termux environment updated"
}}
'''
        
        # Add to bashrc
        bashrc_path = f"{self.termux_home}/.bashrc"
        with open(bashrc_path, 'a') as f:
            f.write('\n# OMEGA-7 ROOT SYNC FUNCTIONS\n')
            f.write(env_sync)
        
        print("[+] Environment sync functions added to .bashrc")
    
    def install_aliases(self):
        """Install smart aliases"""
        aliases = '''
# SMART ROOT ALIASES - OMEGA-7
alias root='smart-root'
alias rpkg='root-pkg'
alias rpip='root -c "pip $@"'
alias rnode='root -c "node $@"' 
alias rpython='root -c "python $@"'
alias rbash='root -c "bash $@"'

# Enhanced root functions
function smart-root() {
    # Preserve current directory and environment
    local current_dir="$PWD"
    su -p -c "cd \\"$current_dir\\"; export PREFIX=/data/data/com.termux/files/usr; export PATH=\\$PREFIX/bin:\\$PATH; export LD_LIBRARY_PATH=\\$PREFIX/lib; export TERM=xterm-256color; exec bash -l"
}

function root-cmd() {
    # Execute single command in root with Termux environment
    su -p -c "export PREFIX=/data/data/com.termux/files/usr; export PATH=\\$PREFIX/bin:\\$PATH; $@"
}
'''
        
        bashrc_path = f"{self.termux_home}/.bashrc"
        with open(bashrc_path, 'a') as f:
            f.write(aliases)
        
        print("[+] Smart root aliases installed")
    
    def install_complete(self):
        """Complete installation"""
        self.create_smart_root()
        self.create_root_pkg()
        self.create_env_sync()
        self.install_aliases()
        
        print("\n[OMEGA-7] ROOT BRIDGE INSTALLATION COMPLETE")
        print("==========================================")
        print("Available commands:")
        print("  root        - Smart root shell with Termux environment")
        print("  root-pkg    - Run pkg commands as root")
        print("  rpkg        - Alias for root-pkg")
        print("  smart-root  - Enhanced root with directory preservation")
        print("  root-cmd    - Run single command in root context")
        print("\nUsage examples:")
        print("  root        # Full root shell with pkg access")
        print("  root-pkg install python # Install packages as root")
        print("  root-cmd 'whoami && pkg list-installed'")

def main():
    parser = argparse.ArgumentParser(description='OMEGA-7 Root Bridge Installer')
    parser.add_argument('--install', action='store_true', help='Install root bridge')
    parser.add_argument('--uninstall', action='store_true', help='Remove root bridge')
    
    args = parser.parse_args()
    
    bridge = RootBridge()
    
    if args.install:
        bridge.install_complete()
    elif args.uninstall:
        print("[-] Uninstall feature not yet implemented")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()