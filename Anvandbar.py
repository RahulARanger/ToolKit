from dir.instwin import *
import threading
class ToolKit:
    def __init__(self):
        self.PageZero=Mini()
    def start(self):
        self.PageZero.mainloop()
        if self.PageZero.failed:
            return
if __name__=='__main__':
    ToolKit().start()
