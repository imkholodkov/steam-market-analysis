#!/usr/bin/env bash
# Проверка опубликованной страницы: код ответа 200 и контрольная строка в HTML.
set -euo pipefail
url="$1"
marker="Конвейер «данные → результат → сайт»"
for attempt in 1 2 3 4 5; do
  code=$(curl -s -o page.html -w '%{http_code}' "$url" || true)
  if [[ "$code" == "200" ]] && grep -q "$marker" page.html; then
    echo "OK: $url -> $code, контрольная строка найдена"
    exit 0
  fi
  echo "Попытка $attempt: $url -> $code, ждём 20 с"
  sleep 20
done
echo "FAIL: $url не прошёл проверку" >&2
exit 1
