from tkinter import *
class ToolTip(object):
    def __init__(self, widget,text):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.createToolTip(text)
    def createToolTip(self,text):
        def enter(event):
            self.showtip(text)
        def leave(event):
            self.hidetip()
        self.widget.bind('<Enter>', enter)
        self.widget.bind('<Leave>', leave)
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle","style", tw._w,"help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
if __name__=='__main__':
    root=Tk()
    a=Button(root,text='check')
    b=ToolTip(a,'Hey Hey Hey')
    a.pack()
    root.mainloop()