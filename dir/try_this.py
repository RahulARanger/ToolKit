from tkinter import *
class MenuFrame(Frame):
    def __init__(self,parent,name,link=''):
        super().__init__(parent)
        self['bg']='#2d2d2d'
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=('#2d2d2d','#474748')
        self.link=link
        self.name=Label(self,text=name,fg=self.textcolor[0],bg=self.backcolor[0],height=2)
        self.name.bind('<Enter>',lambda x:self.bthover(False))
        self.name.bind('<Leave>',lambda x :self.bthover(True))
        self.name.pack()
    def bthover(self,status):
        if status is None:pass
        else:
            if status:
                self.config(bg=self.backcolor[0])
                self.name.config(fg=self.textcolor[0],bg=self.backcolor[0])
            else:
                self.config(bg=self.backcolor[1])
                self.name.config(fg=self.textcolor[1],bg=self.backcolor[1])


        
class MenuOptionFrame(Frame):
    def __init__(self,parent,name):
        super().__init__(parent)
        self.options=StringVar()
        self.options.set('Main')
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=('#2d2d2d','#474748')
        self.select=OptionMenu(self,self.options,'Main','Calculator','Translator')
        self.select.config(background=self.backcolor[0],fg=self.textcolor[0],relief=FLAT,activeforeground=self.textcolor[1],activebackground=self.backcolor[1],highlightthickness=0,indicatoron=0)
        self.select['menu'].config(bg='#1e1e1e',activeforeground='#f1f1ff',fg=self.textcolor[0])
        self.select['menu']['cursor']='hand2'
        print(self.select.keys())
        print(self.select['menu'].keys())
        self.select.pack(fill=BOTH,expand=True,side=LEFT)
if __name__=="__main__":
    root=Tk()
    MFrame=Frame(root)
    MFrame['bg']='#2d2d2d'
    c=MenuOptionFrame(MFrame,'Select')
    b=MenuFrame(MFrame,'About')
    a=MenuFrame(MFrame,'Help')
    c.pack(side=LEFT)
    b.pack(side=LEFT)
    a.pack(side=LEFT)
    MFrame.pack(fill=X,expand=True)
    root.mainloop()
