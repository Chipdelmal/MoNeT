import glob
from PIL import Image
import MoNeT_MGDrivE as monet

folder = '/Volumes/marshallShare/vic/eRACR49/'

for graph in sorted(glob.glob(folder+'images/stack/E_*')):
    filename = graph.split("/")[-1]
    heatmap = folder+'images/heat/'+(filename.replace('_S','F_L'))
    im1 = Image.open(graph)
    im2 = Image.open(heatmap)

    path = folder+'images/stitch2/'+(filename.replace('_S','_C'))
    w1,h1 = im1.size
    w2,h2 = im2.size
    w3  = max(w1,w2)
    h3 = max(h1,h2)
    w4 = (w1*h3)/h1

    im3 = Image.new('RGB', (w3,2*h3),'white')
    im3.paste(im1.resize((int(w4),h3)), (int((w3-w4)/2),0))
    im3.paste(im2.resize((w3,h3)), (0,h3))
    im3.save(path,'PNG')
