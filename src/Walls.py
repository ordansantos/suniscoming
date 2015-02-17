
import pytmx
from pytmx.util_pygame import load_pygame

class Walls:
    
    Matrix = [[0 for i in xrange(8000)] for j in xrange(8000)] 
    
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
        if (Walls.Matrix[x][y]):
            return True
        return False
    
    @staticmethod
    def putAMagicWall (x, y, w, h):
        for i in xrange (int(x), int(x + w)):
            for j in xrange (int(y), int(y + h)):
                Walls.Matrix[i][j] = 1
                
    # About Magic Wall's Algorithm : https://www.youtube.com/watch?v=nX6FNSU_Ywc
    
    
                
    