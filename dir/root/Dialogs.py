from tkinter import *
try:
    from ImageViewer import *
except:
    try:
        from root.ImageViewer import *
    except:
        from dir.root.ImageViewer import *
class Common(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.ok=Button(self,text='Ok',command=self.on_closing,borderwidth=6)
        self.ok.config(relief=FLAT)
        self.ok.config(bg='#FF8000')
        self.ok.bind('<Enter>',lambda x:self.bthover(True))
        self.ok.bind('<Leave>',lambda x:self.bthover(False))
    def bthover(self,status):
        if status:
            self.ok.config(bg='#f27a00',relief=GROOVE)
        else:
            self.ok.config(bg='#FF8000',relief=FLAT)
# ? NIC - No Internet Connection
class NIC(Common):
    def __init__(self,parent):
        super().__init__(parent)        
        self.config(bg='red')
        self.overrideredirect(True)        
        self.show=ImageLabel(self,'Resources\Media\\NIC.jpeg',300,300)        
        self.show.pack()
        self.ok.pack(fill=X)    
    def on_closing(self):
        self.destroy()
class FutureUpdate(Common):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='orange')
        self.overrideredirect(True)        
        self.show=ImageLabel(self,'Resources\Media\\updatenotice.jpeg',600,600)        
        self.show.pack()
        self.ok.pack(fill=X)    
    def on_closing(self):
        self.destroy()
class Instructions(Common):
    def __init__(self,parent,photos):
        super().__init__(parent)
        self.config(bg='orange')        
        self.focus_set()
        self.resizable(0,0)        
        self.Contain=Frame(self,bg='#FF8000')       
        self.index=0
        self.Notify=Label(self.Contain,bg='orange',borderwidth=6,relief=FLAT)
        self.entered=False
        self.photos=photos
        self.Notify.config(text='{} of {}'.format(1,len(self.photos)))
        self.collections=[ImageLabel(self,self.photos[i],500,500) for i in range(len(self.photos))]   
        self.collections[0].pack(side=TOP)
        self.Contain.pack(side=BOTTOM,fill=X)        
        self.Notify.pack(side=RIGHT,fill=Y)
        self.bind('<Left>',lambda x:self.change(False))     
        self.bind('<Right>',lambda x:self.change(True))
    def change(self,next):        
        if self.index==0 and not next:return None
        elif self.index==len(self.photos)-1 and next:return None
        if not self.entered:
            self.ok.pack(side=BOTTOM,fill=BOTH)
            self.entered=True    
        self.collections[self.index].pack_forget()
        if next:                
            self.index+=1
        else:
            self.index-=1
        self.Notify.config(text='{} of {}'.format(self.index+1,len(self.photos)))
        self.collections[self.index].pack(side=TOP)   
    def on_closing(self):
        self.destroy()
if __name__=='__main__':
    root=Tk()
    bt=Button(root,text='Warning',command=lambda :Warning(root,bt))
    bt.pack()
    Button(root,text='Next Update',command=lambda :FutureUpdate(root)).pack()
    root.mainloop()