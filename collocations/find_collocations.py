import nltk
import treetaggerwrapper

from preparation import collocations_format, write_to_txt_file
from pmi.pmi_calculation import get_pmi

from pprint import pprint

EMPTY_TEXT_ERROR_MESSAGE = '''Chosen directory contains empty .txt 
    files. Please, fill them with text or choose another directory.'''
CHUNK_POS = ('CC', 'TO', 'IN', '.', ')', '(', ',', ':', ';', 'CD', 'DT',
             'POS', 'PDT', 'RP', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '-', 'AT')


def tokenize_and_tag(text):
    """
    Split lowercase text into tokens and words with pos tags.
    Attention: USES SPELLCHECKER.
    Args:
        text (str): lowercase text to work on.

    Returns:
        List of tokens, list of word-pos pairs.
    """
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    return tokens, tagged


def filter_chunk(word):
    """
    Remove from frequency calculation symbols, digits,
    possessive ending parent, TO, particles,
    prepositions/subordinating conjunctions,
    coordinating conjunctions, predeterminers.
    Args:
        word (str): sequence of symbols to check.

    Returns:
        Boolean.
    """
    tagged_word = nltk.pos_tag([word, ])[0]
    if tagged_word[1] in CHUNK_POS or '.' in tagged_word[0]:
        return True
    return False


def split_collocations(collocations_pmi, tagged_words):
    """
    Split ready-to-show collocations into lists by pairs.
    Filter all nouns, verbs and adjectives.
    Args:
        collocations_pmi (list): collocations with PMI score.
        tagged_words (dict): word-pos pairs.

    Returns:
        List with 3 Lists with pairs (tuples) of collocations,
        grouped by POS:
            1 list - VERB-NOUN
            2 list - NOUN-NOUN
            3 list - NOUN-ADJ
    """
    verb_noun, noun_noun, noun_adj = [], [], []
    for collocation, pmi in collocations_pmi:
        pos_first = tagged_words[collocation[0]]
        pos_second = tagged_words[collocation[1]]
        if ((pos_first.startswith('VB') and pos_second.startswith('NN'))
            or (pos_second.startswith('VB')
                and pos_first.startswith('NN'))):
            verb_noun_pair = ((collocation if pos_first.startswith('VB')
                              else collocation[::-1]), pmi)
            verb_noun.append(verb_noun_pair)

        elif (pos_first.startswith('NN')
              and pos_second.startswith('NN')):
            noun_noun.append((collocation, pmi))

        elif ((pos_first.startswith('JJ')
              and pos_second.startswith('NN'))
              or (pos_first.startswith('NN')
                  and pos_second.startswith('JJ'))):
            noun_adj_pair = ((collocation if pos_first.startswith('NN')
                             else collocation[::-1], pmi))
            noun_adj.append(noun_adj_pair)
    pprint(noun_noun)
    return verb_noun, noun_noun, noun_adj


def get_collocations(word_tokens):
    """
    Finds collocations of different POS and format them to list for the
    further usage.
    Args:
        word_tokens (list): splitted words by nltk lib.

    Returns:
        List of collocations and their PMI scores.
    """
    finder = nltk.BigramCollocationFinder.from_words(word_tokens)
    finder.apply_word_filter(filter_chunk)
    pmi_scored_bigrams = finder.score_ngrams(get_pmi)
    return pmi_scored_bigrams


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
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
    tags = tagger.tag_text(lower_case_text)
    tags2 = treetaggerwrapper.make_tags(tags)
    pprint(tags2)

    tokens, tagged_words_list = tokenize_and_tag(lower_case_text)
    tagged_words = dict(tagged_words_list)
    collocations_pmi = get_collocations(tokens)
    collocations_list = split_collocations(collocations_pmi,
                                           tagged_words)
    result_str = collocations_format(collocations_list)
    write_to_txt_file(result_str, dir_to_write)

    return result_str
