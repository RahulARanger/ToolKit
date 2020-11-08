import tkinter as tk

def stay(event):
    my_spot = 100,100
    root.geometry("+%d+%d" % (my_spot))

root=tk.Tk()
root.bind('<Configure>', stay)

root.mainloop()