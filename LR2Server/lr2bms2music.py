import subprocess
import os
import glob
import locale

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def encodeFile(bms):
	bms_path = os.path.split(bms)[0]
	bms_name = os.path.split(bms)[1]
	filename = os.path.splitext(bms_name)[0] + ".wav"
	filepath = BASE_DIR+"\\Temp\\" + filename

	# if file is already exists, then dont encode
	if (os.path.isfile(filepath)):
		pass
	else:
		execute(BASE_DIR+"\\bme2wav\\bmx2wavc.exe", [bms.encode(locale.getpreferredencoding()), filepath.encode(locale.getpreferredencoding())])

	return filepath

def execute(path, cmd):
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	si.wShowWindow = subprocess.SW_HIDE
	proc = subprocess.Popen([path] + cmd, startupinfo=si)
	proc.wait()