

# TODO: for installing PIL package (image related package)
#os.system('pip install pillow')

#TODO: For installing pyglet package that can add .ttf files (font files) for adding the custom fonts
#os.system('pip install pyglet')

#TODO: For installing google translate API 
#os.system('pip install googletrans')

# TODO: To install the youtube api (not official ones)
# os.system('pip install pytybe3)

import subprocess
import sys
import os
import time
import urllib.request
from tkinter import font
from tkinter.ttk import Progressbar
import threading
try:
    from root.animatedgif import * # When executed from this file
except:
    from dir.root.animatedgif import *
from tkinter import *
class StepZero:
    def __init__(self):
        self.import_names=['pytube','googletrans','pyglet','PIL']
        self.to_install=[]
        self.import_downloads={'pytube':'pytube3','pyglet':'pyglet','googletrans':'googletrans','PIL':'pillow'}
    def check(self,bar):
        import_='import '
        for i in range(len(self.import_names)):
            try:
                bar['value']+=(i/len(self.import_names))*100
                time.sleep(0.2)
                exec(import_+self.import_names[i])
            except:
                self.to_install.append(self.import_downloads[self.import_names[i]])
    def install(self,lb):
        for i in self.to_install:
            text_='Downloading and Installing '
            wht=text_+i+' Package...'
            lb.config(text=text_+i)
            self.start(i)
    def start(self,package):
        try:
            subprocess.check_call([sys.executable,'-m','pip','install',package])
        except:
            os.system('pip install {}'.format(package))

class Mini(Tk):
    def __init__(self):
        super().__init__()
        self.failed=False
        print('*')
        self.check='https://www.google.co.in/'
        self.iconbitmap('Resources\Media\download.ico')
        self['bg']='#FFFFFF'
        self.title('Welcome to Anvandbar')
        x=int((self.winfo_screenwidth()-360)/2)
        y=int((self.winfo_screenheight()-400)/2)
        self.geometry('360x400+{}+{}'.format(x,y))
        self.result=None
        self.arrange()
    def arrange(self):
        self.hi=AnimatedGif(self,'Resources\Media\\welcoming.gif',0.06)
        self.checking=StepZero()
        self.resizable(0,0) # No maximize button
        self.hi.place(x=0,y=0)
        self.hi.start()
        self.place=threading.Thread(target=self.work,name='Wait')
        self.place.start()
        
    def work(self):
        time.sleep(1.2)
        self.pb=Progressbar(self,orient=HORIZONTAL,length=260,mode='determinate')
        self.pb.place(x=50,y=315)
        self.pb['value']=0
        checker=threading.Thread(target=self.checking.check,args=(self.pb,))
        checker.start()
        self.lb=Label(self,text='Checking Modules...',font=('Comic Sans MS',12,'bold'))
        self.lb['bg']='#FFFFFF'
        self.lb.place(x=80,y=350)
        checker.join()
        self.start_install()
    def test(self):
        try:
            urllib.request.urlopen(self.check)
            self.result=True
        except:
            print('No Internet Connection')
            self.result=False
    def start_install(self):
        result=True if len(self.checking.to_install)>0 else False
        self.pb.destroy()
        self.pb=Progressbar(self,orient=HORIZONTAL,length=260,mode='indeterminate')
        if result:
            self.test()
            if self.result is False:
                self.lb.destroy()
                self.hi.destroy()
                self['bg']='black'
                self.title('Modules Download Failed...')
                x=int((self.winfo_screenwidth()-350)/2)
                y=int((self.winfo_screenheight()-500)/2)
                self.geometry('350x500+{}+{}'.format(x,y))
                self.iconbitmap('Resources\Media\error.ico')
                self.sorry=AnimatedGif(self,'Resources\Media\\sorry.gif',0.03)
                self.sorry.start()
                self.lb=Label(self,text='No Internet Connection',font=('Arial',15,'bold'))
                self.lb2=Label(self,text='Please Try again later after connecting to Internet\n (for downloading Modules)',font=('Arial',10))
                self.lb2['fg']='orange'
                self.lb['bg']='black'
                self.lb2['bg']='black'
                self.lb['fg']='red'
                self.sorry.place(x=0,y=0)
                self.lb2.place(x=30,y=450)
                self.resizable(0,0)
                self.lb.place(x=70,y=420)
                return None
            self.pb.place(x=50,y=315)
            self.pb.start()
            self.lb.place_configure(x=50,y=350)
            self.lb.config(text='Downloading and Installing Modules...')
            installing_thread=threading.Thread(target=self.checking.install,args=(self.lb,),name='Installer')
            installing_thread.start()
            installing_thread.join()
        self.pb.destroy()
        self.lb.config(text='Opening...')
        self.lb.place_configure(x=60,y=350)
        time.sleep(1)
if __name__=='__main__':
    a=Mini()
    a.mainloop()
    del a