import nltk
# nltk.download()
from googletrans import Translator
from pattern.es import pluralize, parse

translator = Translator()
text_es = """grabar
gracias
grande
gripe
gris
guapo
guardar
guerra
gustar
gusto
guía
haber
habitación
hablar
hacer
hamburguesa
hasta
helado
hermana
hermano
hija
hijo
hijos
historia
histórico
hombre
hora
horario
hospital
hotel
hoy
huevo
huracán
idea
idioma
iglesia
igualdad
imagen
impaciente
importante
ingeniero
inglés
insistir
inteligente
interesante
investigar
invierno
invitar
ir
irse
jabón
jamón
jardín
jefe
joven
joyería
juego
jueves
jugador
jugar
julio
junio
justo
la
lago
largo
las
lata
lavadora
lavar
leche
lechuga
leer
legal
lejos
lento
levantarse
libertad
libre
librería
libro
lima
limpiar
limpio
limón
lista
listo
literatura"""
# text_en = translator.translate(text_es, src='es', dest='en').text
# tokenized = nltk.word_tokenize(text_en)
# print(nltk.pos_tag(tokenized))
tokenized = nltk.word_tokenize(text_es)
for token in tokenized:
    print(token)
    try:
        print(parse(token))
        parsed = parse(token).split('/')
        if parsed[1] == 'NN':
            print(pluralize(token))
    except:
        continue