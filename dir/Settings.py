from tkinter import *
from tkinter import font
from tkinter import messagebox
import json
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
try:
    from root.Dialogs import *    
except:
    from dir.root.Dialogs import *
try:
    from dir.root.LogFiles import *
except:
    from root.LogFiles import *
class ChooseButton(Label):
    def __init__(self,p,var):
        super().__init__(p)
        self.var=var        
        self.Ifont=font.Font(family="Times", size="12", weight="bold",slant="roman")
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.config(bg=self.backcolor[0],fg=self.textcolor[0])
        self.config(text=' On ' if self.var.get()==1 else ' Off  ')
        self.arrange()
    def arrange(self):
        self.bind('<Button-1>',lambda x:self.btpressed(True))
        self.bind('<Enter>',lambda x:self.hover(True))
        self.bind('<Leave>',lambda x:self.hover(False))
    def hover(self,status):
        if status:
            self.config(bg=self.backcolor[1],fg=self.textcolor[1])
        else:
            self.config(bg=self.backcolor[0],fg=self.textcolor[0])
    def manual(self,status):
        self.config(text=' On ' if status else ' Off  ')
        self.var.set(1 if status else 0)
    def btpressed(self,status):
        if status:
            self.var.set(not(self.var.get()))
            self.config(text=' On ' if self.var.get()==1 else ' Off  ')
            if self.var.get()==1:
                a=messagebox.showinfo('Done!!!','Now you can check the help box after opening the tool')
        else:
            pass
class Settings(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.file='dir\\root\\settings.json'        
        self['bg']='#252526'   
        self.failed=False
        self.textcolor=('#74878f','#f1f1ff')
        self.sfont=font.Font(family="Lucida Grande", size=14)
        self.sfontl=font.Font(family="Lucida Grande", size=16)
        self.Ifont=font.Font(family="Times", size="12", weight="bold",slant="italic")
        self.TFrame=LabelFrame(self,text='Tools',bg='#252526',padx=10,pady=10,fg='#f1f1ff',font=self.sfont)
        self.SFrame=LabelFrame(self,text='Settings ⚙️',bg='#252526',fg=self.textcolor[0],padx=10,pady=10)
        self.CSFrame=LabelFrame(self.SFrame,text='Calculator 🖩',bg='#252526',fg=self.textcolor[0],padx=50,pady=50)        
        self.MSFrame=LabelFrame(self.SFrame,text='Mp3 Player 🎵',bg='#252526',fg=self.textcolor[0],padx=50,pady=50)        
        self.TSFrame=LabelFrame(self.SFrame,text='Translator ✨',bg='#252526',fg=self.textcolor[0],padx=50,pady=50)        
        self.SFrame.config(relief=RAISED)
        self.SFrame.bind('<Enter>',lambda x:self.hover(True,self.SFrame))
        self.SFrame.bind('<Leave>',lambda x:self.hover(False,self.SFrame))
        self.CSFrame.config(relief=RAISED)
        self.CSFrame.bind('<Enter>',lambda x:self.hover(True,self.CSFrame))
        self.CSFrame.bind('<Leave>',lambda x:self.hover(False,self.CSFrame))
        self.MSFrame.config(relief=RAISED)
        self.MSFrame.bind('<Enter>',lambda x:self.hover(True,self.MSFrame))
        self.MSFrame.bind('<Leave>',lambda x:self.hover(False,self.MSFrame))
        self.TSFrame.config(relief=RAISED)
        self.TSFrame.bind('<Enter>',lambda x:self.hover(True,self.TSFrame))
        self.TSFrame.bind('<Leave>',lambda x:self.hover(False,self.TSFrame))
        self.cvar=BooleanVar()
        self.mvar=BooleanVar()
        self.tvar=BooleanVar()              
        self.mvar.trace('w',lambda x,y,z:self.modifylst('Audio Player',self.mvar.get()))
        self.cvar.trace('w',lambda x,y,z:self.modifylst('Calculator',self.cvar.get()))
        self.tvar.trace('w',lambda x,y,z:self.modifylst('Translator',self.tvar.get()))        
        self.Cti=Label(self.CSFrame,text='⚫ Help Box : ',fg=self.textcolor[1],bg='#252526',font=self.Ifont)
        self.Mti=Label(self.MSFrame,text='⚫ Help Box : ',fg=self.textcolor[1],bg='#252526',font=self.Ifont)
        self.Tti=Label(self.TSFrame,text='⚫ Help Box : ',fg=self.textcolor[1],bg='#252526',font=self.Ifont)
        self.Ctut=ChooseButton(self.CSFrame,self.cvar)
        self.Mtut=ChooseButton(self.MSFrame,self.mvar)
        self.Ttut=ChooseButton(self.TSFrame,self.tvar)
        self.updatelst()  
        self.Reset=Button(self.SFrame,text='Reset',bg=self.Ctut.backcolor[0],fg=self.textcolor[0],activebackground=self.Ctut.backcolor[0],relief=FLAT,activeforeground=self.textcolor[1],command=self.reset_it)
        self.Log=Button(self.SFrame,text='Show Logs',bg=self.Ctut.backcolor[0],fg=self.textcolor[0],activebackground=self.Ctut.backcolor[0],relief=FLAT,activeforeground=self.textcolor[1],command=lambda :ShowLogs(self,'Resources\Logs\Opening.log'))
        self.Reset.bind('<Enter>',lambda x:self.bthover(True,self.Reset))
        self.Reset.bind('<Leave>',lambda x:self.bthover(False,self.Reset))
        self.Log.bind('<Enter>',lambda x:self.bthover(True,self.Log))
        self.Log.bind('<Leave>',lambda x:self.bthover(False,self.Log))
        self.arrange()
    def arrange(self):
        self.SFrame.pack(fill=X)
        self.TFrame.pack(fill=X)
        self.CSFrame.pack(fill=X)
        self.MSFrame.pack(fill=X)
        self.TSFrame.pack(fill=X)
        self.Cti.pack(side=LEFT)
        self.Mti.pack(side=LEFT)
        self.Tti.pack(side=LEFT)
        self.Ctut.pack(side=LEFT)
        self.Mtut.pack(side=LEFT)
        self.Ttut.pack(side=LEFT)
        self.Reset.pack(side=RIGHT,pady=20,padx=(0,30))
        self.Log.pack(side=RIGHT,pady=20,padx=(0,30))
    def reset_it(self):
        a=messagebox.askyesno('Reset! Are you Sure','Once done, all the previous settings will be erased',icon='warning')
        if a:
            with open(self.file,'r') as hand:
                self.container=json.loads(hand.read())
            self.container['Times']=1
            for i in self.container['Tuts']:
                self.container['Tuts'][i]=True
            with open(self.file,'w') as hand:
                hand.write(json.dumps(self.container,indent=4))      
            self.updatelst()
    def bthover(self,status,w):
        if status:
            w.config(fg=self.textcolor[1],bg=self.Ctut.backcolor[1])
        else:
            w.config(fg=self.textcolor[0],bg=self.Ctut.backcolor[0])
    def updatelst(self):
        with open(self.file,'r') as hand:
            self.container=json.loads(hand.read())
        print('here')
        if self.container['Times']==1:
            self.cvar.set('True')
            self.mvar.set('True')
            self.tvar.set('True')            
        else:
            self.cvar.set('True' if self.container['Tuts']['Calculator'] else 'False')
            self.mvar.set('True' if self.container['Tuts']['Audio Player'] else 'False')
            self.tvar.set('True' if self.container['Tuts']['Translator'] else 'False')    
        self.Ctut.manual(True if self.cvar.get()==1 else False)
        self.Mtut.manual(True if self.mvar.get()==1 else False)
        self.Ttut.manual(True if self.tvar.get()==1 else False)
    def modifylst(self,text,value):        
        self.container['Tuts'][text]=True if value else False
        with open(self.file,'w') as hand:
            hand.write(json.dumps(self.container,indent=4))
    def hover(self,status,obj):
        if status:
            obj.config(font=self.sfontl)
            obj['fg']=self.textcolor[1]
            self.SFrame.config(relief=RIDGE)
        else:
            obj.config(font=self.sfont)
            obj['fg']=self.textcolor[0]
            self.SFrame.config(relief=RAISED)   
if __name__=='__main__':
    a=Tk()
    b=Settings(a)
    b.pack(fill=BOTH,expand=True)
    a.mainloop()    