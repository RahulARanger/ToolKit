import googletrans
import json
from tkinter.ttk import Combobox
import tkinter.scrolledtext as scrolledtext
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
from tkinter import *
from tkinter import *
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
import webbrowser
def Open(x):
	new=2
	url=x
	webbrowser.open(url,new=new)
class GTBackend:
    def __init__(self):
        self.lines=['']
        self.from_,self.to_=None,None
        self.detect=None
        self.translator=googletrans.Translator(service_urls=['translate.google.com','translate.google.co.kr',])
        self.c_from,self.c_to=None,None
        self.origin,self.translated,self.pronunciation=str(),str(),str()
        self.Languages=[] # has the list of the Languages
        self.LanCodes=None # has the language codes
        self.collect()
        self.FromLanguages=self.Languages[:]
        self.ToLanguages=self.Languages[:]
        self.trace=googletrans.LANGUAGES
        self.ToLanguages.remove('Detect Language')
    def collect(self):
        with open('dir\\root\\languages.json','r') as hand:
            self.LanCodes=json.loads(hand.read())
            for i in self.LanCodes['Languages']:
                self.Languages.append(i.title())    
            self.LanCodes=self.LanCodes['Languages']  
    def Detect(self,text):
        self.detect=False
        results=self.translator.detect(text)        
        detected=results.lang
        ans=self.trace[detected]
        conf=results.confidence
        return detected,ans
    def translation(self,text,from_='english',to_='japanese'):
        if len(text)==0:return '',''
        from_=from_.lower()
        to_=to_.lower()
        fromcode=self.LanCodes[from_]
        tocode=self.LanCodes[to_]            
        name=None
        try:
            if fromcode=='special':
                fromcode,name=self.Detect(text)
            else:
                fromcode,name=self.Detect(text)
            result=self.translator.translate(text,src=fromcode,dest=tocode)        
        except:
            return None
        try:
            pronunciation=result.pronunciation
        except:
            pronunciation=text
        return result.text,pronunciation,name    
class SearchBox(Frame):
    def __init__(self,parent,lst,var):
        super().__init__(parent)
        self.lst=lst
        self.var=var
        self.config(bg='#E6FFFB')
        self.var.trace('w',self.track)
        self.Search=Entry(self,text='',textvariable=self.var,width=20,font=('Arial',10),bg='#E6FFFB')
        self.Search.config(highlightthickness=3,highlightcolor='#3399FF',highlightbackground='#003333')
        self.HBar=Scrollbar(self,orient=VERTICAL)
        self.lstbox=Listbox(self,yscrollcommand=self.HBar.set,height=6,width=22,exportselection=0)
        self.HBar.config(command=self.lstbox.yview)
        self.lstbox.bind('<Double-Button-1>',self.selected)        
        self.Search.bind('<FocusIn>',self.appear)
        self.Search.bind('<Escape>',lambda cx:self.say())
        self.lstbox.bind('<Escape>',lambda cx:self.say())
        self.arrange()
    def say(self):
        self.HBar.pack_forget()
        self.lstbox.pack_forget()
        self.focus_force()
    def appear(self,*arrgfs):
        self.HBar.pack(fill=Y,side=RIGHT)
        print('Hello')
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
class InputBox(scrolledtext.ScrolledText):
    def __init__(self,parent,special=False):
        super().__init__(parent)
        if not special: self.config(font= ('consolas', '15'))
        self.config(width=50,height=10)        
        self.config(relief=SUNKEN)
        self.config(undo=True)
        self.config(autoseparators=True,maxundo=-1) # ? for unlocking the undo power
        self.config(borderwidth=6) # ? design matters
        self.config(wrap=WORD)
        self.bind('<Control-Z>',lambda x:self.redoit())        
        self.bind('<FocusIn>',self.change)
        self.bind('<FocusOut>',self.revert)        
        self.special=special  
        if self.special:                        
            self.config(state=DISABLED)       
            self.config(width=45,height=10)
            self.config(font= ('consolas', '16'))
        self.arrange()
    def redoit(self):
        try:
            self.edit_redo()
        except:pass
    def change(self,*args):
        self.config(relief=RAISED)
    def revert(self,*args):
        self.config(relief=SUNKEN)
    def arrange(self):
        pass
    def enter_text(self,text):
        self.config(state=NORMAL)
        self.insert(END,text)
        self.config(state=DISABLED)
    def get_it(self):
        return self.get('1.0',END)[:-1]
    def remove_text(self):
        self.config(state=NORMAL)
        self.delete('1.0',END)
        self.config(state=DISABLED)
class SpecialButton(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.backcolor=('orange','skyblue')
        self.textcolor=('white','black')
        self.config(text='Translate')
        self.config(width=10,height=2)
        self.config(relief=RIDGE)
        self.config(bg=self.backcolor[0],fg=self.textcolor[0])        
        self.bind('<Enter>',lambda c:self.bthover(True))
        self.bind('<Leave>',lambda c:self.bthover(False))
    def bthover(self,status):
        if status is True:
            self.config(bg=self.backcolor[1],fg=self.textcolor[1]) 
            self.config(relief=GROOVE)       
        else:
            self.config(relief=RIDGE)
            self.config(bg=self.backcolor[0],fg=self.textcolor[0])        
class GIFButton(ImageAlbum):
    def __init__(self,parent,photos):        
        super().__init__(parent,photos,200,200,100)
        self.backcolor=('#80D4FF','orange')
        self.config(bg=self.backcolor[0])
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Leave>',lambda x:self.bthover(False))
        self.bind('<Button-1>',lambda x:self.btpressed(True))
        self.bind('<ButtonRelease-1>',lambda x:self.btpressed(False))
    def bthover(self,status):
        if status:
            self.config(bg=self.backcolor[1])
            self.config(relief=RAISED)
        else:
            self.config(bg=self.backcolor[0])
            self.config(relief=FLAT)
    def btpressed(self,status):
        if status:
            self.config(relief=RAISED)
            Open('https://translate.google.co.in/')            
        else:
            self.config(relief=FLAT)
class GT(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='#80D4FF')
        self.MainFrame=Frame(self,bg='#80D4FF')
        self.TitleFrame=Frame(self.MainFrame,bg='#80D4FF')
        self.photos=['Resources\Media\Translator\Translator{}.jpg'.format(i) for i in range(20)]
        self.title=ImageAlbum(self.TitleFrame,self.photos,500,500,150,'#80D4FF')
        self.ContainFrame=Frame(self.MainFrame,bg='#E6FFFB')        
        self.SearchFrame=Frame(self.ContainFrame,bg='#80D4FF')
        self.GTBack=GTBackend()
        self.checker=NetworkCheck()
        self.DisplayFrame=Frame(self.ContainFrame,bg='#80D4FF')
        self.fs=StringVar()
        self.failed=False
        self.ts=StringVar()        
        self.fs.set('Detect Language')
        self.ts.set('Japanese')
        self.FromLabel=HoverLabel(self.SearchFrame,'From Language: ')
        self.ToLabel=HoverLabel(self.SearchFrame,'To Language: ')     
        self.FromBox=SearchBox(self.SearchFrame,self.GTBack.FromLanguages,self.fs)
        self.ToBox=SearchBox(self.SearchFrame,self.GTBack.ToLanguages,self.ts)
        self.From=InputBox(self.DisplayFrame)
        self.TranslateButt=SpecialButton(self.DisplayFrame)
        self.To=InputBox(self.DisplayFrame,True)
        self.photos2=['Resources\Media\Translator-Chan\TranslatorChan{}.jpg'.format(i) for i in range(11)]
        self.MoreFrame=Frame(self,bg='#80D4FF')
        self.TranslatorChan=GIFButton(self.MoreFrame,self.photos2)
        self.TranslateButt.bind('<Button-1>',self.TranslateThem)
        self.arrange()   
        self.after(600,self.checknet)           
    def TranslateThem(self,*args):
        text=self.From.get_it()        
        try:translated,pronunciation,setto=self.GTBack.translation(text,self.fs.get(),self.ts.get())
        except:return None
        if translated==False:
            return None
        self.To.remove_text()
        self.fs.set(setto.title())
        self.To.enter_text(translated)
        self.To.enter_text('\n\n'+pronunciation)
    def arrange(self):        
        self.MainFrame.pack(fill=X,expand=True)
        self.TitleFrame.pack(fill=X,expand=True)
        self.MoreFrame.pack(fill=X,expand=True)
        self.title.pack(pady=30)
        self.ContainFrame.pack(fill=X,expand=True)
        self.SearchFrame.pack(fill=X,expand=True)
        self.DisplayFrame.pack(fill=X,expand=True)
        self.FromLabel.pack(side=LEFT,expand=True)
        self.FromBox.pack(side=LEFT,padx=(100,),pady=3)
        self.ToBox.pack(side=RIGHT,padx=(100,),pady=3)
        self.ToLabel.pack(side=RIGHT,expand=True)
        self.From.pack(side=LEFT,expand=True)
        self.TranslateButt.pack(side=LEFT,expand=True)
        self.To.pack(side=RIGHT,expand=True)
        self.TranslatorChan.pack(side=RIGHT,padx=(0,50),pady=6)
    def checknet(self):
        if self.checker.MTest() is False:
            self.failed=True
            self.pack_forget()
        else:
            if self.failed:
                self.pack(fill=BOTH,expand=True)
                self.failed=False
        self.after(600,self.checknet)
if __name__=='__main__':
    root=Tk()
    a=GT(root)
    a.pack(fill=BOTH,expand=True)
    root.mainloop()

