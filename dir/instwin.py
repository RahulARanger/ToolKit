

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
from tkinter import messagebox
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
        self.check='https://www.google.co.in/'
        self.iconbitmap('Resources\Media\download.ico')
        self.increment=0
        self.balance()
        self['bg']='#FFFFFF'
        self.title('Welcome to Anvandbar')
        self.connected=None
        self.completed=False
        self.arrange()
    def balance(self):
        height=340+self.increment
        x=int((self.winfo_screenwidth()-380)/2)
        y=int((self.winfo_screenheight()-height)/2)
        self.geometry('{}x{}+{}+{}'.format(380,height,x,y))
        self.increment+=30
    def test(self):
        try:
            urllib.request.urlopen(self.check)
            self.connected=True
        except:
            print('No Internet Connection')
            self.result=False
    def arrange(self):
        self.checking=StepZero()
        self.resizable(0,0) # No maximize button
        self.attributes('-disabled', True)
        self.backg=Frame(self,background='#B3FFE5')
        self.backg.pack(expand=True,fill=BOTH)
        self.hi=AnimatedGif(self.backg,'Resources\Media\\welcoming.gif',0.06)
        self.hi.pack(padx=6,pady=6)
        self.hi.start()
        self.workingpanel=Frame(self.backg,width=380)
        self.workingpanel2=Frame(self.backg,width=380)
        self.workingpanel3=Frame(self.backg,width=380)
        self.workingpanel4=Frame(self.backg,width=380)
        self.workingpanel.pack()
        self.workingpanel2.pack(padx=6,fill=BOTH,expand=1,pady=2)
        self.workingpanel3.pack(padx=6,fill=BOTH,expand=1,pady=2)
        self.workingpanel4.pack(padx=6,fill=BOTH,expand=1)
        self.place=threading.Thread(target=self.work,name='Wait')
        self.place.start()
    def work(self):
        time.sleep(1)
        self.workingpanel.config(background='#B3FFE5')
        self.workingpanel.pack_configure(padx=6,fill=BOTH,expand=1)
        self.contbt=Button(self.workingpanel,text='Continue')
        self.bt=Button(self.workingpanel,text='Continue',relief=FLAT)
        self.note=Label(self.workingpanel,text='Checking Modules',font=('verdana',10,'bold'),background='#0099E6')
        self.note.pack(side=LEFT,anchor='nw',padx=2)
        self.pb1=Progressbar(self.workingpanel,orient=HORIZONTAL,length=260,mode='determinate')
        self.pb1.pack(side=LEFT,anchor='nw',padx=3)
        self.pb1['value']=0
        checker=threading.Thread(target=self.checking.check,args=(self.pb1,))
        checker.start()
        checker.join()
        self.pb1.destroy()
        self.needin=AnimatedGif(self.workingpanel,'Resources\\Media\\tick2.gif')
        self.needin.start()
        self.needin.pack(side=LEFT,anchor='nw',padx=3)
        self.balance()
        need=True if len(self.checking.to_install)>0 else False
        if need:
            self.start_install()
        self.attributes('-disabled', False)
        self.workingpanel3.config(background='#B3FFE5')
        self.workingpanel3.pack_configure(padx=6,fill=BOTH,expand=1)
        self.note2=Label(self.workingpanel3,text='Installation:',font=('verdana',10,'bold'),background='#0099E6')
        self.note2.pack(side=LEFT,anchor='nw',padx=2,pady=3)
        self.needin=AnimatedGif(self.workingpanel3,'Resources\\Media\\tick2.gif')
        self.needin.start()
        self.needin.pack(side=LEFT,anchor='nw',padx=3)
        self.workingpanel4.config(background='#B3FFE5')
        self.workingpanel4.pack_configure(padx=6,fill=BOTH,expand=1)
        self.note4=Button(self.workingpanel4,text='Continue',command=self.register)
        self.note4.config(relief='flat',width=10,height=2,bg='#FF8000',font=('Comic Sans MS',10,'bold'))
        self.note4.pack(side=RIGHT,anchor='se',padx=3,pady=3)
        self.note4.bind('<Leave>',lambda x:self.bthover(False))
        self.note4.bind('<Enter>',lambda x:self.bthover(True))
        self.note4.bind('<Return>',lambda x:self.bthover(None))
        self.balance()
    def register(self):
        self.completed=True
        self.destroy()
    def bthover(self,status):
        if status is None:
            self.register()
        else:
            if status:
                self.note4['bg']='#FFFF00'
                self.note4.pack_configure(padx=0,pady=0)
                self.note4.config(relief='ridge')
            else:
                self.note4['bg']='#FF8000'
                self.note4.pack_configure(padx=3,pady=3)
                self.note4.config(relief='flat')
    def start_install(self):
        self.test()
        print(self.connected)
        if self.connected:
            self.pb2=Progressbar(self.workingpanel2,orient=HORIZONTAL,length=260,mode='indeterminate')
            self.workingpanel2.pack_configure(padx=6,fill=BOTH,expand=1)
            self.pname=Label(self.workingpanel2,text='Downloading..',font=('verdana',8,'bold'),background='#0099E6')
            self.pname.pack(side=LEFT,anchor='nw',padx=2)
            self.pb2.pack(side=LEFT,anchor='nw',padx=3)
            self.pb2.start()
            installing_thread=threading.Thread(target=self.checking.install,args=(self.pname,),name='Installer')
            installing_thread.start()
            a=messagebox.showinfo('Don\'t Worry happens only at once','Need Some Modules!!! Downloading those so please wait!!!')
            installing_thread.join()
            self.pb2.destroy()
            self.workingpanel2.destroy()
            self.pname.destroy()
        else:
            widgets=self.winfo_children()
            for i in widgets:
                i.pack_forget()
            self.title='No Internet Connection'
            frame=Frame(self,background='#B3FFE5')
            frame.pack(expand=True,fill=BOTH)
            sorry=AnimatedGif(frame,'Resources\Media\\sorry.gif',0.03)
            sorry.pack(padx=6,pady=6)
            sorry.start()
            a=messagebox.showinfo('Need Internet Connection','It seems some modules are needed!!! So for next time try opening this with Internet connection.')
if __name__=='__main__':
    a=Mini()
    a.mainloop()
    