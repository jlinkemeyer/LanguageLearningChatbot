from translate import Translator
from happytransformer import HappyGeneration, GENSettings
import unicodedata
# import unicode
import re


class Bot:
    name = 'GPT2'
    language = 'spanish'

    def __init__(self):
        self.model = self.load_model()
        self.args = GENSettings(max_length=55, early_stopping=True, do_sample=True, top_k=80)
        self.esToEn = Translator(from_lang="es", to_lang="en")
        self.enToEs = Translator(from_lang="en", to_lang="es")
        self.wordlist = self.load_word_list()
        self.session = """
        Leah visits Barcelona as an exchange student. She meets Bot. Both are 13 years old. They plan a picnic with a group of friends.
        Bot likes to eat patatas bravas and choco frito, but dislikes eating caracoles.
        Bot is going to bring Tortilla de jamon y queso and horchata to the picnic.

        They still have to decide for other food. The picnic takes place at 3pm in a park. 

        Bot: Hi Leah, how are you?

        """

    def welcome(self):
        return "Hola, ¿qué tal?"

    def load_word_list(self):
        with open('spanish-word-list.txt', 'r', encoding='utf-8') as f:
            text = [self.remove_accents(line.strip()) for line in f.readlines()]
            text.append('Bot:')
        return text

    def load_model(self):
        # generator = pipeline('text-generation', model='gpt2')
        # set_seed(42)
        generator = HappyGeneration("GPT2", "gpt2-medium")  # Best performance
        return generator

    def remove_accents(self, text=''):
        try:
            text = unicode(text, 'utf-8')
        except NameError: # unicode is a default on python 3
            pass

        text = unicodedata.normalize('NFD', text)\
              .encode('ascii', 'ignore')\
              .decode("utf-8")

        return str(text)

    def chat(self, last_user_message):

        # Receive user input, append this to session storage
        translated_message = self.esToEn.translate(last_user_message)
        self.session += "Leah:" + translated_message + '\n'

        # Generate an answer using gpt-2
        answer = ''
        final_answer = ''
        #possible_answers = []
        while final_answer == '':
          # answers = self.model(self.session, max_length=30, num_return_sequences=5)
          answers = self.model.generate_text(self.session, args=self.args)
          answer = answers.text
          if answer.startswith('Bot:'):
            a = answer.split('\n')[0]
            a = a.split('Leah:')[0]
            a = a[5:]
            if len(a.split()) > 0:
              a_espanol = self.enToEs.translate(a)
              #possible_answers.append(a_espanol)
              #final_answer = a_espanol

              #if all(word in self.wordlist for word in a_espanol.split()):
              #    final_answer = a_espanol
              #    print(final_answer)
              #    break

              if sum(1 for word in a_espanol.lower().split() if self.remove_accents(re.sub("['?!,]", '', word)) in self.wordlist)/len(a_espanol.split()) > 0.75: #  and a_espanol.startswith('Bot: '):
                final_answer = a_espanol
                break
        self.session += 'Bot: ' + a + '\n'
        return final_answer