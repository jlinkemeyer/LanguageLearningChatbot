from ..SuperBot import SuperBot


class Bot(SuperBot):
    name = 'Zara (Kleidung)'
    language = 'es'
    avatar = 'avatar/spain.png'

    def __init__(self):
        SuperBot.__init__(self,
                          wordlist_path='data/es.txt',
                          welcome_message='Hola, ¿qué tal?',
                          session='''
                          Leah visits Barcelona. Leah is an exchange student. Leah is from 
                          Germany.
                          Leah meets Bot. Bot lives in Spain. Leah and Bot are 13 years old.
                          Leah and Bot are best friends.
                          Leah and Bot plan a birthday party with friends. The party takes 
                          place next week on Saturday.
                          They plan the clothes they wear at the party.
                        
                          Bot: Hi Leah, how are you?
                          ''',
                          target_language='es',
                          similarity_score=0.85)