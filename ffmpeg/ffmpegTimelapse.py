import subprocess
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define inputs
id = "Days"
basePath = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/Experiment/MultipleRelease8/ANALYZED/Frames/"
rate = 24
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define paths
outName = id
outPath = basePath + outName + '.mp4'
inPath = basePath + id + "/" + id + '%06d.png'
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Launch process
subprocess.Popen([
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
print("I: " + inPath +"\n" + "O: " + outPath)
