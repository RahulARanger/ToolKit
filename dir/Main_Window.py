from tkinter import *
import time
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
try:
    from Settings import *
except:
    from dir.Settings import *
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
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
try:
    from dir.mediaplayer import *
except:
    from mediaplayer import *
try:
    from dir.root.OpenLink import *
except:
    from root.OpenLink import *
try:
    from dir.YtDownloader import *
except:
    from YtDownloader import*
import time
STATUS=None
BACK=None

pygame.mixer.init()
def do_this():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Horizontal.TScrollbar", gripcount=0,
                    background="#424242", darkcolor='#1e1e1e', lightcolor='#1e1e1e',arrowsize=18,
                    troughcolor='#1e1e1e', bordercolor="#424242", arrowcolor="orange",relief=FLAT)
    style.configure("Vertical.TScrollbar", gripcount=0,
                            background="#424242", darkcolor='#1e1e1e', lightcolor='#1e1e1e',arrowsize=18,
                            troughcolor='#1e1e1e', bordercolor="#424242", arrowcolor="orange",relief=FLAT)

class MenuFrame(Frame):
    def __init__(self,parent,name,link=''):
        super().__init__(parent)
        self['bg']="#424242"
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.link=link
        self.name=Label(self,text=name,fg=self.textcolor[0],bg=self.backcolor[0],height=2)
        self.name.bind('<Enter>',lambda x:self.bthover(False))
        self.name.bind('<Leave>',lambda x :self.bthover(True))
        self.name.bind('<Button-1>',lambda x :self.bthover(None))
        self.name.pack()
    def bthover(self,status):
        if status is None:
            started.info('Opened Browser, pressed {}'.format(self.name['text']))
            BS1.play()
            Open(self.link)
        else:
            if status:
                STATUS.set('ZzZzZzzZzzZZzzZZ')
                self.config(bg=self.backcolor[0])
                self.name.config(fg=self.textcolor[0],bg=self.backcolor[0])
            else:
                hoversound.play()
                STATUS.set('Redirects to {}'.format(self.link))
                self.config(bg=self.backcolor[1])
                self.name.config(fg=self.textcolor[1],bg=self.backcolor[1])        
class MenuOptionFrame(Frame):
    def __init__(self,parent,var):
        super().__init__(parent)
        self.options=var
        self.options.set('Main')
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.select=OptionMenu(self,self.options,'Main','Calculator','Translator','Youtube Downloader')
        self.select.config(background=self.backcolor[0],fg=self.textcolor[0],relief=FLAT,activeforeground=self.textcolor[1],activebackground=self.backcolor[1],highlightthickness=0,indicatoron=0)
        self.select['menu'].config(bg='#1e1e1e',activeforeground='#f1f1ff',fg=self.textcolor[0])
        self.select['menu']['cursor']='hand2'
        self.select.pack(fill=BOTH,expand=True,side=LEFT)
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Leave>',lambda x:self.bthover(False))
    def bthover(self,status):
        if status:
            hoversound.play()
            STATUS.set('Select the Tool')
            self.config(bg=self.backcolor[1])
        else:
            STATUS.set('ZzZzZzzZzzZZzzZZ')
            self.config(bg=self.backcolor[0])
class Clock(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.Seconds=IntVar()
        self.flag=False
        self.Minutes=IntVar()
        self.parent=parent
        self.Hours=IntVar()
        self.WTime=StringVar()
        self.backcolor=('#007acc','#33BBFF')
        self.config(textvariable=self.WTime,bg='#007acc',fg='#f1f1ff',font=('helvetica',12,'bold'))
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Leave>',lambda x:self.bthover(False))
        self.after(1000,self.set_time)
    def set_time(self):
        if self.flag:self.WTime.set(time.strftime('%H:%M:%S'))        
        else:self.WTime.set(time.strftime('%H:%M %S'))        
        self.flag=not(self.flag)
        self.after(1000,self.set_time)
    def bthover(self,status):
        if status is True:
            self.config(bg=self.backcolor[1])
            STATUS.set('Current Date and Time')
            self.config(relief=GROOVE)
        else:
            self.config(bg=self.backcolor[0])
            STATUS.set('ZzZzZzzZzzZZzzZZ')
            self.config(relief=FLAT)
class Wifi(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.status=Label(parent,text='✔️',bg='#007acc',fg='#40FF19',font=('Times',12,'bold'))
        self.config(text='Connected:',bg='#007acc',fg='#f1f1ff',font=('helvetica',12,'bold'))
        self.bind('<Enter>',lambda x:self.hover(True))
        self.bind('<Leave>',lambda x:self.hover(False))
        self.after(500,self.check)
    def check(self):
        if NetworkCheck().MTest():
            if self.status['text']=='❌ ':
                started.debug('Internet is Back')
            self.status.config(text='✔️',fg='#40FF19')
        else:
            if self.status['text']=='✔️':
                started.warning('Internet Connection is Lost')
            self.status.config(text='❌ ',fg='#FF0000')
        self.after(6000,self.check)
    def hover(self,status):
        if status:
            STATUS.set('Not Connected' if self.status['text']=='❌ ' else 'Connected')
        else:
            STATUS.set('ZzZzZzzZzzZZzzZZ')
class BackButton:
    def __init__(self,parent,variable):
        self.var=variable
        image_=PIL.Image.open('Resources\Media\\back-button.png')
        self.image__=PIL.ImageTk.PhotoImage(image_)
        self.bt=Button(parent,bg='#f1f1ff',font=("Comic Sans MS", "10", "normal"),command=lambda : self.var.set('Main'))
        self.parent=parent
        self.arrange()
    def arrange(self):
        self.bt.config(relief=FLAT,image=self.image__)
    def forget(self):
        self.bt.pack_forget()
    def revive(self):
        self.bt.pack(side=LEFT,padx=(10,20),ipadx=3)
        self.arrange()
    
class Tab(Frame):
    def __init__(self,parent,var):
        super().__init__(parent)
        global STATUS,BACK
        self['bg']='#2d2d2d'
        self.DummyFrame=Frame(self,bg='#2d2d2d')
        self.D1=Frame(self.DummyFrame,bg='#2d2d2d')
        self.D2=Frame(self.DummyFrame,bg='#2d2d2d')
        self.Back=BackButton(self.D1,var)
        self.Name=Label(self.D2,text='Main',bg='#1e1e1e',fg='#f1f1ff',font=("Comic Sans MS", "10", "normal"))
        STATUS=StringVar()
        STATUS.set('')
        BACK=self.Back
        self.checkinglabel=Label(self,textvariable=STATUS, justify=LEFT,background="#ffffe0", relief=SOLID,font=("Comic Sans MS", "10", "normal"),borderwidth=2)
        self.DummyFrame.pack(side=LEFT)
        self.D1.pack(side=LEFT)
        self.D2.pack(side=LEFT)
        self.Back.revive()
        self.Name.pack(ipadx=10,ipady=1,side=LEFT,anchor=N)        
        self.checkinglabel.pack(anchor=NE)
class Version(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.config(text='v1.0',fg=self.textcolor[0],bg=self.backcolor[0])
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Leave>',lambda x:self.bthover(False))
    def bthover(self,status):
        if status:
            hoversound.play()
            self.config(text='v1.0',fg=self.textcolor[1],bg=self.backcolor[1])
            STATUS.set('Current Version is {}'.format(self['text']))
        else:
            self.config(text='v1.0',fg=self.textcolor[0],bg=self.backcolor[0])
            STATUS.set('ZzzzZZZzZZZZzZZZZZz')
class Selector(Frame):
    def __init__(self,parent,which_one,var):
        super().__init__(parent)
        self.MCanvas=Canvas(self,bg='#252526')
        self.variable=var
        self.config(bg='#252526')
        self.VBar=ttk.Scrollbar(self,orient=VERTICAL,command=self.MCanvas.yview)
        self.HBar=ttk.Scrollbar(self,orient=HORIZONTAL,command=self.MCanvas.xview)
        self.VFrame=Frame(self.MCanvas,bg='#252526')
        self.whichone=which_one
        self.switchsound='Resources\Media\switch.wav'
        self.arrange()
    def orientScreen(self,event):
        self.MCanvas.yview_scroll(int(-1*(event.delta/120)),'units')
    def arrange(self):
        global BACK,UPLOADED,FILE,STORE
        self.HBar.config(cursor='hand2')
        self.VBar.config(cursor='hand2')
        self.MCanvas.configure(yscrollcommand=self.VBar.set,xscrollcommand=self.HBar.set)
        self.MCanvas.bind('<Configure>',lambda e:self.MCanvas.configure(scrollregion=self.MCanvas.bbox('all')))
        self.MCanvas.bind_all('<MouseWheel>',self.orientScreen)
        self.MCanvas.create_window((0,0),window=self.VFrame,anchor='nw',width=1350)
        self.AcFrame=None
        a=pygame.mixer.Sound(self.switchsound)
        a.play()        
        if self.whichone==0:
            started.info('Opened Main Tab')
            BACK.forget()
            self.AcFrame=Settings(self.VFrame,STATUS,self.variable)
            self.config(bg='#252526')
            started.info('Closed Main Tab')
        elif self.whichone==1:
            BACK.revive()
            started.info('Opened Calculator Tab')
            self.config(bg='#252526')
            self.AcFrame=Calc(self.VFrame,STATUS)
            started.info('Closed Calculator Tab')
        elif self.whichone==2:
            BACK.revive()
            started.info('Opened Translator Tab')
            self.AcFrame=GT(self.VFrame,STATUS) 
            self.MCanvas.config(bg='#80D4FF')  
            started.info('Closed Translator Tab')
        elif self.whichone==3:
            BACK.revive()
            started.info('Opened Yt Downloader Tab')
            self.MCanvas.config(bg='#FF4D4D')
            self.AcFrame=YT(self.VFrame,STATUS)
            started.info('Closed YT Downloader Tab')
        self.AcFrame.pack(expand=True,fill=BOTH)
        self.HBar.pack(side=BOTTOM,fill=X)
        self.VBar.pack(side=RIGHT,fill=Y)
        self.MCanvas.pack(fill=BOTH, expand=True)
class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        do_this()
        self.geometry('{}x{}+-5+-6'.format(self.winfo_screenwidth(),self.winfo_screenheight()))
        self['bg']='#252526'
        self.var=StringVar()
        self.bind('<F11>',self.size)
        self.state('zoomed')
        self.MFrame=Frame(self,bg='#323233')
        self.MeFrame=Frame(self.MFrame,bg="#424242")
        self.TabFrame=Tab(self.MFrame,self.var)
        self.ActiveFrame=None
        self.SFrame=Frame(self.MFrame)
        self.SFrame.config(bg='#007acc')
        self.Mp3Player=MediaPlayer(self.SFrame,STATUS)
        Warning.object=self.Mp3Player
        self.TimeNow=Clock(self.SFrame)
        self.WifiCheck=Wifi(self.SFrame)
        self.VersionInfo=Version(self.MeFrame)
        self.select=MenuOptionFrame(self.MeFrame,self.var)
        self.about=MenuFrame(self.MeFrame,'About','https://github.com/RahulARanger/ToolKit')
        self.help=MenuFrame(self.MeFrame,'Help','https://github.com/RahulARanger/ToolKit/issues')
        self.arrange()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if os.path.exists('temp'):
                for file in os.listdir('temp'):
                    os.remove('temp//'+file)
                os.rmdir('temp')
            self.destroy()
    def arrange(self):
        self.MFrame.pack(fill=BOTH,expand=True)
        self.MeFrame.pack(fill=X)
        self.select.pack(side=LEFT,padx=3,ipadx=3)
        self.about.pack(side=LEFT,padx=3,ipadx=3)
        self.help.pack(side=LEFT,padx=3,ipadx=3)
        self.VersionInfo.pack(side=RIGHT,ipadx=3)
        self.TabFrame.pack(fill=X,pady=3)
        self.SFrame.pack(side=BOTTOM,fill=X)
        self.fullsize=False
        self.Mp3Player.pack(side=LEFT)
        self.TimeNow.pack(side=RIGHT,fill=Y)
        self.WifiCheck.status.pack(side=RIGHT,fill=Y)
        self.WifiCheck.pack(side=RIGHT,fill=Y)
        self.var.trace('w',self.selectTools_2)
        self.whichone=0
        self.var.set('Main')
        self.selectTools(0,True)
    def size(self,*args):
        self.fullsize=not self.fullsize
        self.attributes('-fullscreen',self.fullsize)
    def selectTools_2(self,*args):
        note=['Main','Calculator','Translator','Youtube Downloader']
        got=self.var.get()
        if note.index(got)==self.whichone:
            pass
        else:
            self.whichone=note.index(got)
            self.TabFrame.Name.config(text=note[self.whichone])
            self.ActiveFrame.destroy()
            self.ActiveFrame=Selector(self.MFrame,self.whichone,self.var)
            self.ActiveFrame.pack(expand=True,fill=BOTH)
    def selectTools(self,whichone,special=False):        
        if self.whichone==whichone and not special:
            pass
        else:
            if self.ActiveFrame is not None:self.ActiveFrame.destroy()
            self.whichone=whichone
            if self.whichone!=0:
                pass
            self.ActiveFrame=Selector(self.MFrame,self.whichone,self.var)
            self.ActiveFrame.pack(expand=True,fill=BOTH)
if __name__=='__main__':
    a=MainWindow()
    a.mainloop()