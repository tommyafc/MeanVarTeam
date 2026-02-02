#!/usr/bin/env bash

set -e

echo "=== Installazione pacchetti per Chromium + driver su Render/Ubuntu ==="

apt-get update -y

# Pacchetti essenziali + chromium + driver (usa chromium-driver su molte immagini recenti)
apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-driver \
    libnss3 \
    libglib2.0-0 \
    libfontconfig1 \
    libjpeg-turbo8 \
    libpng16-16 \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgbm1 \
    libnspr4 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    ca-certificates \
    wget \
    unzip

# Se "chromium-driver" non esiste, prova alternativa "chromium-chromedriver" (commenta sopra e decommenta sotto se fallisce)
# apt-get install -y chromium-chromedriver

apt-get clean
rm -rf /var/lib/apt/lists/*

# Symlink per coprire i percorsi più comuni
ln -sf /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver 2>/dev/null || true
ln -sf /usr/bin/chromium-browser /usr/bin/chrome 2>/dev/null || true
ln -sf /usr/bin/chromedriver /usr/local/bin/chromedriver 2>/dev/null || true

# Debug: mostra dove sono installati
echo "=== DEBUG PATHS ==="
which chromium-browser || echo "chromium-browser NON trovato"
which chromedriver || echo "chromedriver NON trovato in PATH"
ls -l /usr/bin/chromedriver /usr/lib/chromium-browser/chromedriver 2>/dev/null || echo "File chromedriver non esiste"
find /usr -name chromedriver 2>/dev/null || echo "Nessun chromedriver trovato in /usr"
