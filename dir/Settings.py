from tkinter import *
from tkinter import font
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
try:
    from root.Dialogs import *    
except:
    from dir.root.Dialogs import *
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

    def btpressed(self,status):
        if status:
            self.var.set(not(self.var.get()))
            self.config(text=' On ' if self.var.get()==1 else ' Off  ')
            if self.var.get()==1:
                a=Check(self)
        else:
            pass


class Settings(Frame):
    def __init__(self,parent):
        super().__init__(parent) 
        self['bg']='#252526'   
        self.textcolor=('#74878f','#f1f1ff')    
        self.sfont=font.Font(family="Lucida Grande", size=12)
        self.sfontl=font.Font(family="Lucida Grande", size=21)
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
        self.cvar.set('True')
        self.mvar.set('True')
        self.tvar.set('True')
        self.Cti=Label(self.CSFrame,text='⚫ Tutorial : ',fg=self.textcolor[1],bg='#252526',font=self.Ifont)
        self.Mti=Label(self.MSFrame,text='⚫ Tutorial : ',fg=self.textcolor[1],bg='#252526',font=self.Ifont)
        self.Tti=Label(self.TSFrame,text='⚫ Tutorial : ',fg=self.textcolor[1],bg='#252526',font=self.Ifont)
        self.Ctut=ChooseButton(self.CSFrame,self.cvar)
        self.Mtut=ChooseButton(self.MSFrame,self.mvar)
        self.Ttut=ChooseButton(self.TSFrame,self.tvar)
        self.arrange()
    def hover(self,status,obj):
        if status:
            obj.config(font=self.sfontl)
            obj['fg']=self.textcolor[1]
            self.SFrame.config(relief=RIDGE)
        else:
            obj.config(font=self.sfont)
            obj['fg']=self.textcolor[0]
            self.SFrame.config(relief=RAISED)       
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
if __name__=='__main__':
    a=Tk()
    b=Settings(a)
    b.pack(fill=BOTH,expand=True)
    a.mainloop()    