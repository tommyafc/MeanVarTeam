#!/usr/bin/env bash

set -e

echo "=== INSTALL CHROME/DRIVER - START ==="

apt-get update -y

# Prova prima la combinazione più comune su Render/Ubuntu 22/24
apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-driver \
    libnss3 libglib2.0-0 libfontconfig1 libjpeg-turbo8 libpng16-16 \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libcups2 libdbus-1-3 libgbm1 libnspr4 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 ca-certificates wget unzip libstdc++6

# Se fallisce, tenta variante (alcune immagini Render lo chiamano così)
if ! command -v chromedriver >/dev/null; then
    echo "chromedriver non trovato dopo primo tentativo → provo chromium-chromedriver"
    apt-get install -y chromium-chromedriver || echo "Install chromium-chromedriver fallito"
fi

apt-get clean
rm -rf /var/lib/apt/lists/*

# Crea symlink ovunque possibile
mkdir -p /usr/local/bin
ln -sf /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver 2>/dev/null || true
ln -sf /usr/bin/chromedriver /usr/local/bin/chromedriver 2>/dev/null || true
ln -sf /usr/bin/chromium-browser /usr/bin/chrome 2>/dev/null || true

echo "=== DEBUG RISULTATI ==="
echo "Pacchetti chrome installati:"
dpkg -l | grep -iE 'chrome|chromium' || echo "Nessun pacchetto chrome trovato!"
echo ""
echo "Posizioni chromedriver:"
find /usr -name "*chromedriver*" -type f -executable 2>/dev/null || echo "find: nessun chromedriver trovato"
echo ""
echo "which chromedriver:" $(which chromedriver || echo "NON TROVATO")
echo "which chromium-browser:" $(which chromium-browser || echo "NON TROVATO")
ls -la /usr/bin/chromedriver /usr/lib/chromium-browser/chromedriver 2>/dev/null || echo "ls: file non esistono"
echo "=== DEBUG END ==="
