import os
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SpectraCorrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spectra Background Correction")
        
        self.file_path = None
        self.start_bkg = None
        self.end_bkg = None
        self.spectra = None
        self.wavenumbers = None
        self.corrected_spectra = None
        
        self.setup_gui()
        
    def setup_gui(self):
        self.load_button = tk.Button(self.root, text="Load Spectra", command=self.load_file)
        self.load_button.pack(pady=10)

        self.figure = Figure(figsize=(10, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.correct_button = tk.Button(self.root, text="Save Corrected Spectra", command=self.save_corrected_spectra)
        self.correct_button.pack(pady=10)
        self.correct_button.config(state=tk.DISABLED)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not self.file_path:
            return
        
        self.load_spectra()
        self.plot_spectra()

    def load_spectra(self):
        df = pd.read_csv(self.file_path, header=None, skiprows=1).iloc[:, :911][::-1]
        self.wavenumbers = df.iloc[:, 0].values
        self.spectra = df.iloc[:, 1:]

    def plot_spectra(self):
        self.ax.clear()
        for col in self.spectra.columns:
            self.ax.plot(self.wavenumbers, self.spectra[col], label=f'Spectrum {col}')
        self.ax.set_xlabel("Wavenumber")
        self.ax.set_ylabel("Intensity")
        #self.ax.legend()
        self.canvas.draw()

    def on_click(self, event):
        if event.inaxes is not None:
            if self.start_bkg is None:
                self.start_bkg = event.xdata
                self.ax.axvline(self.start_bkg, color='red', linestyle='--')
            elif self.end_bkg is None:
                self.end_bkg = event.xdata
                self.ax.axvline(self.end_bkg, color='blue', linestyle='--')
                self.correct_spectra()
                self.plot_corrected_spectra()
                self.correct_button.config(state=tk.NORMAL)
            self.canvas.draw()

    def correct_spectra(self):
        start_index_bkg = np.where(self.wavenumbers >= self.start_bkg)[0][0]
        end_index_bkg = np.where(self.wavenumbers <= self.end_bkg)[0][-1]
        
        self.corrected_spectra = np.zeros_like(self.spectra)
        
        for i in range(self.spectra.shape[1]):
            spectrum = self.spectra.iloc[:, i].values
            slope = (spectrum[end_index_bkg] - spectrum[start_index_bkg]) / (self.wavenumbers[end_index_bkg] - self.wavenumbers[start_index_bkg])
            intercept = spectrum[start_index_bkg] - slope * self.wavenumbers[start_index_bkg]
            background_array = slope * self.wavenumbers + intercept
            self.corrected_spectra[:, i] = spectrum - background_array

    def plot_corrected_spectra(self):
        self.ax.clear()
        for i in range(self.corrected_spectra.shape[1]):
            self.ax.plot(self.wavenumbers, self.corrected_spectra[:, i], label=f'Corrected Spectrum {i}')
        self.ax.set_xlabel("Wavenumber")
        self.ax.set_ylabel("Corrected Intensity")
        #self.ax.legend()
        self.canvas.draw()

    def save_corrected_spectra(self):
        output_directory = os.path.join(os.path.dirname(self.file_path), "Corrected Spectra")
        os.makedirs(output_directory, exist_ok=True)
        trimmed_wavenumbers = self.wavenumbers
        corrected_df = pd.DataFrame(self.corrected_spectra, columns=[f"Spectrum_{i}" for i in range(self.corrected_spectra.shape[1])])
        corrected_df.insert(0, "Wavenumber", trimmed_wavenumbers)
        output_file_path = os.path.join(output_directory, os.path.basename(self.file_path).replace(".csv", "_bkg_corrected.csv"))
        corrected_df.to_csv(output_file_path, index=False, header=False)
        messagebox.showinfo("Save Successful", f"Corrected spectra saved to {output_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpectraCorrectionApp(root)
    root.mainloop()
