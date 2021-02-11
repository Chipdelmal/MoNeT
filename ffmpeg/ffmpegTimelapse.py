import subprocess
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define inputs
id = "E_1_005_005_10_050-HLT"
basePath = "/home/chipdelmal/Documents/WorkSims/SDY/factorial/video/"
rate = 24
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define paths
outName = id
outPath = basePath + outName + '.mp4'
inPath = basePath + id + "/" + '%04d.png'
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Launch process
sp = subprocess.Popen([
    'ffmpeg',
    '-loglevel', '+info',
    '-start_number', '1',
    '-r', str(rate),
    '-f', 'image2',
    '-s', '1920x1080',
    '-i', inPath,
    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
    '-vcodec', 'libx264',
    '-preset', 'veryslow',
    '-crf', '15',
    '-report',
    '-pix_fmt', 'yuv420p',
    outPath
])
sp.wait()
print("I: " + inPath + "\n" + "O: " + outPath)
