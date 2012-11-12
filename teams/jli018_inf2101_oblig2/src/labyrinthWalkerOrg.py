from labyrinthWalker import LabyrinthWalker

class LabyrinthWalkerOrg:
    def decideNextMove(self):
        while self.posDict[self.loadTile(self.nextMove)]['type'] == 'wall':
            self.nextMove = self.lookRight(self.nextMove)
        tile, vis = self.loadTile_NumVis(self.nextMove)
        leftD = self.lookLeft(self.looking)
        tileL, visL = self.loadTile_NumVis(leftD)
        for i in range (4):
            if (visL < vis) and (self.posDict[tileL]['type'] != 'wall'):
                self.nextMove = leftD
                tile, vis = self.loadTile_NumVis(self.nextMove)
            leftD = self.lookLeft(leftD)
            tileL, visL = self.loadTile_NumVis(leftD)
        self.move()