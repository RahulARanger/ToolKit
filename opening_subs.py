from tkinter import *
root=Tk()
def open_it():
    b=Toplevel(root)
    b.grab_set()
a=Button(root,text='Open',command=open_it)
a.pack()
root.mainloop()