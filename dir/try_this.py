from tkinter import *
class Selection(Toplevel):
    def __init__(self,parent,options,var):
        super().__init__(parent)
        self.config(bg='orange')
        self.TopFrame=Frame(self)
        
