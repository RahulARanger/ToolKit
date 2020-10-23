from tkinter import *
try:
	from dir.root.ImageViewer import *
except:
	from root.ImageViewer import *
import tkinter.scrolledtext as scrolledtext
from tkinter import font
class Converter:
    @staticmethod
    def timething(gtime):
        print(type(gtime),gtime)
        hrs,sec,min=0,0,0
        if gtime>=3600:hrs=gtime%3600
        rem=gtime-(3600*hrs)
        print(gtime,rem)
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
class YTBackend():
    def __init__(self):
        self.Title='Testing'*1000
        self.Length=Converter.timething(2000)
        self.Rating=str(5)
        self.Views=str(3443245)
        self.Desc=''' 
        
        gdfg
        sf
        d
        f
        s'''
class TextBox(scrolledtext.ScrolledText):
    def __init__(self,p,text_):
        super().__init__(p)
        self.insert(END,text_)
        self.config(height=10)
        self.config(borderwidth=6) # ? design matters
        self.config(wrap=WORD)
        self.config(relief=RAISED)
        self.config(font= ('consolas', '12'))
        self.config(state=DISABLED)
        self.tag_add('title','1.0 linestart','1.0 lineend')
        self.tag_configure('title',foreground='#802A00',font=('consolas', '15','bold','underline'))
class ListBox(Frame):
    def __init__(self,p):
        super().__init__(p)     
        self.MCanvas=Canvas(self)
        self.VFrame=Frame(self.MCanvas)        
        self.Vbar=Scrollbar(self,orient=VERTICAL,command=self.MCanvas.yview)
        self.MCanvas.bind('<Configure>',lambda e:self.MCanvas.configure(scrollregion=self.MCanvas.bbox('all')))
        self.MCanvas.create_window((0,0),window=self.VFrame,anchor='nw')
        self.MCanvas.config(yscrollcommand=self.Vbar.set)
        self.MFrame=Frame(self.VFrame,bg='red')
        self.config(relief=FLAT)   
    def arrange(self):
        self.Vbar.pack(side=RIGHT,fill=Y)
        self.MCanvas.pack(fill=BOTH,expand=True,side=LEFT)
        self.MFrame.pack(fill=BOTH,expand=True)
    def addEntry(self,text_,color):
        lst=Frame(self.MFrame,borderwidth=3,relief=RIDGE,bg=color)
        a=StringVar()
        a.set(text_)
        textspace=Entry(lst,textvariable=a,relief=FLAT,width=60,font=('helvetica',12,'bold'))
        hbar=Scrollbar(lst,orient=HORIZONTAL,command=textspace.xview)
        textspace.config(xscrollcommand=hbar.set)        
        textspace['bg']='#FF5500'
        def hover(status):
            if status:
                textspace['bg']='#FF5500'
                hbar.pack(side=BOTTOM,fill=X)
            else:
                textspace['bg']='#FF7733'
                hbar.pack_forget()
        lst.bind('<Enter>',lambda x:hover(True))
        lst.bind('<Leave>',lambda x:hover(False))
        textspace.pack(ipady=6,fill=X)
        lst.pack(fill=X,expand=True)
    def addImage(self,image):
        global THUMBNAIL
        lst=Frame(self.MFrame,borderwidth=3,relief=SOLID,height=3)
        self.ThumbNail=ImageLabel(lst,THUMBNAIL,600,600)
        self.ThumbNail.bind('<Enter>',lambda x:self.ThumbNail.pack_configure(ipadx=3,ipady=3))
        self.ThumbNail.bind('<Leave>',lambda x:self.ThumbNail.pack_configure(ipadx=0,ipady=0))
        self.ThumbNail.pack(side=LEFT)
        
        lst.pack(fill=X,expand=True)
    def addTextBox(self,text_,color):
        lst=Frame(self.MFrame,borderwidth=3,relief=SOLID,bg=color,height=6)
        textspace=TextBox(lst,text_)
        textspace.pack(ipady=6,side=LEFT,fill=BOTH,expand=True)
        lst.pack(fill=X,expand=True)
class YTFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.MFrame=Frame(self)
        self.sfont=font.Font(family="Lucida Grande", size=14)
        self.config(borderwidth=6,relief=RIDGE,bg='purple')
        self.DetailsFrame=LabelFrame(self.MFrame,text='Details 🛈:',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.PackagesFrame=LabelFrame(self.MFrame,text='Available Formats:',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.SelectedFrame=LabelFrame(self.MFrame,text='Selected Format:',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.Backend=YTBackend()
        self.parse()
        self.arrange()
    def parse(self):
        self.Dlist=ListBox(self.DetailsFrame)
        self.Dlist1=ListBox(self.PackagesFrame)
        self.Dlist.addImage('temp\id6.jpg')
        self.Dlist1.addImage('temp\id6.jpg')
        self.TempTitle='Title: '+self.Backend.Title
        self.Dlist.addEntry(self.TempTitle,'orange')        
        self.Templength='Length: '+self.Backend.Length
        self.Dlist.addEntry(self.Templength,'orange')
        self.TempRating='Rating: '+self.Backend.Rating
        self.Dlist.addEntry(self.TempRating,'orange')
        self.TempViews='Views: '+self.Backend.Views
        self.Dlist.addEntry(self.TempViews,'orange')
        self.TempDesc='Description:\n\n'+self.Backend.Desc.strip()
        self.Dlist.addTextBox(self.TempDesc,'orange')
        self.Dlist.arrange()
        self.Dlist1.arrange()
        self.Dlist.pack(fill=BOTH,expand=True)
        self.Dlist1.pack(fill=BOTH,expand=True)        
    def arrange(self):
        self.MFrame.pack(fill=BOTH,expand=True)
        self.DetailsFrame.pack(fill=BOTH,side=LEFT,expand=True)
        self.PackagesFrame.pack(fill=BOTH,side=LEFT,expand=True)
        self.SelectedFrame.pack(fill=BOTH,side=LEFT,expand=True)
root=Tk()
f=Frame(root,bg='#FF4D4D')
g=YTFrame(f)
g.pack(fill=BOTH,expand=True)
f.pack(fill=BOTH,expand=True)

root.mainloop()