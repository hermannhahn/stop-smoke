# Stop Smoke

This app will help you stop smoking. You can set the starting interval between cigarettes and the app will let you know when you can smoke again.


## Development

[RUN]

To run the app, run `python stopsmoke.py` in the `src` folder.
<br>
<br>
<br>
[TRANSLATIONS]
<br>
<br>
To add languages, just add a new folder in `src/locales` with the language code.
<br>
e.g. `src/locales/de` for German
<br>
<br>
Then run `./update_translation.sh` in the `src/locales` folder to create .po file. 
<br>
<br>
After this, you can translate the strings in the `src/locales/de/stopsmoke.po` file.
<br>
Re-run `./update_translation.sh` to compile new translations and update existing ones.
<br>
<br>
<br>
[COMPILE]
<br>
<br>
To compile your altered source code, run `./compile.sh` in the `src` folder. This will compile the app, updater, translations and installer run `./compile.sh` in the src folder.
<br>
<br>
<br>
[STRUCTURE]
```
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
´´´
