import nltk
import treetaggerwrapper

from preparation import collocations_format, write_to_txt_file
from pmi.pmi_calculation import get_pmi

from pprint import pprint

EMPTY_TEXT_ERROR_MESSAGE = '''Chosen directory contains empty .txt 
    files. Please, fill them with text or choose another directory.'''
CHUNK_POS = ('CC', 'TO', 'IN', '.', ')', '(', ',', ':', ';', 'CD', 'DT',
             'POS', 'PDT', 'RP', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '-',
             'AT')


def tokenize(text):
    """
    Split lowercase text into tokens and words with pos tags.
    Attention: USES SPELLCHECKER.
    Args:
        text (str): lowercase text to work on.

    Returns:
        List of tokens, dict of word-pos pairs.
    """
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
    tags = tagger.tag_text(text)
    tags = treetaggerwrapper.make_tags(tags)
    tag_dict = {tag.word: tag.pos
                for tag in tags
                if isinstance(tag, treetaggerwrapper.Tag)}
    tokens = [tag.word for tag in tags
              if isinstance(tag, treetaggerwrapper.Tag)]
    return tokens, tag_dict


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
    if (tagged_word[1] in CHUNK_POS or '.' in tagged_word[0]
            or '”' in tagged_word[0]):
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
        if ((pos_first.startswith('VV') and pos_second.startswith('NN'))
            or (pos_second.startswith('VV')
                and pos_first.startswith('NN'))):
            verb_noun_pair = ((collocation if pos_first.startswith('VV')
                              else collocation[::-1]), pmi)
            verb_noun.append(verb_noun_pair)

        elif (pos_first.startswith('NN')
              and pos_second.startswith('NN')):
            noun_noun.append((collocation, pmi))

        elif ((pos_first.startswith('AJ')
              and pos_second.startswith('NN'))
              or (pos_first.startswith('NN')
                  and pos_second.startswith('AJ'))):
            noun_adj_pair = ((collocation if pos_first.startswith('NN')
                             else collocation[::-1], pmi))
            noun_adj.append(noun_adj_pair)
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

    tokens, tagged = tokenize(lower_case_text)
    collocations_pmi = get_collocations(tokens)
    collocations_list = split_collocations(collocations_pmi, tagged)
    result_str = collocations_format(collocations_list)
    write_to_txt_file(result_str, dir_to_write)

    return result_str
