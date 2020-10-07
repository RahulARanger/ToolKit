from tkinter import *
try:
    from ImageViewer import *
except:
    try:
        from root.ImageViewer import *
    except:
        from dir.root.ImageViewer import *
import pygame
pygame.mixer.init()
class NotConnected(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title('No Internet Connection, Senpai!!!')
        photos=['Resources\Media\\bang\\bang{}.jpg'.format(i) for i in range(20)]
        self.geometry('350x250+{}+{}'.format((self.winfo_screenwidth()//2)-50,0))
        self.Bang=ImageAlbum(self,photos,350,300,100,'white')
        self.Bang.pack()
        self.resizable(0,0)
        self.grab_set()
        self.soundbg=pygame.mixer.Sound('Resources\Media\\ayayay.ogg')
        self.back='Resources\Media\\bang.ogg'
        self.IFrame=Frame(self,bg='red')
        self.ILabel=Label(self.IFrame,text='No Internet Connection. Returning to Main Window',bg='red',fg='white')
        self.ok=Button(self.IFrame,text='OK',command=self.vanish)
        self.arrange()
        self.playit()
    def vanish(self):
        self.destroy()
    def arrange(self):
        self.IFrame.pack()
        self.ILabel.pack()
        self.ok.pack()
    def playit(self):
        self.soundbg.play()
if __name__=='__main__':
    a=Tk()    
    NotConnected(a)
    a.mainloop()
