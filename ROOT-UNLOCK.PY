#!/data/data/com.termux/files/usr/bin/python3
"""
OMEGA-7 ROOT UNLOCK PROTOCOL
Bypasses Termux root safety checks
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class RootUnlock:
    def __init__(self):
        self.termux_bin = Path("/data/data/com.termux/files/usr/bin")
        self.backup_dir = Path("/data/data/com.termux/files/usr/backup")
        
    def detect_safety_lock(self):
        """Identify the root safety mechanism"""
        print("[ANALYSIS] Scanning for root safety locks...")
        
        targets = ['apt', 'apt-get', 'pkg', 'dpkg']
        locked_commands = []
        
        for cmd in targets:
            cmd_path = self.termux_bin / cmd
            if cmd_path.exists():
                try:
                    result = subprocess.run(
                        ['su', '-c', f'{cmd_path} --version'],
                        capture_output=True, text=True
                    )
                    if "disabled permanently for safety" in result.stderr:
                        locked_commands.append(cmd)
                        print(f"🔒 LOCKED: {cmd}")
                    else:
                        print(f"✅ UNLOCKED: {cmd}")
                except:
                    print(f"⚠️  UNKNOWN: {cmd}")
        
        return locked_commands
    
    def create_shadow_wrappers(self):
        """Create bypass wrappers for locked commands"""
        print("\n[DEPLOYMENT] Creating shadow wrappers...")
        
        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)
        
        wrappers = {
            'root-apt': '''#!/system/bin/sh
# SHADOW APT WRAPPER - OMEGA-7
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib

# Bypass root detection using environment manipulation
export TERMUX_SAFE_EXEC=0
export TERMUX_SU=1

# Execute original apt with safety disabled
exec $PREFIX/bin/apt.orig "$@"
''',
            'root-pkg': '''#!/system/bin/sh  
# SHADOW PKG WRAPPER - OMEGA-7
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PATH

# Bypass pkg root checks
export TERMUX_PKG_NO_ROOT_CHECK=1
export TERMUX_SU=1

# Use su with preserved environment
exec su -p -c "cd /data/data/com.termux/files/home; $PREFIX/bin/pkg.orig \"$@\""
''',
            'root-dpkg': '''#!/system/bin/sh
# SHADOW DPKG WRAPPER - OMEGA-7  
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PATH

# Direct dpkg execution bypass
exec su -p -c "export LD_LIBRARY_PATH=$PREFIX/lib; $PREFIX/bin/dpkg.orig \"$@\""
'''
        }
        
        for wrapper_name, wrapper_content in wrappers.items():
            wrapper_path = self.termux_bin / wrapper_name
            with open(wrapper_path, 'w') as f:
                f.write(wrapper_content)
            wrapper_path.chmod(0o755)
            print(f"[+] Deployed: {wrapper_name}")
    
    def backup_and_patch(self):
        """Backup original binaries and create patched versions"""
        print("\n[PATCHING] Creating safety-bypass patches...")
        
        targets = ['apt', 'pkg', 'dpkg']
        
        for target in targets:
            original_path = self.termux_bin / target
            backup_path = self.backup_dir / f"{target}.orig"
            
            if original_path.exists():
                # Backup original
                shutil.copy2(original_path, backup_path)
                print(f"[+] Backed up: {target} -> {backup_path}")
                
                # Create symlink from wrapper to original name with .orig
                patched_path = self.termux_bin / f"{target}.orig"
                if not patched_path.exists():
                    original_path.rename(patched_path)
                    
                # Create root- version that points to wrapper
                wrapper_link = self.termux_bin / f"root-{target}"
                if not wrapper_link.exists():
                    original_path.symlink_to(wrapper_link)
    
    def install_smart_aliases(self):
        """Install intelligent aliases for root package management"""
        aliases = '''
# OMEGA-7 ROOT PACKAGE MANAGEMENT ALIASES
alias rapt='root-apt'
alias rpkg='root-pkg' 
alias rdpkg='root-dpkg'
alias rpip='root -c "pip $@"'
alias rnpm='root -c "npm $@"'

# Smart package installation with root context
function rinstall() {
    for package in "$@"; do
        echo "[INSTALL] $package as root..."
        root-pkg install -y "$package"
    done
}

function rupdate() {
    root-pkg update && root-pkg upgrade -y
}
'''
        
        bashrc_path = Path("/data/data/com.termux/files/home/.bashrc")
        with open(bashrc_path, 'a') as f:
            f.write(aliases)
        
        print("[+] Smart aliases installed")
    
    def deploy_complete(self):
        """Execute complete deployment"""
        print("🚀 OMEGA-7 ROOT UNLOCK PROTOCOL")
        print("======================================")
        
        locked = self.detect_safety_lock()
        if not locked:
            print("✅ No root locks detected")
            return
        
        print(f"🔓 Bypassing {len(locked)} safety locks...")
        
        self.create_shadow_wrappers()
        self.backup_and_patch() 
        self.install_smart_aliases()
        
        print("\n🎯 DEPLOYMENT COMPLETE")
        print("=======================")
        print("New commands available:")
        print("  root-apt    - Bypassed apt for root")
        print("  root-pkg    - Bypassed pkg for root") 
        print("  root-dpkg   - Bypassed dpkg for root")
        print("  rapt        - Alias for root-apt")
        print("  rpkg        - Alias for root-pkg")
        print("  rinstall    - Smart root package installer")
        print("  rupdate     - Root package updater")

def main():
    unlock = RootUnlock()
    unlock.deploy_complete()

if __name__ == "__main__":
    main()