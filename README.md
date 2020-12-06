# ac-mod-generator
This tool recreates an assetto corsa mod from a track folder or a car folder
# Prerequirements
* Assetto Corsa

# Prerequirements if not using the installer
* Windows 10 (I did not test on Linux)
* Python 3.9
* 7zip

# Available examples for the command line
To use the command line, you will need basic knowledge of the windows command line

Some .bat files are in the folder "examples". One of them shows the command line usage (ShowHelp.bat). You will see all the available options.

# example to generate a car mod
python.exe export-as-mod.py --cars ac_legends_gt40_mk4 --cars_destination D:/Games/ac-mods/cars

# example to generate a track mod
python.exe export-as-mod.py --tracks estoril1988 --tracks_destination D:/Games/ac-mods/tracks

# example to generate a mod from a downloaded mod archive
python.exe export-as-mod.py --tracks estoril1988 --guess D:/Downloads/my-mod.rar

To generate several cars or tracks, separate them by commas. To generate all your tracks or cars, put #all instead of the name of the mod. For the tracks, kunos cars and tracks can be ignored if you pass the  --skip_kunos_mods argument.
