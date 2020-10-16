from tkinter import *
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
try:
    from root.Dialogs import *
except:
    from dir.root.Dialogs import *
class EnterLink(Entry):
    def __init__(self,parent,var):
        super().__init__(parent)
        self.config(textvariable=var)
        self.var=var
        self.var.set('Enter the Link: ')
        self.bind('<Button-1>',self.check)
        self.config(width=100)
        self.config(borderwidth=6)
        self.config(relief=FLAT)
        self.config(font=('Times','15'))
    def check(self,*args):
        if self.var.get()=='Enter the Link: ':
            self.var.set('')        
class YT(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.link=StringVar()
        self.config(bg='#FF4D4D')
        self.checker=NetworkCheck()
        self.FirstFrame=Frame(self,bg='#FF4D4D')
        self.EnterFrame=Frame(self.FirstFrame)
        self.Enter=EnterLink(self.EnterFrame,self.link)
        self.hbar=Scrollbar(self.EnterFrame,orient=HORIZONTAL,command=self.Enter.xview)
        self.SearchButton=Button(self.FirstFrame,text='🔍',width=2,relief=FLAT,bg='#FF0000',command=self.check)
        self.Enter.config(xscrollcommand=self.hbar.set)
        self.designs()
        self.arrange()
        self.after(3000,self.checknet)   
    def designs(self):
        self.SearchButton.config(font=('Times','20','bold'))
    def arrange(self):
        self.FirstFrame.pack()
        self.EnterFrame.pack(side=LEFT,pady=(10,0))
        self.SearchButton.pack(side=LEFT,fill=Y)
        self.Enter.pack(fill=BOTH)
        self.hbar.pack(fill=X,side=BOTTOM)
    def check(self,*args):
        print(self.link.get())
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
    b=YT(a)
    b.pack(expand=True,fill=BOTH)
    a.mainloop()