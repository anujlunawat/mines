import pandas as pd
import os
import glob
import re


def f():
    def extract_number(file_path):
        match = re.search(r'(\d+)gem', file_path)
        return int(match.group(1)) if match else 0

    file_pattern = os.path.join("assets", "multipliers", "*gem*.xlsx")
    files = glob.glob(file_pattern)
    files.sort(key=extract_number)

    main_dict = {}

    for index, file in enumerate(files, 1):
        df = pd.read_excel(file, engine="openpyxl",)
        diamond = df.iloc[0:, 0]
        mine = df.iloc[:, 1]
        multiplier = df.iloc[:, 2]

        d = {key: multiplier for key, multiplier in zip(mine, multiplier)}
        main_dict[index] = d

    return main_dict
