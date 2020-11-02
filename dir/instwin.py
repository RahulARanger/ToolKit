import subprocess
import os
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import *
import sys
import threading
try:
    from dir.root.NetTest import *
except:
    from root.NetTest import *
try:
    from dir.root.LogFiles import *
except:
    from root.LogFiles import *
class SpecialLabel(Label):
    def __init__(self,parent):
        super().__init__(parent)
        self.var=StringVar()
        self.config(font=('Comic Sans MS', 12, 'bold italic'),fg='#f1f1ff',bg='#5a5a5c')
        self.var.set('Installing')
        self.config(textvariable=self.var)
        self.toggle=False
        self.note=''
        self.switch=True
        self.after(300,self.change)
    def change(self):
        if not self.switch:
            started.critical('Failed >_< No Internet connection!!!')
            self.var.set('Failed >_< No Internet connection!!!')
        else:
            text='Installing {}'.format(self.note)
            if self.toggle:
                text+='.../...'
            else:
                text+='...\...'
            self.var.set(text)
            self.toggle=not(self.toggle)
        self.after(300,self.change)
    def specialcase(self):
        self.switch=False
class preInstall(Tk):
    def __init__(self):
        super().__init__()
        self.VIP=['pygame','PIL.Image']
        self.V={'pygame':'pygame','PIL.Image':'Pillow'}
        self.toInstall=[]
        if self.check():
            self.destroy()
        else:
            self.textcolor=('#74878f','#f1f1ff')
            self.backcolor=("#424242",'#5a5a5c')
            self.tfont=('Courier','23','bold')
            self.Info=Label(self,text='It seems some preModules are Missing!!! Downloading Them...',bg=self.backcolor[1],fg=self.textcolor[1],font=self.tfont)
            self.done=Button(self,text='Proceed',command=self.destroy,relief=FLAT,fg=self.textcolor[0],bg=self.backcolor[0])
            self.resizable(0,0)
            self.colors=['#FF5500','#1A9900','#19FFFF','#FF0000']
            self.config(bg=self.colors[0])
            self.index=1
            self.overrideredirect(True) 
            self.state('zoomed')
            self.current=SpecialLabel(self)
            self.arrange()
            self.done.bind('<Enter>',lambda x:self.bthover(True))
            self.done.bind('<Leave>',lambda x:self.bthover(False))
            self.after(3000,self.checknet)
            a=threading.Thread(target=self.install)
            a.start()
    def bthover(self,status):
        if status:
            self.done.config(bg=self.backcolor[1],fg=self.textcolor[1])
        else:
            self.done.config(bg=self.backcolor[0],fg=self.textcolor[0])
    def checknet(self):
        if self.index==len(self.colors):self.index=0
        self.config(bg=self.colors[self.index])
        self.index+=1
        if NetworkCheck().MTest() is False:
            started.critical('Failed >_< No Internet connection!!!')
            a=messagebox.showerror('>_< Need Internet Connection','It seems some modules are needed!!! So for next time try opening this with Internet connection.')
            self.destroy()
            sys.exit(0)
        self.after(3000,self.checknet)
    def arrange(self):
        self.Info.pack(expand=True)
        self.current.pack(expand=True)
    def check(self):
        flag=True
        for i in self.VIP:
            try:
                exec('import {}'.format(i))
            except:
                flag=False
                self.toInstall.append(i)
        return flag
    def install(self):
        for i in self.toInstall:
            started.debug('Installing {}'.format(i))
            self.current.note=self.V[i]
            try:
                subprocess.check_call([sys.executable,'-m','pip','install',self.V[i]])
            except:
                os.system('pip install {}'.format(self.V[i]))
            started.info('Installed {}'.format(i))
        self.current.destroy()
        self.Info.config(text='Completed UwU')
        self.done.pack(expand=True)
        started.info('PreInstallation is Completed')
preInstall().mainloop()
try:
    from root.ImageViewer import *
except:
    from dir.root.ImageViewer import *
class Installer(Tk):
    def __init__(self):
        super().__init__()
        # ! Imp (Module Names)
        self.textcolor=('#74878f','#f1f1ff')
        self.backcolor=("#424242",'#5a5a5c')
        self.ModuleNames=['googletrans','mutagen','pytube']
        self.PackageNames={'mutagen':'mutagen','googletrans':'googletrans','pytube':'pytubex'}
        
        self.toInstall=[]
        if self.checkFirst():
            self.register()
        else:
            self.title('Setting things up !!!, Senpai')
            self.resizable(0,0)
            #self.attributes('-disabled', True)   
            self.step=100/len(self.ModuleNames)
            self.height=300
            print(self.toInstall)
            self.geometry('{}x{}+{}+{}'.format(360,400,int((self.winfo_screenwidth()-360)/2),int((self.winfo_screenheight()-360)/2)))
            self.MFrame=Frame(self,background='#84bbf8',cursor='coffee_mug')
            self.HiFrame=Frame(self.MFrame,background='#84bbf8')
            self.HiPhotos=['Resources\Media\\hi\\hi{}.jpg'.format(i) for i in range(1,19)]
            self.Hi=ImageAlbum(self.HiFrame,self.HiPhotos,360,300,50)            
            self.InstallerFrame=Frame(self.MFrame,background='#84bbf8')
            self.installing=Progressbar(self.InstallerFrame,orient=HORIZONTAL,length=250,mode='indeterminate')
            self.announce=SpecialLabel(self.InstallerFrame)
            self.flag=False
            self.completed=False
            self.noNet=None
            self.arrange()
            self.check_it=threading.Thread(target=self.checknet)
            self.check_it.start()
            self.do_it=threading.Thread(target=self.install)
            self.do_it.start()            
    def checkFirst(self):
        flag=True
        for i in self.ModuleNames:
            try:
                exec('import {}'.format(i))
            except:
                flag=False
                self.toInstall.append(i)
        return flag
    def checknet(self):
        while True:
            if self.completed is True:
                break
            if NetworkCheck().MTest() is False:
                self.noNet=False
                started.critical('>_< Need Internet Connection')
                a=messagebox.showerror('>_< Need Internet Connection','It seems some modules are needed!!! So for next time try opening this with Internet connection.')
                self.announce.specialcase()
                self.installing.destroy()
                sys.exit(0)
            else:
                self.noNet=True
    def register(self):
        self.completed=True   
        self.destroy()
    def bthover(self,status):
        if status:
            self.done.config(bg=self.backcolor[1],fg=self.textcolor[1])
        else:
            self.done.config(bg=self.backcolor[0],fg=self.textcolor[0])
    def arrange(self):
        self.MFrame.pack(expand=True,fill=BOTH)
        self.HiFrame.pack(fill=X)
        self.Hi.pack(padx=3,pady=3,anchor='n')
        self.InstallerFrame.pack(pady=6)
        self.installing.pack()
        self.announce.pack(side=BOTTOM)
        self.installing.start()
    def exit_from_here(self):
        self.completed=False
        self.destroy()
    def install(self):
        while True:
            if self.noNet is not None:break
        if self.noNet is False:
            sys.exit(0)
            
        for i in self.toInstall:
            self.announce.note=self.PackageNames[i]
            started.debug('Installing {}'.format(i))
            try:
                subprocess.check_call([sys.executable,'-m','pip','install',self.PackageNames[i]])
            except:
                os.system('pip install {}'.format(self.PackageNames[i]))
            started.info('Installed {}'.format(i))
        try:
            self.installing.stop()
            self.InstallerFrame.destroy()
            self.New=Frame(self.MFrame,bg=self.backcolor[0])
            self.New.pack()
            self.newannounce=Label(self.New,text='Completed',font=('Comic Sans MS', 12, 'bold italic'),fg='#f1f1ff',bg='#5a5a5c')
            self.done=Button(self.New,text=' Continue ',command=self.register,relief=FLAT,fg=self.textcolor[0],bg=self.backcolor[0])
            self.done.bind('<Enter>',lambda x:self.bthover(True))
            self.done.bind('<Leave>',lambda x:self.bthover(False))
            self.New.pack(pady=10,fill=BOTH)
            self.newannounce.pack(fill=BOTH)
            self.done.pack(side=RIGHT,fill=X)
        except:
            print('hello',self.noNet,threading.active_count())
            sys.exit(0)
if __name__=='__main__':
    a=Installer()
    a.mainloop()    