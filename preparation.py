import glob
import os
import platform
import sys
from pathvalidate import ValidationError, validate_pathtype


def get_raw_path(path):
    """
    Checks if path is valid and converts it to compatible string.
    Args:
        path (str): absolute path to directory or file.

    Returns:
        Raw path as String.
    """
    try:
        validate_pathtype(path)
        dir_name_path = os.path.normpath(path)
        if platform.system() == 'Windows':
            return dir_name_path + '\\'
        elif platform.system() == 'Linux':
            return dir_name_path + '/'
        return dir_name_path
    except (ValidationError, OSError) as e:
        print(f"{e}\n", file=sys.stderr)


def read_several_from_dir(directory_path):
    """
    Reads from directory all .txt files and merges them to one.
    Placed in the input directory with name concatenated.txt.
    Args:
        directory_path (str): raw absolute path to the folder with .txt
            files to read from.

    Returns:
        Absolute raw path to the concatenated text file as String.
    """
    if not directory_path:
        pass
    read_files = glob.glob(f'{directory_path}*.txt')
    concatenated_file_dir = f'{directory_path}concatenated.txt'

    with open(concatenated_file_dir, 'wb') as outfile:
        for f in read_files:
            with open(f, 'rb') as infile:
                outfile.write(infile.read())
    return concatenated_file_dir


def preparation_stage(input_path):
    """
    Includes checking input path to be valid and merging input .txt
    files into concatenated.txt file.
    Args:
        input_path (str): raw absolute path to the folder with .txt
            files to read from.

    Returns:
        Absolute raw path to the concatenated text file as String.
    """
    raw_dir_path = get_raw_path(input_path)
    file_path_to_work = read_several_from_dir(raw_dir_path)
    return file_path_to_work
