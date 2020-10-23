import urllib.request
import os
# ! make sure to use the valid link for downloading
class Downloader:
    def __init__(self,link,path):
        self.link=link
        self.path=path
    def manual_install(self):
        self.manual_path()
        try:
            urllib.request.urlretrieve(self.link,self.path)
        except:
            return None
        return self.path
    def manual_path(self):
        lst=os.listdir(self.path)
        self.path=self.path+'//id{}.jpg'.format(len(lst))