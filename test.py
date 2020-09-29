import pygame
from tkinter import *
test=Tk()
pygame.mixer.init()
def play():
    pygame.mixer.music.load('Resources\Media\Kokuhaku bungee jump.mp3')
    pygame.mixer.music.play()
def explosion():
    a=pygame.mixer.Sound(file='Resources\Media\explosion.ogg')
    a.play()
exp=Button(test,text='Explosion',command=explosion)
music=Button(test,text='Play',command=play)
exp.pack()
music.pack()
test.mainloop()
