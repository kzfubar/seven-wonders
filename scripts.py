import json


def give_effect(c, name, effect):
    if c['type'] == name:
        if c.get('effect') is None:
            e = {}
            e['effect'] = effect
            e['resources'] = c['resources']
            e['target'] = []
            e['direction'] = ['self']
            c['effects'] = [e]
            del (c['resources'])


def give_effects():
    with open("cards.json") as f:
        cards = json.load(f)

    for card in cards:
        give_effect(card, 'common', 'produce')
        give_effect(card, 'luxury', 'produce')
        give_effect(card, 'military', 'strength')
        give_effect(card, 'civilian', 'victory')
        # tmp(card, 'commercial') ignore commercial b/c wacky-doodle
        give_effect(card, 'science', 'produce')

    with open('cards.json', 'w') as f:
        json.dump(cards, f, indent=2)


def tmp(c):
    if c.get('effect') is not None:
        c_effect = c.get('effect')
        effects = []
        for i, effect in enumerate(c_effect):
            d = {}
            d["effect"] = c_effect[i]
            if c['name'] == "Scientists Guild":
                d["resources"] = c['resources']
            elif len(c['resources']) > 0:
                d["resources"] = [c['resources'][i]]
            else:
                d["resources"] = []
            d["target"] = c['target']
            d["direction"] = c['direction']
            effects.append(d)
        c['effects'] = effects

        del (c['target'])
        del (c['effect'])
        del (c['direction'])
        del (c['resources'])


def effect_to_effects():
    with open("cards.json") as f:
        cards = json.load(f)

    for card in cards:
        tmp(card)

    with open('cards.json', 'w') as f:
        json.dump(cards, f, indent=2)


def modify(c):
    if c.get('effects') is None:
        print(c)
        return

    for e in c['effects']:
        if e['effect'] == "produce" or e['effect'] == "discount":
            continue

        if e['effect'] == "levy":
            e['resources'] = ["c" * e['resources'][0]]
            e['effect'] = "generate"

        if e['effect'] == "strength":
            e['resources'] = ["m" * e['resources'][0]]
            e['effect'] = "generate"

        if e['effect'] == "victory":
            e['resources'] = ["v" * e['resources'][0]]
        print(e)


def modify_effects():
    with open("cards.json") as f:
        cards = json.load(f)

    for card in cards:
        modify(card)

    with open('cards.json', 'w') as f:
        json.dump(cards, f, indent=2)


def to_tuple(resource_raw):
    return resource_raw[0], len(resource_raw)


def tuplify():
    with open("cards.json") as f:
        cards = json.load(f)

    for card in cards:
        r = []
        for effect in card['effects']:
            for resource in effect['resources']:
                print(to_tuple(resource))
                r.append(to_tuple(resource))
            effect['resources'] = r

    with open('cards.json', 'w') as f:
        json.dump(cards, f, indent=2)


# effect_to_effects()
# give_effects()
# modify_effects()

tuplify()
