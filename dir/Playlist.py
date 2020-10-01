import json
from tkinter import *
# TODO:  script that parses the JSON file and then adds or modifies the playlists

# ? delete_playlist is working 

# TODO: to delete a whole playlist call delete_playlist(name_of_exisiting_playlist) method

#? add_playlist() is also now working (returns False if it recieves already exisiting playlist)

# TODO: to add the playlist into JSON file we call add_playlist(name_of_playlist,list_of_songs) method

#? modify_playlist() is now working 

# TODO: modify_playlist adds/deletes a song from a exisiting playlist

# TODO: modify_playlist(True,playlist,song_path) to add the song to the playlist and modify_playlist(False,playlist,song_path) to delete the song_path

class PlayListParser:
    def __init__(self):
        self.file='dir\\root\\playlists.json'
        self.start()
    def start(self):
        with open(self.file,'r') as hand:
            self.data=json.loads(hand.read())
        self.playlists=self.data['Playlists']
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

class PlayListButton(Label):
    def __init__(self,parent,name):
        super().__init__(parent)
        self.config(text=name)
        self.arrange()
    def arrange(self):
        pass
class PlayList(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Select Any Playlist')
        self.grab_set()
        self.PLO=PlayListParser() #(PlayListObject)
        self.arrange()
    def arrange(self):
        self.bts=[]
        for i in self.PLO.playlists:
            self.bts.append(PlayListButton(self,i))
        for i in self.bts:
            i.pack()

if __name__=='__main__':
    a=Tk()
    bt=Button(a,text='Open it',command=PlayList)
    bt.pack()
    a.mainloop()