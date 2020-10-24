from tkinter import *
from tkinter import messagebox
try:
    from dir.root.AddLogFile import *
except:
    try:
        from root.AddLogFile import *
    except:
        from AddLogFile import *
started=setup_logger('Beginning','Resources\Logs\Opening.log')
calculator=setup_logger('Calculator','Resources\Logs\Calculator.log')
class LogBox(Canvas):
    def __init__(self,p,var):
        super().__init__(p)
        self.MFrame=Frame(self)
        self.Vbar=Scrollbar(p,orient=VERTICAL,command=self.yview)
        self.bind('<Configure>',lambda e:self.configure(scrollregion=self.bbox('all')))
        self.bind_all('<MouseWheel>',self.orientScreen)
        self.create_window((0,0),window=self.MFrame,anchor='nw',width=1350)
        self.VFrame=Frame(self.MFrame)
        self.VFrame.pack(fill=X)
        self.var=var
        self.config(yscrollcommand=self.Vbar.set)
        self.config(relief=FLAT)
        self.Vbar.pack(side=RIGHT,fill=Y)
    def append(self,text,color,lvl):
        lst=Listbox(self.VFrame,borderwidth=3,height=1,relief=FLAT,font=('helvetica',12,'bold'))
        lst.bind('<Enter>',lambda X:self.hover(lst,True,lvl))
        lst.bind('<Leave>',lambda X:self.hover(lst,False))
        lst.insert(END,text)
        lst.itemconfig(END,{'bg':color})
        lst.pack(fill=X)        
        lst.bind('<<ListboxSelect>>',lambda x:self.copy_button(text))
    def orientScreen(self,event):
        self.yview_scroll(int(-1*(event.delta/120)),'units')
    def hover(self,lst,status,lvl=None):
        if status:
            lst.config(bg='red',font=('helvetica',13,'bold'))
            self.var.set('Level: {}. Click to Copy'.format(lvl))
        else:
            lst.config(bg='orange',font=('helvetica',12,'bold'))
            self.var.set('')
    def copy_button(self,text):
        self.var.set('Copied to Clipboard!!!')
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(text)
        clip.destroy()
class ShowLogs(Toplevel):
    def __init__(self,parent,file):
        super().__init__(parent)
        self.geometry('{}x{}+10+10'.format(600,600))
        self.file=file
        self.config(bg='#252526')
        self.focus_set()
        self.grab_set()
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.resizable(0,0)
        self.colorcodes={'DEBUG':'#4DA6FF','ERROR':'#FF0000','WARNING':'#FF002B','INFO':'#FF5500','CRITICAL':'red'}
        self.TFrame=Frame(self,bg='#252526')
        self.MFrame=Frame(self)
        self.status=StringVar()
        self.statusFrame=Frame(self,bg='#252526')
        self.checkinglabel=Label(self.statusFrame,textvariable=self.status, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("Comic Sans MS", "10", "normal"))
        self.Clear=Button(self.TFrame,text='Clear',relief=FLAT,command=self.clearlogs,bg=self.backcolor[0],fg=self.textcolor[0])
        self.Refresh=Button(self.TFrame,text='Refresh',relief=FLAT,command=lambda :self.refresh(),bg=self.backcolor[0],fg=self.textcolor[0])
        self.Clear.bind('<Enter>',lambda x:self.bthover(True,self.Clear,'Clear'))
        self.Clear.bind('<Leave>',lambda x:self.bthover(False,self.Clear,'Clear'))
        self.Refresh.bind('<Enter>',lambda x:self.bthover(True,self.Refresh,'Refresh'))
        self.Refresh.bind('<Leave>',lambda x:self.bthover(False,self.Refresh,'Refresh'))
        self.findDetails()
        self.insertThem()
        self.arrange()
    def findLevel(self,line):
        if 'DEBUG' in line:
            note=line.index('DEBUG')
            return 'DEBUG',note+5
        elif 'ERROR' in line:
            note=line.index('ERROR')
            return 'ERROR',note+5
        elif 'WARNING' in line:
            note=line.index('WARNING')
            return 'WARNING',note+7
        elif 'INFO' in line:
            note=line.index('INFO')
            return 'INFO',note+4
        else:
            note=line.index('CRITICAL')
            return 'CRITICAL',note+7
    def findDateTime(self,line):
        if 'AM' in line:
            note=line.index('AM')
        else:
            note=line.index("PM")
        return note+1    
    def findDetails(self):
        self.levels=[]
        self.messages=[]
        self.datetime=[]
        with open(self.file,'r') as hand:
            self.lines=hand.readlines()
        check=len(self.lines)
        if check>1000:
            self.lines=self.lines[check-1000:]
            with open(self.lines,'w') as hand:
                for i in self.lines:
                    hand.write(i)
        for i in range(len(self.lines)-1,-1,-1):
            note=self.findDateTime(self.lines[i])
            self.datetime.append(self.lines[i][:note+1])
            lvl,note=self.findLevel(self.lines[i])
            self.levels.append(lvl)
            self.messages.append(self.lines[i][note+1:-1])        
        '''print(self.messages)
        print(self.levels)
        print(self.datetime)'''
    def clearlogs(self,*args):
        a=messagebox.askyesno('Reset! Are you Sure','Once done, all the previous logs will be erased',icon='warning',parent=self)
        if a:
            with open(self.file,'w') as hand:
                pass
            self.refresh()
    def insertThem(self):
        self.lstbox=LogBox(self.MFrame,self.status)
        for i in range(len(self.lines)):
            formatted='{:50}  {}'.format(self.datetime[i],self.messages[i])
            self.lstbox.append(formatted,self.colorcodes[self.levels[i]],self.levels[i])
    def arrange(self):
        self.TFrame.pack(fill=X)
        self.Clear.pack(side=RIGHT,padx=(20,20))
        self.Refresh.pack(side=RIGHT,padx=(20,20))
        self.MFrame.pack(fill=BOTH,expand=True)        
        self.lstbox.pack(fill=BOTH,expand=True)
        self.statusFrame.pack(side=BOTTOM,fill=X)
        self.checkinglabel.pack(side=LEFT)
    def refresh(self):
        self.MFrame.destroy()
        self.lstbox.destroy()
        self.MFrame=Frame(self)
        self.findDetails()
        self.insertThem()
        self.MFrame.pack(fill=BOTH,expand=True)   
        self.lstbox.pack(fill=BOTH,expand=True)
    def bthover(self,status,w,text):
        if status:
            self.status.set(text)
            w.config(fg=self.textcolor[1],bg=self.backcolor[1])
        else:
            self.status.set('')
            w.config(fg=self.textcolor[0],bg=self.backcolor[0])