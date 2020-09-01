import string

class Select:
    def __init__(self,text):
        self.text=text
        self.case_changes()
        self.details()
    def case_changes(self):
        self.to_upper=self.text.upper()
        self.to_lower=self.text.lower()
        self.to_cap=self.text.capitalize()
        self.to_swap=self.text.swapcase()
        self.to_title=self.text.title()
    def details(self):
        self.length=len(self.text)
        self.letters=0
        self.numbers=0
        for i in self.text:
            if i in string.ascii_letters:
                self.letters+=1
            elif i in string.ascii_letters:
                self.numbers+=1
        self.wordlen=len(self.text.split())
if __name__=='__main__':
    a=Select('Dark Flame Master!!!')
    print(a.to_upper) 
    print(a.to_lower)
    print(a.to_cap)
    print(a.to_swap)
    print(a.to_title)
    print(a.wordlen)
    print(a.length)
    print(a.letters)