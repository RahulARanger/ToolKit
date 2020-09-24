from tkinter import *
from PIL import Image,ImageTk
root=Tk()
a=Frame(root,bg='orange')
root.geometry('100x100')
img=Image.open('Resources\Media\starry.jpg')
img=ImageTk.PhotoImage(img)
lb=Label(image=img)
lb.pack()
a.pack(expand=True,fill=BOTH)
root.mainloop()