import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

colors = ["#090446", "#f20060", "#6898ff", "#ff28d4", "#7fff3a", "#c6d8ff", '#6e44ff','#e56399','#ee6c4d', '#861657', '#5cf64a', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

groups = ['W','H','E','R','B']

legends = []
for (allele,color) in zip(groups, colors):
    legends.append(mpatches.Patch(color=color, label=allele))

fig,ax = plt.subplots(figsize=(1, 1))
plt.legend(handles=legends, loc='center')
ax.tick_params(
axis='both',          # changes apply to the both
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
left=False,
right=False,
labelbottom=False, # labels along the bottom edge are off
labelleft=False)
ax.axis('off')
plt.savefig('legend.png', dpi=1024,
            facecolor='w', edgecolor='w', orientation='portrait',
            papertype=None, format="png", transparent=False,
            bbox_inches='tight', pad_inches=0.05, frameon=None)
plt.close(fig)
plt.close('all')
plt.legend(handles=legends, loc='center')
