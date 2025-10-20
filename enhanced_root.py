#!/data/data/com.termux/files/usr/bin/python3
# enhanced_root.py - Advanced Root Environment Manager

import os
import sys
import subprocess
import json

class TermuxRootEnhancer:
    def __init__(self):
        self.termux_prefix = "/data/data/com.termux/files/usr"
        self.essential_vars = {
            'PREFIX': self.termux_prefix,
            'PATH': f"{self.termux_prefix}/bin:{os.environ.get('PATH', '')}",
            'LD_LIBRARY_PATH': f"{self.termux_prefix}/lib",
            'TMPDIR': f"{self.termux_prefix}/tmp",
            'SHELL': f"{self.termux_prefix}/bin/bash",
            'TERM': 'xterm-256color',
            'HOME': '/data/data/com.termux/files/home'
        }
    
    def create_root_launcher(self):
        """Create advanced root launcher script"""
        launcher_script = f'''#!/system/bin/sh
# Advanced Root Launcher - OMEGA-7 PROTOCOL

export PREFIX={self.termux_prefix}
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib
export TMPDIR=$PREFIX/tmp
export SHELL=$PREFIX/bin/bash
export TERM=xterm-256color
export HOME=/data/data/com.termux/files/home

# Preserve current directory
CURRENT_DIR="$PWD"

# Enhanced root execution with full environment preservation
exec /system/bin/su -p -c "cd \\"$CURRENT_DIR\\"; export USER=root; exec $SHELL -l"
'''
        
        with open('/data/data/com.termux/files/usr/bin/root', 'w') as f:
            f.write(launcher_script)
        os.chmod('/data/data/com.termux/files/usr/bin/root', 0o755)
    
    def install_enhanced_busybox(self):
        """Install enhanced BusyBox with root optimizations"""
        busybox_installer = '''#!/data/data/com.termux/files/usr/bin/bash
# Enhanced BusyBox Installer for Root

BB_URL="https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox"
BB_DIR="/data/data/com.termux/files/usr/bin/busybox-root"

echo "[+] Installing Enhanced BusyBox for Root..."
curl -L -o "$BB_DIR/busybox" "$BB_URL"
chmod 755 "$BB_DIR/busybox"

# Install all applets
cd "$BB_DIR"
./busybox --install -s "$BB_DIR"

echo "[+] Enhanced BusyBox installed to: $BB_DIR"
'''
        
        subprocess.run(['mkdir', '-p', '/data/data/com.termux/files/usr/bin/busybox-root'])
        with open('/data/data/com.termux/files/usr/tmp/install_bb.sh', 'w') as f:
            f.write(busybox_installer)
        subprocess.run(['bash', '/data/data/com.termux/files/usr/tmp/install_bb.sh'])

if __name__ == "__main__":
    enhancer = TermuxRootEnhancer()
    enhancer.create_root_launcher()
    enhancer.install_enhanced_busybox()