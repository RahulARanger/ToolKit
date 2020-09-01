import googletrans
class GT:
    def __init__(self):
        self.lines=['']
        self.from_,self.to_=None,None
        self.origin,self.translated,self.pronunciation=str(),str(),str()
    def get_Input(self,file_import=None,text=None):
        if file_import is not None:
            try:
                hand=open(file_import,'r')
                text=hand.read()
                hand.close()
            except:
                # ? For GUI use a dialog box here
                print('Selected File is Not Supported For now..')
                return False
        self.lines=text.split('\n')
    def translate(self,from_='en',to_='ja'):
        translator=googletrans.Translator()
        self.from_,self.to_=from_,to_
        for i in self.lines:
            result=translator.translate(i,src=from_,dest=to_)
            self.origin+=result.origin+'\n'
            self.pronunciation+=result.pronunciation+'\n'
            self.translated+=result.text+'\n'
    def export(self):
        # TODO: Script inside this method is used to design the output text file
        # ? use save as filedialog to save the exported file
        # * Raw Modules\Google Translate API\test2.txt
        filename=input('Enter the File Name: ')
        
        hand=open(filename,'wb')
        hand.write('{} Text: \n'.format(self.from_).encode())
        check=len('{} Text:'.format(self.from_))
        hand.write('{}\n\n'.format('═'*check).encode())
        hand.write(self.origin.encode())
        hand.write('\n'.encode())
        
        hand.write('Translated to: {} \n'.format(self.to_).encode())
        check=len('Translated to: {}'.format(self.to_))
        hand.write('{}\n\n'.format('═'*check).encode())
        hand.write(self.translated.encode())
        hand.write('\n'.encode())
        
        hand.write('Pronunciation for the {} text is: \n'.format(self.to_).encode())
        check=len('Pronunciation for the {} text is:'.format(self.to_))
        hand.write('{}\n\n'.format('═'*check).encode())
        hand.write(self.pronunciation.encode())
        hand.write('\n'.encode())
        hand.close()
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
    test.export()