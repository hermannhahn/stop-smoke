#####################################################
# Title: Stop Smoke Installer Compiler              #
# Author: Hermann Hahn                              #
# License: GPL-2.0                                  #
# Version: 1.5.2                                    #
# Description: Compiles the installer               #
# Input: src/dist/                                  #
# Output: install/                                  #
# Dependencies: Inno Setup 6                        #
# Usage: ./update.sh VERSION                        #
# Version: Version number of the software           #
#####################################################

# Get version number from argument
project_version=$1

# Modify version number in .iss file
sed -i "s/\(#define MyAppVersion \)\"[^\"]*\"/\1\"$project_version\"/" stopsmoke.iss

# Compile .iss file
ISCC.exe stopsmoke.iss
