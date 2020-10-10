from tkinter import *
import PIL.ImageTk
import PIL.Image
class ImageLabel(Label):
    def __init__(self,parent,img,w,h):
        super().__init__(parent)
        self.img=img
        self.w,self.h=w,h
        self.img=PIL.Image.open(self.img)
        self.resize()
        self.img=PIL.ImageTk.PhotoImage(self.img)
        self.config(image=self.img)
        self.config(bg='white')
    def resize(self):
        r1=self.img.size[0]/self.w
        r2=self.img.size[1]/self.h
        ratio=max(r1,r2)
        newsize=(int(self.img.size[0]/ratio),int(self.img.size[1]/ratio))
        self.img=self.img.resize(newsize,PIL.Image.ANTIALIAS)
class ButtonAlbum(Label):
    def __init__(self,parent,photos,w,h,bag='#1e1e1e'):
        super().__init__(parent)
        self.w,self.h=w,h        
        self['bg']=bag
        self.photos=photos
        self.photos=[PIL.Image.open(i) for i in self.photos]        
        self.photos=[self.resize(i) for i in range(len(self.photos))]        
        self.photos=[PIL.ImageTk.PhotoImage(i) for i in self.photos]
        self.index=0
        self.change()
        self.bind('<Button-1>',lambda x:self.change())
        self.bind('<Enter>',lambda x:self.hover(True))
        self.bind('<Leave>',lambda x:self.hover(False))
    def hover(self,status):
        if status:
            self.config(relief=RIDGE)
        else:
            self.config(relief=FLAT)
    def resize(self,index):
        r1=self.photos[index].size[0]/self.w
        r2=self.photos[index].size[1]/self.h
        ratio=max(r1,r2)
        newsize=(int(self.photos[index].size[0]/ratio),int(self.photos[index].size[1]/ratio))
        self.photos[index]=self.photos[index].resize(newsize,PIL.Image.ANTIALIAS)
        return self.photos[index]
    def change(self):    
        if self.index==len(self.photos):
            self.index=0
        self.config(image=self.photos[self.index])
        self.index+=1
        
class ImageAlbum(Label):
    def __init__(self,parent,photos,w,h,delay=100,bag='#1e1e1e'):
        super().__init__(parent)
        self.w,self.h=w,h
        self.config(bg=bag)
        self.photos=photos
        self.photos=[PIL.Image.open(i) for i in self.photos]        
        self.photos=[self.resize(i) for i in range(len(self.photos))]        
        self.photos=[PIL.ImageTk.PhotoImage(i) for i in self.photos]
        self.index=0
        self.delay=delay
        self.after(self.delay,self.change)
    def resize(self,index):
        r1=self.photos[index].size[0]/self.w
        r2=self.photos[index].size[1]/self.h
        ratio=max(r1,r2)
        newsize=(int(self.photos[index].size[0]/ratio),int(self.photos[index].size[1]/ratio))
        self.photos[index]=self.photos[index].resize(newsize,PIL.Image.ANTIALIAS)
        return self.photos[index]
    def change(self):    
        if self.index==len(self.photos):
            self.index=0
        self.config(image=self.photos[self.index])
        self.index+=1
        self.after(self.delay,self.change)
if __name__=='__main__':
    a=Tk()
    a.geometry('600x600')
    b=ImageLabel(a,'Resources\Media\\hi3.jpg',200,200)
    b.pack()
    a.mainloop()
    photos=['Resources\Media\\hi4.jpg','Resources\Media\hi3.jpg','Resources\Media\\hi4.jpg','Resources\Media\\hi1.png']
    d=Tk()
    c=ImageAlbum(d,photos,200,200)
    c.pack()
    d.mainloop()
