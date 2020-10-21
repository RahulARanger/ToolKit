from tkinter import *
import re
from tkinter import messagebox
import pytube
import threading 
try:
    from dir.root.__pre__ import *
except:
    from root.__pre__ import *
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
try:
    from root.Dialogs import *
except:
    from dir.root.Dialogs import *
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
pytube.__main__.apply_descrambler = apply_descrambler
class EnterLink(Entry):
    def __init__(self,parent,var,status):
        super().__init__(parent)
        self.config(textvariable=var)
        self.status=status
        self.var=var
        self.var.set('Enter the Link: ')
        self.bind('<Button-1>',self.check)
        self.config(width=100)
        self.config(borderwidth=6)
        self.config(relief=FLAT)
        self.config(font=('Times','15'))
        self.bind('<Enter>',lambda x:self.hover(True))
        self.bind('<Leave>',lambda x:self.hover(False))
    def hover(self,status):
        if status:
            self.config(relief=GROOVE,fg='black')
            self.status.set('Enter the Link: ')
        else:
            self.config(relief=FLAT,fg='grey')
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def check(self,*args):
        if self.var.get()=='Enter the Link: ':
            self.var.set('')        
class LoadingFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.photos=['Resources\Media\Loading\Loading{}.jpg'.format(i) for i in range(8)]
        self.LoadingScreen=ImageAlbum(self,self.photos,1000,1000,110)
        self.LoadingScreen.pack(fill=BOTH,expand=True)
class WaitingFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.photos=['Resources\Media\Waiting\Waiting{}.jpg'.format(i) for i in range(41)]
        self.WaitingScreen=ImageAlbum(self,self.photos,800,800,100)
        self.WaitingScreen.pack(fill=BOTH,expand=True)
    def unhide(self):
        self.WaitingScreen.pack(fill=BOTH,expand=True)
        self.pack(fill=BOTH,expand=True)
    def hide(self):
        self.WaitingScreen.pack_forget()
        self.pack_forget()

YTOBJ=None
STATUS=None
class Tester:
    def __init__(self,link,func):
        self.link=link
        self.func=func
    def checkLink(self):
        global STATUS
        print(self.link)
        STATUS=None
        try:
            a=pytube.YouTube(self.link)
            YTOBJ=a
            STATUS=True
        except:
            STATUS=False  
        if STATUS:
            YTOBJ.prefetch()
    def __del__(self):
        self.func(self.link)

class YTFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.MFrame=Frame(self,bg='#FF6A4D')
        self.config(borderwidth=6,relief=RIDGE)
    def unhide(self):
        self.pack(fill=BOTH,expand=True)
    def hide(self):
        self.pack_forget()



class YT(Frame):
    def __init__(self,parent,s):
        super().__init__(parent)
        self.config(borderwidth=10,relief=RIDGE)
        self.config(bg='#FF4D4D')
        self.link=StringVar()
        self.checker=NetworkCheck()
        self.status=s
        self.FirstFrame=Frame(self,bg='#FF4D4D',relief=GROOVE,borderwidth=2)
        self.SecondFrame=Frame(self,bg='#FF4D4D',relief=GROOVE,borderwidth=3,width=1000,height=1000)
        self.EnterFrame=Frame(self.FirstFrame)
        self.READY=False
        self.status.set('Welcome to the YT Downloader UwU')
        self.failed=False
        self.hbar=Scrollbar(self.EnterFrame,orient=HORIZONTAL)
        self.Enter=EnterLink(self.EnterFrame,self.link,self.status)
        self.hbar.config(command=self.Enter.xview)
        self.SearchButton=Button(self.FirstFrame,text='🔍',width=2,relief=FLAT,bg='#FF0000',command=self.check,borderwidth=3)
        self.Enter.config(xscrollcommand=self.hbar.set)      
        self.ContainFrame=WaitingFrame(self.SecondFrame)
        self.ContainFrame.bind('<Enter>',lambda x:self.status.set('Waiting For User\'s Input!'))
        self.ContainFrame.bind('<Leave>',lambda x:self.status.set('ZzzzZZZZzzZZZ'))
        self.LINK=None
        self.SearchButton.bind('<Enter>',lambda x:self.bthover(True))
        self.SearchButton.bind('<Leave>',lambda x:self.bthover(False))
        self.designs()
        self.arrange()
        self.after(3000,self.checknet)   
    def bthover(self,status):
        if status:
            self.status.set('Search?')
            self.SearchButton.config(relief=RIDGE)
        else:
            self.status.set('ZzZzZzzZzzZZzzZZ')
            self.SearchButton.config(relief=FLAT)
    def designs(self):
        self.SearchButton.config(font=('Times','20','bold'))
    def arrange(self):
        self.FirstFrame.pack(pady=20)
        self.SecondFrame.pack()
        self.EnterFrame.pack(side=LEFT,pady=(10,0))
        self.SearchButton.pack(side=LEFT,fill=Y)
        self.Enter.pack(fill=BOTH)
        self.hbar.pack(fill=X,side=BOTTOM)
        self.ContainFrame.pack(fill=BOTH,expand=True)
    def check(self,*args):
        self.status.set('Loading...')
        self.SearchButton.config(state=DISABLED)
        link=self.link.get()
        self.ContainFrame.pack_forget()
        self.Justasec=LoadingFrame(self.SecondFrame)
        self.Justasec.pack(fill=BOTH,expand=True)
        if True:
            tester=Tester(link,self.soNext)
            Hire=threading.Thread(target=tester.checkLink)
            Hire.start()
    def soNext(self,link):
        global STATUS
        print(STATUS)
        self.Justasec.destroy()
        self.ContainFrame.hide()
        if STATUS:
            if self.READY:
                a=messagebox.askyesno('Alert!!!','Ready to Lose Current Details?',icon='warning')
                if a:
                    self.LINK=link
                    self.ContainFrame.unbind('<Enter>')
                    self.ContainFrame.unbind('<Leave>')
                    self.ContainFrame=YTFrame(self.SecondFrame)
                    self.ContainFrame.pack(fill=BOTH,expand=True)
                    # TODO: refresh
                else:self.ContainFrame.unhide()
                self.link.set(self.LINK)
                self.Enter.icursor(self.Enter.index(END))
            else:
                self.LINK=link
                self.ContainFrame.unbind('<Enter>')
                self.ContainFrame.unbind('<Leave>')
                self.ContainFrame=YTFrame(self.SecondFrame)
                self.ContainFrame.pack(fill=BOTH,expand=True)
            self.READY=True
            self.status.set('ZzZzZzzZzzZZzzZZ')
        else:
            a=messagebox.showwarning('Alert!!!','This is not Youtube Related Link or Try again',icon='warning')
            if self.READY is False:
                self.link.set('Enter the Link: ')
                self.Enter.icursor(self.Enter.index(END))
            else:
                self.link.set(self.LINK)
                self.Enter.icursor(self.Enter.index(END))
            self.ContainFrame.unhide()
        self.SearchButton.config(state=NORMAL)
    def checknet(self):
        if self.checker.MTest() is False:
            if self.failed is False:a=NIC(self)
            self.failed=True
            self.pack_forget()
        else:
            if self.failed:
                self.pack(fill=BOTH,expand=True)
                self.failed=False
        self.after(3000,self.checknet)
if __name__=='__main__':
    a=Tk()
    f=Frame(a,bg='#FF4D4D')
    g=StringVar()
    g.set('')
    checkinglabel=Label(f,textvariable=g, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("Comic Sans MS", "10", "normal"))
    b=YT(a,g)
    f.pack()
    checkinglabel.pack(side=RIGHT)
    b.pack(expand=True,fill=BOTH)
    a.mainloop()