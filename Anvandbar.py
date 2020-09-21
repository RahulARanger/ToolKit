from dir.instwin import *
class ToolKit:
    def __init__(self):
        self.PageZero=Installer()
    def start(self):
        self.PageZero.mainloop()        
        if self.PageZero.completed is False:
            return False
        print('Page 0 is executed')
    def __del__(self):
        print('APP TERMINATED')
if __name__=='__main__':
    kit=ToolKit()
    kit.start()
