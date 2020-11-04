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
        self.geometry('+{}+{}'.format(self.winfo_screenwidth()//4,self.winfo_screenheight()//4))
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
class Loading(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.loadingpics=['Resources\Media\Loading\Loading{}.jpg'.format(i) for i in range(8)]
        self.display=ImageAlbum(self,self.loadingpics,800,800,110)
        self.display.pack(fill=BOTH,expand=True)
        self.geometry('+{}+{}'.format(self.winfo_screenwidth()//4,self.winfo_screenheight()//4))
        self.grab_set()
        self.overrideredirect(True) 
        self.resizable(0,0)
    def stopIt(self):
        self.destroy()

if __name__=='__main__':
    root=Tk()
    bt=Button(root,text='Warning',command=lambda :Loading(root))
    bt.pack()
    Button(root,text='Next Update',command=lambda :FutureUpdate(root)).pack()
    root.mainloop()