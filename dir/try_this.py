import googletrans
class GT:
    def __init__(self):
        while True:
            self.translator=googletrans.Translator(service_urls=['translate.google.com'])
            try:
                trial=self.translator.detect('Hello there')
                break
            except Exception as e:
                print(e)   # can be commented
    def doThings(self):
        pass
if __name__=='__main__':
    a=GT()
    