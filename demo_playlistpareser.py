import json
with open('playlists.json','r') as hand:
    a=json.loads(hand.read())
    for i in a:
        print(i,a[i])