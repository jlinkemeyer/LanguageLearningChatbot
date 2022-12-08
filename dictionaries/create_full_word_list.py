import os
import numpy as np
import pandas as pd
from verbecc import Conjugator
from tqdm import tqdm

def create_from_txts(path2txts):
    """

    :param path2txts:
    :return:
    """
    # Read txt
    all_lines = []
    for filename in os.listdir(path2txts):
        filepath = os.path.join(path2txts, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = np.array([line.strip() for line in f.readlines()])

        # Similar to np.unique, but only deletes entries if they are
        # the same and separated by an empty line
        delete_indices = []
        for i, _ in enumerate(lines[:-2]):
            if lines[i] == lines[i + 2] and len(lines[i + 1]) == 0:
                delete_indices.append(i + 1)
                delete_indices.append(i + 2)
        lines = np.delete(lines, delete_indices).tolist()
        spanish_lines = lines[::2]
        all_lines += spanish_lines

    singular_nouns = []
    plural_nouns = []
    for word in all_lines:
        # nouns in list have la/ el
        if word.startswith('la ') or word.startswith('el ') or word.startswith('el/la '):
            singular_nouns.append(word)
            pre, noun = word.split(' ')[0], word.split(' ')[1]
            if pre == 'la':
                pre = 'las'
            elif pre == 'el':
                pre = 'los'
            if noun[-1] in ['a', 'e', 'i', 'o', 'u']:
                plural_nouns.append(f'{pre} {noun}s')
            else:
                plural_nouns.append(f'{pre} {noun}es')

    dict_sgl_pl = {
        'singular': singular_nouns,
        'plural': plural_nouns
    }

    df = pd.DataFrame.from_dict(dict_sgl_pl)
    df.to_csv('singular-to-plural.csv')


    # Get unique words in list
    all_words = ' '.join(all_lines)
    to_replace = ['!', '¡']
    for item in to_replace:
        all_words = all_words.replace(item, '')
    all_words_arr = np.array(all_words.split(' '))
    final = np.unique(all_words_arr).tolist()
    return final


def conjugate_words(wordlist):
    """
    Goes through a list of words, tries to conjugate them and
    appends the conjugated forms to a new list. Returns full
    list of words, conjugated and non-conjugated.
    :param wordlist: list of spanish words
    :return:
    """
    cg = Conjugator(lang='es')
    conjugated_words = []
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
        except:  # catch if word cannot be conjugated (e.g. not a verb)
            continue

    unique_conjugated_words = np.unique(np.array(conjugated_words)).tolist()
    return wordlist + unique_conjugated_words


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
    # all_words = conjugate_words(words)
    # write_to_txt(filename='spanish-word-list.txt', wordlist=all_words)


if __name__ == '__main__':
    main()
