from googletrans import Translator
from happytransformer import HappyGeneration, GENSettings
import unicodedata
import re
import nltk
import difflib


class SuperBot:

    def __init__(self, wordlist_path, welcome_message, session, target_language, similarity_score=0.85):
        """

        :param wordlist_path:
        :param welcome_message:
        :param session:
        :param target_language: either 'es' for spanish or 'fr' for french
        :param similarity_score:
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
        """

        :return:
        """
        return self.welcome_message

    def load_word_list(self, path2wordlist):
        """

        :param path2wordlist:
        :return:
        """
        with open(path2wordlist, 'r', encoding='utf-8') as f:
            text = [self.remove_accents(line.strip()) for line in f.readlines()]
        return text

    def load_model(self):
        """

        :return:
        """
        generator = HappyGeneration("GPT2", "gpt2-medium")
        return generator

    def remove_accents(self, text=''):
        """

        :param text:
        :return:
        """
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
        return str(text)

    def chat(self, last_user_message, session):
        """

        :param last_user_message:
        :return:
        """

        # Receive user input, append this to session storage
        translated_message = self.translator.translate(last_user_message,
                                                       src=self.target_language,
                                                       dest='en').text
        self.session += "Leah:" + translated_message + '\n'

        # Generate an answers using gpt-2-spanish-foods
        final_answer = ''
        while final_answer == '':
            answers = self.model.generate_text(self.session, args=self.args)
            answer = answers.text
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
                if len(a_sentences[0]) < 3:
                    a = a_sentences[0] + ' ' + a_sentences[1]
                else:
                    a = a_sentences[0]

                if len(a.split()) > 0:  # If there are words left in the answer
                    # translate english prediction to target language
                    answer_target_lang = self.translator.translate(a, src='en', dest=self.target_language).text

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
        return final_answer
