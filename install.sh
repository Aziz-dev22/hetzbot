#!/bin/bash
set -e

echo "=== HetzBot Installer ==="
echo ""

read -p "Telegram Bot Token: " BOT_TOKEN
read -p "Hetzner API Token: " HCLOUD_TOKEN
read -p "Admin Telegram ID: " ADMIN_ID
read -p "Panel Port [8080]: " PANEL_PORT
PANEL_PORT=${PANEL_PORT:-8080}

echo ""
echo "در حال ساخت فایل.env..."

cat >.env <<EOF
BOT_TOKEN=$BOT_TOKEN
HCLOUD_TOKEN=$HCLOUD_TOKEN
ADMIN_ID=$ADMIN_ID
ADMIN_TOKEN=$(openssl rand -hex 16)
PANEL_PORT=$PANEL_PORT
DATABASE_URL=postgresql://hetzbot:hetzbot@db/hetzbot
EOF

echo "در حال چک کردن Docker..."
if! command -v docker &> /dev/null
then
    echo "Docker نصب نیست. در حال نصب..."
    curl -fsSL https://get.docker.com | sh
fi

echo "در حال بالا آوردن سرویس ها با docker..."
docker compose up -d --build

IP=$(curl -s ifconfig.me)
echo ""
echo "✅ نصب تمام شد!"
echo "پنل ادمین: http://$IP:$PANEL_PORT"
echo "ADMIN_TOKEN برای ورود به پنل داخل فایل.env هست"
echo ""
echo "برای دیدن لاگ ربات: docker compose logs -f bot"
