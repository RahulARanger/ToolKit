# -*- coding: utf8 -*-
from tkinter import *
from tkinter import messagebox
import os
import colorama
import requests
colorama.init()
root = Tk()
root.title('Test')

def done():
    print("test")

def downscale():
    root.geometry('{}x{}'.format(root.winfo_width()//2,root.winfo_height()//2))

downscale = Button(root, text='Can you see the done button?', command=downscale)
downscale.grid(row=1, column=1)

b = Button(root, text='Done')
b.grid(row=50, column=50)

root.mainloop()