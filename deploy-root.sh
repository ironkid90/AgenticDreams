#!/data/data/com.termux/files/usr/bin/bash
# DARKFORGE-X MINIMAL ROOT DEPLOYMENT

echo "🔧 Deploying minimal root access..."

# Create essential wrappers
cat > $PREFIX/bin/rap << 'EOF'
#!/system/bin/sh
export PREFIX=/data/data/com.termux/files/usr
export PATH=$PREFIX/bin:$PATH
exec su -p -c "cd /data/data/com.termux/files/home; pkg \"$@\""
EOF

cat > $PREFIX/bin/rpkg << 'EOF'
#!/system/bin/sh
export PREFIX=/data/data/com.termux/files/usr  
export PATH=$PREFIX/bin:$PATH
exec su -p -c "cd /data/data/com.termux/files/home; pkg \"$@\""
EOF

# Make executable
chmod +x $PREFIX/bin/rap $PREFIX/bin/rpkg

# Add essential aliases
echo '
# MINIMAL ROOT ACCESS
alias rinstall="rap install -y"
alias rupdate="rap update && rap upgrade -y" 
alias rpip='"'"'su -p -c "export PREFIX=/data/data/com.termux/files/usr; pip $@"'"'"'
alias rnode='"'"'su -p -c "export PREFIX=/data/data/com.termux/files/usr; node $@"'"'"'

# Quick root environment
qroot() {
    su -p -c "export PREFIX=/data/data/com.termux/files/usr; export PATH=\$PREFIX/bin:\$PATH; cd $PWD; exec bash"
}
' >> ~/.bashrc

echo "✅ Minimal root deployment complete!"
echo "Usage: rap, rpkg, rinstall, rupdate, qroot"