from tkinter import *
import subprocess
import os
from tkinter.ttk import Progressbar
class Install_Bar(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.ModuleNames=['pytube','googletrans','pyglet','PIL']
        self.PackageNames={'pytube':'pytube3','pyglet':'pyglet','googletrans':'googletrans','PIL':'pillow'}
        self.index=0
        self.Installing=Progressbar(self,orient=HORIZONTAL,length=250,mode='indeterminate')
        self.lb=Label(self,text='Downloading')
        self.lb.pack()
        self.Installing.pack()
        self.Installing.start()
        
        self.after(100,self.install_them)
        
    def install_them(self):
        try:
            print(self.ModuleNames[self.index])
            if self.index>=len(self.ModuleNames):return None
            exec('import {}'.format(self.ModuleNames[self.index]))
            self.index+=1
        except:
            package=self.PackageNames[self.ModuleNames[self.index]]
            try:
                subprocess.check_call([sys.executable,'-m','pip','install',package])
            except:
                os.system('pip install {}'.format(package))
        self.after(100,self.install_them)



root=Tk()
a=Install_Bar(root)
a.pack()
root.mainloop()
