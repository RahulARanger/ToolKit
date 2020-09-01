import googletrans
class GT:
    def __init__(self):
        self.lines=['']
        self.origin,self.translated,self.pronunciation=str(),str(),str()
    def get_Input(self,file_import=None,text=None):
        if file_import is not None:
            try:
                hand=open(file_import,'r')
                text=hand.read()
            except:
                # ? For GUI use a dialog box here
                print('Selected File is Not Supported For now..')
                return False
        self.lines=text.split('\n')
    def translate(self,from_='en',to_='ja'):
        translator=googletrans.Translator()
        for i in self.lines:
            result=translator.translate(i,src=from_,dest=to_)
            self.origin+=result.origin+'\n'
            self.pronunciation+=result.pronunciation+'\n'
            self.translated+=result.text+'\n'

if __name__=='__main__':
    test=GT()
    test.get_Input(text='Hello there\n How Are You?')
    # !from_=input('Enter the Language Code:')
    # !to_=input('Enter the Language Code:')
    # TODO: add a search bar and drop down list to choose languages
    test.translate(to_='ja')
    # TODO: Label
    print(test.origin)
    # TODO: Label
    print(test.translated)
    # TODO: Label
    print(test.pronunciation)
    # ? using file upload menu in GUI
    test=GT()
    test.get_Input(file_import=input('Enter the File Path: '))
    test.translate()
    # TODO: Label
    print(test.origin)
    # TODO: Label
    print(test.translated)
    # TODO: Label
    print(test.pronunciation)