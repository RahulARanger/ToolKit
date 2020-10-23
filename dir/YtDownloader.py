from tkinter import *
import re
from tkinter import messagebox
from tkinter import font
import pytube
import threading 
import time
try:
    from dir.root.__pre__ import *
except:
    from root.__pre__ import *
try:
    from dir.root.Downloader import *
except:
    from root.Downloader import *
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
import tkinter.scrolledtext as scrolledtext
pytube.__main__.apply_descrambler = apply_descrambler
YTOBJ=None
STATUSE=None
THUMBNAIL=None
class Converter:
    @staticmethod
    def timething(gtime):
        print(type(gtime),gtime)
        hrs,sec,min=0,0,0
        if gtime>=3600:hrs=gtime%3600
        rem=gtime-(3600*hrs)
        if rem>=60:min=rem//60
        rem=rem-(60*min)
        if rem>0:sec=rem
        ans=''
        if hrs!=0:
            ans+=str(hrs)+' hr{} '.format('s' if hrs>1 else '')
        if min!=0:
            ans+=str(min)+' min{} '.format('s' if min>1 else '')
        if sec!=0:
            ans+=str(sec)+' sec{}'.format('s' if sec>1 else '')
        return ans
class TextBox(scrolledtext.ScrolledText):
    def __init__(self,p,text_):
        super().__init__(p)
        self.insert(END,text_)
        self.config(height=10)
        self.config(borderwidth=6) # ? design matters
        self.config(wrap=WORD)
        self.config(relief=RIDGE)
        self.config(font= ('consolas', '12'))
        self.config(state=DISABLED)
        self.tag_add('title','1.0 linestart','1.0 lineend')
        self.tag_configure('title',foreground='#802A00',font=('consolas', '15','bold','underline'))
class SpecialLabel(Label):
    def __init__(self,parent,text1,text2):
        super().__init__(parent)
        self.config(relief=FLAT,font=('helvetica',12,'bold'),anchor=NW)
        self.index=0
        if len(text2)>55:
            self.config(text=text1+text2[:55]+'...')
        else:
            self.config(text=text1+text2)
class ListBox(Frame):
    def __init__(self,p,status):
        super().__init__(p)   
        self.status=status  
        self.MFrame=Frame(self,bg='red')
        self.config(relief=FLAT)   
    def arrange(self):
        self.MFrame.pack(fill=BOTH,expand=True)
    def addEntry(self,text_,color,need=False):
        lst=Frame(self.MFrame,borderwidth=3,relief=RIDGE,bg=color)
        if need:
            textspace=SpecialLabel(lst,'Title: ',text_[6:])
        else:
            textspace=Label(lst,text=text_,relief=FLAT,font=('helvetica',12,'bold'),anchor=NW)
        textspace['bg']='#FF7733'
        def hover(status):
            if status:
                textspace['bg']='#FF5500'
                self.status.set(text_)                
            else:
                textspace['bg']='#FF7733'
                self.status.set('ZzZzZzzZzzZZzzZZ')
        lst.bind('<Enter>',lambda x:hover(True))
        lst.bind('<Leave>',lambda x:hover(False))
        textspace.pack(ipady=6,fill=X)
        lst.pack(fill=X,expand=True,side=TOP)
    def addImage(self,image):
        lst=Frame(self.MFrame,borderwidth=3,relief=SOLID,height=3)
        self.ThumbNail=ImageLabel(lst,THUMBNAIL,600,600)
        self.ThumbNail.pack(side=LEFT) 
        lst.bind('<Enter>',lambda z:self.status.set('Thumbnail'))
        lst.bind('<Leave>',lambda z:self.status.set('ZzZzZzzZzzZZzzZZ'))       
        lst.pack(fill=X,expand=True,side=TOP)
    def addTextBox(self,text_,color):
        lst=Frame(self.MFrame,borderwidth=3,relief=SOLID,bg=color,height=6)
        textspace=TextBox(lst,text_)
        textspace.pack(ipady=6,side=LEFT,fill=BOTH,expand=True)
        lst.bind('<Enter>',lambda z:self.status.set('Description'))
        lst.bind('<Leave>',lambda z:self.status.set('ZzZzZzzZzzZZzzZZ'))       
        lst.pack(fill=X,expand=True,side=TOP)
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
            self.status.set(self.var.get())
        else:
            self.config(relief=FLAT,fg='grey')
            self.status.set('ZzZzZzzZzzZZzzZZ')
    def check(self,*args):
        if self.var.get()=='Enter the Link: ':
            self.var.set('')        
class LoadingFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.config(bg='#FF4D4D')
        self.photos=['Resources\Media\Loading\Loading{}.jpg'.format(i) for i in range(8)]
        self.LoadingScreen=ImageAlbum(self,self.photos,1000,1000,110,'#FF4D4D')
        self.LoadingScreen.pack(fill=BOTH,expand=True)
class WaitingFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.config(bg='#FF4D4D')
        self.photos=['Resources\Media\Waiting\Waiting{}.jpg'.format(i) for i in range(45)]
        self.WaitingScreen=ImageAlbum(self,self.photos,800,800,100,'#FF4D4D')
        self.WaitingScreen.pack(fill=BOTH,expand=True)
    def unhide(self):
        self.WaitingScreen.pack(fill=BOTH,expand=True)
        self.pack(fill=BOTH,expand=True)
    def hide(self):
        self.WaitingScreen.pack_forget()
        self.pack_forget()
class Tester:
    def __init__(self,link,func):
        self.link=link.strip()
        self.func=func
    def checkLink(self):
        global STATUSE,YTOBJ,THUMBNAIL
        STATUSE=None
        regex=r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
        result=re.findall(regex,self.link)
        if len(result)==0:
            STATUSE=False
            return False
        note=time.time()
        for i in range(3):
            print(i)
            if i>=1:
                if time.time()-note>10:
                    break
            try:
                a=pytube.YouTube(self.link)
                YTOBJ=a
                STATUSE=True
                break
            except:
                STATUSE=False  
        if STATUSE:
            x=Downloader(YTOBJ.thumbnail_url,'temp')
            THUMBNAIL=x.manual_install()
    def __del__(self):
        self.func(self.link)
class YTBackend:
    def __init__(self):
        global YTOBJ
        self.obj=YTOBJ
        self.parseDetails()
        self.parseStreams()
    def parseDetails(self):
        self.Title=YTOBJ.title
        self.Desc=YTOBJ.description
        self.Rating=str(YTOBJ.rating)
        self.Views=str(YTOBJ.views)
        self.Length=Converter.timething(YTOBJ.length)
    def parseStreams(self):
        pass
class YTFrame(Frame):
    def __init__(self,p,status):
        super().__init__(p)
        self.status=status
        self.MFrame=Frame(self)
        self.config(borderwidth=10,relief=RIDGE)
        self.sfont=font.Font(family="Lucida Grande", size=14)
        self.config(borderwidth=6,relief=RIDGE,bg='purple')
        self.DetailsFrame=LabelFrame(self.MFrame,text='Details 🛈:',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.SelectedFrame=LabelFrame(self.MFrame,text='Selected Format:',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.Backend=YTBackend()    
        self.parse()
        self.arrange()
    def parse(self):
        self.Dlist=ListBox(self.DetailsFrame,self.status)
        self.MoreInfo=LabelFrame(self.SelectedFrame,text='More Info:',font=self.sfont,borderwidth=2,relief=RIDGE,bg='#FF3333',labelanchor=N)
        self.Dlist2=ListBox(self.MoreInfo,self.status)
        if THUMBNAIL is not None:self.Dlist.addImage(THUMBNAIL)
        self.TempTitle='Title: '+self.Backend.Title
        self.Dlist.addEntry(self.TempTitle,'orange',True)  
        self.Templength='Length: '+self.Backend.Length
        self.Dlist.addEntry(self.Templength,'orange')   
        self.TempRating='Rating: '+self.Backend.Rating
        self.Dlist.addEntry(self.TempRating,'orange')
        self.TempViews='Views: '+self.Backend.Views
        self.Dlist.addEntry(self.TempViews,'orange')
        self.TempDesc='Description:\n\n'+self.Backend.Desc.strip()
        self.Dlist2.addTextBox(self.TempDesc,'orange')     
        self.Dlist.arrange()
        self.Dlist2.arrange()
        self.Dlist.pack(fill=X,side=TOP)
        self.Dlist2.pack(fill=X,expand=True,side=TOP)
        self.MoreInfo.pack(fill=X)
    def arrange(self):
        self.MFrame.pack(expand=True,fill=BOTH)
        self.DetailsFrame.pack(fill=BOTH,side=LEFT)
        self.SelectedFrame.pack(fill=BOTH,side=LEFT,expand=True)
    def unhide(self):
        self.pack(fill=BOTH,expand=True)
    def hide(self):
        self.pack_forget()
class YT(Frame):
    def __init__(self,parent,s):
        super().__init__(parent) 
        self.config(bg='#FF4D4D')
        self.link=StringVar()
        self.checker=NetworkCheck()
        self.status=s
        self.DummyFrame=Frame(self,bg='#FF4D4D',relief=GROOVE,borderwidth=2)
        self.FirstFrame=Frame(self.DummyFrame,bg='#FF4D4D',relief=GROOVE,borderwidth=2)
        self.DummyFrame2=Frame(self,bg='#FF4D4D',relief=GROOVE,borderwidth=2)
        self.SecondFrame=Frame(self.DummyFrame2,bg='orange',relief=GROOVE,borderwidth=3,width=1000,height=1000)
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
        self.Justasec=LoadingFrame(self.SecondFrame)
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
        self.DummyFrame.pack(fill=BOTH,expand=True)
        self.DummyFrame2.pack(fill=BOTH,expand=True,ipady=50)
        self.FirstFrame.pack(pady=20)
        self.SecondFrame.pack(fill=BOTH,expand=True)
        self.EnterFrame.pack(side=LEFT,pady=(10,0))
        self.SearchButton.pack(side=LEFT,fill=Y)
        self.Enter.pack(fill=BOTH)
        self.hbar.pack(fill=X,side=BOTTOM)
        self.ContainFrame.pack(fill=BOTH,expand=True)
    def check(self,*args):
        self.status.set('Loading...')
        self.SearchButton.config(state=DISABLED)
        link=self.link.get()
        if self.READY is True:
            a=messagebox.askyesno('Alert!!!','Ready to Lose Current Details?',icon='warning')
            if a is False:
                self.SearchButton.config(state=NORMAL)
                return
        self.ContainFrame.pack_forget()  
        self.Justasec.pack(fill=BOTH,expand=True)
        if True:
            tester=Tester(link,self.soNext)
            Hire=threading.Thread(target=tester.checkLink)
            Hire.start()
    def soNext(self,link):
        global STATUSE
        print(STATUSE)
        try:
            self.Justasec.pack_forget()
        except:pass
        self.ContainFrame.hide()
        if STATUSE:
            if self.READY:
                self.LINK=link
                self.ContainFrame.unbind('<Enter>')
                self.ContainFrame.unbind('<Leave>')
                self.ContainFrame=YTFrame(self.SecondFrame,self.status)
                self.ContainFrame.pack(fill=BOTH,expand=True)
                
                self.link.set(self.LINK)
                self.Enter.icursor(self.Enter.index(END))
            else:
                self.LINK=link
                self.ContainFrame.unbind('<Enter>')
                self.ContainFrame.unbind('<Leave>')
                self.ContainFrame=YTFrame(self.SecondFrame,self.status)
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