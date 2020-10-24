from tkinter import *
import tkinter.ttk as ttk
import pytube
import sys
import threading
from tkinter import messagebox
try:
    from dir.root.__pre__ import *
except:
    from root.__pre__ import *
pytube.__main__.apply_descrambler = apply_descrambler
class Converter:
    @staticmethod
    def sizething(bytes):
        kb=bytes//1000
        mb=kb//1000
        ans='{} {}'.format(mb if mb!=0 else kb,'Mb' if mb!=0 else 'Kb')
        return ans

class DisplayBox(Frame):
    def __init__(self,parent,streams,status):
        super().__init__(parent)
        self.streams=streams
        self.status=status
    def streamsToList(self,stream):
        ans=[]
        for i in stream:
            type=i.type
            if type=='audio':                
                current=[str(i.itag),str(type),str(i.subtype),str(Converter.sizething(i.filesize)),str(i.abr)]
                if i.abr is None or i.abr=="None": print(i)
            else:
                extra=''
                if not i.is_progressive:extra+='Only '
                current=[str(i.itag),extra+str(type),str(i.subtype),str(Converter.sizething(i.filesize)),str(i.resolution)]
                if i.resolution is None or i.resolution=='None':
                    current.pop()
                    current.append(str(i.fps)+" fps")
            ans.append(current)
        return ans
    def getReady(self):
        self.MCanvas=Canvas(self)
        self.VFrame=Frame(self.MCanvas)
        self.MCanvas.bind('<Configure>',lambda e:self.MCanvas.configure(scrollregion=self.MCanvas.bbox('all')))
        self.MCanvas.bind_all('<MouseWheel>',self.orientScreen)
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
        Back.bind('<Button-1>',lambda x:self.selectit(itag['text'],Back))
        Type.bind('<Button-1>',lambda x:self.selectit(itag['text'],Back))
        filesize.bind('<Button-1>',lambda x:self.selectit(itag['text'],Back))
        subtype.bind('<Button-1>',lambda x:self.selectit(itag['text'],Back))
        quality.bind('<Button-1>',lambda x:self.selectit(itag['text'],Back))
        itag.bind('<Button-1>',lambda x:self.selectit(itag['text'],Back))
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
        a=messagebox.askyesno('Download ? ','Want to Download this Format?')
        if a:print(self.streams.get_by_itag(value))
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
        print(option1,option2)
        result=self.streamsToList(self.streams)
        self.appendTitle()
        for i in result:
            self.append(i)
        self.Vbar.pack(side=RIGHT,fill=Y)
        self.MCanvas.pack(fill=BOTH)
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
    def orientScreen(self,event):
        self.MCanvas.yview_scroll(int(-1*(event.delta/120)),'units')
class SearchingLabel(Label):
	def __init__(self,parent):
		super().__init__(parent)
		self.config(text='Searching.../...')
		self.toggle=False
		self.goon=True
		self.after(1000,self.change)
	def change(self):
		if not self.goon:
			self.config(text='Click to any stream to know to More/select it')
			return
		if self.toggle:self.config(text='Searching....\...')
		else:self.config(text='Searching.../....')
		self.toggle=not(self.toggle)
		self.after(500,self.change)
class SelectStream(Toplevel):
    def __init__(self,parent,options,var,heading):
        super().__init__(parent)
        self.config(bg='#D9D9D9')
        self.title(heading)
        self.status=StringVar()
        self.grab_set()
        self.geometry('400x510')
        self.resizable(0,0)
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
        self.setOptions()
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
        self.Check6=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' File Type',value=1,style='Customized.TRadiobutton')     
        if self.FirstOp.get()==3:
            self.Check7=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Bit rate  ',value=2,style='Customized.TRadiobutton')     
            self.Check8=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Size  ',value=3,style='Customized.TRadiobutton')     
        elif self.FirstOp.get()==2:
            self.Check7=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Resolution  ',value=2,style='Customized.TRadiobutton')     
            self.Check8=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Size  ',value=3,style='Customized.TRadiobutton')     
        elif self.FirstOp.get()==1:
            self.Check7=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Quality  ',value=2,style='Customized.TRadiobutton')     
            self.Check8=ttk.Radiobutton(self.Second,variable=self.SecondOp,text=' Size  ',value=3,style='Customized.TRadiobutton')     
        else:
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
            self.Check8.bind('<Enter>',lambda x:self.status.set(self.Check8['text']))
            self.Check8.bind('<Leave>',lambda x:self.status.set('ZzZzZzzZzzZZzzZZ')) 
            self.Check7.pack(side=LEFT)
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
if __name__=='__main__':
    link=input('Enter the Link: ')    
    try:
        ab=pytube.YouTube(link)
    except:
        sys.exit(0)
    try :
        liste=ab.streams
    except:
        liste=[]
    a=Tk()
    command=StringVar()
    heading=ab.title+' Youtube Video'
    Button(a,text='Open',command=lambda :SelectStream(a,liste,command,heading)).pack()
    a.mainloop()

