from tkinter import *
from tkinter import ttk
class PlayListFrame(Frame):
    def __init__(self,parent,name):
        super().__init(parent)
        self.Modify=Button(self,text='',cursor='pencil')
        self.Delete=Button(self,text='',cursor='')
        self.Name=Label(self,text=name)

class PlayList(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.BFrame=Frame(self)
        self.BCanvas=Canvas(self.BFrame,bg='red')
        self.FFrame=Frame(self.BCanvas,bg='yellow')
        self.MFrame=Frame(self.FFrame,bg='orange')
        self.geometry('400x400')
        self.PlayLists=[]
        self.title('Choose Your PlayLists')
        self.VBar=ttk.Scrollbar(self.BFrame,orient=VERTICAL,command=self.BCanvas.yview)
        self.add=Button(self,text='+',command=self.createplaylist)
        self.openthem()
        self.arrange()
    def arrange(self):
        self.BCanvas.configure(yscrollcommand=self.VBar.set)
        self.BCanvas.bind('<Configure>',lambda e:self.BCanvas.configure(scrollregion=self.BCanvas.bbox('all')))
        self.BCanvas.create_window((0,0),window=self.FFrame,anchor='nw',width=400)
        self.BFrame.pack(fill=BOTH,expand=True)
        self.BCanvas.pack(fill=BOTH,expand=True,side=LEFT)
        self.VBar.pack(expand=True,fill=Y,side=RIGHT)
        self.MFrame.pack(side=LEFT,fill=BOTH,expand=True)
        for i in range(100):
            Button(self.MFrame,text=str(i)).pack()
        
    def openthem(self):
        pass
    def createplaylist(self):
        pass

if __name__=='__main__':
    a=Tk()
    def openit():
        b=PlayList(a)
    bt=Button(a,text='Open',command=openit)
    bt.pack()
    a.mainloop()