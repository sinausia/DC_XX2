import os
import pandas as pd

directory_files = "..."

subdirectories = [
    os.path.join(dirpath, dirname)
    for dirpath, dirnames, filenames in os.walk(directory_files)
    for dirname in dirnames if dirname == '4000-1100' and 'DS_' in dirpath
]

sorted_subdirectories = sorted(subdirectories, key=lambda x: os.path.basename(os.path.dirname(x)))
transposed_dfs = []

for subdir in sorted_subdirectories:
    csv_file = "centered_ReconstructedData_PCs1.csv"
    try:
        file_path = os.path.join(subdir, csv_file)
        df = pd.read_csv(file_path, header=None, skiprows=0)
        df = df[::-1]
        transposed_df = df.T
        transposed_dfs.append(transposed_df)

        print(f"Concatenated: {file_path}")
    except Exception as e:
        print(f"Error file: {file_path}")

final_df = pd.concat(transposed_dfs, axis=1)
final_csv_path = os.path.join(directory_files, "final_concatenated.csv")
final_df.to_csv(final_csv_path, index=False, header=False)
