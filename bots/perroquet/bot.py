class Bot:

    name = 'Perroquet'
    avatar = 'avatar/perroquet.png'
    language = 'spanish'

    def welcome(self):
        return "Hola! Cómo estás?"

    def chat(self, last_user_message, session):
        return last_user_message
