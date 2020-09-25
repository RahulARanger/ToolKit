from tkinter import *
import tkinter.ttk as ttk
import string
from tkinter import font

try:
    from root.animatedgif import *
except:
    from dir.root.animatedgif import *
def Fill(variable,text,status=None):
    if status is None:variable.insert(INSERT,text)
    else:
        if status is True:
            variable.delete(0,END)
        elif status is False:
            pass
        elif status==69:
            pass

class NumButton(Frame):
    def __init__(self,parent,number,font,var,screen):
        super().__init__(parent)
        self.OFont=font
        self.var=var
        self.screen=screen
        self.Number=Label(self,text=number,width=4,height=2,cursor='hand2')
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
            Fill(self.screen,number)
            self.Number.config(relief=SUNKEN)
        else:
            self.Number.config(relief=RAISED)

class MStack:
    def __init__(self):
        self.lst=[]
    def append(self,letter):
        if len(self.lst)>5:
            self.pop()
        self.lst.append(letter)
    def pop(self):
        store=self.lst[0]
        del self.lst[0]
        return store
    def see(self):
        print(self.lst)

class SymButton(Frame):
    def __init__(self,parent,sym,font,var,screen):
        super().__init__(parent)
        self.OFont=font
        self.screen=screen
        self.var=var
        self.sym=sym
        self.config(bg='#a5de03')
        self.Symbol=Label(self,text=sym,width=4,height=2,cursor='hand2')
        self.Symbol.config(relief=RAISED)
        self.Symbol.config(bg='#d5d6d6',fg='black',font=self.OFont)
        self.Symbol.pack(padx=3,pady=3)
        self.isthere=True
        self.Symbol.bind('<Enter>',lambda x:self.hover(True))
        self.Symbol.bind('<Leave>',lambda x:self.hover(False))  
        self.Symbol.bind('<Button-1>',lambda x:self.pressed(True,sym))        
        self.Symbol.bind('<ButtonRelease-1>',lambda x:self.pressed(False,sym))        
    def hover(self,status):
        if status:self.Symbol['bg'],self.Symbol['fg']='#f78419','black'
        else:self.Symbol['bg'],self.Symbol['fg']='#d5d6d6','black'
    def pressed(self,status,number):
        if status:
            self.Symbol.config(relief=SUNKEN)
            if self.sym not in '⌫C=':
                if self.sym in '➗':
                    Fill(self.screen,'/')
                elif self.sym=='➕':
                    Fill(self.screen,'+')
                elif self.sym=='➖':
                    Fill(self.screen,'-')
                elif self.sym=='✖️':
                    Fill(self.screen,'*')
                else:Fill(self.screen,number)
            else:
                demo={'C':True,'⌫':False,'=':69}
                if demo[self.sym]!=69:Fill(self.screen,self.sym,demo[self.sym])
                else:self.just_call()
        else:self.Symbol.config(relief=RAISED)
    def just_call(self):
        # ? Only for the '=' Button
        if self.isthere:
            print(self.var.get())
            Fill(self.var,self.sym,69)
    def disableIt(self):
        if self.isthere:
            self.Symbol.unbind('<Button-1>')        
            self.Symbol.unbind('<ButtonRelease-1>') 
            self.isthere=False
        else:
            pass
    def ableIt(self):
        if self.isthere:
            pass
        else:
            self.Symbol.bind('<Button-1>',lambda x:self.pressed(True,self.sym))        
            self.Symbol.bind('<ButtonRelease-1>',lambda x:self.pressed(False,self.sym)) 
            self.isthere=True
class Calc(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self['bg']='#1e1e1e'
        self.OFont=font.Font(family='verdana',size=20,weight='bold')
        self.OVar=StringVar()
        self.is_there=False
        self.is_therebar=False
        self.CFrame=Frame(self,background='#a5de03',highlightbackground='#9e3501',highlightthickness=6,width=560,height=640)        
        self.OFrame=Frame(self.CFrame,background='#635252')
        self.Row1=Frame(self.CFrame,bg='#a5de03')
        self.Row2=Frame(self.CFrame,bg='#a5de03')
        self.Text=AnimatedGif(self,'Resources\Media\Cal.gif',0.01)
        self.Row3=Frame(self.CFrame,bg='#a5de03')
        self.Row4=Frame(self.CFrame,bg='#a5de03')
        self.Row5=Frame(self.CFrame,bg='#a5de03')
        self.OutputFrame=Frame(self.OFrame,bg='#E6F2FF',height=23)
        self.OutputScreen=Entry(self.OutputFrame,bg='#E6F2FF',justify=RIGHT,width=69,textvariable=self.OVar,cursor='xterm',insertwidth=6,insertbackground='orange')        
        self.Plus=SymButton(self.Row3,'➕',self.OFont,self.OVar,self.OutputScreen)
        self.Minus=SymButton(self.Row4,'➖',self.OFont,self.OVar,self.OutputScreen)
        self.Multiply=SymButton(self.Row2,'✖️',self.OFont,self.OVar,self.OutputScreen)
        self.Divide=SymButton(self.Row1,'➗',self.OFont,self.OVar,self.OutputScreen)        
        self.LB=SymButton(self.Row4,'(',self.OFont,self.OVar,self.OutputScreen)
        self.RB=SymButton(self.Row4,')',self.OFont,self.OVar,self.OutputScreen)
        self.Power=SymButton(self.Row4,'^',self.OFont,self.OVar,self.OutputScreen)
        self.HBar=ttk.Scrollbar(self.OFrame,orient=HORIZONTAL,command=self.OutputScreen.xview)
        self.OutputScreen.config(font=self.OFont)
        self.Equal=SymButton(self.Row5,'=',self.OFont,self.OVar,self.OutputScreen)
        self.Back=SymButton(self.Row5,'⌫',self.OFont,self.OVar,self.OutputScreen)
        self.Zero=NumButton(self.Row5,'0',self.OFont,self.OVar,self.OutputScreen)
        self.Clear=SymButton(self.Row5,'C',self.OFont,self.OVar,self.OutputScreen)
        self.Numbers=[NumButton(self.Row1,str(i),self.OFont,self.OVar,self.OutputScreen) for i in {7,8,9}]
        self.Numbers.extend([NumButton(self.Row2,str(i),self.OFont,self.OVar,self.OutputScreen) for i in {4,5,6}])
        self.Numbers.extend([NumButton(self.Row3,str(i),self.OFont,self.OVar,self.OutputScreen) for i in {3,2,1}])
        self.Error=Label(self.OFrame,text='',relief=GROOVE)
        self.ErrorFont=font.Font(family='Century Gothic',size=10)
        self.arrange()
    def arrange(self):
        self.OVar.trace('w',self.check)
        self.Text.pack(padx=20,pady=20)
        self.Text.start()
        self.CFrame.pack(padx=5,pady=5)
        self.CFrame.pack_propagate(0)
        self.OFrame.pack(padx=30,pady=40)
        self.OutputFrame.pack()
        self.OutputScreen.pack(side=LEFT,ipady=6)
        self.Back.Symbol.bind('<Button-1>',lambda e:self.backspace(e))
        self.OutputScreen.icursor(0)
        self.Row1.pack()
        self.Row2.pack()
        self.Row3.pack()   
        self.Row4.pack()  
        self.Row5.pack()        
        for i in range(len(self.Numbers)):
            if i in [0,3,6]:self.Numbers[i].pack(side=LEFT,padx=28,pady=6)
            else:self.Numbers[i].pack(side=LEFT,padx=20,pady=6)  
        self.Power.pack(side=LEFT,padx=28,pady=6)
        self.LB.pack(side=LEFT,padx=20,pady=6)
        self.RB.pack(side=LEFT,padx=20,pady=6)
        self.Divide.pack(side=LEFT,padx=20,pady=6)
        self.Multiply.pack(side=LEFT,padx=20,pady=6)
        self.Plus.pack(side=LEFT,padx=20,pady=6)
        self.Minus.pack(side=LEFT,padx=20,pady=6)
        self.Zero.pack(side=LEFT,padx=28,pady=6)
        self.Equal.pack(side=LEFT,padx=20,pady=6)
        self.Back.pack(side=LEFT,padx=20,pady=6)
        self.Clear.pack(side=LEFT,padx=20,pady=6)
        self.Error.pack(fill=X,expand=True)
        self.OutputScreen.focus_set()
        self.OutputScreen.bind('<Return>',lambda x: self.printResult(x))
    def backspace(self,e):
        b=self.OutputScreen.index(INSERT)
        a=b-1
        ans=list(self.OVar.get())
        if a>=0:del ans[a]
        self.OVar.set(''.join(ans))
        try:
            self.OutputScreen.icursor(a)
        except:
            self.OutputScreen.icursor(b)
    def check(self,*args):
        exp=self.OVar.get()
        if len(exp)>0:self.filter(exp)
        exp=self.OVar.get()
        if len(exp)>25:
            if not self.is_therebar:
                self.OutputScreen.config(xscrollcommand=self.HBar.set)
                self.HBar.pack(fill=X,expand=True)
                self.is_therebar=True
        else:
            if self.is_therebar:
                self.HBar.pack_forget()
                self.is_therebar=False
        try:
            if len(self.OVar.get())==0:
                return None
            eval(self.OVar.get())            
            if self.is_there:
                self.Equal.ableIt()
                self.Error.config(text='',fg='red',bg='#E6F2FF',font=self.ErrorFont)
                self.OutputScreen.bind('<Return>',lambda x: self.printResult(x))
                self.is_there=False
        except:
            self.Error.config(text='Check the Expression again',fg='red',bg='#E6F2FF',font=self.ErrorFont)
            if not self.is_there:
                self.Equal.disableIt()
                self.OutputScreen.unbind('<Return>')
                self.is_there=True
    def printResult(self,e):
        print(self.OVar.get())
        self.Equal.just_call()
    def filter(self,exp):
            ans=[]
            for letter in exp:
                if letter in string.digits or letter in ['+','/','-','(',')','*','^']:
                    ans.append(letter)
                else:
                    pass
            self.OVar.set(''.join(ans))
if __name__=='__main__':
    root=Tk()
    root.geometry('600x600')
    a=Calc(root)
    a.pack()
    root.mainloop()