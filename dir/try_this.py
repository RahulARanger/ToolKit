
# TODO: THis is the file where new modules are either tested or added
from tkinter import *
import PIL.Image
import PIL.ImageTk
a=Tk()
image_=PIL.Image.open('Resources\Media\\back-button.png')
image__=PIL.ImageTk.PhotoImage(image_)
bt=Button(a,image=image__,bg='#f1f1ff',relief=FLAT)
bt.pack()
a.mainloop()