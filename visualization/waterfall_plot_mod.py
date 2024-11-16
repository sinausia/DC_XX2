import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import matplotlib as mpl
mpl.use('SVG')
mpl.rcParams['svg.fonttype'] = 'none'  # Do not convert fonts to paths

def generate_waterfall_plots(directory):
    output_directory = os.path.join(directory, 'waterfall_plots')
    os.makedirs(output_directory, exist_ok=True)
    
    for file_name in os.listdir(directory):
        if file_name.startswith('DS_') and file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            try:
                df = pd.read_csv(file_path)
                print(f"Successfully read file: {file_path}")
                wavenumbers = df.iloc[:, 0].values

                num_spectra = df.shape[1] - 1  # excluding the wavenumber column
                time_interval = 1.1  # seconds

                time_points = np.arange(num_spectra) * time_interval

                X, Y = np.meshgrid(wavenumbers, time_points)
                Z = df.iloc[:, 1:].values.T  # Transpose to match the meshgrid shape

                fig = plt.figure(figsize=(12, 8))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(X, Y, Z, cmap='magma', edgecolor='none')
                #cset = ax.contourf(X, Y, Z, zdir='z', offset=np.min(Z), cmap='magma', levels=100)
                ax.invert_xaxis()
                ax.set_xlabel('Wavenumbers (cm$^{-1}$)', fontsize=14)
                ax.set_ylabel('Time (s)', fontsize=14)
                ax.tick_params(axis='both', labelsize=14)
                ax.xaxis.labelpad = 10
                ax.yaxis.labelpad = 10
                ax.zaxis.labelpad = 10
                ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
                ax.set_zticklabels([])
                #ax.set_xticks([4000, 3500, 3000, 2500, 2000, 1500, 1000])
                ax.set_yticks([0, 200, 400, 600, 800, 1000])
                ax.set_box_aspect([1.5, 1.2, 1])
                ax.grid(True)
                ax.view_init(elev=15, azim=-80, roll=0)

                base_filename = os.path.splitext(file_name)[0]
                png_filename = os.path.join(output_directory, f'{base_filename}_waterfall_plot.png')
                svg_filename = os.path.join(output_directory, f'{base_filename}_waterfall_plot.svg')
                plt.savefig(png_filename, dpi=300, bbox_inches="tight")
                plt.savefig(svg_filename, format='svg', bbox_inches="tight")
                plt.show()
                
                # interactive html plot
                fig_plotly = go.Figure(data=[go.Surface(z=Z, x=wavenumbers, y=time_points, colorscale='magma')])
                fig_plotly.update_layout(
                    scene=dict(
                        xaxis_title='Wavenumbers (cm$^{-1}$)',
                        yaxis_title='Time (s)',
                        zaxis_title='Intensity',
                        xaxis=dict(tickvals=[4000, 3500, 3000, 2500, 2000, 1500, 1000, 500]),
                        yaxis=dict(tickvals=[0, 200, 400, 600, 800, 1000])
                    ),
                    width=800,
                    height=800
                )

                html_filename = os.path.join(output_directory, f'{base_filename}_waterfall_plot.html')
                fig_plotly.write_html(html_filename)

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

if __name__ == "__main__":
    directory = '...'
    generate_waterfall_plots(directory)
