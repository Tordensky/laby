# -*- coding: utf-8 -*-

# Searcher

from labyrinth import labyrinth
import time
import random

class FindingNemo:

	def __init__(self):
		self.path = [1,2,]
		self.clearpath = []
		self.x = 0
		self.y = 0
		self.lab = labyrinth()
		self.randomwalk = [self.goNorth(),self.goSouth(),self.goWest(),self.goEast()]
		
	def checkPath(self,pos):
		self.pos = pos
		if self.pos in self.path:
			return True
		elif self.pos not in self.path:
			return False
			
	def checkClearPath(self,pos):
		self.pos = pos
		if self.pos in self.clearpath:
			return True
		elif self.pos not in self.clearpath:
			return False
		
	def checkLastPos(self):
		if self.path[-2] == self.north:
			return 'north'
		if self.path[-2] == self.south:
			return 'south'
		if self.path[-2] == self.east:
			return 'east'
		if self.path[-2] == self.west:
			return 'west'
		else:
			return 'Error: No path?!?'
			
			
		
	def checkStuck(self):
		self.sum = 0
		if self.checkClearPath(self.south) == False:
			self.sum += 1
		if self.checkPath(self.south) == True:
			self.sum += 1
		if self.checkClearPath(self.east) == False:
			self.sum += 1
		if self.checkPath(self.east) == True:
			self.sum += 1
		if self.checkClearPath(self.north) == False:
			self.sum += 1
		if self.checkPath(self.north) == True:
			self.sum += 1
		if self.checkClearPath(self.west) == False:
			self.sum += 1
		if self.checkPath(self.west) == True:
			self.sum += 1
		if self.sum >= 4:
			return True
		
	def checkLoop(self):
		if self.path[-1] == self.path[-3]:
			return True
		else:
			return False
		
	def goStuck(self):
		
		if self.checkLoop() == True:
			while self.checkLoop() == True:
				if self.lastpos == 'north':
					self.goNorth()
				elif self.lastpos == 'south':
					self.goSouth()
				elif self.lastpos == 'west':
					self.goWest()
				elif self.lastpos == 'east':
					self.goEast()
		elif self.lastpos == 'north':
			self.goNorth()
		elif self.lastpos == 'south':
			self.goSouth()
		elif self.lastpos == 'west':
			self.goWest()
		elif self.lastpos == 'east':
			self.goEast()
		else:
			return None
		
			
	def lookAround(self):
		self.clear_x = self.x
		self.clear_y = self.y
		self.looklist = self.lab.look()
		if 'tile' in self.looklist[0] or 'toby' in self.looklist[0]:
			self.clear_y -= 1
			self.clearpath.append((self.clear_x,self.clear_y))
			self.clear_y = self.y
		if 'tile' in self.looklist[1] or 'toby' in self.looklist[1]:
			self.clear_y += 1
			self.clearpath.append((self.clear_x,self.clear_y))
			self.clear_y = self.y
		if 'tile' in self.looklist[2] or 'toby' in self.looklist[2]:
			self.clear_x -= 1
			self.clearpath.append((self.clear_x,self.clear_y))
			self.clear_x = self.x
		if 'tile' in self.looklist[3] or 'toby' in self.looklist[3]:
			self.clear_x += 1
			self.clearpath.append((self.clear_x,self.clear_y))
			self.clear_x = self.x
			
		
	def goNorth(self):
		self.y -= 1
		self.path.append((self.x,self.y))
		self.lab.north()
		return None
		
	def goSouth(self):
		self.y += 1
		self.path.append((self.x,self.y))
		self.lab.south()
		return None
		
	def goWest(self):
		self.x -= 1
		self.path.append((self.x,self.y))
		self.lab.west()
		return None
		
	def goEast(self):
		self.x += 1
		self.path.append((self.x,self.y))
		self.lab.east()
		return None
			
	def findToby(self):
		while True:
			time.sleep(0.4)
			self.lookAround()
			self.north = (self.x,(self.y -1))
			self.south = (self.x,(self.y +1))
			self.west = ((self.x -1),self.y)
			self.east = ((self.x +1),self.y)
			self.lastpos = self.checkLastPos()
			self.stuck = self.checkStuck()
			
		
			if self.checkStuck() == True:
				self.goStuck()
			elif self.checkClearPath(self.south) == True and self.checkPath(self.south) == False:
				self.goSouth()
			elif self.checkClearPath(self.east) == True and self.checkPath(self.east) == False:
				self.goEast()
			elif self.checkClearPath(self.north) == True and self.checkPath(self.north) == False:
				self.goNorth()
			elif self.checkClearPath(self.west) == True and self.checkPath(self.west) == False:
				self.goWest()


