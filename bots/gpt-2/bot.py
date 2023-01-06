from googletrans import Translator
from happytransformer import HappyGeneration, GENSettings
import unicodedata
# import unicode
import re
import nltk
import difflib

class Bot:
    name = 'GPT2'
    language = 'spanish'

    def __init__(self):
        self.model = self.load_model()
        self.args = GENSettings(max_length=30, early_stopping=True, do_sample=True, top_k=80)
        # self.esToEn = Translator(from_lang="es", to_lang="en")
        # self.enToEs = Translator(from_lang="en", to_lang="es")
        self.translator = Translator()
        self.wordlist = self.load_word_list()
        self.session = """
        Leah visits Barcelona. Leah is an exchange student. Leah is from 
        Germany.
        Leah meets Bot. Bot lives in Spain. Leah and Bot are 13 years old.
        Leah and Bot plan an international picnic with friends. The picnic takes 
        place on Friday at 3pm.
        They plan the foods they will bring to the picnic.
        Bot's favourite foods are patatas bravas and choco frito. Bot will bring 
        patatas bravas and choco frito to the picnic.
        Leah and Bot are talking about other foods they would like at the picnic.

        Bot: Hi Leah, how are you?

        """

    def welcome(self):
        return "Hola, ¿qué tal?"

    def load_word_list(self):
        with open(r'C:\Users\johan\PycharmProjects\chatbot-seminar\LanguageLearningChatbot\dictionaries\spanish-word-list.txt', 'r', encoding='utf-8') as f:
            text = [self.remove_accents(line.strip()) for line in f.readlines()]
            # text.append('Bot:')
        return text

    def load_model(self):
        # generator = pipeline('text-generation', model='gpt2')
        # set_seed(42)
        generator = HappyGeneration("GPT2", "gpt2-medium")  # Best performance
        return generator

    def remove_accents(self, text=''):
        try:
            text = unicode(text, 'utf-8')
        except NameError:  # unicode is a default on python 3
            pass

        text = unicodedata.normalize('NFD', text) \
            .encode('ascii', 'ignore') \
            .decode("utf-8")

        return str(text)

    def chat(self, last_user_message, session):

        # Receive user input, append this to session storage
        translated_message = self.translator.translate(last_user_message,
                                                       src='es',
                                                       dest='en').text
        self.session += "Leah:" + translated_message + '\n'

        # Generate an answer using gpt-2
        answer = ''
        final_answer = ''
        # possible_answers = []
        while final_answer == '':
            # answers = self.model(self.session, max_length=30, num_return_sequences=5)
            answers = self.model.generate_text(self.session, args=self.args)
            answer = answers.text
            if answer.startswith('Bot:'):
                a = answer.split('\n')[0]  # Does not consider everything after a newline expression
                a = a.split('Leah:')[0]  # Neglect generated answers from Leah
                a = a.replace('Bot: ', '').replace('Bot:', '')  # Bot should not be in answer when its being processed

                if len(a.split()) > 0:  # If there are words left in the answer
                    # translate english prediction to spanish
                    a_espanol = self.translator.translate(a, src='en', dest='es').text

                    # Check how many similar words there are in the generated answer and the spanish word list
                    # (predefined)
                    number_similar_words = 0
                    for word in a_espanol.lower().split():
                        word_no_symbols = self.remove_accents(re.sub("['?!,]", '', word))  # no symbols in answer
                        # get the most similar word from the wordlist
                        closest_match = difflib.get_close_matches(word_no_symbols, self.wordlist, n=1)
                        if len(closest_match) > 0:
                            if nltk.edit_distance(word_no_symbols, closest_match[0]) < 3:
                                number_similar_words += 1
                        else:
                            continue

                    #
                    if number_similar_words / len(a_espanol.split()) > 0.85:
                        final_answer = a_espanol
                        break

        self.session += 'Bot: ' + a + '\n'
        return final_answer