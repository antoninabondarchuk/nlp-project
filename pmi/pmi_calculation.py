import math


def get_pmi(gram_count, each_count, all_count):
    """
    Calculates PMI score for pair of words, which are collocations using
    formula PMI(w1, w2) = log2(P(w1, w2)/P(w1) * P(w2))
    Args:
        gram_count (int): count of words placed together, can be None.
        See Also: nltk.BigramCollocationFinder.score_ngrams.
            self.ngram_fd[(w1, w2)] / (self.window_size - 1.0)
        each_count (tuple): 0) w1.raw_freq - int,
                           1) w2.raw_freq - int.
        all_count (int): quantity of all words.

    Returns:
        Float.
    """
    w1, w2 = each_count
    p_w1 = w1 / all_count
    p_w2 = w2 / all_count
    p_gram = gram_count / all_count if gram_count else 0
    pmi = math.log2(p_gram / (p_w1 * p_w2))
    return pmi
