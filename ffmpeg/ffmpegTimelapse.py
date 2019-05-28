import os
import subprocess

path = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/Experiment/MultipleRelease6/ANALYZED/Frames/Networks/"
id = "Networks"
outName = "outVideo"
rate = 24

optsA = 'ffmpeg -start_number 1 -r ' + str(rate) + ' -f image2 -s 1920x1080 '
optsB = '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '
optsC = '-vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p '
outPath = path + outName + '.mp4'
inPath = '-i ' + path + id + '%06d.png '
inPath

fullCmd = optsA + inPath + optsB + optsC + outPath
subprocess.Popen(fullCmd)


# ffmpegCmd = 'ffmpeg -start_number 1 -r 24 -f image2 -s 1920x1080 -i Networks%06d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 00VD.mp'
# video = subprocess.Popen(['ffmpeg', '-r', '24', '-f', 'image2', '-s', '1920x1080', '-i', subfolder+experiment+'/%05d.png', '-vcodec',
#                           'libx264', '-crf', '25', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-pix_fmt', 'yuv420p', folder+'videos/'+vname+'.mp4'])
# 'ffmpeg -start_number 1 -r 24 -f image2 -s 1920x1080 -i Networks%06d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 00VD.mp'
#
# print(os.system("pwd"))
