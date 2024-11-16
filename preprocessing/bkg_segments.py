import os
import pandas as pd
import numpy as np

input_directory = "..."
output_directory = os.path.join(input_directory, "Corrected Spectra")

start_reciprocal_cm = 651
end_reciprocal_cm = 3999
points = [start_reciprocal_cm, 1253, 1845, 2256, 2400, 3945, end_reciprocal_cm]

os.makedirs(output_directory, exist_ok=True)
csv_files = [f for f in os.listdir(input_directory) if f.endswith('.csv')]

def piecewise_linear_background(trimmed_wavenumbers, spectrum, points):
    background_array = np.zeros_like(spectrum)
    
    for i in range(len(points) - 1):
        start_idx = np.where(trimmed_wavenumbers >= points[i])[0][0]
        end_idx = np.where(trimmed_wavenumbers <= points[i + 1])[0][-1]
        
        x_segment = trimmed_wavenumbers[start_idx:end_idx + 1]
        y_segment = spectrum[start_idx:end_idx + 1]
        
        slope = (y_segment[-1] - y_segment[0]) / (x_segment[-1] - x_segment[0])
        intercept = y_segment[0] - slope * x_segment[0]
        background_array[start_idx:end_idx + 1] = slope * x_segment + intercept
        
    return background_array

for csv_file in csv_files:
    try:
        file_path = os.path.join(input_directory, csv_file)
        df = pd.read_csv(file_path, header=None, skiprows=1)
        df = df.iloc[:, :911]  # Activate for original
        df = df[::-1]  # Activate for original
    
        reciprocal_cm = df.iloc[:, 0].values
        
        start_index = np.where(reciprocal_cm >= start_reciprocal_cm)[0][0]
        end_index = np.where(reciprocal_cm <= end_reciprocal_cm)[0][-1]
    
        trimmed_wavenumbers = df.iloc[start_index:end_index + 1, 0].values
        spectra = df.iloc[start_index:end_index + 1, 1:]  # Skip the first column (wavenumbers)
    
        corrected_spectra = np.zeros_like(spectra)
        intercept_lines = np.zeros_like(spectra)
    
        for i in range(spectra.shape[1]):
            spectrum = spectra.iloc[:, i].values
    
            background_array = piecewise_linear_background(trimmed_wavenumbers, spectrum, points)
            corrected_spectra[:, i] = spectrum - background_array
            intercept_lines[:, i] = background_array
    
        corrected_df = pd.DataFrame(corrected_spectra, columns=[f"Spectrum_{i}" for i in range(corrected_spectra.shape[1])])
        corrected_df.insert(0, "Wavenumber", trimmed_wavenumbers)
        output_file_path = os.path.join(output_directory, f"{csv_file}_bkg_corrected.csv")
        corrected_df.to_csv(output_file_path, index=False, header=False)
        
        intercept_df = pd.DataFrame(intercept_lines, columns=[f"Spectrum_{i}" for i in range(intercept_lines.shape[1])])
        intercept_df.insert(0, "Wavenumber", trimmed_wavenumbers)

        intercept_file_path = os.path.join(output_directory, f"{csv_file}_bkg_intercepts.csv")
        intercept_df.to_csv(intercept_file_path, index=False, header=False)
        
        print(f"Processed and saved: {output_file_path}")
    
    except Exception as e:  # if a file fails
        print(f"Error processing file: {csv_file}")
        print(f"Error message: {e}")
