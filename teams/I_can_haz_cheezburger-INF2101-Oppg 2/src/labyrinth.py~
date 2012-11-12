# -*- coding: utf-8 -*-

# Labyrinth client.

from protocolBase import *
from message import *
import socket as s
import time, sys
PORT = 32323

class Labyrinth:
    
    def __init__(self):
        conn = s.socket(s.AF_INET, s.SOCK_STREAM)
        conn.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        conn.connect(('localhost', PORT))
        
        fsock = conn.makefile()
        port = int(fsock.readline())
        # Set up protocol for message passing
        self.pb = protocolBase()
        # Beauty sleep
        time.sleep(0.1)
        self.pb.connect('localhost', port)
        
    # Interface for navigating the labyrinth
    def north(self):
        """ Sending request to server to go north. """
        self.send("north")
        msg = self.recv()
        
        return [msg.get(0), msg.get(1), msg.get(2)]
        
    def south(self):
        """ Sending request to server to go south. """
        self.send("south")
        msg = self.recv()
            
        return [msg.get(0), msg.get(1), msg.get(2)]
    
    def east(self):
        """ Sending request to server to go east. """
        self.send("east")
        msg = self.recv()
            
        return [msg.get(0), msg.get(1), msg.get(2)]
    
    def west(self):
        """ Sending request to server to go west. """
        self.send("west")
        msg = self.recv()
            
        return [msg.get(0), msg.get(1), msg.get(2)]
    
    def look(self):
        """ Sending request to server to look around.
            Recieves status of adjacent tiles from server. """
        self.send("look")
        msg = self.recv() 
        
        msg_tokens = []
        tiles = []
        
        for i in range(msg.size()):
            msg_tokens.append(msg.get(i))
        for tok in msg_tokens:
            tiles.append(tok.split("|"))
        
        return tiles
    
    def disarm(self, direction):
        """ Sending request to disarm an adjacent trap. """
        self.send("disarm " + direction)
        msg = self.recv() 

        return msg.get(0)
    
    def fire(self):
        self.send("fire")
        msg = self.recv() 

        return msg.get(0)
    
    def inventory(self):
        self.send("inventory")
        msg = self.recv() 

        return int(msg.get(0))
    
    # Methods for communicating with the server
    # Nevermind these.
        
    def send(self, op):
        """ Sends the given operation to the server. """
        tokens = op.split()
        msg = message()
        for token in tokens:    
            msg.add(token)
        self.pb.send(msg)
        
    def recv(self):
        """ Recieves a response from the server. """
        msg = self.pb.recv()
        
        if msg.get(0) == "timeout":
            print "You failed to find Toby before the time ran out!"
            self.cleanup()
        elif msg.get(0) == "toby":
            print "ERMAHGERD!! You found Toby. Good job!"
            self.cleanup()
        elif msg.get(0) == "dead":
            print "You died!"
            self.cleanup()
        
        return msg
    
    # Cleanup
    def cleanup(self):
        """ Close connections and notify server that session is over. """
        self.pb.cleanup()
        sys.exit()


class Vertex(object):
	def __init__(self):
		self.x = 0
		self.y = 0
	def getPos(self):
		return (self.x, self.y)
	def setPos(self, x, y):
		self.x = x
		self.y = y


class Solver(object):
	'''
	Class for solving the labyrinth, keeping track of movement,
	and backtracking the moved path so far
	'''
	def __init__(self):
		
		self.visitedVertex = []
		self.lab = Labyrinth()
		self.stack = []
		self.foundToby = False

	def movement(self):
		'''	
		Method for moving the player around in the labyrinth,
		adding the visited tiles to a graph	
		'''	
		self.v = Vertex()
		self.v.setPos(0,0)
		self._moveSarah()
		
	def _NowhereToGo(self, tiles):
		'''
		Method to dertemine whether we have reach a corner with nowhere to go
		'''
		self.pos = self.v.getPos()
    
		if tiles[1][1] == 'tile':
			if (self.v.x, self.v.y +1) not in self.visitedVertex:
				return ['south', False]
		if tiles[0][1] == 'tile':
			if (self.v.x, self.v.y -1) not in self.visitedVertex:
				return ['north', False]
		if tiles[2][1] == 'tile':
			if (self.v.x -1, self.v.y) not in self.visitedVertex:
				return ['west', False]
		if tiles[3][1] == 'tile':
			if (self.v.x +1, self.v.y) not in self.visitedVertex:
				return ['east', False]
		return [None, True]
	
	def _backTrack(self):
		'''
		Method for backtracking to last pos with another direction
		to walk in
		'''
		self.lastPos = self.stack.pop()
		self.v.setPos(self.lastPos[0][0], self.lastPos[0][1])
		
		if self.lastPos[1] == 'south':
			self.lab.south()
		elif self.lastPos[1] == 'north': 
			self.lab.north()
		elif self.lastPos[1] == 'east':
			self.lab.east()
		elif self.lastPos[1] == 'west':
			self.lab.west()
			
	def _Toby(self, tiles):
		'''
		Check if toby is near, and move to his tile
		'''
		if tiles[0][1] == 'toby':
			self.lab.north()
			return True
		elif tiles[1][1] == 'toby':
			self.lab.south()
			return True
		elif tiles[2][1] == 'toby':
			self.lab.west()
			return True
		elif tiles[3][1] == 'toby':
			self.lab.east()
			return True
		return False
	
		
	def _moveSarah(self):
		'''
		Moves sarah based on the order of the if tests.
		Calls all helping functions earlier in the code to dertermine
		new paths to walk if stuck.
		Also builds a path stack to use in backtracking sarahs movement
		'''
		while self.foundToby == False:
			self.tiles = self.lab.look()
			self.cornered = self._NowhereToGo(self.tiles)
			self.foundToby = self._Toby(self.tiles)
			
			if self.foundToby:
				break
			
			if self.cornered[1] == True:
				self.visitedVertex.append(self.v.getPos())
				self._backTrack()
				continue
				
			if self.cornered[0] == 'south':
				self.visitedVertex.append(self.v.getPos())
				self.stack.append([self.v.getPos(), 'north'])
				self.v.setPos(self.v.x, self.v.y +1)
				self.lab.south()
				continue
				
			if self.cornered[0] == 'north':
				self.visitedVertex.append(self.v.getPos())
				self.stack.append([self.v.getPos(), 'south'])
				self.v.setPos(self.v.x, self.v.y -1)
				self.lab.north()
				continue
			
			if self.cornered[0] == 'east':
				self.visitedVertex.append(self.v.getPos())
				self.stack.append([self.v.getPos(), 'west'])
				self.v.setPos(self.v.x +1, self.v.y)
				self.lab.east()	
				continue
			
			if self.cornered[0] == 'west':
				self.visitedVertex.append(self.v.getPos())
				self.stack.append([self.v.getPos(), 'east'])
				self.v.setPos(self.v.x -1, self.v.y)
				self.lab.west()
				continue

if __name__ == "__main__":
	lab = Solver()
	lab.movement()
	
	
	
