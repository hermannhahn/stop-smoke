#################################################
# Update translation files                      #
# This script is part of the $SOFTWARE_NAME project #
# Author: Hermann Hahn                          #
# License: GPL-3.0                              #
# Version: 1.0                                  #
# Date: 2021-03-21                              #
#################################################

echo "Starting Translation Update"

# Get Project-Id-Version from command line
# If VERSION is --help, None or /?, print help and exit
VERSION=$1
if [ "$VERSION" = "--help" ] || [ "$VERSION" = "" ] || [ "$VERSION" = "/?" ]; then
    echo "Usage: ./update-translations.sh VERSION"
    echo "VERSION is the version number of the software or translation."
    exit 0
fi

# Initialize variables
AUTHOR="Hermann Hahn"
AUTHOR_EMAIL="hermann.h.hahn@gmail.com"
DEFAULT_EMAIL="hermann.h.hahn@gmail.com"
LAGUAGE_LIST="en de es fr it pt_BR ru"
SOFTWARE_NAME="stop-smoke"
OLD_VERSION=$VERSION

# Get Project-Id-Version from file "$SOFTWARE_NAME.pot" if it exists
if [ -f $SOFTWARE_NAME.pot ]; then
    OLD_VERSION=$(grep "Project-Id-Version: " $SOFTWARE_NAME.pot | cut -d " " -f 2)
fi

# Create/Update .pot file
echo "Creating/Updating $SOFTWARE_NAME.pot..."
xgettext --language=Python --from-code=UTF-8 --keyword=_ --keyword=N_ --package-name="$SOFTWARE_NAME" --package-version="$VERSION" --msgid-bugs-address="$AUTHOR_EMAIL" --output=$SOFTWARE_NAME.pot ../*.py

# Update the .po file with Last-Translator to "Hermann Hahn <hermann.h.hahn@gmail.com>" and add \n at the end
sed -i "s/Last-Translator: FULL NAME <EMAIL@ADDRESS>/Last-Translator: $AUTHOR <$AUTHOR_EMAIL>/" $SOFTWARE_NAME.pot
# Update the .pot file with PO-Revision-Date to current date and add \n at the end
sed -i "s/PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE/PO-Revision-Date: $(date +"%Y-%m-%d %H:%M%z")/" $SOFTWARE_NAME.pot
# Update the .pot file with Language-Team to "NO-TEAM <hermann.h.hahn@gmail.com>" and add \n at the end
sed -i "s/Language-Team: LANGUAGE <LL@li.org>/Language-Team: NO-TEAM <$AUTHOR_EMAIL>/" $SOFTWARE_NAME.pot
# Update the .pot file with Language to "en" and add \n at the end
sed -i "s/Language: */Language: en/" $SOFTWARE_NAME.pot
# Update the .pot file with MIME-Version to "1.0" and add \n at the end
sed -i "s/MIME-Version: 1.0/MIME-Version: 1.0/" $SOFTWARE_NAME.pot
# Update the .pot file with Content-Type to "text/plain; charset=UTF-8" and add \n at the end
sed -i "s/Content-Type: text\/plain; charset=CHARSET/Content-Type: text\/plain; charset=UTF-8/" $SOFTWARE_NAME.pot
# Update the .pot file with Content-Transfer-Encoding to "8bit" and add \n at the end
sed -i "s/Content-Transfer-Encoding: 8bit/Content-Transfer-Encoding: 8bit/" $SOFTWARE_NAME.pot

# Create directory for each language in the list if it does not exist
for LANGUAGES_TO_TRANSLATE in $LAGUAGE_LIST; do
    if [ ! -d $LANGUAGES_TO_TRANSLATE ]; then
        mkdir $LANGUAGES_TO_TRANSLATE
    fi
    if [ ! -d $LANGUAGES_TO_TRANSLATE/LC_MESSAGES ]; then
        mkdir $LANGUAGES_TO_TRANSLATE/LC_MESSAGES
    fi
done

# Save the name of all directories in the locales directory in a variable
LOCALES=$(ls -d */)

# Create variable for needed translations
NEEDED_TRANSLATIONS=0

UPDATED_MO_FILES=False

# For each directory in the locales directory
for LOCALE in $LOCALES; do
    # Remove the last character from the variable
    LOCALE=${LOCALE%?}
    # Check if file "LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po" exists
    if [ -f $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po ]; then
        echo "Updating .po file -> $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po"
        # If yes, update the .po file with the .pot file
        msgmerge --update $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po $SOFTWARE_NAME.pot
        # Wait file to be written
        sleep 1
        # Check if the .mo file exists
        # Update / Create .mo file
        if [ -f $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.mo ]; then
            echo "Updating .mo file -> $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.mo"
        else
            echo "Creating .mo file -> $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.mo"
        fi
        msgfmt $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po --output-file=$LOCALE/LC_MESSAGES/$SOFTWARE_NAME.mo
        UPDATED_MO_FILES=True
        echo "... done."
    else
        # If not, create the .po file from the .pot file
        msginit --no-translator --input=$SOFTWARE_NAME.pot --output=$LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po --locale=$LOCALE
        # Wait file to be written
        sleep 1
        # Update the .po file with Last-Translator to "Hermann Hahn <hermann.h.hahn@gmail.com>" and add \n at the end
        sed -i "s/Last-Translator: Automatically generated/Last-Translator: $AUTHOR <$AUTHOR_EMAIL>/" $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po
        # Say to the user that the .po file has been created and needs to be translated and re-run this script
        echo "File $LOCALE/LC_MESSAGES/$SOFTWARE_NAME.po has been created."
        # Add 1 to the variable for needed translations
        NEEDED_TRANSLATIONS=$((NEEDED_TRANSLATIONS+1))
    fi
done

# If there are needed translations, print error message and exit
if [ $NEEDED_TRANSLATIONS -gt 0 ]; then
    echo ""
    echo "Translations finished."
    echo "There are $NEEDED_TRANSLATIONS .po files that need to be translated."
    echo "Please translate them and re-run this script."
fi

# If .mo files have been updated, print success message
if [ $UPDATED_MO_FILES = True ]; then
    echo ""
    echo "Translations finished."
    echo "All .mo files have been updated or created."
fi
