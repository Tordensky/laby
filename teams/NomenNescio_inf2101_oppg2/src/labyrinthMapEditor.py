# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *
from common import *
class editor:

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480), HWSURFACE)
		pygame.display.set_caption('Labyrinth')
		self.screen.fill((150,150,150))

	def main(self, filename):
		self.setup_map(30, 30)

		self.stage = 0


		self.draw_menu()

		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						return

				elif event.type == MOUSEBUTTONDOWN:
					mx = event.pos[0]
					my = event.pos[1]

					if self.maprect.collidepoint(mx,my):
						self.put_tile(mx/TILESZ, my/TILESZ)
					elif self.menurect.collidepoint(mx,my):
						self.stage += 1
			self.draw_map()
			pygame.display.flip()

			if self.stage == 6:
				break

		self.store_map(filename)

	def put_tile(self, x, y):
		self.mapdata[y*self.mapw + x] = self.stage
		if self.stage == 2:
			self.stage += 1
		elif self.stage == 3:
			self.stage += 1

	def draw_menu(self):

		text = "NEXT"

		fnt = pygame.font.Font(pygame.font.get_default_font(),11)

		self.menurect = Rect(550,5,85,32)

		rect = Rect(550,5,85,32)

		ts=fnt.render(text, 1, (255,255,255))
		trect = ts.get_rect()
		trect.center = rect.center
		self.screen.blit(ts,trect.topleft)

	def draw_map(self):
		x = 0
		y = 0
		rect = [0,0,TILESZ,TILESZ]
		for p in self.mapdata:
			if p == -1:
				p = 0
			rect[0] = x*TILESZ
			rect[1] = y*TILESZ
			self.screen.fill(colors[p],rect)
			x+=1
			if x>=self.mapw:
				x=0
				y+=1

	def setup_map(self, w, h):
		self.mapdata = []
		self.mapw = w
		self.maph = h

		size = w*h
		for i in range(size):
			self.mapdata.append(1)

		self.maprect = Rect(0,0,w*TILESZ,h*TILESZ)

	def store_map(self, filename):
		f = open("maps/"+filename+".map", 'w')

		dimentions = str(self.mapw)+" "+str(self.maph)
		buf = ""
		for tile in self.mapdata:
			buf += str(tile)
		f.write(dimentions+"\n")
		f.write(buf)
		f.close()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: python labyrinthMapGenerator mapname"
		sys.exit()
	medit = editor()
	medit.main(sys.argv[1])
