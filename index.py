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
        "matches": []
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
                            dict["matches"].append(row)
                        else:
                            same_tracker_dict[str_row] += 1
    return dict


def create_directory_for_diff_files(directory_name: str):
    pre = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(pre, directory_name)
    if not os.path.exists(path):
        os.makedirs(path)


def save_dict_of_files(dictionary: dict[str, list], directory: str = "diff_files") -> None:
    pre = os.path.dirname(os.path.realpath(__file__))
    for file_name, values in dictionary.items():
        df = pd.DataFrame(values)
        path = os.path.join(pre, directory, f"{file_name}.xlsx")
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Data', index=False)
        writer.save()


def compare_xlsx_files(directory_of_files: str = "./reports", columns_to_ignore: list[str] = []) -> None:
    file_names = get_file_names(directory_of_files, "xlsx")
    if not file_names:
        return print("No files found.")

    files_list = get_files_in_matrix(directory_of_files, file_names)
    if not files_list:
        return print("Error reading files.")

    files_list_after_removing_keys = remove_keys_in_matrix_of_dict(
        files_list, columns_to_ignore)

    files_diff = get_diff_and_same_in_matrix_of_dicts(
        files_list_after_removing_keys, file_names)

    new_directory_name = "diff_files"

    create_directory_for_diff_files(new_directory_name)

    return save_dict_of_files(files_diff, new_directory_name)


def print_cli_headers():
    line = "###########################################################################"
    title = "XLSX FILES COMPARISON"
    line_mins_title = line[:int((len(line) - len(title)) / 2) - 1]
    print(line)
    print(f"{line_mins_title} {title} {line_mins_title}")
    print(line, '\n')


def get_directory_name_from_user():
    directory_of_files = input(
        "Enter path to the directory where the files are located or press Enter to use default location (default='./reports'): \n")
    if not directory_of_files:
        directory_of_files = "./reports"
    return directory_of_files


def get_columns_to_ignore_from_user():
    columns_to_ignore = input(
        "Enter columns to ignore(use ',' for separate) or press Enter to compare all columns: \n")
    if not columns_to_ignore:
        columns_to_ignore = []
    else:
        columns_to_ignore = columns_to_ignore.split(",")
    return columns_to_ignore


if __name__ == "__main__":
    print_cli_headers()

    directory_of_files = get_directory_name_from_user()

    columns_to_ignore = get_columns_to_ignore_from_user()

    compare_xlsx_files(directory_of_files, columns_to_ignore)
