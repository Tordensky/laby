# -*- coding: utf-8 -*-

# Labyrinth server

# Imported modules
import socket, thread, sys, time, random
from protocolBase import *
from message import *
from grue import *

import pygame
from pygame.locals import *
from common import *

class serverListener:
    """ Labyrinth listener server """
    
    def __init__(self):
        pass
        #Socket for game clients
        self.myhost = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind(('', PORT))
        s.listen(5)
   
        self.sock = s
        
    def main(self, filename, gamemode):    
        print "Labyrinth server up and running..."
        while 1:
            (conn, addr) = self.sock.accept()
            
            print "Client connected.", addr
            worker = serverWorker(conn)
        #worker.main(filename, gamemode)
            thread.start_new_thread(worker.main, (filename,gamemode))


class serverWorker:
    """ Labyrinth worker """

    
    def __init__(self, conn):
        """ Initialize the game server by setting up 
            message passing protocol. """
        
        # Get a free port hax
        hax = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hax.bind(('', 0))
        port = hax.getsockname()[1]
        hax.close()
        
        # Set up protocol for message passing
        self.pb = protocolBase()
        
        # Send the port number to the connected client
        fsock = conn.makefile()
        fsock.write(str(port)+"\n")
        fsock.flush()
        # Wait for connection on the new port
        self.pb.wait_for_connect(port)
        
        # Close sockets no longer in use
        fsock.close()
        conn.close()
               
    
    def main(self, filename, gamemode):
        """ Main program """
        
        # Set up pygame
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), HWSURFACE)
        pygame.display.set_caption('Labyrinth')
        self.screen.fill((150,150,150))

        
        # Load map
        self.load_map(filename, gamemode)
        self.setup_grues()
        self.draw_map()
        pygame.display.flip()
        
        # Player variables:
        self.timeleft = 13*60*2
        self._fire = 0
        self.numfire = 11
        self.grue = False
        self.hitpoints = 5
        self.win = False
        
        while 1:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:          
                    if event.key == K_ESCAPE:
                        return
            
            msg = self.recv()
            op = msg.get(0)

            if self.hitpoints == 0:
                op = message()
                op.add("dead")
                self.send(op)
                break
            if self.timeleft <= 0:
                op = message()
                op.add("timeout")
                self.send(op)
                break
            
            
            if op == "north":
                self.north()
            elif op == "south":
                self.south()
            elif op == "east":
                self.east()
            elif op == "west":
                self.west()
            elif op == "look":
                self.look()
            elif op == "disarm":
                self.disarm(msg.get(1))
            elif op == "fire":
                self.fire()
            elif op == "inventory":
                self.inventory()
            elif op == "quit":
                break
            
            if self._fire < 0:
                self._fire = 0
            
            self.update_map()
            self.draw_map()
            #time.sleep(0.05)
            pygame.display.flip()
            
            if self.win:
                time.sleep(1)
                break
            
        self.cleanup()
    
    def north(self):
        """ Recieved a request to move north. 
            Returns result: ok, victory, or bump. """
        if self.valid_pos(self.new[0], self.new[1]-1):
            self.new[1] -= 1
        self.send_movement()
        self.timeleft -=3
        if self._fire > 0:
                self._fire -=3
        
    def south(self):
        """ Recieved a request to move south.
            Returns result: ok, victory, or bump. """
        
        if self.valid_pos(self.new[0], self.new[1]+1):
            self.new[1] += 1
        self.send_movement()
        self.timeleft -=3
        if self._fire > 0:
                self._fire -=3
        
    def east(self):
        """ Recieved a request to move east.
            Returns result: ok, victory, or bump. """
        if self.valid_pos(self.new[0]+1, self.new[1]):
            self.new[0] += 1
        self.send_movement()
        self.timeleft -=3
        if self._fire > 0:
                self._fire -=3
        
    def west(self):
        """ Recieved a request to move west. 
            Returns result: ok, victory, or bump. """
        self.timeleft -=3
        if self._fire > 0:
                self._fire -=3
        
        if self.valid_pos(self.new[0]-1, self.new[1]):
            self.new[0] -= 1
        self.send_movement()

    def look(self):
        """ Recieve a request to look around.
            Sends adjacent tiles to client.""" 
        self.timeleft -= 1
        if self._fire > 0:
                self._fire -=1
        
        msg = message()
        tiles = self.get_adjecent_tiles()        
        for each in tiles:
            msg.add(each[0]+"|"+each[1]+"|"+each[2]+"|"+each[3])
        self.send(msg)
        
    def disarm(self, direction):
        """ Disarm tile next to current position in given direction """
        self.timeleft -= 2
        if self._fire > 0:
                self._fire -=2
        
        pos = [self.old[0], self.old[1]]
        if direction == "north": pos[1] -= 1
        if direction == "south": pos[1] += 1
        if direction == "west": pos[0] -= 1
        if direction == "east": pos[0] += 1
        
        if self.is_trap(pos[0], pos[1]):
            self.mapdata[pos[1]*self.mapw + pos[0]] = 1
       
        msg = message()
        msg.add("ok")
        self.send(msg)
       
    def fire(self):
        """ Light a match, and be immune to grues for 9 minutes.
            Also killes any grue on you """
        self.timeleft -= 1
        msg = message()
        
        if self.numfire > 0:
            self._fire = 9
            self.numfire -= 1
            self.grue = False
            msg.add("ok")
        else:
            msg.add("out")
        self.send(msg)
        
    def inventory(self):
        """ Sends number of matches west to client. """
        msg = message()
        msg.add(str(self.numfire))
        self.send(msg)
    
    def send_movement(self):
        """ Updates the movement of the player and the grues.
            The result is sent to the client.   """
        
        self.update_grues()
        msg = message()
        
        tile = "tile"
        trap = "safe"
        grue = "safe"
        
        if self.grue:
            self.hitpoints -=1
        
        if (self.new[0],self.new[1]) == (self.old[0],self.old[1]): # hit wall
            tile = "wall"
        elif ((self.new[0],self.new[1]) == (self.end[0],self.end[1])): # found toby
            tile = "toby"
            self.win = True
        
        if self.is_trap(self.new[0], self.new[1]):
            trap = "trap"
            self.hitpoints -= 1
        if self.is_grue(self.new[0], self.new[1]):
            grue = "grue"
            self.grue = True
            for g in self.grues:
                if (g.x,g.y) == (self.new[0], self.new[1]):
                    self.grues.remove(g)
                    break
            if self._fire > 0:
                self.grue = False
            
        msg.add(tile)
        msg.add(trap)
        msg.add(grue)
        self.send(msg)
    
    def get_adjecent_tiles(self):
        """ Returns all valid adjecent tiles to current pos (old) """
        tiles = []
        
        # north:
        if self.valid_pos(self.old[0], self.old[1]-1):
            tiles.append(self.get_tile("north", self.old[0], self.old[1]-1))
        else:
            tiles.append(["north", "wall", "safe", "safe"])
        # south:
        if self.valid_pos(self.old[0], self.old[1]+1):
            tiles.append(self.get_tile("south", self.old[0], self.old[1]+1))  
        else:
            tiles.append(["south", "wall", "safe", "safe"]) 
        # west:
        if self.valid_pos(self.old[0]-1, self.old[1]):
            tiles.append(self.get_tile("west", self.old[0]-1, self.old[1]))
        else:
            tiles.append(["west", "wall", "safe", "safe"])
        # east:
        if self.valid_pos(self.old[0]+1, self.old[1]):
            tiles.append(self.get_tile("east", self.old[0]+1, self.old[1]))
        else:
            tiles.append(["east", "wall", "safe", "safe"])
 
        return tiles
    
    def get_tile(self, pos, x, y):    
        trap = "safe"
        grue = "safe"
        tile = "tile"            
            
        if self.is_grue(x, y):
            grue = "grue"
        if self.is_trap(x, y):
            trap = "trap"
        if ((x, y) == (self.end[0],self.end[1])):
            tile = "toby"
       
        return [pos, tile, trap, grue]
    
    def is_trap(self, x, y):
        if self.mapdata[y*self.mapw+x] == 4:
            return True
        return False
    
    def is_grue(self, x, y):
        if self.mapdata[y*self.mapw+x] == 5:
            return True
        return False
    
    def is_toby(self, x, y):
        if self.mapdata[y*self.mapw+x] == 3:
            return True
        return False
    
    def valid_pos(self, x, y):
        """ Check if a tile at position x,y is a valid tile.
            (Traps and grues are also valid) """
        if x < 0 or x >= self.mapw:
            return 0
        if y < 0 or y >= self.maph:
            return 0
        if self.mapdata[y*self.mapw + x] == 0:
            return 0
        return 1
    
    def setup_grues(self):
        """ Parse the mapdata to determine and set up all grues on the map. """
        self.grues = []
        row = 0
        col = 0
        idx = 0
        for tile in self.mapdata:
            if tile == 5:
                self.grues.append(grue(col, row, idx))
                idx +=1
            col += 1
            if col == self.mapw:
                col = 0
                row +=1
    
    def update_grues(self):
        """ Make all grues walk randomly one step from their current position. """
        directions = [(0,1), (0,-1), (-1,0), (1,0)]
        
        for grue in self.grues:
            dire = directions[random.randint(0,3)]
            new_x = grue.x+dire[0]
            new_y = grue.y+dire[1]
            if self.valid_pos(new_x, new_y):
                if self.is_toby(new_x, new_y) or self.is_trap(new_x, new_y) or self.is_grue(new_x, new_y):
                    continue
                else:
                    self.mapdata[grue.y*self.mapw + grue.x] = 1
                    self.mapdata[new_y*self.mapw + new_x] = 5
                    grue.set_pos(new_x, new_y)
                        
                        
    def load_map(self, filename, gamemode):
        
        f = open("maps/"+filename+".map", 'r')
        dimentions = f.readline().split()
        self.mapw = int(dimentions[0])
        self.maph = int(dimentions[1])
        self.mapdata = []
        buf = f.read(self.mapw*self.maph)
        f.close()
        row = 0
        col = 0
        for char in buf:
            if gamemode == "lab":
                if char == "5" or char == "4":
                    self.mapdata.append(1)
                else:
                    self.mapdata.append(int(char))
            elif gamemode == "trapped":
                if char == "5":
                    self.mapdata.append(1)
                else:
                    self.mapdata.append(int(char))
            else:       
                self.mapdata.append(int(char))
            
            if char == "2": # Start location
                self.start = [col, row]
                self.old = [col, row]
                self.new = [col, row]
            if char == "3": # End location
                self.end = [col, row]
            
            col += 1
            if col == self.mapw:
                col = 0
                row +=1
            
        self.maprect = Rect(0,0,self.mapw*TILESZ,self.maph*TILESZ)
    
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
                
    def update_map(self):
        
        omi = (self.old[1]*self.mapw)+self.old[0]
        nmi = (self.new[1]*self.mapw)+self.new[0]

        self.mapdata[omi] = 1
        self.mapdata[nmi] = 2
        self.start = [self.new[0], self.new[1]]
        
        self.old[0] = self.new[0]
        self.old[1] = self.new[1]
        
        # Update grues to be sure =P
        for grue in self.grues:
            self.mapdata[grue.y*self.mapw + grue.x] = 5
        
    def send(self, msg):
        """ Send a mesage to the client """
        self.pb.send(msg)
         
    def recv(self):
        """ recieve a message from the client. """
        msg = self.pb.recv()
        return msg
        
    def cleanup(self):
        """ Clean up by closing connections and exiting the thread. """
        print "Done!"
        pygame.display.quit()
        self.pb.cleanup()
        thread.exit()
        
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print "Usage: python labyrinthServer.py mapname gamemode"
        sys.exit()
    server = serverListener()
    server.main(sys.argv[1], sys.argv[2])
    
    
    
