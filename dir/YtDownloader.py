from tkinter import *
import re
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import pytube
import threading 
import time
import os
try:
    from  dir.root.OtherButtonClick import *
except:
    from root.OtherButtonClick import *
import tkinter.ttk as ttk
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
try:
    from dir.root.LogFiles import *
except:
    from root.LogFiles import *
import tkinter.scrolledtext as scrolledtext
pytube.__main__.apply_descrambler = apply_descrambler
YTOBJ=None
STATUSE=None
THUMBNAIL=None
class Warning:
    object=None
    stopped=False
    store=[]
    @staticmethod
    def checkThis():
        if Warning.object.uploaded is True:
            Warning.stopped=True
            Warning.store.append(Warning.object.file)
            Warning.store.append(Warning.object.selected.get())
            Warning.object.selected.set('')
    @staticmethod
    def restoreThis():
        if Warning.stopped:
            Warning.object.selected.set(Warning.store[1])
            Warning.object.file=(Warning.store[0])
            Warning.object.uploaded=True
pygame.mixer.init()
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
    @staticmethod
    def sizething(bytes):
        kb=bytes//1000
        mb=kb//1000
        ans='{} {}'.format(mb if mb!=0 else kb,'Mb' if mb!=0 else 'Kb')
        return ans
    @staticmethod
    def sortBits(l):
        regex=r'[0-9]+'
        ans=int(re.findall(regex,l)[0])
        return ans
class StreamDownloader(Toplevel):
    def __init__(self,p):
        super().__init__(p)
        self.finished=False
        self.title('Downloader')
        self.MFrame=Frame(self,bg='orange')
        self.ActionStatus=IntVar()
        self.cancelled=False
        self.pause=False
        self.canclose=False
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.StatusFrame=Frame(self.MFrame,bg='#4DA6FF',borderwidth=3,relief=GROOVE)
        self.Cancel=Button(self.StatusFrame,text='Cancel',relief=FLAT,command=self.cancelit,bg='#6AFF4D')
        self.Action=Button(self.StatusFrame,text='Pause',relief=FLAT,bg='#6AFF4D',command=self.pauseit)
        self.Cancel.bind('<Enter>',lambda x:self.Cancel.config(bg='#40FF19'))
        self.Cancel.bind('<Leave>',lambda x:self.Cancel.config(bg='#6AFF4D'))
        self.Action.bind('<Enter>',lambda x:self.Action.config(bg='#40FF19'))
        self.Action.bind('<Leave>',lambda x:self.Action.config(bg='#6AFF4D'))
        self.ProgressArea=Frame(self.MFrame,bg='#FF5500',relief=RIDGE,borderwidth=3)
        self.Lb=Label(self.ProgressArea,text='Progress: ',borderwidth=3,bg='#FF5500',fg='#004D4D',height=2,font=("Times", 15, "bold"))
        self.arrange()
    def pauseit(self):
        if self.pause:
            self.Action.config(text='Pause')
            self.pause=False
        else:
            self.Action.config(text='Resume')
            self.pause=True
    def closing(self):
        if self.canclose:
            self.destroy()
    def cancelit(self):
        truth=messagebox.askyesno('Cancel?','Cancel the download?',parent=self)
        if truth:
            self.pause=False
            self.cancelled=True
            self.canclose=True
    def arrange(self):
        self.MFrame.pack(fill=BOTH)
        self.ProgressArea.pack(side=TOP)
        self.Lb.pack(side=LEFT,padx=6)
        self.StatusFrame.pack(side=BOTTOM,fill=X)
        self.Cancel.pack(side=RIGHT)
        self.Action.pack(side=LEFT)
    def download(self):
        while True:
            try:
                with open(self.location,'wb') as hand:
                    streams=pytube.request.stream(self.stream.url)
                    downloaded=0
                    percent='Downloaded {}% {}'.format(0,self.stream.title)
                    started.debug('Downloaing '+self.stream.title[:9]+'..')
                    self.title(percent)
                    self.PB=ttk.Progressbar(self.ProgressArea,orient=HORIZONTAL,mode = 'determinate',maximum=self.stream.filesize,length=300)
                    self.PB.pack(side=LEFT,padx=6)
                    while True:
                        if self.pause:
                            continue
                        if self.cancelled:
                            break
                        percent='Downloaded {}% {}'.format(round(downloaded/self.stream.filesize,2)*100,self.stream.title)
                        self.title(percent)
                        self.PB['value']=downloaded
                        chunk=next(streams,None)
                        if chunk:
                            hand.write(chunk)
                            downloaded+=len(chunk)
                        else:
                            break
                self.title('Downloaded')
                
                if self.cancelled:
                    if os.path.exists(self.location):
                        os.remove(self.location)
                    started.warning('Cancelled '+self.stream.title[:9]+'..')
                else:
                    started.debug('Downlaoded '+self.stream.title[:9]+'..')
                break
            except Exception as e:
                print(e)
                started.error('Network Error for '+self.stream.title[:9]+'..')
                test=messagebox.askyesno('Distrubted','Might be Low Internet connection! Want to Retry?',parent=self)
                if not test:
                    if os.path.exists(self.location):
                        os.remove(self.location)
                    break
        self.canclose=True
        STARTTIME.play()
        self.destroy()
    def addMember(self,stream,loc):
        self.stream=stream
        self.location=loc
        omega=threading.Thread(target=self.download,daemon=True)
        omega.start()
class DisplayBox(Frame):
    def __init__(self,parent,streams,status):
        super().__init__(parent)
        self.streams=streams
        self.status=status
    def streamsToList(self,stream,op1,op2):
        ans=[]
        allowvarient,allowvideo,allowaudio=False,False,False
        if op1==0:
            allowaudio=True
            allowvideo=True
            allowvarient=True
        elif op1==1:
            allowvarient=True
        elif op1==2:
            allowvideo=True
        elif op1==3:
            allowaudio=True
        for i in stream:
            type=i.type
            current=[]
            if type=='audio': 
                if allowaudio:  
                    exe=str(i.subtype)
                    current=[str(i.itag),str(type),exe,str(Converter.sizething(i.filesize)),str(i.abr),i.filesize]
                    if i.abr is None or i.abr=="None": 
                        print(i)
            else:
                if allowvideo or allowvarient:
                    flag=False
                    if not i.is_progressive:
                        if allowvideo:
                            current=[str(i.itag),'Only '+str(type),str(i.subtype),str(Converter.sizething(i.filesize)),str(i.resolution)]
                            flag=True
                    if  i.is_progressive:
                        if allowvarient:
                            current=[str(i.itag),str(type),str(i.subtype),str(Converter.sizething(i.filesize)),str(i.resolution)]
                            flag=True
                    if flag:
                        if current[4]=='None':
                            current.pop()
                            current.append(str(i.fps)+" fps")
                        current.append(i.filesize)
            if len(current)!=0:ans.append(current)
            if op2==0:ans=sorted(ans,key=lambda x:x[-1])
            elif op2==1:ans=sorted(ans,key=lambda x:x[2])
            elif op2==2:
                if op1==0:ans=sorted(ans,key=lambda x:x[1])
                else:
                    if op1==3:
                        ans=sorted(ans,key=lambda x:Converter.sortBits(x[4]))
                    else:
                        ans=sorted(ans,key=lambda x:x[4])
        return ans
    def getReady(self):
        self.MCanvas=Canvas(self)
        self.VFrame=Frame(self.MCanvas)
        self.MCanvas.bind('<Configure>',lambda e:self.MCanvas.configure(scrollregion=self.MCanvas.bbox('all')))
        self.MCanvas.create_window((0,0),window=self.VFrame,anchor='nw',width=1350)
        self.Vbar=Scrollbar(self,orient=VERTICAL,command=self.MCanvas.yview)        
        self.MCanvas.config(yscrollcommand=self.Vbar.set)
    def append(self,lst):
        Back=Frame(self.VFrame,borderwidth=3,relief=FLAT)
        itag=Label(Back,text=lst[0],bg='#FF8000',width=6,justify=CENTER,relief=SOLID)
        Type=Label(Back,text=lst[1],bg='#00CCAA',width=11,justify=CENTER,relief=SOLID)
        subtype=Label(Back,text=lst[2],bg='#FFFF19',width=12,justify=CENTER,relief=SOLID)
        filesize=Label(Back,text=lst[3],bg='violet',width=9,justify=CENTER,relief=SOLID)
        quality=Label(Back,text=lst[4],bg='#FF4DFF',width=10,justify=CENTER,relief=SOLID)
        itag.bind('<Enter>',lambda x:self.status.set("Itag: {}".format(itag['text'])))
        itag.bind('<Leave>',lambda x:self.status.set("ZzzzZZZzZZZ"))
        Type.bind('<Enter>',lambda x:self.status.set("Type: {}".format(Type['text'])))
        Type.bind('<Leave>',lambda x:self.status.set("ZzzzZZZzZZZ"))
        subtype.bind('<Enter>',lambda x:self.status.set("Extension: {}".format(subtype['text'])))
        subtype.bind('<Leave>',lambda x:self.status.set("ZzzzZZZzZZZ"))
        filesize.bind('<Enter>',lambda x:self.status.set("File Size: {}".format(filesize['text'])))
        filesize.bind('<Leave>',lambda x:self.status.set("ZzzzZZZzZZZ"))
        quality.bind('<Enter>',lambda x:self.status.set("Quality: {}".format(quality['text'])))
        quality.bind('<Leave>',lambda x:self.status.set("ZzzzZZZzZZZ"))
        Back.bind('<Enter>',lambda x:Back.config(relief=FLAT))
        Back.bind('<Leave>',lambda x:Back.config(relief=RAISED))
        Back.bind('<Double-Button-1>',lambda x:self.selectit(itag['text'],Back))
        Type.bind('<Double-Button-1>',lambda x:self.selectit(itag['text'],Back))
        filesize.bind('<Double-Button-1>',lambda x:self.selectit(itag['text'],Back))
        subtype.bind('<Double-Button-1>',lambda x:self.selectit(itag['text'],Back))
        quality.bind('<Double-Button-1>',lambda x:self.selectit(itag['text'],Back))
        itag.bind('<Double-Button-1>',lambda x:self.selectit(itag['text'],Back))
        Back.bind('<Button-1>',lambda x:Back.config(relief=RAISED))
        Type.bind('<Button-1>',lambda x:Back.config(relief=RAISED))
        subtype.bind('<Button-1>',lambda x:Back.config(relief=RAISED))
        quality.bind('<Button-1>',lambda x:Back.config(relief=RAISED))
        filesize.bind('<Button-1>',lambda x:Back.config(relief=RAISED))
        Back.bind('<ButtonRelease-1>',lambda x:Back.config(relief=FLAT))
        Type.bind('<ButtonRelease-1>',lambda x:Back.config(relief=FLAT))
        subtype.bind('<ButtonRelease-1>',lambda x:Back.config(relief=FLAT))
        quality.bind('<ButtonRelease-1>',lambda x:Back.config(relief=FLAT))
        filesize.bind('<ButtonRelease-1>',lambda x:Back.config(relief=FLAT))
        itag.bind('<ButtonRelease-1>',lambda x:Back.config(relief=FLAT))
        itag.pack(fill=X,side=LEFT)
        Type.pack(fill=X,side=LEFT)
        subtype.pack(fill=X,side=LEFT)
        filesize.pack(fill=X,side=LEFT)
        quality.pack(fill=X,side=LEFT)
        Back.pack(fill=X,expand=True)
    def selectit(self,value,w):
        w.config(relief=RAISED)
        a=messagebox.askyesno('Download ? ','Want to Download this Format?',parent=self)
        if a:
            do_this=self.streams.get_by_itag(value)
            extension='.'+do_this.subtype
            loc=filedialog.asksaveasfilename(title='We can Just Enter the File Name',filetypes=[(do_this.type,extension)],parent=self)+extension
            if len(loc)!=0:
                self.downloader=StreamDownloader(self)
                STOPTIME.play()
                self.downloader.addMember(do_this,loc)
        else:pass        
    def appendTitle(self):
        Back=Frame(self.VFrame,borderwidth=3,relief=FLAT)
        itag=Label(Back,text="Id",bg='#FF5500',width=6,justify=CENTER,relief=RAISED)
        Type=Label(Back,text="Type",bg='#00FFD5',width=11,justify=CENTER,relief=RAISED)
        subtype=Label(Back,text="File Extension",bg='#FFFF19',width=12,justify=CENTER,relief=RAISED)
        filesize=Label(Back,text="File Size",bg='#AA00FF',width=9,justify=CENTER,relief=RAISED)
        quality=Label(Back,text="Quality",bg='#FF00FF',width=10,justify=CENTER,relief=RAISED)
        itag.pack(fill=X,side=LEFT)
        Type.pack(fill=X,side=LEFT)
        subtype.pack(fill=X,side=LEFT)
        filesize.pack(fill=X,side=LEFT)
        quality.pack(fill=X,side=LEFT)
        Back.pack(fill=X,expand=True)
    def go(self,option1,option2):
        try:
            result=self.streamsToList(self.streams,option1,option2)
            self.appendTitle()
            for i in result:
                self.append(i)
            self.Vbar.pack(side=RIGHT,fill=Y)
            self.MCanvas.pack(fill=BOTH)
        except:
            print('Neo Armstrong Cyclone Jet Armstrong Cannon')
    def hover(self,lst,status=None,lvl=None):
        if status:
            lst.config(bg='red',font=('helvetica',13,'bold'))
        else:
            lst.config(bg='orange',font=('helvetica',12,'bold'))
    def remove(self):
        try:self.MCanvas.destroy()
        except:pass
        try:self.Vbar.destroy()
        except:pass    
class SearchingLabel(Label):
	def __init__(self,parent):
		super().__init__(parent)
		self.config(text='Searching.../...')
		self.toggle=False
		self.goon=True
		self.after(1000,self.change)
	def change(self):
		if not self.goon:
			self.config(text='Double Click to Download it')
			return
		if self.toggle:self.config(text='Searching....\...')
		else:self.config(text='Searching.../....')
		self.toggle=not(self.toggle)
		self.after(500,self.change)
class SelectStream(Toplevel):
    def __init__(self,parent,options,var,heading):
        super().__init__(parent)
        if Warning.object.uploaded is True:
            errormsg='''
    Well it seems the media Player has imported Mp3 file 

    For some instance music wil be stopped unless the stream Window is Closed 

    Sorry for inconvivence i will try my best to work on this as soon as possible

'''
            messagebox.showerror('Sorry for inconvivence',errormsg,parent=self)
            Warning.checkThis()
        self.config(bg='#D9D9D9')
        self.title(heading)
        self.status=StringVar()
        self.grab_set()
        self.resizable(0,0)
        self.geometry('400x510')        
        self.TopFrame=Frame(self,bg='#D9D9D9')
        self.First=LabelFrame(self.TopFrame,text='Type:',bg='#D9D9D9')
        self.Second=LabelFrame(self.TopFrame,text='Sort By: ',bg='#D9D9D9')        
        self.Confirm=LabelFrame(self.TopFrame,bg='#D9D9D9',text='Info')
        self.Confirm.bind('<Enter>',lambda x:self.status.set('Information'))
        self.Confirm.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ'))        
        self.Fourth=LabelFrame(self.TopFrame,text='Formats Available: ',bg='#D9D9D9')
        self.Display=DisplayBox(self.Fourth,options,self.status)
        self.StatusFrame=Frame(self.TopFrame,bg='#D9D9D9')
        self.checkinglabel=Label(self.StatusFrame,textvariable=self.status, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("Comic Sans MS", "10", "normal"))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setOptions()
    def on_closing(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        Warning.restoreThis()
        self.destroy()
    def setOptions(self):
        self.FirstOp=IntVar()
        self.SecondOp=IntVar()
        self.FirstOp.set(0)
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('Customized.TRadiobutton',indicatorrelief=RIDGE,
                        indicatordiameter=20,
                        relief=RAISED,
                        focusthickness=2, highlightthickness=2, padding=5)
        self.Check1=ttk.Radiobutton(self.First,variable=self.FirstOp,text=' Mixed  ',value=0,style='Customized.TRadiobutton')     
        self.Check2=ttk.Radiobutton(self.First,variable=self.FirstOp,text=' Video + Audio  ',value=1,style='Customized.TRadiobutton')     
        self.Check3=ttk.Radiobutton(self.First,variable=self.FirstOp,text=' Video  ',value=2,style='Customized.TRadiobutton')
        self.Check4=ttk.Radiobutton(self.First,variable=self.FirstOp,text=' Audio  ',value=3,style='Customized.TRadiobutton')  
        self.Check1.bind('<Enter>',lambda x:self.status.set('All Formats'))
        self.Check1.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
        self.Check3.bind('<Enter>',lambda x:self.status.set('Only Video'))
        self.Check3.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ'))
        self.Check4.bind('<Enter>',lambda x:self.status.set('Only Audio'))
        self.Check4.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
        self.Check2.bind('<Enter>',lambda x:self.status.set('Video + Audio'))
        self.Check2.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ'))      
        self.arrange()
        self.setAnotherOptions()
        self.setLastOptions()
        self.setChoices()
        self.FirstOp.trace('w',self.setAnotherOptions)
    def setAnotherOptions(self,*args):
        self.SecondOp.set(0)
        try:
            self.Check5.destroy()
        except:pass
        try:self.Check6.destroy()
        except:pass
        try:self.Check7.destroy()
        except:pass
        try:self.Check8.destroy()
        except:pass
        flag=False
        self.Check5=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' File Size  ',value=0,style='Customized.TRadiobutton')     
        self.Check6=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' File Extension',value=1,style='Customized.TRadiobutton')     
        if self.FirstOp.get()==3:
            self.Check7=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Bit rate  ',value=2,style='Customized.TRadiobutton')     
            self.Check8=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Size  ',value=3,style='Customized.TRadiobutton')     
        elif self.FirstOp.get()==2:
            self.Check7=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Resolution  ',value=2,style='Customized.TRadiobutton')     
        elif self.FirstOp.get()==1:
            self.Check7=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Quality  ',value=2,style='Customized.TRadiobutton')     
        else:
            self.Check8=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' File Type  ',value=3,style='Customized.TRadiobutton')
            flag=True
        self.Check5.bind('<Enter>',lambda x:self.status.set(self.Check5['text']))
        self.Check5.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
        self.Check6.bind('<Enter>',lambda x:self.status.set(self.Check6['text']))
        self.Check6.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
        self.Check5.pack(side=LEFT)
        self.Check6.pack(side=LEFT)
        if not flag:
            self.Check7.bind('<Enter>',lambda x:self.status.set(self.Check7['text']))
            self.Check7.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
            self.Check7.pack(side=LEFT)
        else:
            self.Check8.bind('<Enter>',lambda x:self.status.set(self.Check8['text']))
            self.Check8.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
            self.Check8.pack(side=LEFT)  
    def setLastOptions(self):        
        self.ConfirmThis=Button(self.Confirm,text='Confirm',command=self.initiated)
        self.ConfirmThis.bind('<Enter>',lambda x:self.status.set('Display Formats?'))
        self.ConfirmThis.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ'))
        self.ConfirmThis.pack(side=RIGHT)
        self.initiated()
    def tour(self):
        self.Display.remove()
        self.Display.getReady()
        self.Display.go(self.FirstOp.get(),self.SecondOp.get())
        self.searching.goon=False
    def initiated(self,*args):
        try:self.searching.destroy()
        except:pass
        self.searching=SearchingLabel(self.Confirm)
        self.after(100)
        self.searching.pack(side=LEFT)
        self.searching.bind('<Enter>',lambda x:self.status.set(self.searching['text']))
        self.searching.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ'))
        if True:
            omega=threading.Thread(target=self.tour)
            omega.start()
    def arrange(self):
        self.TopFrame.pack(side=TOP,fill=X)
        self.Check1.pack(side=LEFT)
        self.Check2.pack(side=LEFT)
        self.Check3.pack(side=LEFT)
        self.Check4.pack(side=LEFT)
        self.First.pack(fill=X,padx=3,pady=3)
        self.Second.pack(fill=X,padx=3,pady=3)        
        self.Confirm.pack(fill=X,padx=3,pady=3)
        self.Fourth.pack(fil=X,padx=3,pady=3)
        self.StatusFrame.pack(side=BOTTOM,fill=X,padx=3,pady=3)
        self.checkinglabel.pack(side=LEFT)
    def setChoices(self):
        self.Display.pack()
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
        self.LoadingScreen=ImageAlbum(self,self.photos,800,800,110,'#FF4D4D')
        self.LoadingScreen.pack(fill=BOTH,expand=True)
class WaitingFrame(Frame):
    def __init__(self,p):
        super().__init__(p)
        self.config(bg='#FF4D4D')
        self.photos=['Resources\Media\Lalala\Lalala{}.jpg'.format(i) for i in range(10)]
        self.WaitingScreen=ImageAlbum(self,self.photos,400,400,100,'#FF4D4D')
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
        for i in range(6):
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
        self.streams=YTOBJ.streams
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
        self.DetailsFrame=LabelFrame(self.MFrame,text='Details :',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.SelectedFrame=LabelFrame(self.MFrame,text='Selected Format:',bg='#FF3333',font=self.sfont,borderwidth=3,relief=RAISED)
        self.Backend=YTBackend()    
        self.parse()
        self.arrange()
    def parse(self):
        self.Dlist=ListBox(self.DetailsFrame,self.status)
        self.MoreInfo=LabelFrame(self.SelectedFrame,text='More Info:',font=self.sfont,borderwidth=2,relief=RIDGE,bg='#FF3333',labelanchor=N)
        self.SearchFormats=LabelFrame(self.SelectedFrame,text='Search:',font=self.sfont,borderwidth=2,relief=RIDGE,bg='#FF3333',labelanchor=N)
        self.Dlist2=ListBox(self.MoreInfo,self.status)
        if THUMBNAIL is not None:self.Dlist.addImage(THUMBNAIL)
        self.TempTitle='Title: '+self.Backend.Title
        self.Dlist.addEntry(self.TempTitle,'orange',True)  
        self.Templength='Length: '+self.Backend.Length
        self.Dlist.addEntry(self.Templength,'orange')   
        self.TempRating='Rating: '+self.Backend.Rating
        self.Dlist2.addEntry(self.TempRating,'orange')
        self.TempViews='Views: '+self.Backend.Views
        self.Dlist2.addEntry(self.TempViews,'orange')
        check=len(self.Backend.Desc.strip())
        if check==0 or check==1:
            self.Backend.Desc='<Empty Description>'
        self.TempDesc='Description:\n\n'+self.Backend.Desc.strip()
        self.Dlist2.addTextBox(self.TempDesc,'orange')     
        self.Dlist.arrange()
        self.Dlist2.arrange()
        self.Dlist.pack(fill=X,side=TOP)
        self.Dlist2.pack(fill=X,expand=True,side=TOP)
        self.MoreInfo.pack(fill=X)
        self.SearchingFrame=Frame(self.SearchFormats)
        self.SearchForit=Label(self.SearchFormats,text='Search Streams: ',bg='#FF3333',font=self.sfont)
        self.Searchit=Button(self.SearchFormats,text='Open',command=lambda :self.openStreamWindow(),bg='#FFFF00',fg='#194D00',font=self.sfont)
        self.Searchit.bind('<Enter>',lambda x:self.bthover(True))
        self.Searchit.bind('<Leave>',lambda x:self.bthover(False))
        self.SearchForit.pack(side=LEFT,pady=3)
        self.Searchit.pack(padx=6,pady=6,side=LEFT)
        self.SearchingFrame.pack(fill=X)
        self.SearchFormats.pack(fill=X)
    def bthover(self,status):
        if status:
            self.Searchit.config(bg='#E6E600')
        else:
            self.Searchit.config(bg='#FFFF00')
    def openStreamWindow(self):
        SelectStream(self,self.Backend.streams,StringVar(),self.Backend.Title)
        self.status.set('Opening Stream Window....')
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
        self.ContainFrame.pack(fill=BOTH,expand=True,ipady=20)
    def check(self,*args):
        self.status.set('Loading...')
        self.SearchButton.config(state=DISABLED)
        link=self.link.get()
        if self.READY is True:
            a=messagebox.askyesno('Alert!!!','Ready to Lose Current Details?',icon='warning',parent=self)
            if a is False:
                self.SearchButton.config(state=NORMAL)
                return
        self.ContainFrame.pack_forget()  
        self.Justasec.pack(fill=BOTH,expand=True)
        LOADING.play(loops=-1)
        if True:
            tester=Tester(link,self.soNext)
            Hire=threading.Thread(target=tester.checkLink)
            Hire.start()
    def soNext(self,link):
        global STATUSE
        print(STATUSE)
        try:
            self.Justasec.pack_forget()
            LOADING.stop()
        except:pass
        self.ContainFrame.hide()
        if STATUSE:
            if self.READY:
                self.LINK=link
                self.ContainFrame.unbind('<Enter>')
                self.ContainFrame.unbind('<Leave>')
                self.ContainFrame=YTFrame(self.SecondFrame,self.status)
                self.ContainFrame.pack(fill=BOTH,expand=True,ipady=20)
                
                self.link.set(self.LINK)
                self.Enter.icursor(self.Enter.index(END))
            else:
                self.LINK=link
                self.ContainFrame.unbind('<Enter>')
                self.ContainFrame.unbind('<Leave>')
                self.ContainFrame=YTFrame(self.SecondFrame,self.status)
                self.ContainFrame.pack(fill=BOTH,expand=True,ipady=20)
                
            self.READY=True
            self.status.set('ZzZzZzzZzzZZzzZZ')
        else:
            warningmsg='''
Sorry we were not able to fetch info. from the given Link

Possible Reasons are:

*  Given Link is not related to Youtube Video at all

*  Given Link contains Age Restricted or Restricted  Towards certain age group

*  Due to Some Connection Errors

* If this is not the case, then please Use the Help Button and post an issue in the repo.

Most Importantly Try to open the link again this app it may work!
            '''
            a=messagebox.showwarning('Alert!!!',warningmsg,icon='warning')
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
            if self.failed is False:
                started.error('Lost Network')
                a=NIC(self)
            self.failed=True
            self.pack_forget()
        else:
            if self.failed:
                self.pack(fill=BOTH,expand=True)
                self.failed=False
                started.warning('Regained Net Access')
        self.after(3000,self.checknet)  
if __name__=='__main__':
    a=Tk()
    f=Frame(a,bg='#FF4D4D')
    g=StringVar()
    g.set('')
    checkinglabel=Label(f,textvariable=g, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("Comic Sans MS", "10", "normal"))
    b=YT(a,g,None,None)
    f.pack()
    checkinglabel.pack(side=RIGHT)
    b.pack(expand=True,fill=BOTH)
    a.mainloop()