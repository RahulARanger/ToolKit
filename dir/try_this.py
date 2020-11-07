store=[]
with open('dir\\root\\Translate.lang','rb') as hand:
    lines=hand.readlines()
    for i in lines:
        store.append(i.decode()[:-1])
print(store)