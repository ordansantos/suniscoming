
class Walls:
    
    Matrix = [[0 for i in xrange(8000)] for j in xrange(8000)] 
    
    def __init__(self):
        pass
    
    @staticmethod
    def pushWall ( (x, y), (w, h)):
        # print x, y, w, h
        for i in xrange (int(x), int(x + w)):
            for j in xrange (int(y), int(y + h)):
                print i, j
                Walls.Matrix[i][j] = 1
    
    @staticmethod
    def isThereWall ((x, y)):
        if (Walls.Matrix[x][y]):
            return True
        return False
    