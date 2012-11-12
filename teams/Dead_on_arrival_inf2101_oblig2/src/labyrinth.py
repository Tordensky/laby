# -*- coding: utf-8 -*-

# Labyrinth client.

from protocolBase import *
from message import *
import socket as s
import time, sys
import copy
import random
PORT = 32323

class labyrinth:
    
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
        
        self.pos = Coordinate(0,0)
        self.dictionary = {}
        
              
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
        
    def newTile(self, x, y):
        """Creates a new tile, sets the neighbour references accordingly and updates the neighbours"""
        tile = Tile(x,y)
        
        if tile.pos.north in self.dictionary:
            tile.north = self.dictionary[tile.pos.north]
            if isinstance(self.dictionary[tile.pos.north], Tile):
                self.dictionary[tile.pos.north].south = tile
        if tile.pos.south in self.dictionary:
            tile.south = self.dictionary[tile.pos.south]
            if isinstance(self.dictionary[tile.pos.south], Tile):
                self.dictionary[tile.pos.south].north = tile
        if tile.pos.east in self.dictionary:
            tile.east = self.dictionary[tile.pos.east]
            if isinstance(self.dictionary[tile.pos.east], Tile):
                self.dictionary[tile.pos.east].west = tile
        if tile.pos.west in self.dictionary:
            tile.west = self.dictionary[tile.pos.west]
            if isinstance(self.dictionary[tile.pos.west], Tile):
                self.dictionary[tile.pos.west].east = tile
        return tile
        
    
    def createTiles(self, lookliste, tempTile):
        """A tile is created for all the adjacent Tiles to the current position. A wall is stored in the list as a tuple of position and wall(string).
           The agent tile moves directly to Toby if he is located adjacent to the agent."""
        liste = []
        
        for item in lookliste:
            
            if item[0] == 'north':
                temp = Coordinate(tempTile.pos.x, tempTile.pos.y)
                temp.increase_y()
                if item[1] == 'tile':
                    tile = self.newTile(temp.x, temp.y)
                    tile.south = tempTile
                    liste.append(tile)
                elif item[1] == 'toby':
                    lab.north()
                else:
                    liste.append((temp.tupl(), 'wall'))
            if item[0] == 'east':
                temp = Coordinate(tempTile.pos.x, tempTile.pos.y)
                temp.increase_x()
                if item[1] == 'tile':
                    tile = self.newTile(temp.x, temp.y)
                    tile.west = tempTile
                    liste.append(tile)
                elif item[1] == 'toby':
                    lab.east()
                else:
                    liste.append((temp.tupl(), 'wall'))
                    
            if item[0] == 'south':
                temp = Coordinate(tempTile.pos.x, tempTile.pos.y)
                temp.decrease_y()
                if item[1] == 'tile':
                    tile = self.newTile(temp.x, temp.y)
                    tile.north = tempTile
                    liste.append(tile)
                elif item[1] == 'toby':
                    lab.south()
                else:
                    liste.append((temp.tupl(), 'wall'))
                    
            if item[0] == 'west':
                temp = Coordinate(tempTile.pos.x, tempTile.pos.y)
                temp.decrease_x()
                if item[1] == 'tile':
                    tile = self.newTile(temp.x, temp.y)
                    tile.east = tempTile
                    liste.append(tile)
                elif item[1] == 'toby':
                    lab.west()
                else:
                    liste.append((temp.tupl(), 'wall'))
                
        return liste



    def adddict(self, tilelist):
        """The new created tiles are added to the dictionary if they weren't in it before. The new information about the Tile is added to the Tile's
           representation in the dictionary, in the case that the tile was already present."""
        for item in tilelist:
            if isinstance(item, Tile):
                if item.pos.tupl() not in self.dictionary:
                    self.dictionary[item.pos.tupl()] = item
                else:
                    if item.north != None:
                        temp = item.north
                        item = self.dictionary[item.pos.tupl()]
                        item.north = temp
                        self.dictionary[item.pos.tupl()] = item
                    elif item.south != None:
                        temp = item.south
                        item = self.dictionary[item.pos.tupl()]
                        item.south = temp
                        self.dictionary[item.pos.tupl()] = item
                    elif item.west != None:
                        temp = item.west
                        item = self.dictionary[item.pos.tupl()]
                        item.west = temp   
                        self.dictionary[item.pos.tupl()] = item 
                    elif item.east != None:
                        temp = item.east
                        item = self.dictionary[item.pos.tupl()]
                        item.east = temp  
                        self.dictionary[item.pos.tupl()] = item     
            else:
                if item[0] not in self.dictionary:
                    self.dictionary[item[0]] = item[1]
        return tilelist
                
                
    def updateCurrent(self, tilelist, tempTile):
        """ The current Tile is updated according to the information gathered during the look process"""
        
        tempTile.north = tilelist[0]
        tempTile.south = tilelist[1]
        tempTile.west = tilelist[2]
        tempTile.east = tilelist[3]
        lab.dictionary[lab.pos.tupl()] = tempTile
        
        
    def move(self, tempTile):
        """ The neighbours are checked for unexplored adjacent Tiles and if none are found the iterative process of the Dijkstra's algorithm is initialized"""
        current_count = 0
        neighbours = tempTile.liste()
        
        for tile in neighbours:
            try:
                if tile[1].count() > current_count:
                    current_count = tile[1].count()
                    current_tile = tile
            except:
                pass

        if current_count != 0:
            if current_tile[0] == 'north':
                self.pos = Coordinate(self.pos.x, self.pos.y+1)
                lab.north()
            elif current_tile[0] == 'south':
                self.pos = Coordinate(self.pos.x, self.pos.y-1)
                lab.south()
            elif current_tile[0] == 'west':
                self.pos = Coordinate(self.pos.x-1, self.pos.y)
                lab.west()
            elif current_tile[0] == 'east':
                self.pos = Coordinate(self.pos.x+1, self.pos.y)
                lab.east()
                
                
        else:
            self.init_jump_path(tempTile)           
        
    
    def init_jump_path(self, tempTile):
        """ Start Dijkstra's algorithm by initializing the edge values and calling the iterative forward_propagation method to find the next target.
            The backward_propagation method is then used to gather the list of moves that have to be made and executes them"""
        for key in self.dictionary:
            if isinstance(self.dictionary[key], Tile):
                self.dictionary[key].distance = float("inf")
                self.dictionary[key].direction = None

        tempTile.distance = 0
        liste = tempTile.liste()

        
        new_list = []
        for item in liste:
            item[1].distance = 1
            item[1].direction = item[0]
            new_list.extend(item[1].liste()) 
        
        nearest_tile = self.forward_propagation(new_list, 1)
        path_liste = self.backward_propagation(nearest_tile)
            
            
    def forward_propagation(self, liste, layer):
        """ Iteratively goes through the different levels and searches for nodes with unexplored neighbours"""
        current_layer = layer+1
        new_list = []
        current_count = 0
        current_tile = None
        
        for tile in liste:
            try:
                if tile[1].count() > current_count:
                    current_count = tile[1].count()
                    current_tile = tile
                    tile[1].distance = current_layer
                    tile[1].direction = tile[0]
            except:
                pass    
  
        if current_count != 0:
            return current_tile
        
        
        for item in liste:
            if(item[1].distance > current_layer):
                item[1].distance = current_layer
                item[1].direction = item[0]
                new_list.extend(item[1].liste())
                
        assert len(new_list)
            
        return self.forward_propagation(new_list, current_layer)
            
        
        
    def backward_propagation(self, nearest_tile):
        """Starts at the target tile and follows the path of shortest distance to the root node gathering the methods needed to reach the target. The methods
           are then executed, so that the agent will be at the target node."""
        move_list = []
        pos = Coordinate(nearest_tile[1].pos.x, nearest_tile[1].pos.y)
        distance = nearest_tile[1].distance
        direction = nearest_tile[1].direction
        
        while distance > 0:
            move_list.append(direction)
            
            if direction == 'north':
                pos.decrease_y()
            elif direction == 'south':
                pos.increase_y()
            elif direction == 'west':
                pos.increase_x()
            elif direction == 'east':
                pos.decrease_x()
            temp_tile = self.dictionary[pos.tupl()]
            distance = temp_tile.distance
            direction = temp_tile.direction
        move_list.reverse()
        
        for step in move_list:
            if step == 'north':
                self.pos = Coordinate(self.pos.x, self.pos.y+1)
                lab.north()
            elif step == 'south':
                self.pos = Coordinate(self.pos.x, self.pos.y-1)
                lab.south()
            elif step == 'west':
                self.pos = Coordinate(self.pos.x-1, self.pos.y)
                lab.west()
            elif step == 'east':
                self.pos = Coordinate(self.pos.x+1, self.pos.y)
                lab.east()
    
    
class Coordinate(object):
    """ A representation of coordinate pairs and the methods to act on them """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def increase_x(self):
        self.x += 1 
        
    def decrease_x(self):
        self.x -= 1
        
    def increase_y(self):
        self.y += 1
        
    def decrease_y(self):
        self.y -= 1
    
    def tupl(self):
        return (self.x, self.y)
        
    def getnorth(self):
        x = self.x
        y = self.y
        return (x,y+1)
        
    def getsouth(self):
        x = self.x
        y = self.y
        return (x,y-1)
        
    def geteast(self):
        x = self.x
        y = self.y
        return (x+1,y)
        
    def getwest(self):
        x = self.x
        y = self.y
        return (x-1,y)
        
    def __repr__(self):
        return repr(self.tupl())

    north = property(getnorth)
    south = property(getsouth)
    east = property(geteast)
    west = property(getwest)
        
class Tile(object):
    """ A representation of tiles, among the attributes of the tile is the position and references to adjacent neighbours"""
    
    def __init__(self, x, y):
        self.north = None
       	self.east = None
       	self.south = None
       	self.west = None
       	self.pos = Coordinate(x,y)
       	self.distance = 0
       	self.direction = None

    def liste(self):
        """ Returns a randomly sorted list of the adjacent neighbours that are not walls"""
        result = []
        
        try:
            if isinstance(lab.dictionary[self.pos.north], Tile):
                result.append(('north', lab.dictionary[self.pos.north]))
        except:
            pass
        try:    
            if isinstance(lab.dictionary[self.pos.east], Tile):
                result.append(('east', lab.dictionary[self.pos.east]))
        except:
            pass
        try:
            if isinstance(lab.dictionary[self.pos.south], Tile):
                result.append(('south', lab.dictionary[self.pos.south]))
        except:
            pass
        try:
            if isinstance(lab.dictionary[self.pos.west], Tile):
                result.append(('west', lab.dictionary[self.pos.west]))    
        except:
            pass   
              
        random.shuffle(result)
        
        return result  
        
    def count(self):
        """ Returns the number of unexplored neighbours"""
        counter = 0
        if self.north == None:
            counter +=1
        if self.south == None:
            counter +=1
        if self.east == None:
            counter +=1
        if self.west == None:
            counter +=1
        return counter  
        
    def __repr__(self):
        return 'Tile(pos=%s, dist=%s, dir=%s' % (repr(self.pos), self.distance, self.direction)  

# Test to show some code usage:
if __name__ == "__main__":
    
    # tile is either "tile", "toby" or "wall"
    # trap is either "trap" or "safe"
    # grue is either "grue or "safe"
    
    # Create a new labyrinth client
    lab = labyrinth()
    # Init start position
    lab.dictionary[lab.pos.tupl()] = Tile(0,0)
    
    #Execute the search, exploration, information storing and moving processes.
    while True:
        temp_tile = lab.dictionary[lab.pos.tupl()]
        look_liste = lab.look()
        tiles_list = lab.createTiles(look_liste, temp_tile)
        tiles_list = lab.adddict(tiles_list)
        lab.updateCurrent(tiles_list, temp_tile)
        lab.move(temp_tile)
    

    # To navigate the labyrinth use the directional operations:
    # These gives a list of info on return: [tile, trap, grue]
    # These will make you walk in a "circle" in the labyrinth.
 #   print lab.look()
#    lab.east()
  #  print lab.south()
  #  print lab.look()

	


    
    # The look command gives a list of info of your adjacent tiles.
    # The list contains lists as elements; [ [tile, trap, grue], ...]
    # To see examples here is a call to look.
    #for each in lab.look():
    #    print each
    
    # If you find a trap in front of you, you can disarm it with:
    #print "disarm", lab.disarm("east")
    
    # If you have a grue attached to you, or see one in your way of path
    # you can light a match to be immune to gures for x minutes:
    #lab.fire()
    # You also have the possibility to check the number of matches on you:
    #00print lab.inventory()


    # Now go find toby!
    lab.cleanup()
