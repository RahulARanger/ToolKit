from dir.instwin import *
import threading
class ToolKit:
    def __init__(self):
        self.PageZero=Mini()
    def start(self):
        try:
            self.PageZero.mainloop()
            if self.PageZero.completed is False:
                print('wht',self.PageZero.completed)
                assert(False)
        except:
            print('Failed..')
            sys.exit(0)
        print('Page 0 is succesfully Completed')
if __name__=='__main__':
    kit=ToolKit()
    kit.start()
