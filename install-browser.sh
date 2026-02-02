#!/usr/bin/env bash

# ── Installa Chromium + driver + dipendenze minime ────────────────
# Testato su Render nel 2025–2026

set -e  # esci se un comando fallisce

apt-get update -y
apt-get install -y --no-install-recommends \
    chromium \
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
    wget

# Pulizia per non gonfiare l'immagine
apt-get clean
rm -rf /var/lib/apt/lists/*

echo "Chromium e chromedriver installati"
echo "Chromium path: $(which chromium)"
echo "Chromedriver path: $(which chromedriver)"
