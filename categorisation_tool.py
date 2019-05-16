# python version 3.7
# coding: utf-8
#(c)Sunny AVRY
import pygame,os,ctypes,time,random,sys,csv
from pygame.locals import *
from pathlib import Path
from time import*

################### SCREEN SETUP ###################
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (6,28)
SM_CXSCREEN = 0
SM_CYSCREEN = 1
largeurScreen = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
hauteurScreen = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)
print ("Résolution écran : %d x %d" % (largeurScreen, hauteurScreen))

################### PYGAME INITIALISATION ###################
pygame.init()
pygame.mixer.quit()
pygame.font.init()

screen = pygame.display.set_mode((largeurScreen-12,hauteurScreen-75))
def fill_call(): fill()

################### VARIABLES ###################

categories = []
list_buttons = []

################### DEFINITIONS ###################

def display_text(texte,positionx,positiony,police,taille,couleur):
    police=pygame.font.SysFont(police, taille)
    texte=police.render(texte, 1, couleur)
    rectangle=texte.get_rect()
    rectangle.centerx = positionx
    rectangle.bottom = positiony
    screen.blit(texte, rectangle)
    pygame.display.flip()

def button(texte,couleur,positionx,positiony,longueur,largeur):
    bouton=pygame.draw.rect(screen, couleur,(positionx, positiony, longueur, largeur))
    display_text(texte,positionx+longueur/2,positiony+largeur/1.4,"VERDANA",14,(0,0,0))

def enter():
    enter=False
    while not enter:
            for ev in pygame.event.get():
                    if ev.type==KEYDOWN:
                            if ev.key==K_SPACE:
                                    enter=True
                                    return True
def fill():
    screen.fill([0,0,0])
    pygame.display.flip()

def cat():
	categories_file = Path("categories_file.txt")
	if categories_file.is_file():
	   	with open("categories_file.txt") as f:
	   		content = f.readlines()
	   		content = [x.strip() for x in content]
	   		categories = content
	   		return categories
	else:
		n = input("number of categories: ")
		categories_file = open("categories_file.txt", "a")
		for i in range(1, n + 1):
		   	cat = str(raw_input("categorie " + str(i) + ": "))
		   	categories.append(cat)
		   	categories_file.write(cat + "\n")
		   	categories_file.close()

def buttons():
	x = 30
	y = (hauteurScreen-75)/2
	for i in range(0,len(categories)):
		button(categories[i],(255, 255, 255), x, y, 200, 50)
		list_buttons.append([categories[i], x, y, x + 200, y + 50])
		x += 220
		if x > largeurScreen - 200:
			x = 30
			y += 70

def removeletter(sentence):
	sentence = sentence[1:]
	return sentence

################### MAIN ###################

chat = []
categories = cat()
buttons()

chat_recoded = open("chat_recoded.txt", "a")

for line in open('chat.txt', encoding='utf-8-sig'):
	chat.append(line)

chat = [x.strip() for x in chat]

end = False
while not end:
	for i in range(0, len(chat)):
		p = chat[i]
		pt_virgule = 0
		while pt_virgule < 2:
			if (p[0] == ";"):
				pt_virgule += 1
			p = removeletter(p)
		display_text(p,largeurScreen/2,200,"VERDANA",18,(255,255,255))
		pygame.display.flip()
		
		fin = False
		while not fin:
			for ev in pygame.event.get():
				if ev.type == pygame.MOUSEBUTTONDOWN:
						if ev.button == 1:
							for j in range(0,len(list_buttons)):
								if ev.pos[0] > list_buttons[j][1] and ev.pos[0] < list_buttons[j][3] and ev.pos[1] > list_buttons[j][2] and ev.pos[1] < list_buttons[j][4]:
										pygame.draw.rect(screen,(0,0,0),(0,0,1680,450))
										pygame.display.flip() 
										display_text("précédent : "+list_buttons[j][0],largeurScreen/2,400,"VERDANA",18,(255,255,255))
										pygame.display.flip()
										q = chat[i]
										count = 0
										while q[count].isnumeric() or q[count] == "_":
											count += 1
										chat_recoded.write(chat[i][0:count] + ";" + list_buttons[j][0] + ";" + p + "\n")
										print(chat[i][0:count] + ";" + list_buttons[j][0] + ";" + p)
										fin = True
				if ev.type == pygame.QUIT:
					pygame.quit()
					exit()
		if (i == len(chat)-1):
			end = True 

chat_recoded.close()
pygame.quit()







