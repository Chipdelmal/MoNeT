import os

files = [ f for f in os.listdir('.') if os.path.isfile(os.path.join('.',f)) and f.endswith('.png') ]
for i, file in enumerate(sorted(files)):
    os.rename(file, 'image%03d.png' % i)
