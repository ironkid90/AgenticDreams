#!/data/data/com.termux/files/usr/bin/python3
"""
DARKFORGE-X PRECISION ROOT ENVIRONMENT
Surgical bypass of Termux root safety checks
"""

import os
import sys
import subprocess
from pathlib import Path

class PrecisionRootEnv:
    def __init__(self):
        self.termux_prefix = Path("/data/data/com.termux/files/usr")
        self.bin_dir = self.termux_prefix / "bin"
        
    def analyze_safety_mechanism(self):
        """Precisely identify the root detection method"""
        print("[ANALYSIS] Scanning Termux safety mechanisms...")
        
        # Test different execution contexts
        test_commands = {
            'direct_su': ['su', '-c', 'pkg --version'],
            'preserved_env': ['su', '-p', '-c', 'pkg --version'],
            'env_simulation': ['su', '-p', '-c', 'env; pkg --version']
        }
        
        for test_name, cmd in test_commands.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if "disabled permanently for safety" in result.stderr:
                    print(f"🔒 {test_name}: Safety lock active")
                else:
                    print(f"✅ {test_name}: Possible bypass")
                    print(f"   Output: {result.stdout[:100]}")
            except Exception as e:
                print(f"⚠️  {test_name}: Error - {e}")

    def create_surgical_wrappers(self):
        """Create precision wrappers that bypass root detection"""
        print("\n[DEPLOYMENT] Deploying surgical wrappers...")
        
        wrappers = {
            'rap': f'''#!/system/bin/sh
# PRECISION APT WRAPPER - DARKFORGE-X
export PREFIX={self.termux_prefix}
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib
export TERMUX_SAFE_EXEC=0

# Execute with environment preservation
exec su -p -c "cd $PWD; $PREFIX/bin/apt \"$@\""
''',
            
            'rpkg': f'''#!/system/bin/sh  
# PRECISION PKG WRAPPER - DARKFORGE-X
export PREFIX={self.termux_prefix}
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib

# Bypass via environment variable manipulation
export TERMUX_PKG_NO_SU_CHECK=1
exec su -p -c "cd /data/data/com.termux/files/home; $PREFIX/bin/pkg \"$@\""
''',
            
            'rdpkg': f'''#!/system/bin/sh
# PRECISION DPKG WRAPPER - DARKFORGE-X
export PREFIX={self.termux_prefix}
export PATH=$PREFIX/bin:$PATH

# Direct execution with full environment
exec su -p -c "export LD_LIBRARY_PATH=$PREFIX/lib; $PREFIX/bin/dpkg \"$@\""
'''
        }
        
        for wrapper_name, content in wrappers.items():
            wrapper_path = self.bin_dir / wrapper_name
            with open(wrapper_path, 'w') as f:
                f.write(content)
            wrapper_path.chmod(0o755)
            print(f"  → Deployed: {wrapper_name}")

    def install_smart_integration(self):
        """Install intelligent shell integration"""
        integration = '''
# DARKFORGE-X ROOT INTEGRATION
alias rap='rpkg'  # Unified package management
alias rpip='su -p -c "export PREFIX=/data/data/com.termux/files/usr; pip $@"'
alias rnode='su -p -c "export PREFIX=/data/data/com.termux/files/usr; node $@"'

# Smart package operations
rinstall() {
    for pkg in "$@"; do
        echo "📦 Installing $pkg as root..."
        rpkg install -y "$pkg"
    done
}

rupdate() {
    echo "🔄 Updating package database..."
    rpkg update && rpkg upgrade -y
}

rsearch() {
    rpkg search "$@"
}

# Environment preservation function
rootenv() {
    su -p -c "export PREFIX=/data/data/com.termux/files/usr; 
              export PATH=\\$PREFIX/bin:\\$PATH;
              export LD_LIBRARY_PATH=\\$PREFIX/lib;
              export TERM=xterm-256color;
              cd $PWD; exec bash -l"
}
'''
        
        bashrc_path = Path.home() / ".bashrc"
        with open(bashrc_path, 'a') as f:
            f.write(integration)
        print("  → Shell integration installed")

    def deploy(self):
        """Execute precision deployment"""
        print("🛠️  DARKFORGE-X PRECISION ROOT UNLOCK")
        print("=====================================")
        
        self.analyze_safety_mechanism()
        self.create_surgical_wrappers()
        self.install_smart_integration()
        
        print("\n🎯 DEPLOYMENT COMPLETE")
        print("=====================")
        print("New Commands:")
        print("  rap [args]    - Root apt operations")
        print("  rpkg [args]   - Root pkg operations") 
        print("  rdpkg [args]  - Root dpkg operations")
        print("  rinstall pkg  - Smart root installation")
        print("  rupdate       - Full system update")
        print("  rootenv       - Full root shell with Termux environment")

if __name__ == "__main__":
    env = PrecisionRootEnv()
    env.deploy()