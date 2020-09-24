from tkinter import *
import tkinter.ttk as ttk
import string
from tkinter import font
def Fill(variable,text):
    text=variable.get()+text
    variable.set(text)
class NumButton(Frame):
    def __init__(self,parent,number,font,var):
        super().__init__(parent)
        self.OFont=font
        self.var=var
        self.Number=Label(self,text=number,width=4,height=1,cursor='hand2')
        self.config(bg='#a5de03')
        self.Number.config(relief=RAISED)
        self.Number.config(bg='#77ba1c',fg='black',font=self.OFont)
        self.Number.pack(padx=3,pady=3)
        self.Number.bind('<Enter>',lambda x:self.hover(True))
        self.Number.bind('<Leave>',lambda x:self.hover(False))
        self.Number.bind('<Button-1>',lambda x:self.pressed(True,number))
        self.Number.bind('<ButtonRelease-1>',lambda x:self.pressed(False,number))
    def hover(self,status):
        if status:self.Number['bg'],self.Number['fg']='#f78419','black'
        else:self.Number['fg'],self.Number['bg']='black','#77ba1c'
    def pressed(self,status,number):
        if status:
            Fill(self.var,number)
            self.Number.config(relief=SUNKEN)
        else:
            self.Number.config(relief=RAISED)

class SymButton(Frame):
    def __init__(self,parent,sym,font,var):
        super().__init__(parent)
        self.OFont=font
        self.var=var
        self.sym=sym
        self.config(bg='#a5de03')
        self.Symbol=Label(self,text=sym,width=4,height=1,cursor='hand2')
        self.Symbol.config(relief=RAISED)
        self.Symbol.config(bg='#d5d6d6',fg='black',font=self.OFont)
        self.Symbol.pack(padx=3,pady=3)
        self.Symbol.bind('<Enter>',lambda x:self.hover(True))
        self.Symbol.bind('<Leave>',lambda x:self.hover(False))  
        self.Symbol.bind('<Button-1>',lambda x:self.pressed(True,sym))        
        self.Symbol.bind('<ButtonRelease-1>',lambda x:self.pressed(False,sym))        
    def hover(self,status):
        if status:self.Symbol['bg'],self.Symbol['fg']='#f78419','black'
        else:self.Symbol['bg'],self.Symbol['fg']='#d5d6d6','black'
    def pressed(self,status,number):
        if status:
            if self.sym not in '⌫C=':Fill(self.var,number)
            self.Symbol.config(relief=SUNKEN)
        else:
            self.Symbol.config(relief=RAISED)
class Calc(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self['bg']='#EFDECD'
        self.OFont=font.Font(family='verdana',size=20,weight='bold')
        self.OVar=StringVar()
        self.CFrame=Frame(self,background='#a5de03',highlightbackground='#9e3501',highlightthickness=6,width=500,height=560)        
        self.OFrame=Frame(self.CFrame,background='#635252')
        self.Row1=Frame(self.CFrame,bg='#a5de03')
        self.Row2=Frame(self.CFrame,bg='#a5de03')
        self.Row3=Frame(self.CFrame,bg='#a5de03')
        self.Row4=Frame(self.CFrame,bg='#a5de03')
        self.Row5=Frame(self.CFrame,bg='#a5de03')
        self.Plus=SymButton(self.Row3,'➕',self.OFont,self.OVar)
        self.Minus=SymButton(self.Row4,'➖',self.OFont,self.OVar)
        self.Multiply=SymButton(self.Row2,'✖️',self.OFont,self.OVar)
        self.Divide=SymButton(self.Row1,'➗',self.OFont,self.OVar)        
        self.LB=SymButton(self.Row4,'(',self.OFont,self.OVar)
        self.RB=SymButton(self.Row4,')',self.OFont,self.OVar)
        self.Power=SymButton(self.Row4,'^',self.OFont,self.OVar)
        self.OutputFrame=Frame(self.OFrame,bg='#E6F2FF',height=23)
        self.OutputScreen=Entry(self.OutputFrame,bg='#E6F2FF',justify=RIGHT,width=69,textvariable=self.OVar,cursor='xterm')        
        self.OutputScreen.config(font=self.OFont)
        self.Equal=SymButton(self.Row5,'=',self.OFont,self.OVar)
        self.Back=SymButton(self.Row5,'⌫',self.OFont,self.OVar)
        self.Zero=NumButton(self.Row5,'0',self.OFont,self.OVar)
        self.Clear=SymButton(self.Row5,'C',self.OFont,self.OVar)
        self.Numbers=[NumButton(self.Row1,str(i),self.OFont,self.OVar) for i in {7,8,9}]
        self.Numbers.extend([NumButton(self.Row2,str(i),self.OFont,self.OVar) for i in {4,5,6}])
        self.Numbers.extend([NumButton(self.Row3,str(i),self.OFont,self.OVar) for i in {3,2,1}])
        self.arrange()
    def arrange(self):
        self.CFrame.pack(padx=50,pady=50)
        self.CFrame.pack_propagate(0)
        self.OFrame.pack(padx=30,pady=40)
        self.OutputFrame.pack()
        self.OutputScreen.pack(side=LEFT)
        self.Row1.pack()
        self.Row2.pack()
        self.Row3.pack()   
        self.Row4.pack()  
        self.Row5.pack()        
        for i in range(len(self.Numbers)):
            if i in [0,3,6]:self.Numbers[i].pack(side=LEFT,padx=28,pady=16)
            else:self.Numbers[i].pack(side=LEFT,padx=20,pady=16)  
        self.Power.pack(side=LEFT,padx=28,pady=16)
        self.LB.pack(side=LEFT,padx=20,pady=16)
        self.RB.pack(side=LEFT,padx=20,pady=16)
        self.Divide.pack(side=LEFT,padx=20,pady=16)
        self.Multiply.pack(side=LEFT,padx=20,pady=16)
        self.Plus.pack(side=LEFT,padx=20,pady=16)
        self.Minus.pack(side=LEFT,padx=20,pady=16)
        self.Zero.pack(side=LEFT,padx=28,pady=16)
        self.Equal.pack(side=LEFT,padx=20,pady=16)
        self.Back.pack(side=LEFT,padx=20,pady=16)
        self.Clear.pack(side=LEFT,padx=20,pady=16)
        self.OutputScreen.focus_set()
if __name__=='__main__':
    root=Tk()
    root.geometry('600x600')
    a=Calc(root)
    a.pack()
    root.mainloop()
