import os
import subprocess

id = "Flow"
path = "/Volumes/marshallShare/ERACR/Bakersfield/Riverside/Experiment/MultipleRelease8/ANALYZED/Frames/" + id + "/"
outName = id
rate = 24

outPath = path + outName + '.mp4'
inPath = path + id + '%06d.png'


print(' '.join(command))
print('\n')

subprocess.Popen(['ffmpeg','-loglevel','+info', '-start_number', '1','-r', str(rate), '-f', 'image2', '-s', '1920x1080', '-i', inPath, '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-vcodec', 'libx264', '-preset', 'veryslow','-crf', '15', '-pix_fmt', 'yuv420p',outPath])


# ffmpegCmd = 'ffmpeg -start_number 1 -r 24 -f image2 -s 1920x1080 -i Networks%06d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 00VD.mp4'
# video = subprocess.Popen(['ffmpeg', '-r', '24', '-f', 'image2', '-s', '1920x1080', '-i', subfolder+experiment+'/%05d.png', '-vcodec',
#                           'libx264', '-crf', '25', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', '-pix_fmt', 'yuv420p', folder+'videos/'+vname+'.mp4'])
# 'ffmpeg -start_number 1 -r 24 -f image2 -s 1920x1080 -i Networks%06d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 00VD.mp'
#
# print(os.system("pwd"))
