import glob
import os
import platform
import sys
from pathvalidate import ValidationError, validate_pathtype
from prettytable import PrettyTable


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
            dir_name_path = dir_name_path + '\\'
        elif platform.system() == 'Linux':
            dir_name_path = dir_name_path + '/'
        return dir_name_path
    except (ValidationError, OSError) as e:
        print(f"{e}\n", file=sys.stderr)


def read_write_several_dir(read_path, write_path):
    """
    Reads from directory all .txt files and merges them to one.
    Placed in the input directory with name concatenated.txt.
    Args:
        read_path (str): raw absolute path to the folder with .txt
            files to read from.
        write_path (str): raw absolute path to the folder with .txt
            files to write.

    Returns:
        Absolute raw path to the concatenated text file as String.
    """
    read_files = glob.glob(f'{read_path}*.txt')
    concatenated_file_dir = f'{write_path}concatenated.txt'

    with open(concatenated_file_dir, 'wb') as outfile:
        for f in read_files:
            with open(f, 'rb') as infile:
                outfile.write(infile.read())
    return concatenated_file_dir


def collocations_format(collocations):
    """
    Converts pairs of collocations data into string format to display
    and write into .txt file.
    Args:
        collocations (tuple): tuples of words(strings)-collocations,
            by POS pairs with PMI.

    Returns:
        String.
    """
    result_str = '\n'
    headers = [['Headword (Verb)', 'Collocate (Noun)', 'PMI'],
               ['Headword (Noun)', 'Collocate (Noun)', 'PMI'],
               ['Headword (Noun)', 'Collocate (Adjective)', 'PMI']]
    types = ['Verbal', 'Substantive (Objective)',
             'Substantive (Attribute)']
    for i, table in enumerate(collocations):
        result_str += types[i] + '\n \n'
        t = PrettyTable(headers[i])
        for coll in table:
            t.add_row([*coll[0], round(coll[1], 5)])
        result_str += str(t) + '\n \n'
    return result_str


def write_to_txt_file(str_to_write, dir_to_write):
    """
    Creates new file and writes content there.
    Args:
        str_to_write (str): text to be inserted to the
        dir_to_write (str): directory path to create result .txt file.
    Returns:
        None.
    """
    with open(f'{dir_to_write}collocations.txt', 'w',
              encoding='windows-1251') as f:
        f.write(str_to_write)
