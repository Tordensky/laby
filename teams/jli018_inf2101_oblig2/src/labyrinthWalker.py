import random

class LabyrinthWalker:
    def __init__(self, lab):
        """Initiates the walker assigning the startposition as (0,0) and the startdirection as South"""
        self.lab = lab
        self.pos = (0,0)
        self.looking = 'S'
        self.nextMove = 'S'
        self.posDict = {}
        self.path = []

        self.posDict[self.pos] = {'NumVis':1, 'type':'tile'}

    def solve(self):
        """A simple loop execution the algorithm"""
        for i in range (1337):
            self.addAdjacent()
            self.lookAround()
            self.decideNextMove()

    def decideNextMove(self):
        """Will first try to see if the tile infront is a valid move (Not wall & not visited)
        If not it will try go to either side, chosen at random
        If both these have been explored it will backtrack"""
        doBacktrack = 1
        if (self.posDict[self.loadTile(self.nextMove)]['type'] != 'wall') and (self.posDict[self.loadTile(self.nextMove)]['NumVis'] == 0):
            self.move()
            doBacktrack = 0
        else:
            dirS = self.lookRandom(self.looking)
            tileS, visS = self.loadTile_NumVis(dirS)
            for i in range (100):
                if (visS == 0) and (self.posDict[tileS]['type'] != 'wall'):
                    self.nextMove = dirS
                    doBacktrack = 0
                    self.move()
                    break
                dirS = self.lookRandom(dirS)
                tileS, visS = self.loadTile_NumVis(dirS)
        if doBacktrack == 1:
            self.backtrack()

    def lookLeft(self, looking):
        """Returns the direction as if you had looked to the left"""
        if looking == 'S': return 'E'
        if looking == 'E': return 'N'
        if looking == 'N': return 'W'
        if looking == 'W': return 'S'

    def lookRight(self, looking):
        """Returns the direction as if you had looked to the right"""
        if looking == 'S': return 'W'
        if looking == 'W': return 'N'
        if looking == 'N': return 'E'
        if looking == 'E': return 'S'

    def lookBack(self, looking):
        """Returns the direction as if you had looked behind you"""
        if looking == 'S': return 'N'
        if looking == 'W': return 'E'
        if looking == 'N': return 'S'
        if looking == 'E': return 'W'

    def lookRandom(self,looking):
        """Will randomly look to either the left or the right side"""
        rand = random.randint(0,1)
        if rand == 0: return self.lookLeft(looking)
        if rand == 1: return self.lookRight(looking)

    def addAdjacent(self):
        """Calculate the adjacent tiles and add them to the position dictinary"""
        self.south = self.findPosSouth()
        self.north = self.findPosNorth()
        self.east =  self.findPosEast()
        self.west =  self.findPosWest()
        self.adjacent = [self.south, self.north, self.east, self.west]
        for direct in self.adjacent:
            if not (direct in self.posDict):
                self.posDict[direct] = {'NumVis': 0, 'type':'unknown'}
        
    def loadTile(self, direction):
        """Loads the tile in the specified direction"""
        if (direction == 'S'): return self.south
        if (direction == 'N'): return self.north
        if (direction == 'E'): return self.east
        if (direction == 'W'): return self.west
        
    def loadTile_NumVis(self,direction):
        """Loads the tile in the specified direction, and the number of times it has been visited"""
        if (direction == 'S'): return (self.south, self.posDict[self.south]['NumVis'])
        if (direction == 'N'): return (self.north, self.posDict[self.north]['NumVis'])
        if (direction == 'E'): return (self.east, self.posDict[self.east]['NumVis'])
        if (direction == 'W'): return (self.west, self.posDict[self.west]['NumVis'])
        
    def rewordLook(self, look):
        """Changes the default wording for directions to their shorthand version"""
        for ele in look:
            if ele[0] == 'south': ele[0] = 'S'
            if ele[0] == 'north': ele[0] = 'N'
            if ele[0] == 'east':  ele[0] = 'E'
            if ele[0] == 'west':  ele[0] = 'W'
        return look
        
    def findPosSouth(self):
        """Calculate the tile south of the position"""
        return ((self.pos[0]), (self.pos[1]+1))
        
    def findPosNorth(self):
        """Calculate the tile north of the position"""
        return ((self.pos[0]), (self.pos[1]-1))
        
    def findPosEast(self):
        """Calculate the tile east of the position"""
        return ((self.pos[0]+1), (self.pos[1]))
        
    def findPosWest(self):
        """Calculate the tile west of the position"""
        return ((self.pos[0]-1), (self.pos[1]))
        
    def move(self):
        """Will send the move signal to the server and verify that it was a valid move
        If so it will update the class-specific values
        If not it will look around so the next move is not so ill-informed"""
        if self.posDict[self.loadTile(self.nextMove)]['type'] == 'wall': newTile=[0]
        elif self.nextMove == 'S': newTile = self.lab.south()
        elif self.nextMove == 'E': newTile = self.lab.east()
        elif self.nextMove == 'N': newTile = self.lab.north()
        elif self.nextMove == 'W': newTile = self.lab.west()
        if newTile[0] == 'tile':
            self.pos = self.loadTile(self.nextMove)
            self.posDict[self.pos]['NumVis'] += 1
            self.looking = self.nextMove
            self.path.append(self.looking)
        elif newTile is not [0]:
            self.lookAround()

    def backtrack(self):
        """Will pop the last movement made and backtrack one step"""
        last = self.path.pop()
        back = self.lookBack(last)
        if back == 'S': newTile = self.lab.south()
        elif back == 'E': newTile = self.lab.east()
        elif back == 'N': newTile = self.lab.north()
        elif back == 'W': newTile = self.lab.west()
        self.nextMove = last
        self.pos = self.loadTile(back)
        self.posDict[self.pos]['NumVis'] += 1
        self.looking = self.nextMove
        
    def lookAround(self):
        """Calls the server for information from the adjacent tiles and add them into the local dictionary"""
        sur = self.rewordLook(self.lab.look())
        for ele in sur:
            self.posDict[self.loadTile(ele[0])]['type'] = ele[1]
