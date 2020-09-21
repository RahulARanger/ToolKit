import urllib.request
class NetworkCheck:
    def __init__(self):
        self.link='https://www.google.co.in/'
        self.result=None
        self.test()
    def test(self):
        try:
            urllib.request.urlopen(self.link)
            self.result=True
        except:
            self.result=False
    def MTest(self):
        try:
            urllib.request.urlopen(self.link)
            return True
        except:
            return False