from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
try:
    from GoogleTranslate import *
except:
    from dir.GoogleTranslate import *
try:
    from Calculator import *
except:
    from dir.Calculator import *
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
import time
import webbrowser
class EmptyFrame(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self['bg']='#323233'
        self.lb=Label(self,text='Default Label')
        self.lb.pack()

class Default(Frame):
    def __init__(self,parent2,parent):
        super().__init__(parent)
        self['bg']='orange'
        self.parent=parent
        self.parent2=parent2
        self.bt=Button(self,text='Translator',command=lambda: self.select(1))
        self.bt2=Button(self,text='Calculator',command=lambda: self.select(2))
        self.bt.pack()
        self.bt2.pack()
    def select(self,choice):
        for i in self.winfo_children():
            i.destroy()
        if choice==1:
            a=GT(self)
            a.pack(expand=True,fill=BOTH)
            self.parent2.ActiveTab.name.config(text='Translator')
            self.parent2.attributes('-fullscreen',True)
            self.parent2.attributes('-fullscreen',False)
        elif choice==2:
            a=Calc(self)
            self.parent2.ActiveTab.name.config(text='Calculator')
            a.pack(expand=True,fill=BOTH)
def Open(x):
	new=2
	url=x
	webbrowser.open(url,new=new)
class Tab:
    def __init__(self,win,frame,parent):
        self.frame=Frame(win,bg='#2d2d2d')
        self.index=None
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=('#2d2d2d','#1e1e1e')
        self.name=Label(self.frame,text='Main',bg=self.backcolor[0],fg=self.textcolor[0],height=2)
        self.cross=Label(self.frame,text='✖',bg=self.backcolor[0],fg=self.textcolor[0])
        self.TabFrame=Default(parent,frame)
        self.arrange()
    def arrange(self):
        self.name.pack(side=LEFT)
        self.cross.pack(side=RIGHT)
    def getFrame(self):
        return self.frame
    def activate(self):
        self.name['bg']=self.backcolor[1]
        self.frame['bg']=self.backcolor[1]
        self.cross['bg']=self.backcolor[1]
        self.name['fg']=self.textcolor[1]
        self.cross['fg']=self.textcolor[1]
        self.TabFrame.pack(fill=BOTH,expand=True)
    def deactivate(self):
        self.name['bg']=self.backcolor[0]
        self.frame['bg']=self.backcolor[0]
        self.cross['bg']=self.backcolor[0]
        self.name['fg']=self.textcolor[0]
        self.cross['fg']=self.textcolor[0]
        self.TabFrame.pack_forget()
    def destruct(self):
        self.frame.destroy()
        self.TabFrame.destroy()
class Clock(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.Seconds=IntVar()
        self.flag=False
        self.Minutes=IntVar()
        self.parent=parent
        self.Hours=IntVar()
        self.WTime=StringVar()
        self.config(textvariable=self.WTime,bg='#007acc',fg='#f1f1ff',font=('helvetica',12,'bold'))
        self.after(1000,self.set_time)
    def set_time(self):
        if self.flag:self.WTime.set(time.strftime('%H:%M:%S'))        
        else:self.WTime.set(time.strftime('%H:%M %S'))        
        self.flag=not(self.flag)
        self.after(1000,self.set_time)
class Wifi(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.status=Label(parent,text='✔️',bg='#007acc',fg='#40FF19',font=('Times',12,'bold'))
        self.config(text='Connected:',bg='#007acc',fg='#f1f1ff',font=('helvetica',12,'bold'))
        self.after(1000,self.check)
    def check(self):
        if NetworkCheck().MTest():
            self.status.config(text='✔️',fg='#40FF19')
        else:
            self.status.config(text='❌ ',fg='#FF0000')
        self.after(1000,self.check)

class Main(Tk):
    def __init__(self):
        super().__init__()        
        self.fullsize=False
        self.title('ToolKit')
        self.geometry('{}x{}+-5+-6'.format(self.winfo_screenwidth(),self.winfo_screenheight()))
        self.bind('<F11>',self.size)
        self.MFrame=Frame(self)
        self.MFrame.config(bg='#323233')
        self.textcolor='#74878f'
        self.buttoncolor='#323233'
        self.Tabs=[]
        self.MBFrame=Frame(self.MFrame)
        self.MBFrame.config(bg='#323233')
        self.TFrame=Frame(self.MFrame,height=1)
        self.TFrame.config(bg='#252526')
        self.SFrame=Frame(self.MFrame)
        self.SFrame.config(bg='#007acc')
        self.AFrame=Frame(self.MFrame,bg='#252526')
        self.MCanvas=Canvas(self.AFrame,bg='#252526')
        self.New=Label(self.MBFrame,relief=FLAT,text='New',bg='#323233',fg=self.textcolor,font=('helvetica',12,'bold'))
        self.About=Label(self.MBFrame,relief=FLAT,text='About',bg='#323233',fg=self.textcolor,font=('helvetica',12,'bold'))
        self.Help=Label(self.MBFrame,relief=FLAT,text='Help',bg='#323233',fg=self.textcolor,font=('helvetica',12,'bold'))
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Horizontal.TScrollbar", gripcount=0,
                background="#424242", darkcolor='#1e1e1e', lightcolor='#1e1e1e',arrowsize=18,
                troughcolor='#1e1e1e', bordercolor="#424242", arrowcolor="orange",relief=FLAT)
        style.configure("Vertical.TScrollbar", gripcount=0,
                        background="#424242", darkcolor='#1e1e1e', lightcolor='#1e1e1e',arrowsize=18,
                        troughcolor='#1e1e1e', bordercolor="#424242", arrowcolor="orange",relief=FLAT)
        self.VBar=ttk.Scrollbar(self.AFrame,orient=VERTICAL,command=self.MCanvas.yview)
        self.HBar=ttk.Scrollbar(self.AFrame,orient=HORIZONTAL,command=self.MCanvas.xview)
        self.AcFrame=Frame(self.MCanvas,bg='#1e1e1e')
        self.ActiveFrame=Frame(self.AcFrame)
        self.AIFrame=EmptyFrame(self.ActiveFrame)
        self.ActiveTab=None
        self.add_events()
    def add_events(self):
        self.TimeNow=Clock(self.SFrame)
        self.WifiCheck=Wifi(self.SFrame)
        self.HBar.config(cursor='hand2')
        self.VBar.config(cursor='hand2')
        self.New.bind('<Enter>',lambda x:self.bthover_menu(self.New,True))
        self.New.bind('<Button-1>',self.summonmain)
        self.New.bind('<Leave>',lambda x:self.bthover_menu(self.New,False))
        self.About.bind('<Enter>',lambda x:self.bthover_menu(self.About,True))
        self.About.bind('<Button-1>',lambda x:self.bthover_menu(self.About,None,'https://github.com/RahulARanger/ToolKit'))
        self.About.bind('<Leave>',lambda x:self.bthover_menu(self.About,False))
        self.Help.bind('<Enter>',lambda x:self.bthover_menu(self.Help,True))
        self.Help.bind('<Button-1>',lambda x:self.bthover_menu(self.Help,None,'https://github.com/RahulARanger/ToolKit/issues'))
        self.Help.bind('<Leave>',lambda x:self.bthover_menu(self.Help,False))
        self.arrange()
    def arrange(self):
        self.MFrame.pack(expand=True,fill=BOTH)
        self.MBFrame.pack(fill=X)
        self.TFrame.pack(fill=X)
        self.SFrame.pack(side=BOTTOM,fill=X)
        self.AFrame.pack(fill=BOTH,expand=True)
        self.MCanvas.configure(yscrollcommand=self.VBar.set,xscrollcommand=self.HBar.set)
        self.MCanvas.bind('<Configure>',lambda e:self.MCanvas.configure(scrollregion=self.MCanvas.bbox('all')))
        self.MCanvas.create_window((0,0),window=self.AcFrame,anchor='nw',width=1339)
        self.ActiveFrame.pack(fill=BOTH,expand=True)
        self.AIFrame.pack(fill=BOTH,expand=True)
        self.HBar.pack(side=BOTTOM,fill=X)
        self.VBar.pack(side=RIGHT,fill=Y)
        self.MCanvas.pack(fill=BOTH, expand=True)
        self.New.pack(side=LEFT,anchor='nw',padx=3)
        self.About.pack(side=LEFT,anchor='nw',padx=3)
        self.Help.pack(side=LEFT,anchor='nw',padx=3)
        self.TimeNow.pack(side=RIGHT)
        self.WifiCheck.status.pack(side=RIGHT)
        self.WifiCheck.pack(side=RIGHT)
    def bthover_menu(self,bt,status,link=''):
        if status is None:
            print('Clicked')
            Open(link)
        else:
            bt['bg']='#4d4d4d' if status else '#323233'
    def size(self,*args):
        self.fullsize=not self.fullsize
        self.attributes('-fullscreen',self.fullsize)
    def summonmain(self,*args):
        if len(self.Tabs)==4:
            messagebox.showwarning(title="Sorry, We are Currently Working On this issue", message='Opening More than 4 tabs freezes app!')
        else:
            if self.ActiveTab is None:self.AIFrame.pack_forget()
            new=Tab(self.TFrame,self.ActiveFrame,self)
            new.index=len(self.Tabs)
            new.frame.pack(side=LEFT)
            new.name.bind('<Button-1>',lambda e:self.shiftTab(new))
            new.cross.bind('<Button-1>',lambda e:self.closeTab(new))
            self.Tabs.append(new)
            self.shiftTab(self.Tabs[-1])
    def shiftTab(self,new):
        print(len(self.Tabs))
        if self.ActiveTab is None:
            self.ActiveTab=new
            self.ActiveTab.activate()
        else:
            self.ActiveTab.TabFrame.pack_forget()
            self.ActiveTab.deactivate()
            self.ActiveTab=new
            self.ActiveTab.activate()
    def closeTab(self,new):
        current=new.index
        if current==self.ActiveTab.index:
            self.ActiveTab=None
        print(current)
        print(len(self.Tabs))
        del self.Tabs[current]
        new.destruct()
        if len(self.Tabs)==0:
            self.ActiveTab=None
            a=EmptyFrame(self.ActiveFrame)
            a.pack(expand=True,fill=BOTH)
        else:
            if self.ActiveTab is None:
                if current==len(self.Tabs):current-=1
                self.ActiveTab=self.Tabs[current]
                self.ActiveTab.activate()
        for i in range(len(self.Tabs)):
            self.Tabs[i].index=i
        print(len(self.Tabs))
if __name__=='__main__':
    Main().mainloop()