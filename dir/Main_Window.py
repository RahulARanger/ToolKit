from tkinter import *
from MainPage import *
import time
class Clock(Label):
    def __init__(self,parent):
        Label.__init__(self,parent)
        self.Seconds=IntVar()
        self.Minutes=IntVar()
        self.parent=parent
        self.Hours=IntVar()
        self.WTime=StringVar()
        self.config(textvariable=self.WTime,bg='#007acc',fg='#f1f1ff',font=('helvetica',10,'bold'))
        self.after(1000,self.set_time)
    def set_time(self):
        self.WTime.set(time.strftime('%H:%M:%S'))
        print(self.parent.winfo_width())
        self.after(1000,self.set_time)
class Main(Tk):
    def __init__(self):
        super().__init__()
        self.fullsize=False
        self.ActiveTab=None
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
        self.New=Label(self.MBFrame,relief=FLAT,text='New',bg='#323233',fg=self.textcolor,font=('helvetica',12,'bold'))
        self.About=Label(self.MBFrame,relief=FLAT,text='About',bg='#323233',fg=self.textcolor,font=('helvetica',12,'bold'))
        self.Help=Label(self.MBFrame,relief=FLAT,text='Help',bg='#323233',fg=self.textcolor,font=('helvetica',12,'bold'))
        self.add_events()
    def add_events(self):
        self.TimeNow=Clock(self.SFrame)
        self.New.bind('<Enter>',lambda x:self.bthover_menu(self.New,True))
        self.New.bind('<Button-1>',self.summonmain)
        self.New.bind('<Leave>',lambda x:self.bthover_menu(self.New,False))
        self.About.bind('<Enter>',lambda x:self.bthover_menu(self.About,True))
        self.About.bind('<Button-1>',lambda x:self.bthover_menu(self.About,None))
        self.About.bind('<Leave>',lambda x:self.bthover_menu(self.About,False))
        self.Help.bind('<Enter>',lambda x:self.bthover_menu(self.Help,True))
        self.Help.bind('<Button-1>',lambda x:self.bthover_menu(self.Help,None))
        self.Help.bind('<Leave>',lambda x:self.bthover_menu(self.Help,False))
        self.arrange()
    def arrange(self):
        self.MFrame.pack(expand=True,fill=BOTH)
        self.MBFrame.pack(fill=X)
        self.TFrame.pack(fill=X)
        self.SFrame.pack(side=BOTTOM,fill=X)
        self.New.pack(side=LEFT,anchor='nw',padx=3)
        self.About.pack(side=LEFT,anchor='nw',padx=3)
        self.Help.pack(side=LEFT,anchor='nw',padx=3)
        self.TimeNow.pack(side=RIGHT)
        
    def bthover_menu(self,bt,status):
        if status is None:
            print('Clicked')
        else:
            bt['bg']='#4d4d4d' if status else '#323233'
    def size(self,*args):
        self.fullsize=not self.fullsize
        self.attributes('-fullscreen',self.fullsize)
    def summonmain(self,*args):
        Tab=Page1(self.TFrame)
        Tab.index=(len(self.Tabs))
        self.Tabs.append(Tab)
        self.opentab(self.Tabs[-1])
        self.Tabs[-1].name.bind('<Button-1>',lambda x:self.opentab(self.Tabs[Tab.index],Tab.index))
        self.Tabs[-1].cross.bind('<Button-1>',lambda x: self.closetab(self.Tabs[Tab.index],Tab.index))
        self.Tabs[-1].getFrame().pack(side=LEFT)
    def opentab(self,tab,index=0):
        if self.ActiveTab is not None:
            self.ActiveTab.name['bg']=tab.backcolor[0]
            self.ActiveTab.cross['bg']=tab.backcolor[0]
            self.ActiveTab.frame['bg']=tab.backcolor[0]
            self.ActiveTab.name['fg']=tab.textcolor[0]
            self.ActiveTab.name['fg']=tab.textcolor[0]
        tab.name['bg']=tab.backcolor[1]
        tab.cross['bg']=tab.backcolor[1]
        tab.frame['bg']=tab.backcolor[1]
        tab.name['fg']=tab.textcolor[1]
        tab.name['fg']=tab.textcolor[1]
        self.ActiveTab=tab
    def closetab(self,tab,index):
        change=False
        if self.ActiveTab==tab:
            change=tab.index
        self.Tabs[index].getFrame().pack_forget()
        del self.Tabs[index]
        for i in range(len(self.Tabs)):
            self.Tabs[i].index=(i)
        if change is not False: 
            print(change)
            if len(self.Tabs)==0:
                self.ActiveTab=None
                return None
            elif len(self.Tabs)==change or change>len(self.Tabs):
                self.ActiveTab=self.Tabs[-1]
            else: 
                self.ActiveTab=self.Tabs[change-1 if change!=0 else change]
            self.opentab(self.ActiveTab)

Main().mainloop()