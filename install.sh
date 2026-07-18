#!/bin/bash
set -e

echo "=== HetzBot Installer ==="
echo ""

read -p "Telegram Bot Token: " BOT_TOKEN
read -p "Admin Telegram ID: " ADMIN_ID
read -p "Panel Username: " PANEL_USER
read -s -p "Panel Password: " PANEL_PASS && echo
read -p "Panel Port [8080]: " PANEL_PORT
PANEL_PORT=${PANEL_PORT:-8080}

echo ""
echo "در حال ساخت فایل.env..."

cat >.env <<EOF
BOT_TOKEN=$BOT_TOKEN
ADMIN_ID=$ADMIN_ID
PANEL_USER=$PANEL_USER
PANEL_PASS=$PANEL_PASS
PANEL_PORT=$PANEL_PORT
DATABASE_URL=postgresql://hetzbot:hetzbot@db/hetzbot
EOF

echo "در حال بالا آوردن سرویس ها با docker..."
docker compose up -d --build

IP=$(curl -s ifconfig.me)
echo ""
echo "✅ نصب تمام شد!"
echo "پنل ادمین: http://$IP:$PANEL_PORT"
echo "یوزر: $PANEL_USER | پسورد: $PANEL_PASS"
echo ""
echo "برای دیدن لاگ ربات: docker compose logs -f bot"
