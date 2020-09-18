from dir.instwin import *
import threading
class ToolKit:
    def __init__(self):
        self.PageZero=Mini()
    def start(self):
        self.PageZero.mainloop()
        if self.PageZero.failed or not self.PageZero.completed:
            print(threading.active_count())
            sys.exit(0)
        print('Page 0 is succesfully Completed')
if __name__=='__main__':
    ToolKit().start()
