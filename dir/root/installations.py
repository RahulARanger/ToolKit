
# TODO: for installing PIL package (image related package)
#os.system('pip install pillow')
#os.system('pip install --upgrade pip')
#TODO: For installing pyglet package that can add .ttf files (font files) for adding the custom fonts
#os.system('pip install pyglet')
#TODO: For installing google translate API 
#os.system('pip install googletrans')
# TODO: To install the youtube api (not official ones)
import subprocess
import sys
import os
class StepZero:
    def __init__(self):
        self.packages=['pytube3','googletrans','pyglet','pillow']
    def pre_install(self):
        for i in self.packages:
            self.start(i)
    def start(self,package):
        try:
            subprocess.check_call([sys.executable,'-m','pip','install','pytube3'])
        except:
            os.system('pip install {}'.format(package))
if __name__=='__main__':
    # TODO: to begin with basic installations
    a=StepZero()
    a.pre_install()