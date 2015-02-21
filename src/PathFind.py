

import Queue
import Walls
import math
from collections import deque

class PathFind():


    @staticmethod
    def neighbors((x, y)):
        
        l  = []
        
        if not Walls.Walls.isThereWall((x - 1, y)):
            l.append((x - 1, y))   
        if not Walls.Walls.isThereWall((x + 1, y)):
            l.append((x + 1, y))
        if (not Walls.Walls.isThereWall((x, y - 1))):
            l.append ((x, y - 1))
        if not Walls.Walls.isThereWall((x, y + 1)):
            l.append ((x, y + 1))
        if not Walls.Walls.isThereWall((x + 1, y - 1)):
            l.append ((x + 1, y - 1))
        if not Walls.Walls.isThereWall((x + 1, y + 1)):
            l.append ((x + 1, y + 1))
        if not Walls.Walls.isThereWall((x - 1, y + 1)):
            l.append ((x - 1, y + 1))
        if not Walls.Walls.isThereWall((x - 1, y - 1)):
            l.append ((x - 1, y - 1))
        
        return l
    
    @staticmethod
    def manhattanDistance ((x0, y0), (x1, y1)):
        return math.fabs (x0 - x1) + math.fabs (y0 - y1)

    @staticmethod
    def aStar((x0, y0), (x1, y1)):
        
        parent_map = {}
        cost = {}
        
        parent_map[(x0, y0)] = (x0, y0)
        cost[(x0, y0)] = 0
        
        q = Queue.PriorityQueue()

        q.put ( (0, (x0, y0) ) )
        
        while (not q.empty()):
            x0, y0 = q.get()[1]
            
            if ((x0, y0) == (x1, y1)):
                break
            
            neighbors = PathFind.neighbors((x0, y0))
            
            parent_cost = cost[(x0, y0)]
            
            for x, y in neighbors:
                
                if ( parent_map.get((x, y)) == None or cost[(x, y)] > parent_cost + 1):
                    parent_map[(x, y)] = (x0, y0)
                    priority = parent_cost + 1 + PathFind.manhattanDistance((x1, y1), (x, y))
                    cost[(x, y)] = parent_cost + 1
                    q.put( (priority, (x, y)) )
                    
        return parent_map
    
    
    # There is no memory for recursive solution
    @staticmethod    
    def buildPath (deque_path, parent_map, xy):
        
        while (parent_map[xy] != xy):
            deque_path.appendleft(xy)
            xy = parent_map[xy]
            
    @staticmethod
    def getPath ((x0, y0), (x1, y1)):
        
        parent_map = PathFind.aStar((x0, y0), (x1, y1))
        
        path_deque = deque()
        
        PathFind.buildPath (path_deque, parent_map, (x1, y1))
        
        return path_deque
        
        
        