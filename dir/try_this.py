from tkinter import *
from tkinter import ttk
import json
class PlayListFrame(Frame):
    def __init__(self,parent,name='Hello'):
        super().__init__(parent)
        self.Modify=Button(self,text='',cursor='pencil')
        self.Delete=Button(self,text='',cursor='')
        self.Name=Label(self,text=name)
    


class PlayList(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.BFrame=Frame(self)
        self.BCanvas=Canvas(self.BFrame,bg='#EFDECD')
        self.FFrame=Frame(self.BCanvas,bg='#EFDECD')
        self.MFrame=Frame(self.FFrame,bg='#EFDECD')
        self.geometry('400x400')
        self.lst=[]
        self.openplaylist()
        self.PlayLists=PlayListFrame(self)
        self.title('Choose Your PlayLists')
        self.VBar=ttk.Scrollbar(self.BFrame,orient=VERTICAL,command=self.BCanvas.yview)
        self.add=Button(self,text='+',command=self.createplaylist)
        self.openthem()
        self.arrange()
    def arrange(self):
        self.BCanvas.configure(yscrollcommand=self.VBar.set)
        self.BCanvas.bind('<Configure>',lambda e:self.BCanvas.configure(scrollregion=self.BCanvas.bbox('all')))
        self.BCanvas.create_window((0,0),window=self.FFrame,anchor='nw',width=400)
        self.BCanvas.bind_all('<MouseWheel>',self.orientScreen)
        self.BFrame.pack(fill=BOTH,expand=True)
        self.BCanvas.pack(fill=BOTH,expand=True,side=LEFT)
        self.VBar.pack(expand=True,fill=Y,side=RIGHT)
        self.MFrame.pack(fill=BOTH,expand=True)
    def openplaylist(self):
        with open('dir\playlists.json','r') as playlistfile:
            playlist=json.loads(playlistfile.read())
            self.lst=playlist["Playlists"]
            print(self.lst)
    def orientScreen(self,event):
        self.BCanvas.yview_scroll(int(-1*(event.delta/120)),'units')
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
    