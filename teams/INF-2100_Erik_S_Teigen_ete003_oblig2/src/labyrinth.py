# -*- coding: utf-8 -*-

# Labyrinth client.

from protocolBase import *
from message import *
from seek import *
import socket as s
import time, sys
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
    

# Test to show some code usage:
if __name__ == "__main__":
    
    # tile is either "tile", "toby" or "wall"
    # trap is either "trap" or "safe"
    # grue is either "grue or "safe"
    
    # Create a new labyrinth client
	lab = labyrinth()
	seek = FindingNemo()
    
    # To navigate the labyrinth use the directional operations:
    # These gives a list of info on return: [tile, trap, grue]
    # These will make you walk in a "circle" in the labyrinth.

	seek.findToby()
    #find.findToby()
    
    # The look command gives a list of info of your adjacent tiles.
    # The list contains lists as elements; [ [tile, trap, grue], ...]
    # To see examples here is a call to look.
    #for each in lab.look():
       #print each
    
    # If you find a trap in front of you, you can disarm it with:
    #print "disarm", lab.disarm("east")
    
    ## If you have a grue attached to you, or see one in your way of path
    ## you can light a match to be immune to gures for x minutes:
    #lab.fire()
    ## You also have the possibility to check the number of matches on you:
    #print lab.inventory()


    # Now go find toby!
	lab.cleanup()
