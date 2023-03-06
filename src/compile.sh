# Description: Build script for stop-smoke
# Input: __main__.py
# Output: dist/stop-smoke.exe

# Delete dist folder
rm -rf dist

# Delete build folder
rm -rf build

# Delete stop-smoke.spec file
rm stop-smoke.spec

# Install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico stop-smoke.py

# Copy src/locales to dist folder
cp -r locales dist

# Delete .pot file from dist/locales
rm dist/locales/*.pot

# Delete .po file from dist/locales/*/LC_MESSAGES
rm dist/locales/*/LC_MESSAGES/*.po

