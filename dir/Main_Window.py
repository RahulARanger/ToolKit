from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
try:
    from GoogleTranslate import *
except:
    from dir.GoogleTranslate import *
import time
import webbrowser

def Open(x):
	new=2
	url=x
	webbrowser.open(url,new=new)
class Page1:
    def __init__(self,win,win2):
        self.frame=Frame(win,bg='#2d2d2d')
        self.index=None
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=('#2d2d2d','#1e1e1e')
        self.name=Label(self.frame,text='Main',bg=self.backcolor[0],fg=self.textcolor[0],height=2,width=6)
        self.cross=Label(self.frame,text='✖',bg=self.backcolor[0],fg=self.textcolor[0])
        self.TFrame=GT(win2)
        self.arrange()
    def arrange(self):
        self.name.pack(side=LEFT)
        self.cross.pack(side=RIGHT)
    def getFrame(self):
        return self.frame
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
        self.AFrame=Frame(self.MFrame)
        self.MCanvas=Canvas(self.AFrame)
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
        self.ActiveFrame=Frame(self.MCanvas,bg='#1e1e1e')
        self.add_events()
    def add_events(self):
        self.TimeNow=Clock(self.SFrame)
        self.HBar.config(cursor='sb_h_double_arrow')
        self.VBar.config(cursor='sb_v_double_arrow')
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
        self.HBar.pack(side=BOTTOM,fill=X)
        self.VBar.pack(side=RIGHT,fill=Y)
        self.MCanvas.configure(yscrollcommand=self.VBar.set,xscrollcommand=self.HBar.set)
        self.MCanvas.bind('<Configure>',lambda e:self.MCanvas.configure(scrollregion=self.MCanvas.bbox('all')))
        self.MCanvas.create_window((0,0),window=self.ActiveFrame,anchor='nw')
        self.MCanvas.pack(expand=True,fill=BOTH)
        self.New.pack(side=LEFT,anchor='nw',padx=3)
        self.About.pack(side=LEFT,anchor='nw',padx=3)
        self.Help.pack(side=LEFT,anchor='nw',padx=3)
        self.TimeNow.pack(side=RIGHT)
        self.ActiveFrame.pack(expand=True,fill=BOTH)
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
            Tab=Page1(self.TFrame,self.ActiveFrame)
            Tab.index=(len(self.Tabs))
            self.Tabs.append(Tab)
            self.opentab(self.Tabs[-1])
            self.Tabs[-1].name.bind('<Button-1>',lambda x:self.opentab(self.Tabs[Tab.index],Tab.index))
            self.Tabs[-1].cross.bind('<Button-1>',lambda x: self.closetab(self.Tabs[Tab.index],Tab.index))
            self.Tabs[-1].getFrame().pack(side=LEFT)
    def opentab(self,tab,index=0):
        if self.ActiveTab is not None:
            self.ActiveTab.TFrame.pack_forget()
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
        self.ActiveTab.TFrame.pack(fill=BOTH)
    def closetab(self,tab,index):
        change=False
        if self.ActiveTab==tab:
            change=tab.index
            self.ActiveTab.TFrame.destroy()
        self.Tabs[index].getFrame().destroy()
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
if __name__=='__main__':
    Main().mainloop()