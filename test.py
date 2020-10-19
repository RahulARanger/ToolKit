from tkinter import *
class LogBox(Canvas):
    def __init__(self,p):
        super().__init__(p)
        self.MFrame=Frame(self)
        self.Vbar=Scrollbar(p,orient=VERTICAL,command=self.yview)
        self.bind('<Configure>',lambda e:self.configure(scrollregion=self.bbox('all')))
        self.bind_all('<MouseWheel>',self.orientScreen)
        self.create_window((0,0),window=self.MFrame,anchor='nw',width=1350)
        self.VFrame=Frame(self.MFrame)
        self.VFrame.pack(fill=X)
        self.config(yscrollcommand=self.Vbar.set)
        self.config(relief=FLAT)
        self.Vbar.pack(side=RIGHT,fill=Y)
    def append(self,text,color):
        lst=Listbox(self.VFrame,borderwidth=3,height=1,relief=FLAT,font=('helvetica',12,'bold')) # border width thing
        lst.bind('<Enter>',lambda X:self.hover(lst,True)) # for hover effects
        lst.bind('<Leave>',lambda X:self.hover(lst,False))
        lst.insert(END,text)
        lst.config(bg='orange')
        lst.itemconfig(END,{'bg':color})
        lst.pack(fill=X)        
        lst.bind('<<ListboxSelect>>',lambda x:self.copy_button(text)) # for click event
    def orientScreen(self,event):
        self.yview_scroll(int(-1*(event.delta/120)),'units')
    def hover(self,lst,status):
        if status:
            lst.config(bg='red',font=('helvetica',15,'bold'))            
        else:
            lst.config(bg='orange',font=('helvetica',12,'bold'))            
    def copy_button(self,text):        
        d = Tk()
        d.withdraw()
        d.clipboard_clear()
        d.clipboard_append(text)
        d.destroy()
if __name__=='__main__':
    root=Tk()
    f=Frame(root)
    b=LogBox(f)
    for i in range(1000):
        b.append(i,'orange')
    b.pack()
    f.pack()
    root.mainloop()