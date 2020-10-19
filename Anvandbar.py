import os
import threading
import sys
def createPreFiles():
    if os.path.exists('Resources/Logs'):
        pass
    else:
        os.mkdir('Resources/Logs')        
createPreFiles()
from dir.root.LogFiles import *
from dir.instwin import *
started.debug('App was Opened')
while True:
    print('The Following Messages in these Prompt are Just Log Messages!!! Just Ignore them')
    PageZero=Installer()
    PageZero.mainloop()
    if PageZero.completed is False:
        started.error('App was Closed before starting')
        print(threading.active_count())
        sys.exit(0)
    del PageZero
    from dir.Main_Window import *
    started.info('Opened Main Window')
    PageOne=MainWindow()
    PageOne.mainloop()
    started.debug('Exited the App')
    break