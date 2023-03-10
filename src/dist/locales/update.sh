#################################################
# Update translation files                      #
# This script is part of the $SOFTWARE_NAME project #
# Author: Hermann Hahn                          #
# License: GPL-3.0                              #
# Version: 1.0                                  #
# Date: 2021-03-21                              #
#################################################

# Project information
SOFTWARE_NAME="stop-smoke"
LAGUAGE_LIST="en de es fr it pt_BR ru"

# Initialize variables
VERSION=$1
VERSION_FILE=../../VERSION.md
OLD_VERSION=$(cat $VERSION_FILE)

# Print version number
echo New version: $VERSION
echo Old version: $OLD_VERSION

# Author information
# Get author name from git config
AUTHOR=$(git config user.name)
# Get author email from git config
AUTHOR_EMAIL=$(git config user.email)

### HELP ###
if [ "$VERSION" = "--help" ] || [ "$VERSION" = "/?" ]; then
    echo "Update translation files help:"
    echo ""
    echo "Usage: ./update.sh VERSION"
    echo ""
    echo "VERSION is the version number of the software."
    exit 0
fi

### CONDITIONS ###
# Check if version number is given
if [ "$VERSION" = "" ]; then
    echo ""
    echo "[ERROR] Missing argument VERSION"
    echo ""
    echo "Usage: ./update.sh VERSION"
    echo ""
    echo "VERSION is the version number of the software."
    exit 0
fi
# Check if version number is valid, e.g. 1.0.0
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo ""
    echo "[ERROR] Invalid version number"
    echo ""
    echo "Ex: ./update.sh 1.0.0"
    echo ""
    echo "VERSION is the version number of the software."
    exit 0
fi

# Start translation update
echo "Starting Translation Update"

# Locate old version number in all files in ../gui folder and replace it with the new version number
sed -i "s/$OLD_VERSION/$VERSION/g" ../gui/*.py

# Create and update the .pot file
xgettext --language=Python --from-code=UTF-8 --keyword=_ --package-name="$SOFTWARE_NAME" --msgid-bugs-address="$AUTHOR_EMAIL" --output=$SOFTWARE_NAME.pot ../gui/*.py
sleep 2

# Update the .pot file with Project-Id-Version to version number
sed -i "s/Project-Id-Version: stop-smoke/Project-Id-Version: $VERSION/" $SOFTWARE_NAME.pot
# Update the .po file with Last-Translator to "Hermann Hahn <hermann.h.hahn@gmail.com>"
sed -i "s/Last-Translator: FULL NAME <EMAIL@ADDRESS>/Last-Translator: $AUTHOR <$AUTHOR_EMAIL>/" $SOFTWARE_NAME.pot
# Update the .pot file with PO-Revision-Date to current date and add \n at the end
sed -i "s/PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE/PO-Revision-Date: $(date +"%Y-%m-%d %H:%M%z")/" $SOFTWARE_NAME.pot
# Update the .pot file with Language-Team to "NO-TEAM <hermann.h.hahn@gmail.com>"
sed -i "s/Language-Team: LANGUAGE <LL@li.org>/Language-Team: NO-TEAM <$AUTHOR_EMAIL>/" $SOFTWARE_NAME.pot
# Update the .pot file with Language to "en"
sed -i "s/Language: */Language: en/" $SOFTWARE_NAME.pot
# Update the .pot file with MIME-Version to "1.0"
sed -i "s/MIME-Version: 1.0/MIME-Version: 1.0/" $SOFTWARE_NAME.pot
# Update the .pot file with Content-Type to "text/plain; charset=UTF-8" and add \n at the end
sed -i "s/Content-Type: text\/plain; charset=CHARSET/Content-Type: text\/plain; charset=UTF-8/" $SOFTWARE_NAME.pot
# Update the .pot file with Content-Transfer-Encoding to "8bit" and add \n at the end
sed -i "s/Content-Transfer-Encoding: 8bit/Content-Transfer-Encoding: 8bit/" $SOFTWARE_NAME.pot
sleep 1

# Create directory for each language in the list if it does not exist
for LANGUAGES_TO_TRANSLATE in $LAGUAGE_LIST; do
    if [ ! -d $LANGUAGES_TO_TRANSLATE ]; then
        mkdir $LANGUAGES_TO_TRANSLATE
    fi
    if [ ! -d $LANGUAGES_TO_TRANSLATE/LC_MESSAGES ]; then
        mkdir $LANGUAGES_TO_TRANSLATE/LC_MESSAGES
    fi
done
sleep 1

# Save the name of all directories in the locales directory in a variable
LOCALES=$(ls -d */)

# For each directory in the locales directory
for LOCALE in $LOCALES; do

    # Remove the last character from the variable
    LOCALE=${LOCALE%?}

    # Check if file "LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po" exists
    if [ -f $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po ]; then

        # Update the .po file with the .pot file
        msgmerge -q --update --no-fuzzy-matching --lang=$LOCALE $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po $SOFTWARE_NAME.pot
        sleep 2

        # Update Project-Id-Version in the .po file
        sed -i "s/\(Project-Id-Version: *\)[0-9.]\+/\1$VERSION/" $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po
        sleep 1
        sed -i "s/$OLD_VERSION/$VERSION/g" $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po
        sleep 1

        msgfmt $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po --output-file=$LOCALE/LC_MESSAGES/$SOFTWARE_NAME.mo
        sleep 1
        echo "Language $LOCALE have been updated"

    else

        # If not, create the .po file from the .pot file
        msginit --no-translator --input=$SOFTWARE_NAME.pot --output=$LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po --locale=$LOCALE
        sleep 2

        # Say to the user that the .po file has been created and needs to be translated and re-run this script
        echo "File $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po has been created."

    fi
done

# Update .pot file messages with the new version number
sed -i "s/$OLD_VERSION/$VERSION/g" $SOFTWARE_NAME.pot

# Update the VERSION.md file with package version
sed -i "s/$OLD_VERSION/$VERSION/g" $VERSION_FILE

# Remove .po~ files in all directories
echo "Removing unnecessary files..."
find . -name "*.po~" -type f -delete

echo ""
echo "Translation Update finished"
echo "If there are .po files that need to be translated."
echo "Please translate them and re-run this script."
