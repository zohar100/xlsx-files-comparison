from __future__ import annotations

import glob
import os

import pandas as pd


def get_file_names(directory: str, files_type: str) -> list or False:
    try:
        file_names = []
        os.chdir(directory)

        for file in glob.glob(f"*.{files_type}"):
            file_names.append(file)

        if len(file_names) <= 0:
            return False

        return file_names
    except Exception:
        return False


def read_xlsx_file(directory: str, file_name: str) -> dict or False:
    try:
        pre = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(pre, directory, file_name)
        data = pd.read_excel(path).to_dict('records')

        return data

    except Exception as e:
        return False
