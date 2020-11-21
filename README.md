# ac-mod-generator
This tool recreates an assetto corsa mod from a track folder or a car folder

# Prerequirements
* Windows 10 (I did not test on Linux)
* Python 3.9
* 7zip
* Assetto Corsa
* Configure "actools-config.json" with your environment

# example to generate a car mod
'C:\Python39\python.exe' export-as-mod.py' '--cars' 'ac_legends_gt40_mk4' '--cars_destination' 'D:/Games/ac-mods/cars'

# example to generate a track mod
'C:\Python39\python.exe' export-as-mod.py' '--tracks' 'estoril1988' '--tracks_destination' 'D:/Games/ac-mods/tracks' 

# example to generate a mod from a downloaded mod archive
TODO

To generate several cars or tracks, separate them by commas. To generate all your tracks or cars, put #all instead of the name of the mod. For the tracks, kunos tracks will be ignored. I did not do it for the cars for now because it's gonna be very long to generate the list of kunos cars.
