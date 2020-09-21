from tkinter import *
class DeafultPage(Frame):
    pass
class Page1:
    def __init__(self,win):
        self.frame=Frame(win,bg='#2d2d2d')
        self.index=None
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=('#2d2d2d','#1e1e1e')
        self.name=Label(self.frame,text='Main',bg=self.backcolor[0],fg=self.textcolor[0],height=2,width=6)
        self.cross=Label(self.frame,text='✖',bg=self.backcolor[0],fg=self.textcolor[0])
        self.arrange()
    def arrange(self):
        self.name.pack(side=LEFT)
        self.cross.pack(side=RIGHT)
    def getFrame(self):
        return self.frame