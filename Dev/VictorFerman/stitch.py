import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import MoNeT_MGDrivE as monet

folder = '/Volumes/marshallShare/vic/eRACR49/'

for graph in sorted(glob.glob(folder+'images/stack/E_*')):
    filename = graph.split("/")[-1]
    heatmap = folder+'images/heat/'+(filename.replace('_S','F_L'))
    im1 = mpimg.imread(graph)
    im2 = mpimg.imread(heatmap)
    fig,ax = plt.subplots(nrows = 2)
    ax[0].imshow(im1)
    ax[1].imshow(im2)
    ax[0].set_axis_off()
    ax[1].set_axis_off()
    path = folder+'images/stitch/'+(filename.replace('_S','_C'))
    fig.savefig(
        path, facecolor='w', dpi=512,
        edgecolor='w', orientation='portrait', papertype=None,
        format='png', transparent=True, bbox_inches='tight',
        pad_inches=0, frameon=None
    )
    plt.close()
