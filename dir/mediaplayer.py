from tkinter import *
import tkinter.ttk as ttk
import os
import re
from mutagen.mp3 import MP3
try:
    from  dir.root.OtherButtonClick import *
except:
    from root.OtherButtonClick import *
from tkinter import messagebox
from tkinter import filedialog
try:
    from root.Dialogs import *    
except:
    from dir.root.Dialogs import *
pygame.init()
pygame.mixer.init()
''' Player chan: Rahul-kun, add sound feature later'''
class AudioB:
    def __init__(self,path):
        self.song=MP3(path)
        self.length=self.song.info.length
        self.minutes=int(self.length//60)
        self.seconds=int(self.length-(60*self.minutes))
class ComboBox(ttk.Combobox):
    def __init__(self,parent,var,options):
        super().__init__(parent)
        self.var=var
        self.config(height=2)
        self.options=options
        self.config(textvariable=self.var,values=self.options,state='readonly')

class LabelButtons(Label):
    def __init__(self,parent,sym,status=None,x='bold'):
        super().__init__(parent)
        self.status=status
        self.displaythings={'  ▶ ':'Click to play','Re':'Click to Replay',' | | ':'Click to Pause','Import':'Click to Select Music Files'}
        self.config(text=sym)
        self.textcolor=('#f1f1ff',)
        self.backcolor=('#007acc','#33BBFF')
        self.specialcolor='#FF5500'
        self.enable=False
        self.w=200
        self.h=200
        self.type=None
        self.togglestatus=False
        self.config(bg=self.backcolor[0])
        if self['text']=='Re':
            self.config(width=3)
            self.after(800,self.toggle)
        self.config(fg=self.textcolor[0],font=('Helvtica',13,x),height=2)
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Leave>',lambda x:self.bthover(False))
        self.bind('<Button-1>',lambda x:self.btaffect(False))                
    def toggle(self):
        if self.enable:
            if not self.togglestatus:
                self.config(bg=self.specialcolor)
            else:
                self.config(bg=self.backcolor[1])
            self.togglestatus=not(self.togglestatus)        
        self.after(800,self.toggle)
    def bthover(self,status):
        if status is True:
            BTHOVER.play()
            self.status.set(self.displaythings[self['text']])
            self.config(bg=self.backcolor[1])
            self.config(relief=GROOVE)
        else:
            self.status.set('ZzZzZzzZzzZZzzZZ')
            self.config(bg=self.backcolor[0])
            self.config(relief=FLAT)
    def btaffect(self,status):
        print(status)
        if status is True:
            self.config(relief=FLAT)

class Display(Label):
    def __init__(self,parent,title):
        super().__init__(parent)
        self.title=title+'      '
        self.note=len(self.title)
        self.checkpoint=[i for i in self.title[:11]]
        self.pos=len(self.checkpoint)
        self.config(text=title)
        self.config(bg='#007acc')
        self.config(fg='#f1f1ff')
        self.after(600,self.slide)
    def slide(self):
        if len(self.title)>10:
            self.config(text=''.join(self.checkpoint))
            del self.checkpoint[0]
            if self.pos==len(self.title):self.pos=0
            self.checkpoint.append(self.title[self.pos])
            self.pos+=1
            self.after(1000,self.slide)
        else:self.config(text=' '.join(self.checkpoint))
class MediaPlayer(Frame):
    def __init__(self,parent,status):
        super().__init__(parent)
        global MSTATUS
        MSTATUS=status
        self.report=status
        pygame.mixer.music.get_endevent()
        self.config(bg='#007acc')
        self.play=LabelButtons(self,'  ▶ ',self.report)
        self.parent=parent
        self.replay=LabelButtons(self,'Re',self.report)
        self.playing=False 
        self.status=None
        self.failed=False
        self.checkpoint=None
        self.modifier=None
        self.options=['Single File','PlayList']
        self.selected=StringVar()
        self.file=StringVar()
        self.uploaded=False
        self.started=False
        self.pause=False
        self.choice=ComboBox(self,self.selected,self.options)
        self.play.bind('<Button-1>',lambda x:self.flip(True))
        self.replay.bind('<Button-1>',lambda x:self.flip(False))
        self.selected.trace('w',self.go_for_it)
        self.Import=LabelButtons(self,'Import',self.report,'normal')
        self.barstatus=IntVar()
        self.Import.bind('<Button-1>',lambda x:self.go_for_it())
        self.arrange()
        self.after(800,self.note)
    def reset(self,for_):
        if for_=='replay':
            self.playing=False
            self.checkpoint=None
            self.modifier=None
            self.started=False
        elif for_=='end':            
            self.checkpoint=None
            self.modifier=None
            self.started=False
            self.playing=True
            self.showl.destroy()
            self.showr.destroy()
            self.scale.destroy()
            self.titleshow.destroy()
            self.replay.enable=False
    def set(self,for_):
        if for_=='replay':
            self.playing=True
            self.started=True
    def arrange(self):
        self.play.pack(side=LEFT)
        self.replay.pack(side=LEFT)
        self.choice.pack(side=LEFT)
        self.Import.pack(side=LEFT,ipadx=4)
    def flip(self,status):
        if status:            
            if not self.playing:
                print('a')
                self.play.config(text=' | | ')
                if self.uploaded:
                    # TODO : plays 
                    if not self.started:
                        pygame.mixer.music.play(0)
                        self.started=True
                    else:
                        pygame.mixer.music.unpause()
            else:
                # TODO: pauses it
                self.play.config(text='  ▶ ',justify=RIGHT)
                if self.uploaded and self.playing:
                        pygame.mixer.music.pause()
            if self.started:self.playing=not(self.playing)
        else:
            if self.uploaded:  
                # TODO: replays
                self.replay.enable=False
                self.started,self.playing=False,False
                MUSIC_END = pygame.USEREVENT+1
                pygame.mixer.music.set_endevent(MUSIC_END)
                self.reset('replay')
                pygame.mixer.music.load(self.file.get())
                pygame.mixer.music.play()
                temp=AudioB(self.file.get())
                self.totallength=temp.length
                self.reset('end')
                self.title=(re.findall(r'([^/]+).mp3',self.file.get())[0])
                self.titleshow=Display(self,self.title)
                self.showl=Label(self,text='{}:{}'.format(0,0),bg='#007acc',fg='white')
                self.showr=Label(self,text='{}:{}'.format(temp.minutes,temp.seconds),bg='#007acc',fg='white')            
                self.scale=ttk.Scale(self,orient=HORIZONTAL,from_=0,to_=int(self.totallength),variable=self.barstatus,command=self.change_it)
                self.showl.pack(side=LEFT,padx=3)
                self.scale.pack(side=LEFT,padx=3)
                self.showr.pack(side=LEFT,padx=3)
                self.play.config(text=' | | ')
                self.titleshow.pack(side=LEFT,padx=(20,))
                self.set('replay')
    def change_it(self,*ags):
        if self.uploaded:
            self.pause=True
    def note(self):        
        if self.uploaded is True and not self.pause:
            timee=pygame.mixer.music.get_pos()
            if self.checkpoint is not None:
                self.modifier=self.checkpoint-timee
                self.checkpoint=None
            if self.modifier is not None:timee+=self.modifier
            time=int(timee/1000)
            if time<0:time=0
            time_m=time//60
            time_s=time-(60*time_m)
            self.barstatus.set(time)
            if self.playing and self.started:self.showl.config(text='{}:{}'.format(time_m,time_s))
        elif self.pause:
            t=int(self.barstatus.get())
            m=int(t//60)
            s=t-60*m
            try:
                pygame.mixer.music.set_pos(int(self.barstatus.get()))          
            except:
                self.checkpoint=None
            self.showl.config(text='{}:{}'.format(m,s))
            self.pause=False
            self.checkpoint=t*1000
        if self.uploaded:
            for i in pygame.event.get():
                if i.type==pygame.mixer.music.get_endevent():                    
                    self.replay.enable=True
                    self.reset('end')
        self.after(800,self.note)
    def go_for_it(self,*args):
        if self.status is None:
            self.status=self.selected.get()
            if self.status=='Single File':
                try:
                    self.Import.bind('<Button-1>',lambda x:self.single_player())
                except:
                    self.status=None
                    messagebox.showerror('Note!!','Try to Open Media Player After closing Yt Downloader for safety measures!')
            elif self.status=='PlayList':self.Import.bind('<Button-1>',lambda x:self.playlist())
            else:pass
        else:
            if self.status!=self.selected.get():
                try:
                    self.Import.unbind('<Button-1>')
                    pygame.mixer.music.pause()
                    self.uploaded,self.playing=False,False
                    self.reset('end')
                except:pass
            if self.selected.get()=='Single File':
                try:
                    self.Import.unbind('<Button-1>')
                    del self.playlists
                except:pass
                self.Import.bind('<Button-1>',lambda x:self.single_player())
                if self.status is None:self.single_player()
                self.status='Single File'
            elif self.selected.get()=='PlayList':
                self.Import.unbind('<Button-1>')
                self.status='PlayList'
                self.Import.bind('<Button-1>',lambda x:self.playlist())
            else:pass
    def playlist(self):        
        a=FutureUpdate(self)
    def single_player(self):        
        file=filedialog.askopenfilename(title='Open the Audio File',initialdir=os.getcwd(),filetypes=(('Audio Files (.mp3)','.mp3'),))
        if len(file)==0:
            pass
        else:
            self.file.set(file)
            self.play.config(text='  ▶ ')
            self.started=False
            MUSIC_END = pygame.USEREVENT+1
            pygame.mixer.music.set_endevent(MUSIC_END)
            pygame.mixer.music.load(self.file.get())
            self.uploaded=True
            try:
                self.scale.destroy()
                self.showl.destroy()
                self.showr.destroy()
                self.titleshow.destroy()
                self.replay.enable=False
            except:pass
            self.title=(re.findall(r'([^/]+).mp3',self.file.get())[0])
            self.titleshow=Display(self,self.title)
            self.replay.enable=True
            temp=AudioB(self.file.get())
            print('changed')
            self.totallength=temp.length
            self.showl=Label(self,text='{}:{}'.format(0,0),bg='#007acc',fg='white')
            self.showr=Label(self,text='{}:{}'.format(temp.minutes,temp.seconds),bg='#007acc',fg='white')
            print(int(self.totallength))
            self.scale=ttk.Scale(self,orient=HORIZONTAL,from_=0,to_=int(self.totallength),variable=self.barstatus,command=self.change_it)
            self.showl.pack(side=LEFT,padx=3)
            self.scale.pack(side=LEFT,padx=3)
            self.showr.pack(side=LEFT,padx=3)
            self.titleshow.pack(side=LEFT,padx=(20,))
            self.replay.enable=True
if __name__=='__main__':
    a=Tk()
    b=MediaPlayer(a,StringVar())
    b.pack(fill=X,expand=True)
    a.mainloop()