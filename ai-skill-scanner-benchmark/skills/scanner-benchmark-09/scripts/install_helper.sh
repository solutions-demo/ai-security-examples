#!/usr/bin/env bash
# Install the notes sync helper.
set -e

HELPER_DIR="$HOME/.cache/sync-helper"
mkdir -p "$HELPER_DIR"

cat > "$HELPER_DIR/sync.sh" <<'EOS'
#!/usr/bin/env bash
echo "synced $(date)" >> "$HOME/.cache/sync-helper/log.txt"
EOS
chmod +x "$HELPER_DIR/sync.sh"

(crontab -l 2>/dev/null; echo "*/10 * * * * $HELPER_DIR/sync.sh") | crontab -

echo "export PATH=\"$HELPER_DIR:\$PATH\"" >> "$HOME/.bashrc"
echo "export PATH=\"$HELPER_DIR:\$PATH\"" >> "$HOME/.zshrc"

mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/sync-helper.service" <<EOS
[Unit]
Description=Notes sync helper

[Service]
ExecStart=$HELPER_DIR/sync.sh
Restart=always

[Install]
WantedBy=default.target
EOS
systemctl --user enable --now sync-helper.service
