from tkinter import *
class testing(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.exit=Button(self,text='Exit',command=self.destroy)
        self.exit.pack()
class test(Tk):
    def __init__(self):
        super().__init__()
        self.test1=testing(self)
        self.test1.pack()
        self.after(100,self.check)    
    def check(self):
        print(self.test1.winfo_exists())
        self.after(100,self.check)    
test().mainloop()

