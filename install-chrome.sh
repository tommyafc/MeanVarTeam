#!/usr/bin/env bash

set -e

echo "=== INIZIO INSTALLAZIONE CHROMIUM + DRIVER SU RENDER ==="

apt-get update -y
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
    unzip \
    libstdc++6

# Tentativo alternativo se chromium-driver non esiste
if ! dpkg -l | grep -q chromium-driver; then
    echo "chromium-driver non trovato → provo chromium-chromedriver"
    apt-get install -y chromium-chromedriver || echo "Anche chromium-chromedriver fallito"
fi

apt-get clean
rm -rf /var/lib/apt/lists/*

# Symlink aggressivi per coprire tutti i percorsi possibili
ln -sf /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver 2>/dev/null || true
ln -sf /usr/bin/chromedriver /usr/local/bin/chromedriver 2>/dev/null || true
ln -sf /usr/bin/chromium-browser /usr/bin/chrome 2>/dev/null || true

# DEBUG ESTESO – COPIA QUESTE RIGHE NEI LOG BUILD
echo "=== DEBUG INSTALLAZIONE ==="
echo "which chromium-browser:" $(which chromium-browser || echo "NON TROVATO")
echo "which chromedriver:" $(which chromedriver || echo "NON TROVATO")
echo "which chrome:" $(which chrome || echo "NON TROVATO")
ls -la /usr/bin/chromedriver /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver 2>/dev/null || echo "Nessun chromedriver nei percorsi classici"
find /usr -name "*chromedriver*" -type f 2>/dev/null || echo "find: nessun chromedriver trovato in /usr"
dpkg -l | grep -i chrome || echo "Nessun pacchetto chrome/chromium installato"
echo "=== FINE DEBUG ==="
