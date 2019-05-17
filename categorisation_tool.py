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

def remove_first_letter(sentence):
	sentence = sentence[1:]
	return sentence

################### MAIN ###################

chat = []  #list containing the conversation
categories = cat()
buttons()

chat_recoded = open("chat_recoded.txt", "a")

for line in open('chat.txt', encoding='utf-8-sig'):
	chat.append(line)

chat = [x.strip() for x in chat]

end_chat = False #notify the end of the chat reading 
current_sentence = 0 #number of the current chat sentence
while not end_chat:
	
	p = chat[current_sentence] #p is the current chat sentence
	
	"""
	Keeping only the chat sentence. Remove date, category and name. 
	The loop uses the function removeletter that remove one letter at each iteration of the loop.
	When 3 semicolons is found (only the dialogue is remaining), the function stops.
	"""
	semicolons = 0
	while semicolons < 2: 
		if p[0] == ";":
			semicolons+=1
		p=remove_first_letter(p)
					
	display_text(p,largeurScreen/2,200,"VERDANA",18,(255,255,255))
	pygame.display.flip()


	end_sentence = False #notify the end of the sentence reading
	while not end_sentence:
		
		"""guarantee that the current sentence is not below 0"""
		if(current_sentence <= 1): current_sentence = 1 
		for ev in pygame.event.get():
			if ev.type == pygame.MOUSEBUTTONDOWN:
					if ev.button == 1:
							for j in range(0,len(list_buttons)):
								if ev.pos[0] > list_buttons[j][1] and ev.pos[0] < list_buttons[j][3] and ev.pos[1] > list_buttons[j][2] and ev.pos[1] < list_buttons[j][4]:
									
									"""create a black screen"""
									pygame.draw.rect(screen,(0,0,0),(0,0,1680,450))
									pygame.display.flip()

									"""Display current chat sentence"""
									display_text("Catégorie précédente : "+list_buttons[j][0],largeurScreen/2,400,"VERDANA",18,(255,255,255))
									pygame.display.flip()
									q = chat[current_sentence]
									count = 0
									while q[count].isnumeric() or q[count] == "_":
										count += 1
									chat_recoded.write(chat[current_sentence][0:count] + ";" + list_buttons[j][0] + ";" + p + "\n")
									print("["+str(current_sentence)+"] "+chat[current_sentence][0:count] + ";" + list_buttons[j][0] + ";" + p) #numéro de ligne + date + nom + phrase 
									current_sentence+=1
									print(current_sentence)
									end_sentence = True
					if ev.button == 3:
						"""create a black screen"""
						pygame.draw.rect(screen,(0,0,0),(0,0,1680,450))
						pygame.display.flip()
						
						current_sentence-=1
						print(current_sentence)
						end_sentence = True
			if ev.type == pygame.QUIT:
				pygame.quit()
				exit()
	if (current_sentence == len(chat)-1):
		end_chat = True 

chat_recoded.close()
pygame.quit()







