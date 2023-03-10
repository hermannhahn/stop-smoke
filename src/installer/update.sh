#####################################################
# Installer files                                   #
# This script is part of the Stop Smoke project     #
# Author: Hermann Hahn                              #
# License: GPL-3.0                                  #
# Version: 1.0                                      #
# Date: 2021-03-21                                  #
# Description: Compiles the installer               #
# Input: src/installer/, src/dist/                  #
# Output: install/                                  #
#####################################################

# Get version number from .po file
project_version=$(grep -oP 'Project-Id-Version:\s*\K[0-9.]+' ../locales/en/LC_MESSAGES/stop-smoke.po)
project_version=$(echo "$project_version" | tr -d '\0')
# Modify version number in .iss file
sed -i "s/\(#define MyAppVersion \)\"[^\"]*\"/\1\"$project_version\"/" stop-smoke.iss
# Compile .iss file
ISCC.exe stop-smoke.iss
