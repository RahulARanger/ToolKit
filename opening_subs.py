from tkinter import *
class SearchingLabel(Label):
	def __init__(self,parent):
		super().__init__(parent)
		self.config(text='Searching.../...')
		self.toggle=False
		self.goon=True
		self.after(1000,self.change)
	def change(self):
		if not self.goon:
			self.config(text='Click to any stream to know to More/select it')
			return
		if self.toggle:self.config(text='Searching....\...')
		else:self.config(text='Searching.../....')
		self.toggle=not(self.toggle)
		self.after(500,self.change)
root=Tk()
SearchingLabel(root).pack()
root.mainloop()
