from mutagen.mp3 import MP3
class AudioB:
    def __init__(self,path):
        self.song=MP3(path)
        self.length=self.song.info.length
        self.refine()
    def refine(self):
        self.hour=int(self.length//3600)
        self.length=self.length-3600*self.hour
        self.minutes=int(self.length//60)
        self.length=self.length-60*self.minutes
        self.seconds=int(self.length)+1 if self.length-int(self.length)>=0.5 else int(self.length)
if __name__=='__main__':
    a=AudioB(input("Enter the Path: "))
    print('{}:{}:{}'.format(a.hour,a.minutes,a.seconds))