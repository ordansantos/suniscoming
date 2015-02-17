
import pytmx
from pytmx.util_pygame import load_pygame

class Walls:
    
    Matrix = [[None for i in xrange(7210)] for j in xrange(7210)] 
    
    def __init__(self):
        pass
    
    @staticmethod
    def pushWalls (tile_map):
        for layer in tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    Walls.putAMagicWall (obj.x, obj.y, obj.width, obj.height)
                    
    @staticmethod
    def isThereWall ((x, y)):
        if (Walls.Matrix[x][y] != None and Walls.Matrix[x][y] == -1):
            return True
        return False
    
    @staticmethod
    def putAMagicWall (x, y, w, h):
        for i in xrange (int(x), int(x + w)):
            for j in xrange (int(y), int(y + h)):
                Walls.Matrix[i][j] = -1
    # About Magic Wall's Algorithm : https://www.youtube.com/watch?v=nX6FNSU_Ywc
    
    @staticmethod
    def pushPerson (x, y, p):
        if (not Walls.isThereWall((x, y))):
            Walls.Matrix[x][y] = p.getId()
            return True
        return False;
    
    @staticmethod
    def changePersonLocation (p, x, y):
        x0, y0 = p.getPosition()
        if ( Walls.pushPerson(x, y, p)):
            Walls.Matrix[x0][y0] = None
            return True
        return False
        
        
    @staticmethod
    def isTherePerson (x, y):
        if (Walls.Matrix[x][y] != None and Walls.Matrix[x][y] != -1):
            return True
        return False

    @staticmethod
    def getIdPosition (x, y):
        if (Walls.Matrix[x][y] == None or Walls.Matrix[x][y] == -1):
            return -1
        return Walls.Matrix[x][y]
    
    
   
    
    
                
    