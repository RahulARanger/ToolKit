import json
with open('Raw Modules\Google Translate API\languages.json','r') as hand:
    a=json.loads(hand.read())
    # TODO: Displays all languages
    print(a['Languages'])
    # TODO: Code for the particular Language
    print(a['Languages']['japanese'])