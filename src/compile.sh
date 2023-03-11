#####################################################
# Title: Stop Smoke Updater                         #
# Author: Hermann Hahn                              #
# License: GPL-2.0                                  #
# Version: 1.5.2                                    #
# Description: Compiles the app and the updater app #
# Input: src/                                       #
# Output: dist/                                     #
# Dependencies: pyinstaller, git, sed, ISCC.exe,    #
#               jq, curl, wget, zip.                #
# Usage: ./compile.sh VERSION [optionals]           #
# Version: Version number of the software           #
# Optionals:                                        #
#   --no-translation: Don't create translation      #
#                     files.                        #
#   --no-install: Don't compile installer.          #
#####################################################

# Get version number
VERSION=$1

# Get arguments
ARGUMENTS=$@

# Set default values
TRANSLATION=true
INSTALL=true

# echo colored text
function echoo() {
    echo -e "\033[0;33m$1\033[0m" # yellow
}
function echor() {
    echo -e "\033[0;31m$1\033[0m" # red
}
function echog() {
    echo -e "\033[0;32m$1\033[0m" # green
}


# Show help
if [ "$VERSION" == "--help" ] | [ "$VERSION" == "-h" ] | [ "$VERSION" == "-?" ] | [ "$VERSION" == "?" ] | [ "$VERSION" == "/?" ] | [ "$VERSION" == "/h" ] | [ "$VERSION" == "/help" ] | [ "$VERSION" == "" ]; then
    echo "Usage: compile.sh [version] [optionals]"
    echo ""
    echo "  version: Version of the app"
    echo "  optionals:"
    echo "    --no-translation: Don't compile translation files"
    exit 0
fi

# Check if have optionals arguments
if [ "$ARGUMENTS" != "$VERSION" ]; then

    # Check if have --no-translation argument
    if [[ "$ARGUMENTS" == *"--no-translation"* ]]; then
        echoo "Skipping translation files compilation..."
        TRANSLATION=false
    fi

    # Check if have --no-install argument
    if [[ "$ARGUMENTS" == *"--no-install"* ]]; then
        echoo "Skipping installer compilation..."
        INSTALL=false
    fi

fi

# Check if have version number is valid (e.g. 1.0.0)
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echor "Error: Version number is not valid!"
    exit 1
fi

# Check if have pyinstaller
if ! [ -x "$(command -v pyinstaller)" ]; then
    echor "Error: pyinstaller is not installed!"
    exit 1
fi

# Start compilation
echoo "Starting compilation..."

# Delete old files
echoo "Deleting old files..."
rm -rf dist
rm -rf build
echog "Old files deleted successfully!"

# If don't have --no-translation argument
if [ "$TRANSLATION" = true ]; then

    # Update translation files
    echoo "Updating translation files..."
    cd locales
    ./update.sh $VERSION
    cd ..
    echog "Translation files updated successfully!"

fi

# Compile app
echoo "Compiling stopsmoke.exe..."
pyinstaller --onefile --windowed --icon=icon.ico --add-data "modules;modules" --log-level=ERROR stopsmoke.py
echog "Done!"

# Compile updater
echoo "Compiling update.exe..."
pyinstaller --onefile --windowed --icon=icon.ico --log-level=ERROR update.py
echog "Done!"

# Copy files to dist folder
echoo "Copying files to dist folder..."
cp -r locales dist
rm dist/locales/*.pot
rm dist/locales/*/LC_MESSAGES/*.po
cp icon.ico dist
cp VERSION.md dist
cp ../LICENSE dist
echog "Files copied successfully!"

# If don't have --no-install argument
if [ "$INSTALL" = true ]; then

    # Delete old files
    echoo "Deleting old install files..."
    rm -rf ../install/*
    echog "Old install files deleted successfully!"

    # Create zip file
    echoo "Creating zip file..."
    cd dist
    zip -r stopsmoke.zip *
    mv stopsmoke.zip ../../install
    cd ..
    echog "Zip file created successfully!"

    # Create installer
    echoo "Creating installer..."
    cd installer
    ./update.sh $VERSION
    cd ..
    echog "Installer updated successfully!"
fi

# Finish
echog "Compilation finished successfully!"
echoo "If there are .po files that need to be translated,"
echoo "please translate them and re-run this script"
echoo "to create/update compiled translation files."
