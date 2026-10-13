#!/usr/bin/env bash
# Одна команда для Hermes: ставит сайт aiventurebuilder.xyz и автообновление раз в минуту.
# Hermes и другие сервисы не трогает. Caddy только reload после validate, при ошибке — откат.
set -euo pipefail
RAW=https://raw.githubusercontent.com/Vladimirmakarov82/pulse/site-aiventurebuilder
command -v git >/dev/null || (apt-get update -qq && apt-get install -y -qq git)
curl -fsSL "$RAW/deploy.sh" -o /usr/local/bin/aiventurebuilder-deploy && chmod +x /usr/local/bin/aiventurebuilder-deploy
/usr/local/bin/aiventurebuilder-deploy
echo '* * * * * root /usr/local/bin/aiventurebuilder-deploy >/dev/null 2>&1' > /etc/cron.d/aiventurebuilder
chmod 644 /etc/cron.d/aiventurebuilder
CF=$(systemctl show caddy -p ExecStart --value 2>/dev/null | grep -o -- '--config [^ ;]*' | awk '{print $2}' || true); CF=${CF:-/etc/caddy/Caddyfile}
BK="$CF.bak.$(date +%s)"; cp "$CF" "$BK"
curl -fsSL "$RAW/aiventurebuilder.caddy" -o /etc/caddy/aiventurebuilder.caddy
grep -qF 'import /etc/caddy/aiventurebuilder.caddy' "$CF" || printf '\nimport /etc/caddy/aiventurebuilder.caddy\n' >> "$CF"
if caddy validate --config "$CF" --adapter caddyfile >/tmp/avb-caddy.log 2>&1; then
  systemctl reload caddy || caddy reload --config "$CF" --adapter caddyfile
  echo "ГОТОВО: сайт стоит, Caddy перезагружен, автообновление раз в минуту."
else
  cp "$BK" "$CF"; cat /tmp/avb-caddy.log; echo "ОШИБКА: Caddy не принял конфиг, Caddyfile восстановлен."; exit 1
fi
echo "DNS сейчас: $(getent hosts aiventurebuilder.xyz | awk '{print $1}') (нужно 62.238.35.82)"
