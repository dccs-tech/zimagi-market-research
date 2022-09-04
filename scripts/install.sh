#!/usr/bin/env bash
#
# Install module related dependencies
#
set -e

echo "Installing Chrome browser"
curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --yes --dearmor -o /usr/share/keyrings/chrome.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/chrome.gpg] " \
        "http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

apt-get update
apt-get install -y google-chrome-stable

echo "Installing Chrome Driver"
CHROME_DRIVER_VERSION="104.0.5112.79"

wget -qN https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip -P /tmp
rm -f /usr/bin/chromedriver
unzip /tmp/chromedriver_linux64.zip -d /usr/bin

chmod +x /usr/bin/chromedriver
rm -f /tmp/chromedriver_linux64.zip
