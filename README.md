# Stop Smoke

This app will help you stop smoking. You can set the starting interval between cigarettes and the app will let you know when you can smoke again.


## Development

[RUN]
\n
To run the app, run `python stopsmoke.py` in the `src` folder.
\n
\n
[TRANSLATIONS]
\n
To add languages, just add a new folder in `src/locales` with the language code.
    e.g. `src/locales/de` for German
\n
Then run `./update_translation.sh` in the `src/locales` folder to create .po file. 
\n
After this, you can translate the strings in the `src/locales/de/stopsmoke.po` file. Re-run `./update.sh` to compile new translations and update existing ones.
\n
\n
[COMPILE]
\n
To compile your altered source code, run `./compile.sh` in the `src` folder. This will compile the app, updater, translations and installer run `./compile.sh` in the src folder.
\n
\n
[FOLDER STRUCTURE]\n
    src\n
    ├── db\n
    │   └── Database Class\n
    ├── dist\n
    │   └── Compiled files\n
    ├── gui\n
    │   └── GUI Class\n
    ├── installer\n
    │   └── Innosetup file\n
    ├── locales\n
    │   └── Language Folders\n
    ├── modules\n
    │   └── Modules\n
\n