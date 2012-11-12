# -*- coding: utf-8 -*-
'''
Author: Håvard Mathisen
Email: hma030@post.uit.no
Date: 1/10/2012
'''

import sys
import time

from double_dict import DoubleDict

class Algorithm:
    def __init__(self, lab):
        # The start position
        self.x = 0
        self.y = 0

        # A map over the tiles we know about.
        # Implemented as a double-dict (A dict of dicts).
        # The key x, y is the position.
        # 1, 0 is one tile to the west.
        # -1, 0 is one tile to the east.
        # 0, 1 is one tile to the north.
        # 0, -1 is one tile to the south.
        # The value is what we know about the tile.
        # A list of value meanings:
        # 0 = unknown
        # 1 = tile
        # 2 = wall
        # 3 = trap
        # 4 = toby
        # 5 = grue
        # 6 = start_block
        # 7 = next_block
        # 8 = third_block
        # ....
        self.map = DoubleDict()
        self.map.set(self.x, self.y, 6) # Set the starting tile
        self.next_node = 6 # Sets the first node number

        # Holds the labyrinth object
        self.lab = lab

        # How many lives the palyer has left
        self.lives = 5

        # Are there any grues biting the player?
        self.biting_grue = False

    def get_next_node(self):
        self.next_node = self.next_node + 1
        return self.next_node

    def go(self, move, look):
        '''
        Makes the player go in a given direction.
        The first argument is the direction, and has to be
        one of 'north', 'south', 'west' or 'east'.
        The second argument is a boolean value indicating if 
        the player shuld look around afterwards.
        '''
        assert move in ['north', 'south', 'west', 'east']

        # Go to the next tile.
        # Set x and y to the tile we intended to go to.
        if move == 'north':
            tmp = self.lab.north()
            x = self.x
            y = self.y + 1
        elif move == 'south':
            tmp = self.lab.south()
            x = self.x
            y = self.y - 1
        elif move == 'west':
            tmp = self.lab.west()
            x = self.x + 1
            y = self.y
        elif move == 'east':
            tmp = self.lab.east()
            x = self.x - 1
            y = self.y

        # Make shure we stepped into something we know about.
        assert tmp[0] in ['tile', 'wall'], 'I found a ' + tmp[0]
        assert tmp[1] in ['safe', 'trap'], 'I found a ' + tmp[1]
        assert tmp[2] in ['safe', 'grue'], 'I found a ' + tmp[2]

        # What did we go into?
        if tmp[0] == 'tile':
            # Set the new position
            self.y = y
            self.x = x
            if self.map.get(self.x, self.y) == 0:
                self.map.set(self.x, self.y, 1)
        elif tmp[0] == 'wall':
            self.map.set(x, y, 2)
        # Did we go into a trap?
        if tmp[1] == 'trap':
            self.lives = self.lives - 1
        # Did we walk into a grue?
        if tmp[2] == 'grue':
            self.biting_grue = True
            self.remove_grue()

        if look:
            self.look()

    def remove_grue(self):
        assert self.biting_grue, 'Why do we light a match if there is no grue?'

        if self.lab.inventory() > 0:
            self.lab.fire()
            self.biting_grue = False

    def look(self):
        look = self.lab.look()

        for i in look:
            assert i[0] in ['north', 'south', 'east', 'west'], 'Where do you go if you dont go north, south, east or west?'
            assert i[1] in ['tile', 'wall', 'toby'], 'I found a ' + i[1]
            assert i[2] in ['trap', 'safe'], 'I found a ' + i[2]

            # Where are we looking?
            if i[0] == 'north':
                x = self.x
                y = self.y + 1
            elif i[0] == 'south':
                x = self.x
                y = self.y - 1
            elif i[0] == 'west':
                x = self.x + 1
                y = self.y
            elif i[0] == 'east':
                x = self.x - 1
                y = self.y

            # What is around?
            if i[1] == 'tile':
                if self.map.get(x, y) == 0:
                    self.map.set(x, y, 1)
            elif i[1] == 'wall':
                self.map.set(x, y, 2)
            elif i[1] == 'toby':
                self.map.set(x, y, 4)
                # Goto Toby immedeatly.
                self.goto(x, y, 4, False)
            # Are there any traps around?
            if i[2] == 'trap':
                self.map.set(x, y, 3)

    def goto(self, x, y, node_number, look):
        '''
        Tries to go to a position x, y.
        Returns True if we can,
        returns False if we meet a wall.
        returns False if we try to go into another rectangle.
        returns false if ...
        '''
        #GO EAST
        while self.x > x:
            if not self.map.get(self.x-1, self.y) in [0, 1, node_number]:
                return False
            tmpx = self.x
            self.go('east', look)
            if self.x != tmpx-1:
                return False
        #GO WEST
        while self.x < x:
            if not self.map.get(self.x+1, self.y) in [0, 1, node_number]:
                return False
            tmpx = self.x
            self.go('west', look)
            if self.x != tmpx+1:
                return False
        #GO SOUTH
        while self.y > y:
            if not self.map.get(self.x, self.y-1) in [0, 1, node_number]:
                return False
            tmpy = self.y
            self.go('south', look)
            if self.y != tmpy-1:
                return False
        #GO NORTH
        while self.y < y:
            if not self.map.get(self.x, self.y+1) in [0, 1, node_number]:
                return False
            tmpy = self.y
            self.go('north', look)
            if self.y != tmpy+1:
                return False
        return True

    def search(self):
        '''
        Start the search algorithm.
        '''

        #The current tile need to be numbered for the function to search out the current rectange.
        #Numbering of the first tile is done in the __init__() function.
        #Numbering of the rest of the tiles are done in check_tile().

        self.find_rectangle()
        self.search_neighbor_rectangles()

    def find_rectangle(self):
        self.foundNorth = False
        self.foundWest = False
        self.foundSouth = False
        self.foundEast = False

        self.lineWestX = self.x
        self.lineEastX = self.x
        self.lineSouthY = self.y
        self.lineNorthY = self.y

        self.rectangle_number = self.map.get(self.x, self.y)

        print 'Completing rectangle ' + str(self.rectangle_number)

        # Check that we are not in a narrow corridor
        self.look()
        if self.map.get(self.x, self.y + 1) != 1:
            self.foundNorth = True
        if self.map.get(self.x, self.y - 1) != 1:
            self.foundSouth = True
        if self.map.get(self.x + 1, self.y) != 1:
            self.foundWest = True
        if self.map.get(self.x - 1, self.y) != 1:
            self.foundEast = True

        #Dont search-out a rectangle if it is 1 by 1
        if not((self.foundNorth and self.foundSouth) or (self.foundWest and self.foundEast)):
            if not self.foundNorth:
                #Start the spiral-search
                self.box_search_north()
            elif not self.foundWest:
                #Start the spiral-search
                self.box_search_west()
            elif not self.foundSouth:
                #Start the spiral-search
                self.box_search_south()
            elif not self.foundEast:
                #Start the spiral-search
                self.box_search_east()

        print 'Rectangle found'

    def check_tile(self, tile_x, tile_y, rec_x, rec_y, tile):
        '''
        Check a tile if you can run a rectange function on it.

        (tileX, tileY) is the position of the tile we are checking.
        (recX, recY) is the position of the closest tile in the current rectangle.
        Use tile = 1 if you want to go to tiles that has not been searched out.
        Use tile = 3 if you want to go through traps.
        '''
        assert (tile_x == rec_x + 1) or (tile_x == rec_x - 1) or (tile_y == rec_y + 1) or (tile_y == rec_y - 1), 'The tiles have to be close.'

        #Store the current rectangle number
        rectangleNumber = self.map.get(self.x, self.y)
        
        # Which way are we going?
        if tile == 3:
            if tile_x == rec_x + 1:
                way = 'west'
            elif tile_x == rec_x - 1:
                way = 'east'
            elif tile_y == rec_y + 1:
                way = 'north'
            elif tile_y == rec_y - 1:
                way = 'south'

        # Is this a tile we have not visited?
        if self.map.get(tile_x, tile_y) == tile:
            # Get a nodenumber for the next rectangle.
            next_node = self.get_next_node()

            #Go close to the next rectangle
            self.goto(rec_x, rec_y, rectangleNumber, False)
            #Dissarm
            if (self.lives == 1) and (tile == 3):
                self.lab.disarm(way)
            #Set next rectangle number
            self.map.set(tile_x, tile_y, next_node)
            #Go into next rectangle
            self.goto(tile_x, tile_y, next_node, False)
            # Check that we are where we are suppose to be.
            assert self.map.get(self.x, self.y) == next_node, 'this is not the next node'
            #Complete the next rectangle
            self.search()
            #Go back
            self.goto(tile_x, tile_y, next_node, False)
            self.goto(rec_x, rec_y, rectangleNumber, False)

    def search_neighbor_rectangles(self):
        # These are the current rectangle. Note that self.lineSouthY, ... can change under recursive calls
        lineSouthY = self.lineSouthY
        lineNorthY = self.lineNorthY
        lineWestX = self.lineWestX
        lineEastX = self.lineEastX

        #Check adjacent tiles (AKA depth first search)
        for x in range(lineEastX, lineWestX + 1):
            self.check_tile(x, lineNorthY+1, x, lineNorthY, 1)

        for x in range(lineEastX, lineWestX + 1):
            self.check_tile(x, lineSouthY-1, x, lineSouthY, 1)

        for y in range(lineSouthY, lineNorthY + 1):
            self.check_tile(lineEastX-1, y, lineEastX, y, 1)

        for y in range(lineSouthY, lineNorthY + 1):
            self.check_tile(lineWestX+1, y, lineWestX, y, 1)

        # If we have to disarm any adjacent tiles we do it after we have tried all the other ways
        for x in range(lineEastX, lineWestX+1):
            self.check_tile(x, lineNorthY+1, x, lineNorthY, 3)

        for x in range(lineEastX, lineWestX+1):
            self.check_tile(x, lineSouthY-1, x, lineSouthY, 3)

        for y in range(lineSouthY, lineNorthY + 1):
            self.check_tile(lineEastX-1, y, lineEastX, y, 3)

        for y in range(lineSouthY, lineNorthY+1):
            self.check_tile(lineWestX+1, y, lineWestX, y, 3)

#############################################################
#  The recursice rectangle search functions:
##############################################################
    def box_search_north(self):
        assert not self.foundNorth, 'north is already found'

        #Do we need to seach?
        #if self.map.get(self.lineEastX, self.lineNorthY + 1) in [2, 3]:
         #   self.foundNorth = True
        #Goto north east
        self.goto(self.lineEastX, self.lineNorthY, self.rectangle_number, False)
        if not self.goto(self.lineEastX, self.lineNorthY + 1, self.rectangle_number, True):
            self.foundNorth = True
        #Search north line
        elif not self.goto(self.lineWestX, self.lineNorthY + 1, self.rectangle_number, True):
            self.foundNorth = True
            self.go('south', False)

        if not self.foundNorth:
            #Expand the rectangle towards north
            self.lineNorthY = self.lineNorthY + 1
            #Fill the matrix
            for x in range(self.lineEastX, self.lineWestX + 1):
                self.map.set(x, self.lineNorthY, self.rectangle_number)

        # Where to search next
        if not self.foundWest:
            self.box_search_west()
        elif not self.foundNorth:
            self.box_rsearch_north()
        elif not self.foundSouth:
            self.box_search_south()
        elif not self.foundEast:
            self.box_rsearch_east()
        # else: return to complete_rectangle

    def box_rsearch_north(self):
        assert not self.foundNorth, 'north is already found'

        #Goto north west
        self.goto(self.lineWestX, self.lineNorthY, self.rectangle_number, False)
        if not self.goto(self.lineWestX, self.lineNorthY + 1, self.rectangle_number, True):
            self.foundNorth = True

        #Search north line
        elif not self.goto(self.lineEastX, self.lineNorthY + 1, self.rectangle_number, True):
            self.foundNorth = True
            self.go('south', False)

        if not self.foundNorth:
            #Expand the rectangle towards north
            self.lineNorthY = self.lineNorthY + 1
            #Fill the matrix
            for x in range(self.lineEastX, self.lineWestX + 1):
                self.map.set(x, self.lineNorthY, self.rectangle_number)

        # Where to search next
        if not self.foundEast:
            self.box_rsearch_east()
        elif not self.foundNorth:
            self.box_search_north()
        elif not self.foundSouth:
            self.box_rsearch_south()
        elif not self.foundWest:
            self.box_search_west()
        # else: return to complete_rectangle

    def box_search_west(self):
        assert not self.foundWest, 'west is already found'

        #Goto west north
        self.goto(self.lineWestX, self.lineNorthY, self.rectangle_number, False)
        if not self.goto(self.lineWestX + 1, self.lineNorthY, self.rectangle_number, True):
            self.foundWest = True

        #Search west line
        elif not self.goto(self.lineWestX + 1, self.lineSouthY, self.rectangle_number, True):
            self.foundWest = True
            self.go('east', False)

        if not self.foundWest:
            #Expand the rectangle towards west
            self.lineWestX = self.lineWestX + 1
            #Fill the matrix
            for y in range(self.lineSouthY, self.lineNorthY + 1):
                self.map.set(self.lineWestX, y, self.rectangle_number)
        
        # Where to search next
        if not self.foundSouth:
            self.box_search_south()
        elif not self.foundWest:
            self.box_rsearch_west()
        elif not self.foundEast:
            self.box_search_east()
        elif not self.foundNorth:
            self.box_rsearch_north()
        # else: return to complete_rectangle

    def box_rsearch_west(self):
        assert not self.foundWest, 'west is already found'

        #Goto west south
        self.goto(self.lineWestX, self.lineSouthY, self.rectangle_number, False)
        if not self.goto(self.lineWestX + 1, self.lineSouthY, self.rectangle_number, True):
            self.foundWest = True

        elif not self.goto(self.lineWestX +1, self.lineNorthY, self.rectangle_number, True):
            self.foundWest = True
            self.go('east', False)

        if not self.foundWest:
            #Expand the rectangle towards west
            self.lineWestX = self.lineWestX + 1
            #Fill the matrix
            for y in range(self.lineSouthY, self.lineNorthY + 1):
                self.map.set(self.lineWestX, y, self.rectangle_number)

        # Where to serach next
        if not self.foundNorth:
            self.box_rsearch_north()
        elif not self.foundWest:
            self.box_search_west()
        elif not self.foundEast:
            self.box_rsearch_east()
        elif not self.foundSouth:
            self.box_search_south()
        # else: return to complete_rectangle

    def box_search_south(self):
        assert not self.foundSouth, 'south is already found'

        #Goto south west
        self.goto(self.lineWestX, self.lineSouthY, self.rectangle_number, False)
        if not self.goto(self.lineWestX, self.lineSouthY - 1, self.rectangle_number, True):
            self.foundSouth = True

        #Search south line
        elif not self.goto(self.lineEastX, self.lineSouthY - 1, self.rectangle_number, True):
            self.foundSouth = True
            self.go('north', False)

        if not self.foundSouth:
            #Expand the rectangle towards south
            self.lineSouthY = self.lineSouthY - 1
            #Fill the matrix
            for x in range(self.lineEastX, self.lineWestX + 1):
                self.map.set(x, self.lineSouthY, self.rectangle_number)
            
        # Where to search next
        if not self.foundEast:
            self.box_search_east()
        elif not self.foundSouth:
            self.box_rsearch_south()
        elif not self.foundNorth:
            self.box_search_north()
        elif not self.foundWest:
            self.box_rsearch_west()
        # else: return to complete_rectangle

    def box_rsearch_south(self):
        assert not self.foundSouth, 'south is already found'

        #Goto south east
        self.goto(self.lineEastX, self.lineSouthY, self.rectangle_number, False)
        if not self.goto(self.lineEastX, self.lineSouthY - 1, self.rectangle_number, True):
            self.foundSouth = True

        #Search south line
        elif not self.goto(self.lineWestX, self.lineSouthY - 1, self.rectangle_number, True):
            self.foundSouth = True
            self.go('north', False)

        if not self.foundSouth:
            #Expand the rectangle toward south
            self.lineSouthY = self.lineSouthY - 1
            #Fill the matrix
            for x in range(self.lineEastX, self.lineWestX + 1):
                self.map.set(x, self.lineSouthY, self.rectangle_number)
        
        # Where to serach next
        if not self.foundWest:
            self.box_rsearch_west()
        elif not self.foundSouth:
            self.box_search_south()
        elif not self.foundNorth:
            self.box_rsearch_north()
        elif not self.foundEast:
            self.box_search_east()
        # else: return to complete_rectangle

    def box_search_east(self):
        assert not self.foundEast, 'east is already found'

        #Goto east south
        self.goto(self.lineEastX, self.lineSouthY, self.rectangle_number, False)
        if not self.goto(self.lineEastX - 1, self.lineSouthY, self.rectangle_number, True):
            self.foundEast = True

        #Search east line
        elif not self.goto(self.lineEastX - 1, self.lineNorthY, self.rectangle_number, True):
            self.foundEast = True
            self.go('west', False)

        if not self.foundEast:
            #Expand the rectangle towards east
            self.lineEastX = self.lineEastX - 1
            #Fill the matrix
            for y in range(self.lineSouthY, self.lineNorthY + 1):
                self.map.set(self.lineEastX, y, self.rectangle_number)

        # Where to search next
        if not self.foundNorth:
            self.box_search_north()
        elif not self.foundEast:
            self.box_rsearch_east()
        elif not self.foundWest:
            self.box_search_west()
        elif not self.foundSouth:
            self.box_rsearch_south()
        # else: return to complete_rectangle

    def box_rsearch_east(self):
        assert not self.foundEast, 'east is already found'

        #Goto east north
        self.goto(self.lineEastX, self.lineNorthY, self.rectangle_number, False)
        if not self.goto(self.lineEastX - 1, self.lineNorthY, self.rectangle_number, True):
            self.foundEast = True

        #Search east line
        elif not self.goto(self.lineEastX - 1, self.lineSouthY, self.rectangle_number, True):

            self.foundEast = True
            self.go('west', False)

        if not self.foundEast:
            #Expand the rectange towards east
            self.lineEastX = self.lineEastX - 1
            #Fill the matrix
            for y in range(self.lineSouthY, self.lineNorthY + 1):
                self.map.set(self.lineEastX, y, self.rectangle_number)

        # Where to search next
        if not self.foundSouth:
            self.box_rsearch_south()
        elif not self.foundEast:
            self.box_search_east()
        elif not self.foundWest:
            self.box_rsearch_west()
        elif not self.foundNorth:
            self.box_search_north()
        # else: return to complete_rectangle


