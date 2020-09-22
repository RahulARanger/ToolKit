import googletrans
import json
from tkinter.ttk import Combobox
try:
    from root.animatedgif import * # When executed from this file
except:
    from dir.root.animatedgif import *
from tkinter import *
class GTBackend:
    def __init__(self):
        self.lines=['']
        self.from_,self.to_=None,None
        self.c_from,self.c_to=None,None
        self.origin,self.translated,self.pronunciation=str(),str(),str()
        self.Languages=[]
        self.collect()
    def collect(self):
        with open('Raw Modules\Google Translate API\languages.json','r') as hand:
            lan=json.loads(hand.read())
            for i in lan['Languages']:
                self.Languages.append(i.title())
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
    def translate(self,from_='english',to_='japanese'):
        from_=from_.lower()
        to_=to_.lower()
        with open('Raw Modules\Google Translate API\languages.json','r') as hand:
            lan=json.loads(hand.read())
        self.c_from=lan['Languages'][from_]
        self.c_to=lan['Languages'][to_]
        translator=googletrans.Translator()
        self.from_,self.to_=from_,to_
        for i in self.lines:
            result=translator.translate(i,src=self.c_from,dest=self.c_to)
            self.origin+=result.origin+'\n'
            try:
                self.pronunciation+=result.pronunciation+'\n'
            except:
                self.pronunciation+=result.origin+'\n'
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

class GT(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(height=300)
        self.TFrame=Frame(self)
        self.TFrame['bg']='#84bbf8'
        self.TGif=AnimatedGif(self.TFrame,'Resources\Media\Translator.gif')
        
        self.arrange()
    def arrange(self):
        self.TFrame.pack(fill=X)
        self.TGif.pack(anchor='n')
        self.TGif.start()

if __name__=='__main__':
    root=Tk()
    a=GT(root)
    a.pack(fill=X)
    root.mainloop()