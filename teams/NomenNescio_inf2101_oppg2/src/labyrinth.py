# -*- coding: utf-8 -*-

# Labyrinth client.

from protocolBase import *
from message import *
import math
import socket as s
import time, sys
import random
PORT = 32323

NORTH	=	0
SOUTH	=	1
WEST	=	2
EAST	=	3

NORTHBOUND	= 1
SOUTHBOUND	= -1
WESTBOUND	= -1
EASTBOUND	= 1

class labyrinth:

	def __init__(self, host='localhost'):
		conn = s.socket(s.AF_INET, s.SOCK_STREAM)
		conn.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
		conn.connect((host, PORT))

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
			print "You found Toby. Good job!"
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

class AiPlayer(object):
	def __init__(self, labyrinth):
		self.tiles = {}

		self.labyrinth = labyrinth
		self.pos = (0,0)
		self.tiles[self.pos] = self.parse_look(self.labyrinth.look())

	def play(self):
		while True:
			adjacenct_unexplored_tiles = []
			for (pos, weight) in zip(self.adjacent_nodes(self.pos), self.tiles[self.pos]):
				if weight < 0: # toby
					self.move(pos)
				elif pos in self.tiles and self.tiles[pos] is None:
					adjacenct_unexplored_tiles.append(pos)

			nadjacenct_unexplored_tiles = len(adjacenct_unexplored_tiles)
			if nadjacenct_unexplored_tiles > 0:
				#self.move(adjacenct_unexplored_tiles[random.randint(0, nadjacenct_unexplored_tiles-1)])
				self.move(adjacenct_unexplored_tiles[0])
			else:
				self.go_to_closest_unexplored_tile()

			self.tiles[self.pos] = self.parse_look(self.labyrinth.look())

	def new_pos(self, direction, pos):
		if (direction == NORTH):
			return (pos[0]+1, pos[1])
		elif(direction == SOUTH):
			return (pos[0]-1, pos[1])
		elif(direction == EAST):
			return (pos[0], pos[1]+1)
		elif(direction == WEST):
			return (pos[0], pos[1]-1)
		else:
			raise ValueError

	def adjacent_nodes(self, pos):
		return [self.new_pos(i, pos) for i in range(0,4)]


	def go_to_closest_unexplored_tile(self):
		dist, previous = self.dijkstras_algorithm(self.pos)

		closest_unexplored_tile = None
		closest_unexplored_tile_d = sys.maxint
		for pos, d in dist.iteritems():
			if pos in self.tiles and self.tiles[pos] is None:
				if closest_unexplored_tile is None or d < closest_unexplored_tile_d:
					closest_unexplored_tile = pos
					closest_unexplored_tile_d = d

		path = []
		n = closest_unexplored_tile
		while True:
			path.insert(0,n)
			if n == self.pos:
				break
			n = previous[n]

		for step in path:
			self.move(step)

	def distance_between(self, a, b):
		return 1

	def dijkstras_algorithm(self, source): # based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
		dist = {}
		previous = {}
		for n in self.tiles:
			dist[n] = sys.maxint
			previous[n] = None

		dist[source] = 0
		Q = set(self.tiles)
		while len(Q) > 0:
			u = min(Q, key=dist.get)
			Q.remove(u)

			if dist[u] == sys.maxint:
				break

			for n in self.adjacent_nodes(u):
				if n not in Q:
					continue

				alt = dist[u]+self.distance_between(u, n)
				if alt < dist[n]:
					dist[n] = alt
					previous[n] = u
		return dist, previous

	def move(self, pos):
		relative_pos = (pos[0]-self.pos[0], pos[1]-self.pos[1])
		if relative_pos == (1, 0):
			self.labyrinth.north()
		elif relative_pos == (-1, 0):
			self.labyrinth.south()
		elif relative_pos == (0, 1):
			self.labyrinth.east()
		elif relative_pos == (0, -1):
			self.labyrinth.west()
		elif relative_pos == (0, 0):
			pass
		else:
			raise ValueError("new position is out of range")
		self.pos = pos

	def weight(self, string):
		if string == "wall":
			return sys.maxint
		elif string == "tile":
			return 1
		elif string == "toby":
			return -sys.maxint
		else:
			raise ValueError("\"%s\" is not parseable\n" %(string))

	def parse_look(self, look):
		weights = [self.weight(look[i][1]) for i in range(0,4)]

		for i in range(0, 4):
			if weights[i] <= 1:
				self.add_empty_if_not_in_tiles(self.new_pos(i, self.pos))

		return weights

	def add_empty_if_not_in_tiles(self, pos):
		if pos not in self.tiles:
			self.tiles[pos] = None

# Test to show some code usage:
if __name__ == "__main__":

	host = 'localhost'
	if len(sys.argv) == 2:
		host = sys.argv[1]
	ai = AiPlayer(labyrinth(host))
	ai.play()
