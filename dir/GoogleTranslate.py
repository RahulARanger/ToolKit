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

class GT(Tk):
    def __init__(self):
        super().__init__()
        self.title('Translator')
        self.maxsize(700,700)
        self.minsize(500,500)
        self.balance()
        self.Translator=GTBackend()
        self.ToVar=StringVar()
        self.FromVar=StringVar()
        self.backg=Frame(self)
        self.titlegif=Frame(self.backg)
        self.selectframe=Frame(self.backg)
        self.selectlang=Frame(self.backg)
        self.boxframe=Frame(self.backg,bg='#B3F2FF')
        self.fromselect=Combobox(self.selectframe)
        self.toselect=Combobox(self.selectframe)
        self.emptyshell=Frame(self.backg,bg='#CCF7FF',height=40)
        self.To=Text(self.boxframe,width=35,height=15)
        self.From=Text(self.boxframe,width=35,height=15)
        self.TranslateB=Button(self.selectframe,text='Translate',relief=FLAT)
        self.TTitle=AnimatedGif(self.titlegif,'Resources\Media\Translator.gif',0.04)
        self.arrange()
    def balance(self):
        x=int((self.winfo_screenwidth()-600)/2)
        y=int((self.winfo_screenheight()-600)/2)
        self.geometry('{}x{}+{}+{}'.format(600,600,x,y))
    def arrange(self):
        self.FromVar.set('Select to Enter the text:')
        self.ToVar.set('Displayed Here')
        self.titlegif.config(bg='#131415')
        self.backg.config(bg='#99EEFF')
        self.backg.pack(expand=True,fill=BOTH)
        self.titlegif.pack(fill=X)
        self.emptyshell.pack(fill=X)
        self.selectlang.pack(fill=X)
        self.selectlang.config(bg='#CCF7FF')
        self.selectframe.pack(fill=X)
        self.selectframe.config(bg='#009999')
        self.boxframe.pack(fill=X)
        
        self.TTitle.pack(anchor='n',side=LEFT,padx=50,expand=True)
        self.TTitle.start()
        self.selectlanguages=Label(self.selectlang,text='Select Any Languages: ')
        self.selectlanguages.pack(anchor='nw',padx=10,pady=10,side=LEFT)

        self.fromselect.config(values=self.Translator.Languages)
        self.fromselect.pack(anchor='nw',padx=10,pady=10,side=LEFT)
        self.TranslateB.pack(anchor='n',padx=100,pady=10,side=LEFT)
        self.toselect.config(values=self.Translator.Languages)
        self.toselect.pack(anchor='ne',padx=10,pady=10,side=RIGHT)
        
        self.To.pack(anchor='ne',padx=10,pady=10,side=RIGHT)
        
        self.From.pack(anchor='nw',padx=10,pady=10,side=LEFT)
if __name__=='__main__':
    GT().mainloop()