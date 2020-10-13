from tkinter import *
from tkinter import ttk

class MainWindow:
    def __init__(self):
        self.parent=Tk()
        self.parent.geometry("494x410+370+100")
        self.parent.title("My Software - TEST")

        Button = ttk.Button(self.parent, text="open a new widnow", command=self.OpenNewWindow)
        Button.place(x=16, y=16)

    def OpenNewWindow(self):
        self.obj = NewWindow(self)

class NewWindow:
    def __init__(self, mw):
        self.window, self.mw = Toplevel(mw.parent), mw
        self.window.geometry("200x150+360+200")
        self.window.title("New Window")
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window.focus()
        self.mw.parent.attributes('-disabled', 1)
        self.window.transient(mw.parent)
        self.window.grab_set()
        self.mw.parent.wait_window(self.window)

    def on_close(self):
        self.mw.parent.attributes('-disabled', 0)
        self.window.destroy()

def main():
    app=MainWindow()
    app.parent.mainloop()

if __name__=="__main__":
    main()