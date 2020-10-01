import tkinter as tk
from tkinter import ttk

root = tk.Tk()
buttons = [None] * 7


def del_button():
    for i in range(5, 7):
        buttons[i].destroy()


for i in range(7):
    buttons[i] = ttk.Button(root, text=f"{i}")
    buttons[i].grid(column=i, row=0, sticky=tk.E)
    root.columnconfigure(i, weight=1)

button_del = ttk.Button(root, text='Delete', command=del_button)
button_del.grid(column=0, row=1)

root.mainloop()