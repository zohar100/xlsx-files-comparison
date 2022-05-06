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


def remove_keys_in_matrix_of_dict(matrix_of_dicts: list[list[dict]], keys_to_remove: list[str]) -> list[list[dict]]:
    if len(keys_to_remove) <= 0:
        return matrix_of_dicts
    for list in matrix_of_dicts:
        for dict in list:
            dict = remove_keys_in_dict(dict, keys_to_remove)
    return matrix_of_dicts


def get_diff_and_same_in_matrix_of_dicts(list_of_dicts: list[list[dict]], file_names: list[str]) -> dict:
    dict: dict[str, list] = {
        "diffrences": [],
        "same": []
    }
    same_tracker_dict: dict[str, int] = {}
    for file in list_of_dicts:
        for file_tow in list_of_dicts:
            if list_of_dicts.index(file_tow) != list_of_dicts.index(file):
                for row in file:
                    if row not in file_tow and row not in dict['diffrences']:
                        dict["diffrences"].append(row)
                    elif row not in dict['diffrences']:
                        str_row = str(row.copy())
                        if str_row not in same_tracker_dict:
                            same_tracker_dict[str_row] = 1
                        elif str_row in same_tracker_dict and same_tracker_dict[str_row] == (len(list_of_dicts) - 1):
                            same_tracker_dict[str_row] += 1
                            dict["same"].append(row)
                        else:
                            same_tracker_dict[str_row] += 1
    return dict


def create_directory_for_diff_files(directory_name: str):
    pre = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(pre, directory_name)
    if not os.path.exists(path):
        os.makedirs(path)