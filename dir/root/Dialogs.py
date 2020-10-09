from tkinter import *
try:
    from ImageViewer import *
except:
    try:
        from root.ImageViewer import *
    except:
        from dir.root.ImageViewer import *
class FutureUpdate(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='orange')
        self.overrideredirect(True)
        self.ok=Button(self,text='Ok',command=self.on_closing,borderwidth=6)
        self.show=ImageLabel(self,'Resources\Media\\updatenotice.jpeg',600,600)
        self.ok.config(relief=FLAT)
        self.ok.config(bg='#FF8000')
        self.arrange()
        self.show.pack()
        self.ok.pack(fill=X)
    def on_closing(self,*args):
        self.destroy()
    def arrange(self):
        self.ok.bind('<Enter>',lambda x:self.bthover(True))
        self.ok.bind('<Leave>',lambda x:self.bthover(False))
    def bthover(self,status):
        if status:
            self.ok.config(bg='#f27a00',relief=GROOVE)
        else:
            self.ok.config(bg='#FF8000',relief=FLAT)
class Warning(Toplevel):
    def __init__(self,parent,bt=None):
        super().__init__(parent)
        self.config(bg='red')  
        self.things=bt
        self.overrideredirect(True)
        if self.things is not None:self.things.config(state=DISABLED)
        self.display=ImageLabel(self,'Resources\Media\\warning.jpeg',200,200)
        self.Close=Button(self,text="Ok",relief=FLAT,bg='red',activebackground='yellow',fg='orange',command=self.on_closing)         
        self.Close.bind('<Enter>',lambda c:self.bthover(True))
        self.Close.bind('<Leave>',lambda ccx:self.bthover(False))
        self.display.pack()
        self.resizable(0,0)
        self.Close.pack(fill=X)
    def bthover(self,status):
        if status:
            self.Close['bg']='yellow'
            self.Close['relief']='groove'
        else:
            self.Close['bg']='red'
            self.Close['relief']='flat'
    def on_closing(self):
        if self.things is not None:self.things.config(state=NORMAL)
        self.destroy()
class Instructions(Toplevel):
    def __init__(self,parent,photos):
        super().__init__(parent)
        self.config(bg='orange')        
        self.focus_set()
        self.resizable(0,0)        
        self.Contain=Frame(self,bg='#FF8000')
        self.ok=Button(self.Contain,text='Ok',command=self.destroy,borderwidth=6)
        self.ok.config(relief=FLAT)
        self.ok.config(bg='orange')
        self.index=0
        self.Notify=Label(self.Contain,bg='orange',borderwidth=6,relief=FLAT)
        self.entered=False
        self.photos=photos
        self.Notify.config(text='{} of {}'.format(1,len(self.photos)))
        self.collections=[ImageLabel(self,self.photos[i],500,500) for i in range(len(self.photos))]   
        self.collections[0].pack()
        self.Contain.pack(side=BOTTOM,fill=X)        
        self.Notify.pack(side=RIGHT,fill=Y)
        self.bind('<Left>',lambda x:self.change(False))     
        self.bind('<Right>',lambda x:self.change(True))
    def change(self,next):        
        if self.index==0 and not next:return None
        elif self.index==len(self.photos)-1 and next:return None
        if not self.entered:
            self.ok.pack(side=LEFT,fill=BOTH)
            self.entered=True    
        self.collections[self.index].pack_forget()
        if next:                
            self.index+=1
        else:
            self.index-=1
        self.Notify.config(text='{} of {}'.format(self.index+1,len(self.photos)))
        self.collections[self.index].pack()   
    def bthover(self,status):
        if status:
            self.ok.config(bg='yellow',relief=GROOVE)
        else:
            self.ok.config(bg='orange',relief=FLAT)
if __name__=='__main__':
    root=Tk()
    bt=Button(root,text='Warning',command=lambda :Warning(root,bt))
    bt.pack()
    Button(root,text='Next Update',command=lambda :FutureUpdate(root)).pack()
    root.mainloop()