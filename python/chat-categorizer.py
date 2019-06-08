# coding: utf-8

"""chat-categorizer :  a tool to categorize chat interactions"""
__author__      = "Sunny Avry"
__version__     = "3.7.0"

import pygame,os,ctypes,time,random,sys,csv,random
from pygame import *
from pathlib import Path
from time import*

################### SCREEN SETUP ###################
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (6,28)
SM_CXSCREEN = 0
SM_CYSCREEN = 1
widthScreen = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
heightScreen = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)
print ("Screen resolution : %d x %d" % (widthScreen, heightScreen))

################### PYGAME INITIALISATION ###################
pygame.init()
pygame.mixer.quit()
pygame.font.init()

screen = pygame.display.set_mode((widthScreen-12,heightScreen-75))
pygame.display.set_caption('Chat categorizer 1.0')
icone = pygame.image.load("icon.ico")
pygame.display.set_icon(icone)

def fill_call(): fill()

################### VARIABLES ###################
categories               = [] #list of categories
list_buttons             = [] #list containing the list of buttons (category + rect())
chat                     = []  #list containing the conversation
length_recoded_sentences = [] #list containing the lengths of the different recoded sentences

heightButton = 50
widthButton = 200

################### DEFINITIONS ###################
def display_text(texte,positionx,positiony,police,taille,couleur):
    police=pygame.font.SysFont(police, taille, bold = True)
    texte=police.render(texte, 1, couleur)
    rectangle=texte.get_rect()
    rectangle.centerx = positionx
    rectangle.centery = positiony
    screen.blit(texte, rectangle)
    pygame.display.flip()


def rounded_button(surface,rect,color,radius=0.4):

    """
    display_rounded_button(surface,rect,color,radius=0.4)
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """
    original_rect = Rect(rect)
    rect          = Rect(rect)
    color         = Color(*color)
    alpha         = color.a
    color.a       = 0
    pos           = rect.topleft
    rect.topleft  = 0,0
    rectangle     = Surface(rect.size,SRCALPHA)

    circle        = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle        = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    surface.blit(rectangle,pos)
    return original_rect

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
	path_categories_file = Path("categories_file.txt")
	if path_categories_file.is_file():
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

def coordinates():
	global coord #coord is a global variable
	coord = []
	path_buttons_config_file = Path("buttons_config_file.cfg")
	if path_buttons_config_file.is_file():
		buttons_config_file = open("buttons_config_file.cfg", "r")
		config = buttons_config_file.readlines()
		config = eval(config[0])
		coord = config
		buttons_config_file.close()
	else:
		x = 30
		y = (heightScreen-200)/2
		coord.append((x,y))
		for i in range(0,len(categories)):
			y += 70
			if (y > heightScreen - 100):
				x += 220
				y = (heightScreen-200)/2
			coord.append((x,y))

def make_buttons():
	for i in range(0,len(categories)):
		button = rounded_button(screen,(coord[i][0], coord[i][1], widthButton, heightButton),(50,50,50),0.5)
		text = display_text(categories[i],coord[i][0]+widthButton/2,coord[i][1]+heightButton/2,"HELVETICA",20,(255,255,255))
		list_buttons.append([categories[i], button])

def remove_first_letter(sentence):
	sentence = sentence[1:]
	return sentence

################### MAIN ###################
categories = cat()
coordinates()
make_buttons()

display_text("Left click to move forward" ,widthScreen-102,10,"VERDANA",11,(255,255,255))
display_text("Right click to go back" ,widthScreen-87,30,"VERDANA",11,(255,255,255))
display_text("Hold middle click then release to move buttons" ,widthScreen-170,50,"VERDANA",11,(255,255,255))

chat_recoded = open("chat_recoded.txt", "w")

for line in open('chat.txt', encoding='utf-8-sig'):
	chat.append(line)

chat = [x.strip() for x in chat]

end_chat = False #notify the end of the chat reading 
current_sentence = 0 #number of the current chat sentence
while not end_chat:
	
	p = chat[current_sentence] #p is the current chat sentence
	
	#keep only the chat sentence. Remove date, category and name. 
	#loop uses the function removeletter which remove the first letter at every iteration of the loop
	#when 3 semicolons are found (only name and speech are remaining), the function stops
	semicolons = 0
	while semicolons < 2: 
		if p[0] == ";":
			semicolons+=1
		p=remove_first_letter(p)
					
	display_text(p.replace(";", " : ", 1),widthScreen/2,120,"VERDANA",18,(255,255,255))
	pygame.display.flip()

	end_sentence = False #notify the end of the sentence reading
	button_moving = False
	while not end_sentence:
		
		#guarantee that the current sentence is not below 0
		if(current_sentence < 0): current_sentence = 0 
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				chat_recoded.close()
				pygame.quit()
				exit()

			if ev.type == pygame.MOUSEBUTTONDOWN:			
					if ev.button == 1: #left mouse click
							for j in range(0,len(list_buttons)):
								if list_buttons[j][1].collidepoint(ev.pos):
									
									#create a black screen in the top third part
									pygame.draw.rect(screen,(0,0,0),(0,60,widthScreen,heightScreen/3-70))
									pygame.display.flip()

									#if the category chosen is Other, user has to refine the category themselves
									if list_buttons[j][0] == "Other":
										response = input("Specify Other: ")

									#Display current chat sentence"""
									display_text("Catégorie précédente : "+list_buttons[j][0],widthScreen/2,heightScreen/3-100,"VERDANA",16,(255,255,255))
									pygame.display.flip()

									q = chat[current_sentence]
									count = 0
									while q[count].isnumeric() or q[count] == "_":
										count += 1
									
									if list_buttons[j][0] == "Other":
										recoded_sentence = chat[current_sentence][0:count] + ";" + list_buttons[j][0] +": "+ response + ";" + p + "\n"
										chat_recoded.write(recoded_sentence)
									else:
										recoded_sentence = chat[current_sentence][0:count] + ";" + list_buttons[j][0] + ";" + p + "\n"
										chat_recoded.write(recoded_sentence)

									length_recoded_sentences.append(len(recoded_sentence)) #save the length of the current line
									print("["+str(current_sentence)+"] "+chat[current_sentence][0:count] + ";" + list_buttons[j][0] + ";" + p) #line number + date + category + name + sentence 
									current_sentence+=1
									end_sentence = True

					if ev.button == 2:
						for j in range(0,len(list_buttons)):
							if list_buttons[j][1].collidepoint(ev.pos):
								text_button = list_buttons[j][0]
								index_button = j
								button_moving = True

					if ev.button == 3: #right mouse click for coming back to previous sentences
						if current_sentence > 0:
							
							#create a black screen in the upper third part
							pygame.draw.rect(screen,(0,0,0),(0,60,widthScreen,heightScreen/3-70))
							pygame.display.flip()
							current_sentence-=1 #come back to the previous line
					
						    #remove the previous line in text file
							length_last_recoded_sentence = length_recoded_sentences[current_sentence]
							chat_recoded.seek(0, os.SEEK_END) #seek to end of file
							if chat_recoded.tell() - length_last_recoded_sentence >= 0: #check if the return seek position does not below 0
								chat_recoded.seek(chat_recoded.tell() - length_last_recoded_sentence , os.SEEK_SET) #go back to the beginning of the previous line
								chat_recoded.truncate()
							else:
								chat_recoded.seek(0) #if case, seek position is set to 0
								chat_recoded.truncate()
							end_sentence = True

			if ev.type == pygame.MOUSEBUTTONUP:
				if ev.button == 2:
						if button_moving:
							#create a black screen in the lower two thirds part
							pygame.draw.rect(screen,(0,0,0),(0,heightScreen/3,widthScreen,heightScreen-heightScreen/3))
							pygame.display.flip()
							coord[index_button] = ev.pos
							if ev.pos[0] >= widthScreen-widthButton:
								coord[index_button] = (widthScreen-widthButton-15,ev.pos[1])
							if ev.pos[1] <= heightScreen/3:
								coord[index_button] = (ev.pos[0],heightScreen/3)
							buttons_config_file = open("buttons_config_file.cfg", "w")
							buttons_config_file.write(str(coord))
							buttons_config_file.close()
							button_moving = False
							list_buttons = []
							make_buttons()

	#the program ends when all the chat sentences are read								
	if (current_sentence == len(chat)-1):
		end_chat = True 

chat_recoded.close()
pygame.quit()
sys.exit()








