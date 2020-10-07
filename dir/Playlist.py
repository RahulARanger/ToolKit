import json
from tkinter import *
import os
try:
    from root.Dialogs import *    
except:
    from dir.root.Dialogs import *
# TODO:  script that parses the JSON file and then adds or modifies the playlists

# ? delete_playlist is working 

# TODO: to delete a whole playlist call delete_playlist(name_of_exisiting_playlist) method

#? add_playlist() is also now working (returns False if it recieves already exisiting playlist)

# TODO: to add the playlist into JSON file we call add_playlist(name_of_playlist,list_of_songs) method

#? modify_playlist() is now working 

# TODO: modify_playlist adds/deletes a song from a exisiting playlist

# TODO: modify_playlist(True,playlist,song_path) to add the song to the playlist and modify_playlist(False,playlist,song_path) to clearing deleted songs

class PlayListParser:
    def __init__(self):
        self.file='dir\\root\\playlists.json'
        self.start()
    def start(self):
        with open(self.file,'r') as hand:
            self.data=json.loads(hand.read())        
        self.playlists=self.data['Playlists']
        for i in self.playlists:
            for j in self.data[i]:
                if not os.path.exists(j):
                    self.modify_playlist(False,i,j)
                    return None
    def getPlaylists(self):
        return self.playlists
    def getSongs(self,playlist):
        return self.data[playlist]
    def add_playlist(self,name,songs):
        if name in self.playlists:
            print('This Playlists is alrady exisiting in the list ')
            print('Either try renaming either one')
            return False
        self.playlists.append(name)
        self.data[name]=songs
        self.write_it()
        self.start()
    def write_it(self):
        with open(self.file,'w') as hand:
            json.dump(self.data,hand,indent=4)
    def delete_playlist(self,name):
        del self.playlists[self.playlists.index(name)]
        self.data['Playlists']=self.playlists
        del self.data[name]
        self.write_it()
        self.start()
    def modify_playlist(self,add,playlist,song):
        
        if add:
            self.data[playlist].append(song)
        else:
            at=self.data[playlist].index(song)
            del self.data[playlist][at]
        self.write_it()
        self.start()
    def rename_playlist(self,name,newname):
        # ! This is done assuming name exists in the playlist
        store=self.data[name]
        self.delete_playlist(name)
        self.add_playlist(newname,store)
        self.start()
    def delete_song(self,playlist,song):
        if self.check_song(playlist,song):
            at=self.data[playlist].index(song)
            del self.data[playlist][at]
        print('Backed')

    def check_song(self,playlist,song):
        if song in self.data[playlist]:return True
        else:False
    def check(self,new):        
        if new in self.getPlaylists():return False
        else:return True

class PlayListLevel(Toplevel):
    def __init__(self,parent,name,songs):
        super().__init__(parent)
        self.p=parent
        self.title='Modify the Playlist {}'.format(name)
        self.lst=songs
    def on_closing(self):
        self.p.deiconify()
        self.destroy()
class PlayListButton(Frame):
    def __init__(self,parent,name,plo):
        super().__init__(parent)
        self.name=Label(self)        
        self.name.config(text=name)
        self.PLO=plo
        self.locked=False
        self.parent=parent
        if name=='Default':self.locked=True
        self.backcolor=('#FF8C19',)
        self.newname=name
        self['bg']=self.backcolor[0]        
        self.fontcolor=('#FFE6F7',)
        self.bind('<Enter>',lambda x:self.bthover(True))
        self.bind('<Button-1>',lambda x:self.pressed(True))        
        self.bind('<ButtonRelease-1>',lambda x:self.pressed(False))        
        self.config(borderwidth=3)
        self.deleteit=Button(self,text='🔒' if self.locked else 'T',command=self.deletep,cursor='diamond_cross')
        self.Modify=Button(self,text='🔒' if self.locked else '竄',command=self.modifyp,cursor='pencil')
        if self.locked:
            self.Modify.config(state=DISABLED)
            self.deleteit.config(state=DISABLED)
        self.Modify.config(relief=RIDGE)
        self.deleteit.config(relief=RIDGE)
        self.designname()
        self.bind('<Leave>',lambda X:self.bthover(False))
        self.config(relief=RIDGE)
        self.arrange()
    def rename(self):
        self.name.destroy()
        self.name=Entry(self)              
        self.name.pack(anchor='n')  
        self.name.focus_set()     
        self.name.bind('<Return>',lambda x:self.done())     
    def designname(self):
        self.name.config(fg=self.fontcolor[0])
        self.name['bg']=self.backcolor[0]        
        self.name.config(font=('Arial',8,'bold'))
        self.name.bind('<ButtonRelease-1>',lambda x:self.pressed(False))
        if not self.locked:self.name.bind('<Double-Button-1>',lambda x:self.rename())
        self.name.bind('<Button-1>',lambda x:self.pressed(True))
    def modifyp(self):
        self.withdraw()
        

    def done(self):
        newname=self.name.get()[:10]
        newname=newname.title()
        if self.PLO.check(newname):
            self.PLO.rename_playlist(self.newname,newname)
            self.newname=newname            
        else:
            Warning(self)
        self.name.destroy()
        self.name=Label(self)
        self.name.config(text=self.newname)
        self.designname()
        self.name.pack()       
    def pressed(self,status):
        if status:
            self.config(relief=RAISED)            
        else:
            self.config(relief=SUNKEN)
    def bthover(self,status):
        if status:
            self.name.config(font=('Arial',12,'bold'))
            self.config(relief=GROOVE)
        else:
            self.name.config(font=('Arial',8,'bold'))
            self.config(relief=RIDGE)
    def deletep(self):
        pass
    def arrange(self):
        self.name.pack(anchor='n')        
        self.deleteit.pack(side=RIGHT)
        self.Modify.pack(side=RIGHT)
class PlayList(Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        self.geometry('200x200')
        self.resizable(0,0)
        self.title('Select Any Playlist')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.PLO=PlayListParser() #(PlayListObject)
        self.arrange()
    def arrange(self):
        self.bts=[]
        for i in self.PLO.playlists:
            self.bts.append(PlayListButton(self,i,self.PLO))
        for i in self.bts:
            i.pack(fill=X)
    def on_closing(self):
        a=self.master
        while True:
            try:
                a.deiconify()
                break
            except:
                a=a.master
        self.destroy()

if __name__=='__main__':
    a=Tk()
    bt=Button(a,text='Open it',command=lambda :PlayList(a))
    bt.pack()
    a.mainloop()