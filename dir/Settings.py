from tkinter import *
from tkinter import font
try:
    from  dir.root.OtherButtonClick import *
except:
    from root.OtherButtonClick import *
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
    def __init__(self,p,var,var2,setitto):
        super().__init__(p)
        self.var=var2        
        self.setitto=setitto
        self.status=var
        self.Ifont=font.Font(family="Times", size="12", weight="bold",slant="roman")
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.config(bg=self.backcolor[0],fg=self.textcolor[0])
        self.config(text='Open This')
        self.arrange()
    def arrange(self):
        self.bind('<Button-1>',lambda x:self.btpressed(True))
        self.bind('<Enter>',lambda x:self.hover(True))
        self.bind('<Leave>',lambda x:self.hover(False))
    def hover(self,status):
        if status:
            hoversound.play()
            self.config(bg=self.backcolor[1],fg=self.textcolor[1])
            self.status.set('Open this tool?')
        else:
            self.config(bg=self.backcolor[0],fg=self.textcolor[0])
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def btpressed(self,status):
        if status:
            self.var.set(self.setitto)
        else:
            pass
class Settings(Frame):
    def __init__(self,parent,var,variable):
        super().__init__(parent)
        self.file='dir\\root\\settings.json'        
        self['bg']='#252526'   
        self.failed=False
        self.variable=variable
        self.status=var
        self.textcolor=('#74878f','#f1f1ff')
        self.sfont=font.Font(family="Lucida Grande", size=14)
        self.sfontl=font.Font(family="Lucida Grande", size=16)
        self.Ifont=font.Font(family="Times", size="12", weight="bold",slant="italic")
        self.TFrame=LabelFrame(self,text='Tools',bg='#252526',padx=10,pady=10,fg='#f1f1ff',font=self.sfont)
        self.SFrame=LabelFrame(self,text='Short Cuts ',bg='#252526',fg=self.textcolor[0],padx=10,pady=10)
        self.CSFrame=LabelFrame(self.SFrame,text='Calculator ',bg='#252526',fg=self.textcolor[0],padx=50,pady=50)        
        self.MSFrame=LabelFrame(self.SFrame,text='Translator ',bg='#252526',fg=self.textcolor[0],padx=50,pady=50)        
        self.TSFrame=LabelFrame(self.SFrame,text='Youtube Downloader ',bg='#252526',fg=self.textcolor[0],padx=50,pady=50)        
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
        self.Ctut=ChooseButton(self.CSFrame,self.status,self.variable,'Calculator')
        self.Mtut=ChooseButton(self.MSFrame,self.status,self.variable,'Translator')
        self.Ttut=ChooseButton(self.TSFrame,self.status,self.variable,'Youtube Downloader')
        self.Log=Button(self.SFrame,text='Show Logs',bg=self.Ctut.backcolor[0],fg=self.textcolor[0],activebackground=self.Ctut.backcolor[0],relief=FLAT,activeforeground=self.textcolor[1],command=lambda :self.displayLogs())
        self.Log.bind('<Enter>',lambda x:self.bthover(True,self.Log))
        self.Log.bind('<Leave>',lambda x:self.bthover(False,self.Log))
        self.arrange()
    def displayLogs(self):
        BS1.play()
        ShowLogs(self,'Resources\Logs\MainLog.log',BS1)
    def arrange(self):
        self.SFrame.pack(fill=X)
        self.TFrame.pack(fill=X)
        self.CSFrame.pack(fill=X)
        self.MSFrame.pack(fill=X)
        self.TSFrame.pack(fill=X)
        self.Ctut.pack(side=LEFT)
        self.Mtut.pack(side=LEFT)
        self.Ttut.pack(side=LEFT)
        self.Log.pack(side=RIGHT,pady=20,padx=(0,30))    
    def bthover(self,status,w):
        if status:
            w.config(fg=self.textcolor[1],bg=self.Ctut.backcolor[1])
            self.status.set(w['text'])
        else:
            w.config(fg=self.textcolor[0],bg=self.Ctut.backcolor[0])
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def hover(self,status,obj):
        if status:
            obj.config(font=self.sfontl)
            obj['fg']=self.textcolor[1]
            self.SFrame.config(relief=RIDGE)
            self.status.set(obj['text'])
        else:
            obj.config(font=self.sfont)
            obj['fg']=self.textcolor[0]
            self.SFrame.config(relief=RAISED)   
            self.status.set('ZzZzZzzZzzZZzzZZ')
if __name__=='__main__':
    a=Tk()
    b=Settings(a,StringVar(),IntVar())
    b.pack(fill=BOTH,expand=True)
    a.mainloop()    