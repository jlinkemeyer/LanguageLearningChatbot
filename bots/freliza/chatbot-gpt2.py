from happytransformer import HappyGeneration, GENSettings
import transformers

happy_gen = HappyGeneration("GPT2", "gpt2-xl")  # Best performance
args = GENSettings(max_length=55, early_stopping=True, do_sample=True, top_k=80)  # for more options, see https://happytransformer.com/text-generation/settings/
transformers.logging.set_verbosity_error()

conversation_sofar = """
Leah visits Barcelona as an exchange student. She meets Bot. Both are 13 years old. They plan a picnic with a group of friends.
Bot likes to eat patatas bravas and choco frito, but dislikes eating caracoles.
Bot is going to bring Tortilla de jamon y queso and horchata to the picnic.

They still have to decide for other food. The picnic takes place at 3pm in a park. 

Bot: Hi Leah, how are you?
"""

bot_turn = True

for i in range(12):
    result = happy_gen.generate_text(conversation_sofar, args=args)
    lines = result.text.split("\n")
    prefix = 'Bot:' if bot_turn else 'Leah:'
    for l in lines:
        if l.startswith(prefix):
            answer = l
            break
    else:
        continue

    # clip away any Bot: or Jim: later in the answer
    try:
        bidx = answer.index('Bot:', 4)
        if bidx > 0:
            answer = answer[:bidx]
    except ValueError:
        pass
    try:
        bidx = answer.index('Leah:', 4)
        if bidx > 0:
            answer = answer[:bidx]
    except ValueError:
        pass

    # add answer to conversation and go on
    print(answer)
    conversation_sofar += answer+"\n"
    bot_turn = not bot_turn

print("COMPLETE: \n\n")
print(conversation_sofar)
