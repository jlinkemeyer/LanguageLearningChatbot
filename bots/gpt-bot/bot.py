from transformers import pipeline, set_seed
from translate import Translator
from happytransformer import HappyGeneration, GENSettings
import transformers


class Bot:

    name = 'GPT Bot'
    language ='spanish'

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
        with open('data/spanish-word-list.txt', 'r', encoding='utf-8') as f:
            text = [line.strip() for line in f.readlines()]
            text.append('Bot:')
        return text

    def load_model(self):
        # generator = pipeline('text-generation', model='gpt2')
        # set_seed(42)
        generator = HappyGeneration("GPT2", "gpt2-medium")  # Best performance
        return generator

    def chat(self, last_user_message, session):
        translated_message = self.esToEn.translate(last_user_message)
        self.session += "Leah:" + translated_message + '\n'

        # Generate an answer using gpt-2
        answer = ''
        while answer == '':
            # answers = self.model(self.session, max_length=30, num_return_sequences=5)
            answers = self.model.generate_text(self.session, args=self.args)

            print(answers)

            # Retranslate
            translated_answers = []
            for answer in answers:
                translated_answers.append(self.enToEs.translate(answer['generated_text']))

            # Filter for words
            for translated_answer in translated_answers:
                if all(word in self.wordlist for word in translated_answer.split()) and translated_answer.startswith('Bot: '):
                    answer = translated_answer
                    break
                if sum(1 for word in translated_answer.lower().split() if word.split("'?!") in self.wordlist)/len(translated_answer.split()) > 0.9 and translated_answer.startswith('Bot: '):
                    answer = translated_answer
                    break
            if answer != '':
                break
        # remove bot: from answer
        answer = answer.replace('Bot:', '')
        # append answer to session
        self.session += answer + '\n'
        return answer


