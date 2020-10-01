
# ? this is the script that is not used in the application but helped a lot during it's birth
#TODO : python script that renames the files in the order
path=input('Enter the Path: ')
name=input('Enter the name: ')
import os
a=(os.listdir(path))
print(a)
path2=path+'\\'
for i in range(len(os.listdir(path))):
    os.rename(path2+a[i],path2+'{}{}.jpg'.format(name,i)) 
print(os.listdir(path))