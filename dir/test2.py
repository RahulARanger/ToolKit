from PIL import Image, ImageTk
import tkinter as tk
from Calculator import *

from PIL import Image, ImageTk
import tkinter as tk


class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget


if __name__ == '__main__':

    IMAGE_PATH = 'Resources\Media\starry.jpg'
    
    root2=tk.Tk()
    root = tk.Frame(root2)
    root.pack(expand=True,fill=tk.BOTH)
    WIDTH=root2.winfo_screenwidth()
    HEIGTH=root2.winfo_screenheight()
    root2.geometry('{}x{}'.format(WIDTH, HEIGTH))
    bkrgframe = BkgrFrame(root, IMAGE_PATH, WIDTH, HEIGTH)
    bkrgframe.pack(expand=True,fill=tk.BOTH)

    # Put some tkinter widgets in the BkgrFrame.
    button1 = bkrgframe.add(Calc(root), 100, 100)
    root2.mainloop()