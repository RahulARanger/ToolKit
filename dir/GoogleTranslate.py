import googletrans
import json
from tkinter.ttk import Combobox
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
from tkinter import *
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
class SearchBox(Frame):
    def __init__(self,parent,lst):
        super().__init__(parent)
        self.lst=lst
        self.var=StringVar()
        self.config(bg='#E6FFFB')
        self.var.trace('w',self.track)
        self.Search=Entry(self,text='',textvariable=self.var,width=20,font=('Arial',10),bg='#E6FFFB')
        self.Search.config(highlightthickness=3,highlightcolor='#3399FF',highlightbackground='#003333')
        self.HBar=Scrollbar(self,orient=VERTICAL)
        self.lstbox=Listbox(self,yscrollcommand=self.HBar.set,height=6,width=22,exportselection=0)
        self.HBar.config(command=self.lstbox.yview)
        self.lstbox.bind('<Double-Button-1>',self.selected)
        self.Search.bind('<FocusIn>',self.appear)
        self.arrange()
    def appear(self,*arrgfs):
        self.HBar.pack(fill=Y,side=RIGHT)
        self.lstbox.pack(side=LEFT,padx=(1,0))
    def track(self,*args):
        text=self.var.get()
        store=self.lstbox.get(0,END)
        for i in range(len(store)):
            self.lstbox.delete(0)
        if len(text)==0:
            for i in self.lst:
                self.lstbox.insert(END,i)
        else:
            for i in self.lst:
                if text in i:
                    self.lstbox.insert(END,i)       
    def arrange(self):
        self.Search.pack()
        for i in self.lst:
            self.lstbox.insert(END,i)
    def selected(self,*args):
        self.var.set(self.lstbox.get(ACTIVE))
        self.HBar.pack_forget()
        self.lstbox.pack_forget()
class HoverLabel(Label):
    def __init__(self,parent,text_):
        super().__init__(parent)
        self.config(text=text_)
        self.config(font=('Helvetica',16,'bold','underline'))
        self.backcolor=('#E6FFFB','#FF8000')
        self.textcolor=('#000000','#FFFFFF')
        self.config(bg=self.backcolor[0],fg=self.textcolor[0])
        self.bind('<Enter>',lambda x: self.bthover(True))
        self.bind('<Leave>',lambda x: self.bthover(False))
    def bthover(self,status):        
        if status:            
            self.config(bg=self.backcolor[1],fg=self.textcolor[1],relief=RAISED)
        else:
            self.config(bg=self.backcolor[0],fg=self.textcolor[0],relief=FLAT)
class GT(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='#E6FFFB')
        self.IFrame=Frame(self,bg='#E6FFFB')
        self.SeFrame=Frame(self,bg='#E6FFFB')
        self.FromLabel=HoverLabel(self.IFrame,'From Language: ')
        self.ToLabel=HoverLabel(self.IFrame,'To Language: ')     
        self.ToBox=None
        self.TBack=GTBackend()
        self.Languages=self.TBack.Languages
        self.FromBox=SearchBox(self.SeFrame,self.Languages)
        self.ToBox=SearchBox(self.SeFrame,self.Languages)
        self.arrange()
    def arrange(self):
        self.IFrame.pack(fill=X,expand=True)
        self.FromLabel.pack(side=LEFT,padx=15)
        self.ToLabel.pack(side=RIGHT,padx=60)
        self.SeFrame.pack(fill=X,expand=True,pady=10)
        self.FromBox.pack(side=LEFT,padx=60)
        self.ToBox.pack(side=RIGHT,padx=15)
if __name__=='__main__':
    root=Tk()
    a=GT(root)
    a.pack(fill=BOTH,expand=True)
    root.mainloop()