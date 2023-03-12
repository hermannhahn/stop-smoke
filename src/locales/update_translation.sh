#####################################################
# Title: Translation Updater                        #
# Author: Hermann Hahn                              #
# License: GPL-2.0                                  #
# Version: 1.5.2                                    #
# Description: Updates the translation files        #
# Input: src/locales/                               #
# Output: src/locales/                              #
# Dependencies: git, msgmerge, xgettext, sed,       #
#               msginit, msgfmt.                    #
# Usage: ./update.sh VERSION                        #
# Version: Version number of the software           #
#####################################################

# Project information
SOFTWARE_NAME="stopsmoke"
UPDATER_NAME="update"
LAGUAGE_LIST="en de es fr it pt_BR ru"

# Get version number from argument
VERSION=$1

# Initialize variables
VERSION_FILE=../VERSION.md
OLD_VERSION=$(cat $VERSION_FILE)

# Colored echo functions
function echoo() {
    echo -e "\033[0;33m$1\033[0m" # yellow
}


function echor() {
    echo -e "\033[0;31m$1\033[0m" # red
}


function echog() {
    echo -e "\033[0;32m$1\033[0m" # green
}

# Get author name from git config
AUTHOR=$(git config user.name)

# Get author email from git config
AUTHOR_EMAIL=$(git config user.email)

# Check if git config is set
if [ "$AUTHOR" = "" ] || [ "$AUTHOR_EMAIL" = "" ]; then
    echo ""
    echor "[ERROR] Git config is not set"
    echo ""
    echog "Ex: git config --global user.name \"John Doe\""
    echog "Ex: git config --global user.email \"john@example.com\""
    echo ""
    exit 0
fi

# Show help
if [ "$VERSION" = "--help" ] || [ "$VERSION" = "/?" ]; then
    echo "Update translation files help:"
    echo ""
    echog "Usage: ./update.sh VERSION"
    echo ""
    echo "VERSION is the version number of the software."
    echo ""
    exit 0
fi

# Check if version number is given
if [ "$VERSION" = "" ]; then
    echo ""
    echor "[ERROR] Missing argument VERSION"
    echo ""
    echog "Usage: ./update.sh VERSION"
    echo ""
    echo "VERSION is the version number of the software."
    echo ""
    exit 0
fi

# Check if version number is valid, e.g. 1.0.0
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo ""
    echor "[ERROR] Invalid version number"
    echo ""
    echog "Ex: ./update.sh 1.0.0"
    echo ""
    echo "VERSION is the version number of the software."
    echo ""
    exit 0
fi

# Print version number
echo New version: $VERSION
echo Old version: $OLD_VERSION

# Start translation compilation
echog "Starting translation compilation..."

# Update the version number in gui files
sed -i "s/VERSION = \"$OLD_VERSION\"/VERSION = \"$VERSION\"/" ../gui/*.py

# Create or update the stopsmoke.pot file relative to the app gui folder
xgettext --language=Python --from-code=UTF-8 --keyword=_ --package-name="$SOFTWARE_NAME" --msgid-bugs-address="$AUTHOR_EMAIL" --output=$SOFTWARE_NAME.pot ../gui/*.py
sleep 2

# Create or update the update.pot file relative to the updater app file
xgettext --language=Python --from-code=UTF-8 --keyword=_ --package-name="$UPDATER_NAME" --msgid-bugs-address="$AUTHOR_EMAIL" --output=$UPDATER_NAME.pot ../update.py
sleep 2

# Update the .pot files with Project-Id-Version to version number
sed -i "s/Project-Id-Version: stopsmoke/Project-Id-Version: $VERSION/" $SOFTWARE_NAME.pot
sed -i "s/Project-Id-Version: update/Project-Id-Version: $VERSION/" $UPDATER_NAME.pot

# Update the .po files with Last-Translator to "Hermann Hahn <hermann.h.hahn@gmail.com>"
sed -i "s/Last-Translator: FULL NAME <EMAIL@ADDRESS>/Last-Translator: $AUTHOR <$AUTHOR_EMAIL>/" $SOFTWARE_NAME.pot
sed -i "s/Last-Translator: FULL NAME <EMAIL@ADDRESS>/Last-Translator: $AUTHOR <$AUTHOR_EMAIL>/" $UPDATER_NAME.pot

# Update the .pot files with PO-Revision-Date to current date and add \n at the end
sed -i "s/PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE/PO-Revision-Date: $(date +"%Y-%m-%d %H:%M%z")/" $SOFTWARE_NAME.pot
sed -i "s/PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE/PO-Revision-Date: $(date +"%Y-%m-%d %H:%M%z")/" $UPDATER_NAME.pot

# Update the .pot files with Language-Team to "NO-TEAM <AUTHOR_EMAIL>"
sed -i "s/Language-Team: LANGUAGE <LL@li.org>/Language-Team: NO-TEAM <$AUTHOR_EMAIL>/" $SOFTWARE_NAME.pot
sed -i "s/Language-Team: LANGUAGE <LL@li.org>/Language-Team: NO-TEAM <$AUTHOR_EMAIL>/" $UPDATER_NAME.pot

# Update the .pot files with Language to "en"
sed -i "s/Language: */Language: en/" $SOFTWARE_NAME.pot
sed -i "s/Language: */Language: en/" $UPDATER_NAME.pot

# Update the .pot files with MIME-Version to "1.0"
sed -i "s/MIME-Version: 1.0/MIME-Version: 1.0/" $SOFTWARE_NAME.pot
sed -i "s/MIME-Version: 1.0/MIME-Version: 1.0/" $UPDATER_NAME.pot

# Update the .pot files with Content-Type to "text/plain; charset=UTF-8" and add \n at the end
sed -i "s/Content-Type: text\/plain; charset=CHARSET/Content-Type: text\/plain; charset=UTF-8/" $SOFTWARE_NAME.pot
sed -i "s/Content-Type: text\/plain; charset=CHARSET/Content-Type: text\/plain; charset=UTF-8/" $UPDATER_NAME.pot

# Update the .pot files with Content-Transfer-Encoding to "8bit" and add \n at the end
sed -i "s/Content-Transfer-Encoding: 8bit/Content-Transfer-Encoding: 8bit/" $SOFTWARE_NAME.pot
sed -i "s/Content-Transfer-Encoding: 8bit/Content-Transfer-Encoding: 8bit/" $UPDATER_NAME.pot


# Create directory for each language in the list if it does not exist
for LANGUAGES_TO_TRANSLATE in $LAGUAGE_LIST; do

    # Check if directory exists
    if [ ! -d $LANGUAGES_TO_TRANSLATE ]; then

        # Create directory
        mkdir $LANGUAGES_TO_TRANSLATE

    fi

    # Check if directory exists
    if [ ! -d $LANGUAGES_TO_TRANSLATE/LC_MESSAGES ]; then

        # Create directory
        mkdir $LANGUAGES_TO_TRANSLATE/LC_MESSAGES

    fi

    sleep 1

done

# Save the name of all directories in the locales directory in a variable
LOCALES=$(ls -d */)

# For each directory in the locales directory
for LOCALE in $LOCALES; do

    # Remove the last character from the variable
    LOCALE=${LOCALE%?}
    LOCALE_GREEN=$(echog $LOCALE)

    # Check if file "LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po" exists
    if [ -f $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po ]; then
    
        # Update the .po file with the .pot file
        msgmerge -q --update --no-fuzzy-matching --lang=$LOCALE $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po $SOFTWARE_NAME.pot
        sleep 1

        # Update Project-Id-Version in the .po file
        sed -i "s/\(Project-Id-Version: *\)[0-9.]\+/\1$VERSION/" $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po
        sleep 1

        # Update Version in the .po file
        sed -i "s/$OLD_VERSION/$VERSION/g" $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po
        sleep 1

        # Compile the .po file to .mo file
        msgfmt $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po --output-file=$LOCALE/LC_MESSAGES/$SOFTWARE_NAME.mo
        sleep 1

    else

        # If not, create the .po file from the .pot file
        msginit --no-translator --input=$SOFTWARE_NAME.pot --output=$LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po --locale=$LOCALE
        sleep 1
        
    fi

    # Check if file "LOCALE/LC_MESSAGES/$UPDATER_NAME.po" exists
    if [ -f $LOCALE/LC_MESSAGES/$UPDATER_NAME.po ]; then

        # Update the .po file with the .pot file
        msgmerge -q --update --no-fuzzy-matching --lang=$LOCALE $LOCALE/LC_MESSAGES/$UPDATER_NAME.po $UPDATER_NAME.pot
        sleep 1

        # Update Project-Id-Version in the .po file
        sed -i "s/\(Project-Id-Version: *\)[0-9.]\+/\1$VERSION/" $LOCALE/LC_MESSAGES/$UPDATER_NAME.po
        sleep 1

        # Update Version in the .po file
        sed -i "s/$OLD_VERSION/$VERSION/g" $LOCALE/LC_MESSAGES/$UPDATER_NAME.po
        sleep 1

        # Compile the .po file to .mo file
        msgfmt $LOCALE/LC_MESSAGES/$UPDATER_NAME.po --output-file=$LOCALE/LC_MESSAGES/$UPDATER_NAME.mo
        sleep 1

    else

        # If file .po does not exist, create it from the .pot file
        msginit --no-translator --input=$UPDATER_NAME.pot --output=$LOCALE/LC_MESSAGES/$UPDATER_NAME.po --locale=$LOCALE
        sleep 2

    fi
    
    echo "Translation for" $LOCALE_GREEN "has been updated."

done

# Update .pot file messages with the new version number
sed -i "s/$OLD_VERSION/$VERSION/g" $SOFTWARE_NAME.pot
sed -i "s/$OLD_VERSION/$VERSION/g" $UPDATER_NAME.pot

# Update the VERSION.md file with package version
sed -i "s/$OLD_VERSION/$VERSION/g" $VERSION_FILE

# Remove .po~ files in all directories
echoo "Removing unnecessary files..."
find . -name "*.po~" -type f -delete
echog "Done"
