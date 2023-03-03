from ..SuperBot import SuperBot


class Bot(SuperBot):
    name = 'Coco (Kleidung)'
    language = 'fr'
    avatar = 'avatar/france.png'

    def __init__(self):
        SuperBot.__init__(self,
                          wordlist_path='data/fr.txt', # 'data/fr.txt',
                          welcome_message='Bonjour comment allez-vous?',
                          session='''
                          Leah visits Paris. Leah is an exchange student. Leah is from 
                          Germany.
                          Leah meets Bot. Bot lives in France. Leah and Bot are 13 years old.
                          Leah and Bot are best friends.
                          Leah and Bot plan a birthday party with friends. The party takes 
                          place next week on Saturday.
                          They plan the clothes they wear at the party.
                        
                          Bot: Hi Leah, how are you?
                          ''',
                          target_language='fr',
                          similarity_score=0.85)