import os
import shutil

def cleanCars(acdir):
	modspath = os.path.join(acdir, 'content', 'cars')
	if not os.path.isdir(modspath):
		print("Error: Cannot find cars dir " + modspath)
		return
	cars = os.listdir(modspath)
	for car in cars:
		mod_ui_dir = os.path.join(modspath, car, 'ui')
		if not os.path.isdir(mod_ui_dir):
			print("deleting " + os.path.join(modspath, car) + " because " + mod_ui_dir + " is not a directory")
			shutil.rmtree(os.path.join(modspath, car))
			
def cleanTracks(acdir):
	modspath = os.path.join(acdir, 'content', 'tracks')
	if not os.path.isdir(modspath):
		print("Error: Cannot find tracks dir " + modspath)
		return
	tracks = os.listdir(modspath)
	for track in tracks:
		if len(os.listdir(os.path.join(modspath, track))) <= 2:
				print("deleting " + os.path.join(modspath, track) + " because the track does not contain more than 2 dirs")
				shutil.rmtree(os.path.join(modspath, track))
		else:		
			mod_ui_dir = os.path.join(modspath, track, 'ui')
			if not os.path.isdir(mod_ui_dir):
				print("deleting " + os.path.join(modspath, track) + " because " + mod_ui_dir + " is not a directory")
				shutil.rmtree(os.path.join(modspath, track))