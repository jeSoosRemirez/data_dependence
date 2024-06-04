import os
from utils.read_data import load_data


en_files = [
    os.path.join("data_files/en_files", file)
    for file in os.listdir("data_files/en_files")
    if file.endswith(".csv")
]
gp_files = [
    os.path.join("data_files/gm_files", file)
    for file in os.listdir("data_files/gm_files")
    if file.endswith(".csv")
]

en_df, gp_df = load_data(en_files, gp_files)
