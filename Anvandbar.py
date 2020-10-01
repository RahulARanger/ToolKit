from dir.instwin import *
while True:
    print('The Following Messages in these Prompt are Just Log Messages!!! Just Ignore them')
    PageZero=Installer()
    PageZero.mainloop()
    if PageZero.completed is False:
        break
    del PageZero
    from dir.Main_Window import *
    PageOne=MainWindow()
    PageOne.mainloop()
    break
