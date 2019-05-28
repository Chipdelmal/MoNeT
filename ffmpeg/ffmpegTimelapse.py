import os
import subprocess

path = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/Experiment/MultipleRelease6/ANALYZED/Frames/Networks/"
id = "Networks"
outName = "outVideo"
rate = 24

inPath = path + id + '%06d.png" '
outPath = path + outName + '.mp4'


subprocess.Popen([
    'ffmpeg',
    '-start_number', '1',
    '-r', str(rate),
    '-f', 'image2',
    '-s', '1920x1080',
    '-i', inPath,
    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
    '-vcodec', 'libx264',
    '-preset', 'veryslow',
    '-crf', '15',
    '-pix_fmt', 'yuv420p',
    outPath
])
