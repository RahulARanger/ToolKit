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
class Check(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='orange')
        self.overrideredirect(True)
        self.ok=Button(self,text='Ok',command=self.on_closing,borderwidth=6)
        self.show=ImageLabel(self,'Resources\Media\\check.jpeg',600,600)
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

if __name__=='__main__':
    root=Tk()
    bt=Button(root,text='Warning',command=lambda :Warning(root,bt))
    bt.pack()
    Button(root,text='Next Update',command=lambda :FutureUpdate(root)).pack()
    Button(root,text='Check',command=lambda :Check(root)).pack()
    root.mainloop()
