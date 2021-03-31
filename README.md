# Assetto Corsa Mod Packager
This tool has 2 main purposes:
 * Help you extract archives of your mods automatically with a command line program.
 * Update automatically information on your mods, for example by adding specific tags to tracks that support CSP effects (currently, it can add these tags: rainfx, lightingfx, weatherfx, grassfx). 
 * Add a contextual menu item when you right click on a file with windows explorer to generate a valid mod archive. When doing it from an installed mod, it will identify all the files needed by the mod, not only the folder itself (fonts, drivers, etc.). Archives will be generated in the current directory or your desktop if the current directory is not writable.
 
Keep in mind that it's still a work in progress app:
 * make backups of your mods before using it. Be careful with the option which update all your tracks tags, although I have tested it on all my tracks without any problems.
 * give feedback if something does not work so I can fix it. I tried to identify all the files needed by a mod, but if you have identified something missing, don't hesitate to report it.

## Prerequirements
* Assetto Corsa

## Prerequirements if not using the installer
* Windows 10
* Python 3.9
* 7zip

## Available examples for the command line
To use the command line, you will need basic knowledge of the windows command line

Some .bat files are in the folder "examples". One of them shows the command line usage (ShowHelp.bat). You will see all the available options.

### example to generate a car mod
python.exe export-as-mod.py --cars ac_legends_gt40_mk4 --cars_destination D:/Games/ac-mods/cars

### example to generate a track mod
python.exe export-as-mod.py --tracks estoril1988 --tracks_destination D:/Games/ac-mods/tracks

### example to generate a mod from a downloaded mod archive
python.exe export-as-mod.py --guess D:/Downloads/my-mod.rar

To generate several cars or tracks, separate them by commas. To generate all your tracks or cars, put #all instead of the name of the mod. For the tracks, kunos cars and tracks can be ignored if you pass the  --skip_kunos_mods argument.
