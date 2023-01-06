import os
import numpy as np
from verbecc import Conjugator
from tqdm import tqdm
import nltk
from pattern.es import pluralize, attributive, FEMALE, MALE, PLURAL


def create_from_txts(path2txts):
    """

    :param path2txts:
    :return:
    """

    # Create a list of all spanish words based on txt files
    all_lines = []
    all_english_lines = []
    for filename in os.listdir(path2txts):

        # Read each txt file
        filepath = os.path.join(path2txts, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = np.array([line.strip() for line in f.readlines()])

        # Specific to spanish-dict word lists: Filtering for spanish
        # words based on their location in the txt file
        delete_indices = []
        for i, _ in enumerate(lines[:-2]):
            if lines[i] == lines[i + 2] and len(lines[i + 1]) == 0:
                delete_indices.append(i + 1)
                delete_indices.append(i + 2)
        lines = np.delete(lines, delete_indices).tolist()
        spanish_lines = lines[::2]
        english_lines = lines[1::2]
        all_english_lines += english_lines
        all_lines += spanish_lines

    # Part of speech tagging to generate new word forms # Doing this in english
    # as spanish versions all do not work well
    verbs, nouns, adjectives, rest = [], [], [], []
    for word_en, word_es in zip(all_english_lines, all_lines):

        # Create POS tags
        word_tokenized = nltk.word_tokenize(word_en)
        pos_tags = nltk.pos_tag(word_tokenized)
        actual_tags = np.array(pos_tags)[:, 1]

        # Append further word forms depending on pos tag
        if 'VB' in actual_tags:
            verbs += word_es.split(' ')
        elif 'NN' in actual_tags and len(actual_tags) == 1:  # if # counts == len, append both
            if word_es.startswith('el') or word_es.startswith('la'):
                nouns.append(word_es)
                nouns.append(pluralize(word_es))
        elif 'JJ' in actual_tags:
            adjectives.append(word_es)

            # Generate adjective word forms; adjectives have male/ female +
            # singular/ plural word forms
            for adj in word_es.split(' '):
                gender_change = ''
                if adj.endswith('o'):
                    gender_change = attributive(adj, gender=FEMALE)
                if adj.endswith('a'):
                    gender_change = attributive(adj, gender=MALE)
                gender_female_pl = attributive(adj, gender=FEMALE+PLURAL)
                gender_male_pl = attributive(adj, gender=MALE+PLURAL)
                adjectives += [gender_change, gender_female_pl, gender_male_pl]
        else:
            rest.append(word_es)

    # Conjugate the verbs, doing this outside the loop for processing
    # time reason
    verb_conjugation = conjugate_words(verbs)
    verbs += verb_conjugation

    # Get unique words in list, delete exclamation marks
    all_lines = verbs + nouns + adjectives + rest
    all_words = ' '.join(all_lines)
    to_replace = ['!', '¡', '?', '¿', ',']
    for item in to_replace:
        all_words = all_words.replace(item, '')
    all_words_as_arr = np.array(all_words.split(' '))
    unique_words = np.unique(all_words_as_arr).tolist()

    return unique_words


def conjugate_words(wordlist):
    """
    Goes through a list of words, tries to conjugate them and
    appends the conjugated forms to a new list. Returns full
    list of words, conjugated and non-conjugated.
    :param wordlist: list of spanish words
    :return:
    """
    cg = Conjugator(lang='es')
    conjugated_words, rest_words = [], []
    for word in tqdm(wordlist):
        try:
            # Get present tense conjugation of current word
            conjugation = cg.conjugate(word)
            present_tense_conjugation = conjugation['moods']['indicativo']['presente']

            # Append unique words to full word list
            all_conj = ' '.join(present_tense_conjugation)
            all_words_arr = np.array(all_conj.split(' '))
            all_words_unique = np.unique(all_words_arr).tolist()
            conjugated_words += all_words_unique
        except:  # catch if word cannot be conjugated (e.g. not a verb), still append to list for final wordlist
            rest_words.append(word)

    unique_conjugated_words = np.unique(np.array(conjugated_words + rest_words)).tolist()
    return unique_conjugated_words


def write_to_txt(filename, wordlist):
    """

    :param filename:
    :param wordlist:
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        [f.write("%s\n" % word) for word in wordlist]
    f.close()


def main():
    words = create_from_txts(path2txts='wordlists')
    write_to_txt(filename='spanish-word-list.txt', wordlist=words)


if __name__ == '__main__':
    main()
