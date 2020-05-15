import nltk
from preparation import collocations_format, write_to_txt_file

EMPTY_TEXT_ERROR_MESSAGE = '''Chosen directory contains empty .txt 
    files. Please, fill them with text or choose another directory.'''


def get_collocations(text):
    """
    Finds collocations of different POS and format them to list for the
    further usage.
    Args:
        text (str): lower-cased text to analyze.

    Returns:
        List with 3 Lists with pairs (tuples) of collocations,
        grouped by POS:
            1 list - VERB-NOUN
            2 list - NOUN-NOUN
            3 list - NOUN-ADJ
    """
    pass


def collocations_stage(work_file, dir_to_write):
    """
    Contains POS tagging stage and finding the collocations.
    Args:
        work_file (str): valid raw path to file with concatenated text.
        dir_to_write (str): valid path to input result files.

    Returns:
        String of 3 formatted tables of collocations
        or Message about empty input files.
    """
    with open(work_file) as f:
        text = f.read()
    if not text:
        return EMPTY_TEXT_ERROR_MESSAGE
    lower_case_text = text.lower()

    collocations_lists = get_collocations(lower_case_text)
    result_str = collocations_format(collocations_lists)
    write_to_txt_file(result_str, dir_to_write)

    return result_str
