import os
import numpy as np


def main():
    # Read txt
    path2txts = 'wordlists'
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

    # Get unique words in list
    all_words = ' '.join(all_lines)
    to_replace = ['!', '¡']
    for item in to_replace:
        all_words = all_words.replace(item, '')
    all_words_arr = np.array(all_words.split(' '))
    final = np.unique(all_words_arr)

    with open('spanish-word-list.txt', 'w', encoding='utf-8') as f:
        [f.write("%s\n" % word) for word in final]
    f.close()


if __name__ == '__main__':
    main()
