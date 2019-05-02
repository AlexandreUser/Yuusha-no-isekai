import pygame
import time
from levels_scripts.level_1 import phases
from game_scripts.Better_logic import render_font,HUD,event_holder
from game_scripts.house import background
from game_scripts.tiles import path
from game_scripts.character import character
from game_scripts.prop import prop
from game_scripts.furniture import furniture
from game_scripts.camera import camera
from game_scripts.npc import npc

class options:
	def __init__(self,width,height):
		self.width = width
		self.height = height
	def resolution_lowScaled(self):
		return (int(self.width/1.5),int(self.height/1.5))
	def resolution_medScaled(self):
		return (self.width,self.height)
	def mid_place(self,hero):
		return (-(self.width/2-hero.width),-(self.height/2-hero.height))
	def menu_placement(self):
		return (self.width/3,self.height-130)
pygame.init()
screenwidth = 1280
screenheight = 680
gaming = options(screenwidth,screenheight)

hero = character("Naofumi",pygame)
hero.x = 500
hero.y = 500
camera = camera(hero.x,hero.y)
win = pygame.display.set_mode((gaming.resolution_medScaled()))
pygame.display.set_caption("Yuusha no isekai")
run = True
level = phases(1)
level.init(pygame)
newhud = HUD(-100,screenheight-200,"./scenarios/huds/0.png",pygame)
not_trigger = False

def level_1(keys,level,hero,pygame,win,camera,cutScene,cutScene_inside,not_trigger,run):
	if level.is_inside == False:
		if cutScene_inside < 200:
			cutScene = 200
			cutScene_inside += 10
			win.fill((cutScene_inside,cutScene_inside,cutScene_inside))
		else:
			level.display(camera,pygame,win,hero,keys,cutScene_inside)	
			hero.draw(keys,win,pygame,camera)
			level.display_sobreposto(camera,pygame,win,hero,keys)

			hero.collision(level.houses,pygame,camera)
			level.npcs[0].dialogue(hero,win,pygame,camera,keys,gaming.menu_placement())
			#level.npcs[1].dialogue(hero,win,pygame,camera,keys,gaming.menu_placement())
			camera.update(gaming.mid_place(hero)[0]+hero.x,gaming.mid_place(hero)[1]+hero.y)	
	else:
		cutScene_inside = 0 
	return cutScene, cutScene_inside,level.is_inside
cutScene = 200
cutScene_inside = 0
while run:
	win.fill((103, 140, 51))
	keys = pygame.key.get_pressed()
	cutScene,cutScene_inside,level.is_inside = level_1(keys,level,hero,pygame,win,camera,cutScene,cutScene_inside,not_trigger,run)
	if level.is_inside != False:
		if cutScene > 10:
			win.fill((cutScene, cutScene, cutScene))
			cutScene-=10
		else:
			level,run = event_holder("loja_de_armas",keys,win,pygame,hero,run,camera,level)
	else:
		level.is_inside = False
	newhud.render(win,pygame,hero)
	pygame.time.delay(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
