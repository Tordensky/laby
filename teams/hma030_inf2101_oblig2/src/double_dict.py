# -*- coding: utf-8 -*-

'''
Author: Håvard Mathisen
Email: hma030@post.uit.no
Date: 1/10/2012
'''

class DoubleDict:

    def __init__(self):
        self.mat = {}

        # The boundarys, used by print
        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0

    def set(self, x, y, val):
        '''
        Set the value of an item, and updates the dict-boundaries.
        '''
        if x > self.maxX:
            self.maxX = x
        if x < self.minX:
            self.minX = x
        if y > self.maxY:
            self.maxY = y
        if y < self.minY:
            self.minY = y
        
        try:
            self.mat[x][y] = val
        except KeyError:
            self.mat[x] = {}
            self.mat[x][y] = val

    def get(self, x, y):
        '''
        Get value from the dictionary, or return 0 if it does not exists.
        '''
        try:
            return self.mat[x][y]
        except KeyError:
            return 0 # Return 0 if there is no entry in the map

    def __repr__(self):
        # Do not print the boundaries (They are only for the __str__ fucntion).
        return self.mat.__repr__()

    def __str__(self):
        # Print the double-dict as a matrix.
        l = ['DoubleDict: TopLeft (', str(self.maxX), ', ', str(self.maxY), '), BottomRight (', str(self.minX), ', ', str(self.minY), ') \n']
        for y in range(self.maxY, self.minY-1, -1):
            for x in range(self.maxX, self.minX - 1, -1):
                l.append(('%2i' % self.get(x, y)) + ' ')
            l.append('\n')

        return str().join(l)

