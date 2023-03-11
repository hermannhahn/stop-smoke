# Stop Smoke

This app will help you stop smoking. You can set the starting interval between cigarettes and the app will let you know when you can smoke again.


## For developers

[RUN]
To run the app, run `python stopsmoke.py` in the `src` folder. This will compile the app, updater, translations and installer and run the app.

[TRANSLATIONS]
To add languages, add a new folder in `src/locales` with the language code (e.g. `src/locales/de` for German) and run `./update.sh` in the `src/locales` folder to create .po file. After this, you can translate the strings in the `src/locales/de/stopsmoke.po` file. Re-run `./update.sh` to compile new translations and update existing ones.

[COMPILE]
To compile your altered source code, run `./compile.sh` in the `src` folder. This will compile the app, updater, translations and installer run `./compile.sh` in the src folder.

[FOLDER STRUCTURE]

    src
    ├── db
    │   └── Database Class
    ├── dist
    │   └── Compiled files
    ├── gui
    │   └── GUI Class
    ├── installer
    │   └── Innosetup file
    ├── locales
    │   └── Language Folders
    ├── modules
    │   └── Modules
