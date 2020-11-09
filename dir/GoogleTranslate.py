import googletrans
import json
from tkinter import font
import threading
import tkinter.scrolledtext as scrolledtext
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
try:
    from root.Dialogs import *
except:
    from dir.root.Dialogs import *
from tkinter import *
from tkinter import *
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
try:
    from dir.root.OpenLink import *
except:
    from root.OpenLink import *
try:
    from dir.root.LogFiles import *
except:
    from root.LogFiles import *
class GTBackend:
    def __init__(self,parent):
        self.lines=['']
        self.from_,self.to_=None,None
        self.detect=None
        self.parent=parent
        beta=threading.Thread(target=self.getThingsReady)
        beta.start()
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
    def getThingsReady(self):
        #print('doing')
        zawardu=Loading(self.parent)
        while True:
            self.translator=googletrans.Translator(service_urls=['translate.google.com'])
            try:
                trial=self.translator.detect('Hello there')
                break
            except Exception as e:
                #print(e)
                pass    
        zawardu.stopIt()
        #print('done')
    def Detect(self,text):
        self.detect=False
        for i in range(6):
            try:
                results=self.translator.detect(text)
                detected=results.lang
                ans=self.trace[detected]
                return detected,ans
            except Exception as e:
                #print(e)
                pass
        return None
    def translation(self,text,from_='english',to_='japanese'):
        if len(text)==0:return False,'',from_
        from_=from_.lower()
        to_=to_.lower()
        fromcode=self.LanCodes[from_]
        tocode=self.LanCodes[to_]            
        name=None
        if fromcode=='special':
            try:
                fromcode,name=self.Detect(text)
            except:
                return False,'',from_
        else:
            fromcode,name=self.Detect(text)
        result=self.translator.translate(text,src=fromcode,dest=tocode)    
        try:
            pronunciation=result.pronunciation
            if type(pronunciation)!=str:pronunciation=''
        except:
            pronunciation=text
        return result.text,pronunciation,name    
class SearchBox(Frame):
    def __init__(self,parent,lst,var,status):
        super().__init__(parent)
        self.lst=lst
        self.var=var
        self.status=status
        self.config(bg='#7DF6FF')
        self.var.trace('w',self.track)
        self.Search=Entry(self,text='',textvariable=self.var,font=('Arial',10),bg='#E6FFFB')
        self.DummyFrame=Frame(self)
        self.Search.config(highlightthickness=2,highlightcolor='#3399FF',highlightbackground='#003333',relief=RAISED)
        self.HBar=Scrollbar(self.DummyFrame,orient=VERTICAL)
        self.lstbox=Listbox(self.DummyFrame,yscrollcommand=self.HBar.set,height=6,width=22,exportselection=0,bg='#E6FFFB',selectbackground='orange',highlightthickness=2,highlightcolor='#3399FF',highlightbackground='#003333',setgrid=1,relief=RAISED)
        self.HBar.config(command=self.lstbox.yview)
        self.lstbox.bind('<Double-Button-1>',self.selected)        
        self.Search.bind('<Enter>',lambda x:self.hoverEntry(True))
        self.Search.bind('<Leave>',lambda x:self.hoverEntry(False))
        self.lstbox.bind('<Enter>',lambda x:self.hoverbox(True))
        self.lstbox.bind('<Leave>',lambda x:self.hoverbox(False))
        self.arrange()
    def hoverEntry(self,status):
        if status:
            self.Search.config(relief=RIDGE,highlightbackground='#3399FF')
            self.status.set('Type to Search')
        else:
            self.Search.config(relief=RAISED,highlightbackground='#003333')
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def hoverbox(self,status):
        if status:
            self.lstbox.config(relief=RIDGE,highlightbackground='#3399FF')
            self.status.set('Double Click on any to select')
        else:
            self.lstbox.config(relief=RAISED,highlightbackground='#003333')
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def track(self,*args):
        text=self.var.get().title()
        for i in range(len(self.lstbox.get(0,END))):
            self.lstbox.delete(0)
        if len(text)==0:
            for i in self.lst:
                self.lstbox.insert(END,i)
        else:
            for i in self.lst:
                if text in i:
                    self.lstbox.insert(END,i)       
    def arrange(self):
        self.Search.pack(fill=X,expand=True)
        self.DummyFrame.pack(fill=BOTH,expand=True)
        for i in self.lst:
            self.lstbox.insert(END,i)
        self.HBar.pack(fill=Y,side=RIGHT,expand=True)
        self.lstbox.pack(fill=BOTH,side=LEFT,expand=True)
    def selected(self,*args):
        self.var.set(self.lstbox.get(ACTIVE))
class HoverLabel(Label):
    def __init__(self,parent,text_,status):
        super().__init__(parent)
        self.config(text=text_)
        self.status=status
        self.config(font=('Helvetica',16,'bold','underline'),highlightthickness=3,highlightcolor='#3399FF')
        self.backcolor=('#E6FFFB','#FF8000')
        self.textcolor=('#000000','#FFFFFF')
        self.config(bg=self.backcolor[0],fg=self.textcolor[0])
        self.bind('<Enter>',lambda x: self.bthover(True))
        self.bind('<Leave>',lambda x: self.bthover(False))
    def bthover(self,status):        
        if status:            
            self.config(bg=self.backcolor[1],fg=self.textcolor[1],relief=RAISED,highlightthickness=6,highlightbackground='#3399FF')
            self.status.set(self['text'])
        else:
            self.config(bg=self.backcolor[0],fg=self.textcolor[0],relief=FLAT,highlightthickness=3,highlightcolor='#3399FF')
            self.status.set('ZzZzZzzZzzZZzzZZ')
class InputBox(scrolledtext.ScrolledText):
    def __init__(self,parent,special,status):
        super().__init__(parent)
        if not special: self.config(font= ('consolas', '15'))
        self.config(width=50,height=10)        
        self.config(undo=True)
        self.status=status
        self.config(autoseparators=True,maxundo=-1) # ? for unlocking the undo power
        self.config(borderwidth=6) # ? design matters
        self.config(wrap=WORD)
        self.bind('<Control-Z>',lambda x:self.redoit())        
        self.bind('<FocusIn>',self.change)
        self.bind('<FocusOut>',self.revert)     
        self.bind('<Enter>',lambda x:self.boxhover(True))
        self.bind('<Leave>',lambda x:self.boxhover(False))
        self.config(relief=RAISED)   
        self.special=special  
        if self.special:                        
            self.config(state=DISABLED)  
            self.config(width=45,height=10)
            self.config(font= ('consolas', '16'))
        self.arrange()
    def boxhover(self,status):
        if status:
            self.status.set('Display box')
            self.config(relief=GROOVE)
        else:
            self.config(relief=RAISED)
            self.status.set('ZZzZzZZZZZZzzz')
    def redoit(self):
        try:
            self.edit_redo()
        except:pass
    def change(self,*args):
        self.config(relief=RAISED)
    def revert(self,*args):
        self.config(relief=SUNKEN)
    def arrange(self):
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        try:
            result = self.tk.call(cmd)
        except:
            result=None
        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")
        return result
    def enter_text(self,text,status):
        self.config(state=NORMAL)
        #print('*',text,'->',status)
        if status is False:
            self.markindex=self.index(END)
        self.insert(END,text)
        if status:
            pass
        else:
            self.tag_add('Pronunciation',self.markindex,END)
            self.tag_configure('Pronunciation',foreground='orange')
            self.markindex=None
        self.config(state=DISABLED)
    def get_it(self):
        return self.get('1.0',END)[:-1]
    def remove_text(self):
        self.config(state=NORMAL)
        self.delete('1.0',END)
        self.config(state=DISABLED)
class SpecialButton(Label):
    def __init__(self,parent,status):
        super().__init__(parent)
        self.status=status
        self.backcolor=('orange','yellow')
        self.textcolor=('white','black')
        self.config(text='Translate')
        self.config(width=10,height=2)
        self.config(relief=FLAT)
        self.store=[]
        self.index=0
        with open('dir\\root\\Translate.lang','rb') as hand:
            lines=hand.readlines()
            for i in lines:
                self.store.append(i.decode()[:-1])
        self.note=len(self.store)
        self.config(bg=self.backcolor[0],fg=self.textcolor[0],font=('Comic Sans MS', 12))        
        self.bind('<Enter>',lambda c:self.bthover(True))
        self.bind('<Leave>',lambda c:self.bthover(False))
        self.config(text=self.store[self.index])
        self.after(1000,self.change)
    def change(self):
        self.index+=1
        if self.index>=self.note:
            self.index=0
        self.config(text=self.store[self.index])
        self.after(1000,self.change)
    def bthover(self,status):
        if status is True:
            self.config(bg=self.backcolor[1],fg=self.textcolor[1]) 
            self.status.set('Translate it?')
        else:
            self.config(bg=self.backcolor[0],fg=self.textcolor[0])           
            self.status.set('ZzZzZzzZzzZZzzZZ')   
class Status(Text):
    def __init__(self,parent,status):
        super().__init__(parent)
        self.config(bg='#006655')
        self.status=status
        self.config(relief=RAISED,state=DISABLED,highlightthickness=0,highlightbackground='#3399FF')
        self.config(width=70,height=11)   
        self.typed=0
        self.TitleFont=("Times", "24", "bold italic",True) 
        self.TitleFont=font.Font(family='Times',size='24',underline=True,weight='bold',slant='italic')
        self.NormalFont=("Verdana 10 bold")
        self.translated=0
        self.config(state=NORMAL)
        self.CurrentLog='''        
            Current Log
        
    Number of Characters Typed: {}

    Translated: {}

    Number of Characters in the Translation: {}
        '''.format(self.typed,'NO',self.translated)  
        self.insert(END,self.CurrentLog)  
        self.tag_add('title','2.0 linestart','2.0 lineend')
        self.tag_add('Line1','4.0 linestart','4.0 lineend')
        self.tag_add('Line2','6.0 linestart','6.0 lineend')
        self.tag_add('Line3','8.0 linestart','8.0 lineend')
        self.tag_configure('title',foreground='white',font=self.TitleFont)
        self.tag_configure('Line1',foreground='#FFE6CC',font=self.NormalFont)
        self.tag_configure('Line2',foreground='#FFE6CC',font=self.NormalFont)
        self.tag_configure('Line3',foreground='#FFE6CC',font=self.NormalFont)
        self.config(state=DISABLED)
        self.bind('<Enter>',lambda x:self.hoverbox(True))
        self.bind('<Leave>',lambda x:self.hoverbox(False))
    def hoverbox(self,status):
        if status:
            self.config(relief=RIDGE,highlightthickness=2,highlightbackground='#3399FF')
            self.status.set('Log box')
        else:
            self.config(relief=RAISED,highlightthickness=0,highlightbackground='#3399FF')
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def enter_text(self,text,status,frm='',to=''):
        if frm!='':
            update='( '+frm+' ➜ '+to+' )'
        else:update=''
        self.config(state=NORMAL)
        if status:
            self.typed=len(text)
        else:
            self.translated=len(text)
        self.CurrentLog='''        
            Log {}
        
    Number of Characters Typed: {}

    Translated: {}

    Number of Characters in the Translation: {}
        '''.format(update,self.typed,'NO' if status else 'YES',self.translated)    
        self.delete('1.0',END)
        self.insert(END,self.CurrentLog)
        self.tag_add('title','2.0 linestart','2.0 lineend')
        self.tag_add('Line1','4.0 linestart','4.0 lineend')
        self.tag_add('Line2','6.0 linestart','6.0 lineend')
        self.tag_add('Line3','8.0 linestart','8.0 lineend')
        self.tag_configure('title',foreground='white',font=self.TitleFont)
        self.tag_configure('Line1',foreground='#FFE6CC',font=self.NormalFont)
        self.tag_configure('Line2',foreground='#FFE6CC',font=self.NormalFont)
        self.tag_configure('Line3',foreground='#FFE6CC',font=self.NormalFont)
        self.config(state=DISABLED)    
    def save(self):
        # ! create a function that saves the logs into a log file
        pass
class GT(Frame):
    def __init__(self,parent,status):
        super().__init__(parent)
        self.config(bg='#80D4FF',relief=RAISED,borderwidth=6)
        self.status=status
        self.parent=parent
        self.checker=NetworkCheck()
        self.failed=False
        self.packed=False
        self.checknet()
    def reviveThis(self):
        self.packed=True
        self.GTBack=GTBackend(self.parent)
        self.ContainFrame=Frame(self,bg='#7DF6FF',relief=GROOVE,borderwidth=3)        
        self.MoreFrame=Frame(self,bg='#7DF6FF',relief=GROOVE,borderwidth=3)
        self.SearchFrame=Frame(self.ContainFrame,bg='#7DF6FF')
        self.DisplayFrame=Frame(self.ContainFrame,bg='#7DF6FF')
        self.fs=StringVar()
        self.ts=StringVar()        
        self.fs.set('Detect Language')
        self.ts.set('Japanese')
        self.FromLabel=HoverLabel(self.SearchFrame,'From Language: ',self.status)
        self.ToLabel=HoverLabel(self.SearchFrame,'To Language: ',self.status)     
        self.FromBox=SearchBox(self.SearchFrame,self.GTBack.FromLanguages,self.fs,self.status)
        self.ToBox=SearchBox(self.SearchFrame,self.GTBack.ToLanguages,self.ts,self.status)
        self.bind('<Button-1>',lambda cx:self.cleanit())
        self.From=InputBox(self.DisplayFrame,False,self.status)
        self.toggle=None
        self.TranslateButt=SpecialButton(self.DisplayFrame,self.status)
        self.To=InputBox(self.DisplayFrame,True,self.status)
        self.photos2=['Resources\Media\Translator-Chan\TranslatorChan{}.jpg'.format(i) for i in range(11)]                
        self.onHoldFrame=Frame(self.MoreFrame,bg='#7DF6FF')
        self.StatusBar=Status(self.onHoldFrame,self.status)
        self.TranslatorChan=ButtonAlbum(self.onHoldFrame,self.photos2,300,300,'#7DF6FF')
        self.TranslatorChan.bind('<ButtonRelease-1>',lambda x:Open('https://translate.google.co.in/'))
        self.From.bind("<<TextModified>>", lambda x:self.StatusBar.enter_text(self.From.get_it(),True))
        self.TranslatorChan.bind('<Enter>',lambda x:self.HoverChan(True))
        self.TranslatorChan.bind('<Leave>',lambda x:self.HoverChan(False))
        self.TranslateButt.bind('<ButtonRelease-1>',self.TranslateThem)
        self.TranslateButt.bind('<Button-1>',lambda c:self.TranslateButt.config(relief=RAISED))
        self.arrange()   
        self.after(3000,self.checknet)  
    def HoverChan(self,status):
        if status:
            self.TranslatorChan.config(relief=RAISED,borderwidth=6)
            self.status.set('Redirects to https://translate.google.co.in/')
        else:
            self.TranslatorChan.config(relief=FLAT,borderwidth=0)
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def TranslatorThread(self):
        text=self.From.get_it()   
        self.TranslateButt.config(relief=FLAT)
        if len(text)==0:
            self.stop=True
            self.status.set('ZzZzZzzZzzZZzzZZ')
            return
        try:
            translated,pronounciation,setto=self.GTBack.translation(text,self.fs.get(),self.ts.get())
            #print(translated,'}')
            #print(pronounciation)
        except:
            self.stop=True
            return None
        if translated==False:
            self.stop=True
            return None
        # TODO: need to add the waiting or translating thing here
        self.after(500)
        self.To.remove_text()
        self.fs.set(setto.title())
        self.To.enter_text(translated,True)
        self.StatusBar.enter_text(translated,False,self.fs.get(),self.ts.get())
        self.To.enter_text('\n\n'+pronounciation,False)
        self.stop=True
        self.status.set('ZzZzZzzZzzZZzzZZ')
    def TranslateThem(self,*args):
        self.after(10)
        if True:
            self.stop=False
            self.after(10,self.StartTranslating)
            self.alpha=Loading(self)
            #print('Clicked')
            omega=threading.Thread(target=self.TranslatorThread)
            omega.start()
    def StartTranslating(self):
        if self.stop:
            self.alpha.stopIt()
            #print('over')
            return
        if self.toggle:self.status.set('Translating.../...')
        else:self.status.set('Translating...\...')
        self.toggle=not(self.toggle)
        self.after(600,self.StartTranslating)
    def arrange(self):        
        self.ContainFrame.pack(fill=X,side=TOP)
        self.MoreFrame.pack(fill=X,expand=True,ipady=50,side=BOTTOM)
        self.SearchFrame.pack(fill=X)
        self.DisplayFrame.pack(fill=X)
        self.FromLabel.pack(side=LEFT,expand=True,ipady=10,padx=(0,30))
        self.FromBox.pack(side=LEFT,pady=(4,))
        self.ToBox.pack(side=RIGHT,padx=(100,),pady=(6,))
        self.ToLabel.pack(side=RIGHT,expand=True,ipady=10,padx=(270,0))
        self.From.pack(side=LEFT,expand=True)
        self.TranslateButt.pack(side=LEFT,expand=True)
        self.To.pack(side=RIGHT,expand=True)
        self.onHoldFrame.pack(side=TOP,fill=BOTH,pady=6)
        self.StatusBar.pack(side=LEFT,padx=(320,0),pady=0,ipady=3)
        self.TranslatorChan.pack(side=RIGHT,padx=(0,50),pady=0)
    def checknet(self):
        if self.checker.MTest() is False:
            if self.failed is False:
                started.error('Failed to Open due to Network Issues')
                a=NIC(self)
            self.failed=True
            self.pack_forget()
        else:
            if not self.packed:
                self.reviveThis()
            if self.failed:
                self.pack(fill=BOTH,expand=True)
                self.failed=False
                self.GTBack=GTBackend(self.parent)
                started.warning('Regained Net Access')
            
        self.after(3000,self.checknet)  
if __name__=='__main__':
    root=Tk()
    a=GT(root,StringVar())
    a.pack(fill=BOTH,expand=True)
    root.mainloop()