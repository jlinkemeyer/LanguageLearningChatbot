import os.path

from googletrans import Translator
from happytransformer import HappyGeneration, GENSettings
import unicodedata
import re
import nltk
import difflib
import time
import pandas as pd


class SuperBot:

    def __init__(self,
                 wordlist_path: str,
                 welcome_message: str,
                 session: str,
                 target_language: str,
                 similarity_score: float = 0.85):
        """
        :param wordlist_path: path to the wordlist for word filtering
        :param welcome_message: message from Bot upon chat start
        :param session: text from the current chat session
        :param target_language: either 'es' for spanish or 'fr' for french
        :param similarity_score: portion of words that has to be contained in wordlist
        """
        self.model = self.load_model()
        self.args = GENSettings(max_length=30, early_stopping=True, do_sample=True, top_k=80)
        self.translator = Translator()
        self.wordlist = self.load_word_list(wordlist_path)
        self.welcome_message = welcome_message
        self.session = session
        self.target_language = target_language
        self.similarity_score = similarity_score

    def welcome(self):
        return self.welcome_message

    def load_word_list(self, path2wordlist: list[str]):
        """

        :param path2wordlist:
        :return:
        """
        with open(path2wordlist, 'r', encoding='utf-8') as f:
            text = [self.remove_accents(line.strip()) for line in f.readlines()]
        return text

    def load_model(self):
        """
        Load the generator model (here: GPT-2 medium)
        :return: HappyGeneration model
        """
        generator = HappyGeneration("GPT2", "gpt2-medium")
        return generator

    def remove_accents(self, text: str = ''):
        """
        Removes accents from a given string
        :param text: text to remove accents from
        :return: accent-free text
        """
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
        return str(text)

    def chat(self, last_user_message, session):
        """
        Based on the previous chat, uses the GPT-2 model to generate a new answer from the
        Bot after the user entered a message. Returns the first generated answer that comprises
        of a specific portion of words contained in the Bot's wordlist.
        :param last_user_message: last message entered by user
        :return: chatbot's answer
        """

        if not os.path.exists(r'data'):
            os.mkdir(r'data')
        csv_path = r'data/file.csv'

        if not os.path.exists(csv_path):
            df_dict = {
                'TranslationToEnglish': [],
                'AnswerGeneration': [],
                'TranslationToTarget': [],
                'TotalTime': []
            }
        else:
            df = pd.read_csv(csv_path, index_col=False)
            df_dict = df.to_dict('list')

        starttime = time.time()

        # Receive user input, append this to session storage
        translated_message = self.translator.translate(last_user_message,
                                                       src=self.target_language,
                                                       dest='en').text
        self.session += "Leah:" + translated_message + '\n'

        intermediate_time_1 = time.time() - starttime
        df_dict['TranslationToEnglish'].append([intermediate_time_1])

        # Generate an answers using gpt-2-spanish-foods
        final_answer = ''
        for_answer_generation = []
        for_translation = []
        while final_answer == '':
            current_time = time.time()
            answers = self.model.generate_text(self.session, args=self.args)
            answer = answers.text
            for_answer_generation.append(time.time() - current_time)
            if answer.startswith('Bot:'):
                a = answer.split('\n')[0]  # Does not consider everything after a newline expression
                a = a.split('Leah:')[0]  # Neglect generated answers from Leah
                a = a.replace('Bot: ', '').replace('Bot:', '')  # Bot should not be in answer when its being processed
                a_sentences = []
                for i in a.split('.'):
                    if not i.endswith('!') and not i.endswith('?'):
                        i = i + '.'
                    for j in i.split('!'):
                        if not j.endswith('.') and not j.endswith('?'):
                            j = j + '!'
                        # print(j)
                        for x in j.split('?'):
                            if not x.endswith('.') and not x.endswith('!'):
                                x = x + '?'
                            if x == '.' or x == '!' or x == '?':
                                continue
                            if x.startswith(' '):
                                a_sentences.append(x[1:])
                            else:
                                a_sentences.append(x)
                try:
                    if len(a_sentences[0]) < 3:
                        try:
                            a = a_sentences[0] + ' ' + a_sentences[1]
                        except:
                            a = a_sentences[0]
                    else:
                        a = a_sentences[0]
                except:
                    continue # If there is no answer?

                if len(a.split()) > 0:  # If there are words left in the answer
                    # translate english prediction to target language
                    translation_starttime = time.time()
                    answer_target_lang = self.translator.translate(a, src='en', dest=self.target_language).text
                    for_translation.append(time.time() - translation_starttime)

                    # Check how many similar words there are in the generated answer and the given
                    # (predefined) word list
                    number_similar_words = 0
                    for word in answer_target_lang.lower().split():
                        word_no_symbols = self.remove_accents(re.sub("['?!,]", '', word))  # no symbols in answer
                        # get the most similar word from the wordlist
                        closest_match = difflib.get_close_matches(word_no_symbols, self.wordlist, n=1)
                        if len(closest_match) > 0:
                            if nltk.edit_distance(word_no_symbols, closest_match[0]) < 3:
                                number_similar_words += 1
                        else:
                            continue

                    # At least a specific percentage of words have to be similar to those in the given wordlist
                    if number_similar_words / len(answer_target_lang.split()) > self.similarity_score:
                        final_answer = answer_target_lang
                        break

        self.session += 'Bot: ' + a + '\n'

        df_dict['AnswerGeneration'].append(for_answer_generation)
        df_dict['TranslationToTarget'].append(for_translation)

        endtime = time.time() - starttime
        df_dict['TotalTime'].append([endtime])

        df = pd.DataFrame.from_dict(df_dict)
        df.to_csv(csv_path, index=False)

        return final_answer
