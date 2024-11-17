import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.cm import magma
#import matplotlib.colors as colors
mpl.use('SVG')
mpl.rcParams['svg.fonttype'] = 'none'  # Do not convert fonts to paths



file_path = "..."
output_folder_path = "..."
experiment_classification = '_08'

df = pd.read_csv(file_path, header=None, skiprows=0)
df = df.T
df.columns = df.iloc[0]
df = df[1:911] 

#%%

time_per_spectrum = 1.1 # s
total_time = time_per_spectrum * df.shape[0]

x = df.columns.astype(float)
time = np.linspace(0, total_time, df.shape[0])
#depth = np.arange(df.shape[0])
X, Y = np.meshgrid(x, time)
Z = df.values


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='magma', edgecolor='none')
cset = ax.contourf(X, Y, Z, zdir='z', offset=85, cmap='magma', levels=100)
ax.invert_xaxis()
ax.set_zlim(85, 105)  # Adjust levels
ax.set_xlabel('Wavenumbers (cm$^{-1}$)', fontsize=14)
ax.set_ylabel('Time (s)', fontsize=14)
#ax.set_zlabel('Transmittance (a.u.)', fontsize=14)
ax.tick_params(axis='both', labelsize=14)
ax.xaxis.labelpad = 10
ax.yaxis.labelpad = 10
ax.zaxis.labelpad = 10

ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

ax.set_zticklabels([]) # Eliminates text in vertical axis
ax.set_xticks([4000, 3500, 3000, 2500, 2000, 1500, 1000, 500]) 
ax.set_yticks([0, 200, 400, 600, 800, 1000]) 
#ax.set_zticks([])
ax.set_box_aspect([1.5, 1.2, 1])
ax.grid(True)
ax.view_init(elev=15, azim=-80, roll=0)

output_plot_path = output_folder_path + "loaded data"
plt.savefig(output_plot_path + ".png", dpi=300, bbox_inches="tight")
#plt.savefig(output_plot_path + ".eps", format='eps', dpi=300, bbox_inches="tight")
plt.savefig(output_plot_path + ".svg", format='svg', bbox_inches="tight")


plt.show()
