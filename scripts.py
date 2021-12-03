import json


def tmp(c, name, effect):
    if c['type'] == name:
        if c.get('effect') is None:
            c['effect'] = effect
            c['target'] = []
            c['direction'] = ['self']


with open("cards.json") as f:
    cards = json.load(f)


for card in cards:
    tmp(card, 'common', 'produce')
    tmp(card, 'luxury', 'produce')
    tmp(card, 'military', 'strength')
    tmp(card, 'civilian', 'victory')
    # tmp(card, 'commercial') ignore commercial b/c wacky-doodle
    tmp(card, 'science', 'produce')

with open('cards.json', 'w') as f:
    json.dump(cards, f, indent=2)



