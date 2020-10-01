from tkinter import *
import tkinter.ttk as ttk
import pygame
import os
import re
from mutagen.mp3 import MP3
from tkinter import filedialog
pygame.init()
pygame.mixer.init()
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
    def __init__(self,parent,sym,x='bold'):
        super().__init__(parent)
        self.config(text=sym)
        self.textcolor=('#f1f1ff',)
        self.backcolor=('#007acc','#33BBFF')
        self.specialcolor='#FF5500'
        self.enable=False
        self.togglestatus=False
        self.config(bg=self.backcolor[0])
        if self['text']=='    🔄️':
            self.config(width=3)
        self.config(fg=self.textcolor[0],font=('Helvtica',13,x),height=2)
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Leave>',lambda x:self.bthover(False))
        self.bind('<Button-1>',lambda x:self.btaffect(False))        
        if self['text']=='    🔄️':
            self.after(1000,self.toggle)
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
            self.config(bg=self.backcolor[1])
            self.config(relief=GROOVE)
        else:
            self.config(bg=self.backcolor[0])
            self.config(relief=FLAT)
    def btaffect(self,status):
        print(status)
        if status is True:
            self.config(relief=FLAT)

class MediaPlayer(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        pygame.mixer.music.get_endevent()
        self.config(bg='#007acc')
        self.play=LabelButtons(self,'  ▶ ')
        self.replay=LabelButtons(self,'    🔄️')
        self.playing=False 
        self.status=None
        self.checkpoint=None
        self.modifier=None
        self.options=['Single File','PlayList']
        self.selected=StringVar()
        self.uploaded=False
        self.started=False
        self.pause=False
        self.choice=ComboBox(self,self.selected,self.options)
        self.play.bind('<Button-1>',lambda x:self.flip(True))
        self.replay.bind('<Button-1>',lambda x:self.flip(False))
        self.selected.trace('w',self.go_for_it)
        self.Import=LabelButtons(self,'Import','normal')
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
            print(self.playing,self.started)
            if not self.playing:
                print('a')
                self.play.config(text='⏸️')
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
                pygame.mixer.music.load(self.file)
                pygame.mixer.music.play()
                temp=AudioB(self.file)
                self.totallength=temp.length
                self.reset('end')
                self.showl=Label(self,text='{}:{}'.format(0,0),bg='#007acc',fg='white')
                self.showr=Label(self,text='{}:{}'.format(temp.minutes,temp.seconds),bg='#007acc',fg='white')            
                self.scale=ttk.Scale(self,orient=HORIZONTAL,from_=0,to_=int(self.totallength),variable=self.barstatus,command=self.change_it)
                self.showl.pack(side=LEFT,padx=3)
                self.scale.pack(side=LEFT,padx=3)
                self.showr.pack(side=LEFT,padx=3)
                self.play.config(text='⏸️')
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
            if self.status=='Single File':self.Import.bind('<Button-1>',lambda x:self.single_player())
            else:self.Import.bind('<Button-1>',lambda x:self.playlist())
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
                except:pass
                self.Import.bind('<Button-1>',lambda x:self.single_player())
                if self.status is None:self.single_player()
                self.status='Single File'
            else:
                self.Import.unbind('<Button-1>')
                self.status='PlayList'
                self.Import.bind('<Button-1>',lambda x:self.playlist())
    def playlist(self):
        pass
    def single_player(self):
        
        file=filedialog.askopenfilename(title='Open the Audio File',initialdir=os.getcwd(),filetypes=(('Audio Files','.mp3'),))
        if len(file)==0:
            pass
        else:
            self.file=file
            self.play.config(text='  ▶ ')
            self.started=False
            MUSIC_END = pygame.USEREVENT+1
            pygame.mixer.music.set_endevent(MUSIC_END)
            pygame.mixer.music.load(self.file)
            self.uploaded=True
            try:
                self.scale.destroy()
                self.showl.destroy()
                self.showr.destroy()
            except:pass
            self.title=(re.findall(r'([^/]+).mp3',self.file)[0])
            temp=AudioB(self.file)
            print('changed')
            self.totallength=temp.length
            self.showl=Label(self,text='{}:{}'.format(0,0),bg='#007acc',fg='white')
            self.showr=Label(self,text='{}:{}'.format(temp.minutes,temp.seconds),bg='#007acc',fg='white')
            print(int(self.totallength))
            self.scale=ttk.Scale(self,orient=HORIZONTAL,from_=0,to_=int(self.totallength),variable=self.barstatus,command=self.change_it)
            self.showl.pack(side=LEFT,padx=3)
            self.scale.pack(side=LEFT,padx=3)
            self.showr.pack(side=LEFT,padx=3)
if __name__=='__main__':
    a=Tk()
    b=MediaPlayer(a)
    b.pack(fill=X,expand=True)
    a.mainloop()