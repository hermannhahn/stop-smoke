#####################################################
# Update translation files                          #
# This script is part of the Stop Smoke project     #
# Author: Hermann Hahn                              #
# License: GPL-3.0                                  #
# Version: 1.0                                      #
# Date: 2021-03-21                                  #
#####################################################

# Description: Build script for stop-smoke
# Input: stop-smoke.py
# Output: dist/

# echo orange text
function echoo() {
    echo -e "\033[0;33m$1\033[0m"
}

# echo red text
function echor() {
    echo -e "\033[0;31m$1\033[0m"
}

# echo green text
function echog() {
    echo -e "\033[0;32m$1\033[0m"
}

VERSION=$1
TRANSLATIONS=$2

# Show help
if [ "$VERSION" == "--help" ] | [ "$VERSION" == "-h" ] | [ "$VERSION" == "-?" ] | [ "$VERSION" == "?" ] | [ "$VERSION" == "/?" ] | [ "$VERSION" == "/h" ] | [ "$VERSION" == "/help" ] | [ "$VERSION" == "" ]; then
    echo "Usage: compile.sh [version] [optionals]"
    echo ""
    echo "  version: Version of the app"
    echo "  optionals:"
    echo "    --no-translation: Don't compile translation files"
    exit 0
fi

echog "Starting compilation..."

if [ "$TRANSLATIONS" != "--no-translation" ]; then
    cd locales
    ./update.sh $VERSION
    cd ..
    echog "Translations files compiled successfully!"
fi

echoo "Deleting old files..."
rm -rf dist
rm -rf build
rm stop-smoke.spec
rm update.spec
echog "Old files deleted successfully!"

echoo "Compiling stop-smoke.exe..."
pyinstaller --onefile --windowed --icon=icon.ico --add-data "modules;modules" --log-level=ERROR stop-smoke.py
echog "Done!"
echoo "Compiling update.exe..."
pyinstaller --onefile --windowed --icon=icon.ico --log-level=ERROR update.py
echog "Done!"

echoo "Copying files to dist folder..."
cp -r locales dist
rm dist/locales/*.pot
rm dist/locales/*/LC_MESSAGES/*.po
cp icon.ico dist
cp VERSION.md dist
cp ../LICENSE dist
echog "Files copied successfully!"

echog "Compilation finished successfully!"
echoo "If there are .po files that need to be translated,"
echoo "please translate them and re-run this script."
