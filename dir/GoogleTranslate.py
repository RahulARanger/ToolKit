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
        self.c_from,self.c_to=None,None
        self.origin,self.translated,self.pronunciation=str(),str(),str()
        self.Languages=[] # has the list of the Languages
        self.LanCodes=None # has the language codes
        self.collect()
    def collect(self):
        with open('dir\\root\\languages.json','r') as hand:
            self.LanCodes=json.loads(hand.read())
            for i in self.LanCodes['Languages']:
                self.Languages.append(i.title())    
            self.LanCodes=self.LanCodes['Languages']
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
    def translation(self,text,from_='english',to_='japanese'):
        if len(text)==0:return '',''
        from_=from_.lower()
        to_=to_.lower()
        fromcode=self.LanCodes[from_]
        tocode=self.LanCodes[to_]
        translator=googletrans.Translator()
        result=translator.translate(text,src=fromcode,dest=tocode)        
        try:pronunciation=result.pronunciation
        except:pronunciation=text
        return result.text,pronunciation
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
        self.bind('<FocusIn>',self.change)
        self.bind('<FocusOut>',self.revert)        
        self.special=special  
        if self.special:                        
            self.config(state=DISABLED)       
            self.config(width=45,height=10)
            self.config(font= ('consolas', '16'))
        self.arrange()
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
class GT(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='#E6FFFB')
        self.IFrame=Frame(self,bg='#E6FFFB')
        self.SeFrame=Frame(self,bg='#E6FFFB')
        self.FromLabel=HoverLabel(self.IFrame,'From Language: ')
        self.ToLabel=HoverLabel(self.IFrame,'To Language: ')     
        self.IIFrame=Frame(self,bg='#E6FFFB')
        self.photos=['Resources\Media\Translator\Translator{}.jpg'.format(i) for i in range(22)]
        self.title=ImageAlbum(self,self.photos,500,500,100,'#E6FFFB')
        self.StatusFrame=Frame(self,bg='orange')        
        self.TranslateThem=SpecialButton(self.IIFrame)
        self.fs=StringVar()
        self.ts=StringVar()        
        self.fs.set('English')
        self.ts.set('Japanese')
        self.From=InputBox(self.IIFrame)
        self.To=InputBox(self.IIFrame,True)
        self.TBack=GTBackend()
        self.Languages=self.TBack.Languages        
        self.checker=NetworkCheck()
        self.FromBox=SearchBox(self.SeFrame,self.Languages,self.fs)
        self.ToBox=SearchBox(self.SeFrame,self.Languages,self.ts)
        self.FromText=None
        self.arrange()        
        self.From.focus_set() 
        self.after(3000,self.check)       
    def arrange(self):
        self.title.pack()
        self.IFrame.pack(fill=X,expand=True)
        self.FromLabel.pack(side=LEFT,padx=30)
        self.ToLabel.pack(side=RIGHT,padx=(0,460))
        self.SeFrame.pack(fill=X,expand=True,pady=10)
        self.FromBox.pack(side=LEFT,padx=60)
        self.ToBox.pack(side=RIGHT,padx=(0,420))
        self.IIFrame.pack(expand=True,fill=X)
        self.From.pack(side=LEFT,padx=30,pady=30)
        self.TranslateThem.pack(side=LEFT,padx=(3,0))
        self.To.pack(side=RIGHT,padx=30,pady=30)  
        self.TranslateThem.bind('<Button-1>',self.do_it)    
    def do_it(self,*ags):
        text=self.From.get_it()        
        translated,pronunciation=self.TBack.translation(text,self.fs.get(),self.ts.get())
        self.To.remove_text()
        self.To.enter_text(translated)
        self.To.enter_text('\n\n'+pronunciation)
    def check(self):
        if self.checker.MTest() is False:
            print('Not Connected')
        self.after(3000,self.check)
if __name__=='__main__':
    root=Tk()
    a=GT(root)
    a.pack(fill=BOTH,expand=True)
    root.mainloop()