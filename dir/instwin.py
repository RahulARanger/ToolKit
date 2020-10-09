import subprocess
import os
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import *
import sys
import json
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
try:
    import PIL.Image
except:
    root=Tk()
    lb=Label(root,text='This Window will disappear after this process is over')
    lb.pack()
    try:
        root.title('Wait untill this window disappers')
        if NetworkCheck().MTest() is False:
            a=messagebox.showerror('Need Internet Connection','It seems some modules are needed!!! So for next time try opening this with Internet connection.')
            root.destroy()
            sys.exit(0)
        else:
            a=messagebox.showinfo('Don\'t Worry happens only at once','Need an Important Module!!! Downloading those so please wait!!!')
            subprocess.check_call([sys.executable,'-m','pip','install','Pillow'])
    except:
        os.system('pip install Pillow')
    root.destroy()
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
import threading
import time
class Packages:
    def __init__(self):
        self.ModuleNames=['pytube','googletrans','mutagen','pygame']
        self.PackageNames={'pytube':'pytube3','mutagen':'mutagen','googletrans':'googletrans','pygame':'pygame'}
class Installer(Tk):
    def __init__(self):
        super().__init__()
        # ! Imp (Module Names)
        self.ModuleNames=Packages().ModuleNames
        # ! Imp. (Package Names)
        self.PackageNames=Packages().PackageNames
        self.to_Install=[]
        self.title('Setting things up !!!, Senpai')
        self.file='dir\\root\\settings.json'    
        self.resizable(0,0)
        self.attributes('-disabled', True)        
        self.step=100/len(Packages().ModuleNames)
        self.height=300
        self.geometry('{}x{}+{}+{}'.format(360,300,int((self.winfo_screenwidth()-360)/2),int((self.winfo_screenheight()-300)/2)))
        self.MFrame=Frame(self,background='#84bbf8',cursor='coffee_mug')
        self.HiFrame=Frame(self.MFrame,background='#84bbf8')
        self.HiPhotos=['Resources\Media\\hi\\hi{}.jpg'.format(i) for i in range(1,19)]
        self.Hi=ImageAlbum(self.HiFrame,self.HiPhotos,360,300,50)
        self.NFrame1=Frame(self.MFrame,background='#84bbf8')
        self.NFrame2=Frame(self.MFrame,background='#84bbf8')
        self.NFrame3=Frame(self.MFrame,background='#84bbf8')
        self.NFrame4=Frame(self.MFrame,background='#84bbf8')
        self.Note1=Label(self.NFrame1,text='Checking Modules',font=('verdana',10,'bold'),background='#84bbf8')
        self.Note2=Label(self.NFrame2,text='Downloading',font=('verdana',10,'bold'),background='#84bbf8')
        self.Note3=Label(self.NFrame3,text='Installed',font=('verdana',10,'bold'),background='#84bbf8')
        self.Note4=Button(self.NFrame4,text='Continue',command=self.register)
        self.Note4.config(activebackground='#FFFF00',relief='flat',width=10,height=2,bg='#FF8000',font=('Comic Sans MS',10,'bold'))
        self.Note4.bind('<Leave>',lambda x:self.bthover(False))
        self.Note4.bind('<Enter>',lambda x:self.bthover(True))
        self.Note4.bind('<Return>',lambda x:self.bthover(None))
        self.ticks=['Resources\\Media\\tick\\tick{}.jpg'.format(i) for i in range(35)]
        self.Tick1=ImageAlbum(self.NFrame1,self.ticks,50,20,50)
        self.Tick2=ImageAlbum(self.NFrame3,self.ticks,50,20,50)
        self.checking=Progressbar(self.NFrame1,orient=HORIZONTAL,length=250,mode='determinate')
        self.installing=Progressbar(self.NFrame2,orient=HORIZONTAL,length=250,mode='determinate')
        self.checking['value']=0
        self.setup1=None
        self.setup2=None
        self.setup3=None
        self.setup4=None
        self.flag=False
        self.completed=False
        self.arrange()
    def register(self):
        with open(self.file,'r') as hand:
            container=json.loads(hand.read())
        container['Times']+=1
        with open(self.file,'w') as hand:
            hand.write(json.dumps(container,indent=4))
        self.completed=True   
        self.destroy()
    def bthover(self,status):
        if status is None:
            self.register()
        else:
            if status:
                self.Note4['bg']='#FFFF00'
                self.Note4.pack_configure(padx=3,pady=3)
                self.Note4.config(relief='solid')
            else:
                self.Note4['bg']='#FF8000'
                self.Note4.pack_configure(padx=3,pady=3)
                self.Note4.config(relief='flat')
    def arrange(self):
        self.MFrame.pack(expand=True,fill=BOTH)
        self.HiFrame.pack(fill=X)
        self.Hi.pack(padx=3,pady=3,anchor='n')
        self.NFrame1.pack(fill=X)          
        try:
            self.after(1000,self.setup_1)  
        except:pass
    def check_modules(self,package):
        statement='import '+package
        try:
            exec(statement)
        except:
            print(statement,package)
            self.to_Install.append(self.PackageNames[package])
            self.checking['value']+=self.step
            try:
                del self.ModuleNames[0]
            except:
                print('Empty List')
        print(self.to_Install)
    def quick_check(self):
        for i in Packages().ModuleNames:
            try:
                exec('import {}'.format(i))
            except:
                return False
        return True
    def install(self):
        for i in Packages().ModuleNames:
            package=self.PackageNames[i]
            print(package)
            try:
                exec('import {}'.format(i))
                continue
            except:
                pass
            print(self.PackageNames[i])
            try:
                print('wht')
                time.sleep(3)
                subprocess.check_call([sys.executable,'-m','pip','install',package])
            except:
                print('wht')
                time.sleep(3)
                os.system('pip install {}'.format(package))
    def setup_1(self):        
        if self.setup1 is None:
            self.NFrame1.pack(fill=X)
            self.balance()
            self.Note1.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            self.checking.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            self.checking['value']=0
            self.setup1=False
        elif self.setup1 is False:
            if len(self.ModuleNames)!=0:
                CThread=threading.Thread(target=self.check_modules,args=(self.ModuleNames[0],))
                CThread.start()
                self.checking['value']+=self.step
                del self.ModuleNames[0]
            else:
                self.setup1=True
        elif self.setup1 is True:
            self.checking.pack_forget()
            self.Tick1.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            self.setup1=69
        elif self.setup2 is None:
            self.setup2=False
            self.balance()
            self.NFrame2.pack(fill=X)
            self.Note2.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            self.installing.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            self.installing.start()
            self.setup2=False
        elif self.setup2 is False:
            print(threading.active_count())
            if self.quick_check() is False:
                if NetworkCheck().MTest() is False:
                    self.completed=False
                    self.installing.stop()
                    self.a=messagebox.showerror('Need Internet Connection','It seems some modules are needed!!! So for next time try opening this with Internet connection.')
                    self.destroy()
                if NetworkCheck().MTest() is True and not self.flag:
                    a=messagebox.showinfo('Don\'t Worry happens only at once','Need Some Modules!!! Downloading those so please wait!!!')
                    self.flag=True
                    self.Note2.config(text='Downloading and Installing Modules')
                    self.IThread=threading.Thread(target=self.install)
                    self.IThread.start()
            else:    
                self.setup2=69
                self.attributes('-disabled', False)
                self.installing.stop()
                self.NFrame2.pack_forget()
                self.balance(69)
        elif self.setup3 is None:
            self.balance()
            self.NFrame3.pack(fill=X)
            self.Note3.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            self.Tick2.pack(side=LEFT,padx=3,pady=3,anchor='nw')
            
            self.setup3=69
        elif self.setup4 is None:
            self.balance()            
            self.NFrame4.pack(fill=X)
            self.Note4.pack(side=RIGHT,padx=3,pady=3,anchor='ne')
            self.setup4=69
        else:
            print('Hello')
            return None
        try:self.after(1000,self.setup_1)   
        except:pass
    def balance(self,minus=None):
        if minus is None:
            self.height+=35
            self.geometry('{}x{}+{}+{}'.format(360,self.height,int((self.winfo_screenwidth()-360)/2),int((self.winfo_screenheight()-self.height)/2)))
        else:
            self.height-=35
            self.geometry('{}x{}+{}+{}'.format(360,self.height,int((self.winfo_screenwidth()-360)/2),int((self.winfo_screenheight()-self.height)/2)))
if __name__=='__main__':
    a=Installer()
    a.mainloop()    