#!/usr/bin/env bash

set -e  # esci subito se un comando fallisce

echo "=== Installazione Chromium + chromedriver su Render ==="

apt-get update -y
apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-chromedriver \
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

apt-get clean
rm -rf /var/lib/apt/lists/*

# Symlink per compatibilità (molti codici cercano questi path)
ln -sf /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
ln -sf /usr/bin/chromium-browser /usr/bin/chrome

echo "Chromium: $(which chromium-browser)"
echo "Chromedriver: $(which chromedriver)"
ls -l /usr/bin/chromedriver /usr/lib/chromium-browser/chromedriver
