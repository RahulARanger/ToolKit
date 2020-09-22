from dir.instwin import *
from dir.Main_Window import *
class ToolKit:
    def __init__(self):
        self.PageZero=Installer()        
    def start(self):
        self.PageZero.mainloop()        
        if self.PageZero.completed is False:
            return False
        else:
            del self.PageZero
            self.start_page1()
    def start_page1(self):
        self.PageOne=Main()
        self.PageOne.mainloop()
    def __del__(self):
        print('APP TERMINATED')
if __name__=='__main__':
    kit=ToolKit()
    kit.start()
