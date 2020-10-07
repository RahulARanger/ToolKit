from tkinter import *
class Test(Toplevel):
    def __init__(self,p):
        super().__init__(p)
        Whole=Menu(self)        
        select=Menu(Whole)
        select.add_command(label='Dozo')
        select.add_command(label='Hmmm')
        Whole.add_cascade(label='Select',menu=select)
        self.config(menu=Whole)
a=Tk()
Button(a,text='Open',command=lambda :Test(a)).pack()
a.mainloop()