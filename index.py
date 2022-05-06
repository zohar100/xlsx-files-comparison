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


def get_files_in_matrix(directory, file_names_array) -> list[list[dict]] or False:
    if len(file_names_array) <= 0:
        return False

    files_data_list = []
    for file_name in file_names_array:
        file = read_xlsx_file(directory, file_name)

        if not file:
            return False

        files_data_list.append(file)

    return files_data_list


def remove_keys_in_dict(dict_to_remove_keys: dict, keys_to_remove: list) -> dict:
    if len(keys_to_remove) <= 0:
        return dict_to_remove_keys

    for key in keys_to_remove:
        if key in dict_to_remove_keys:
            del dict_to_remove_keys[key]
    return dict_to_remove_keys
