
import Queue
import Walls
import math
from collections import deque

class PathFind():

    CONST_BOT_MIN_DISTANCE = 4
    @staticmethod
    def neighbors((x, y)):
        
        l  = []
        
        if not Walls.Walls.isThereWall((x - 1, y)) and not Walls.Walls.isTherePerson(x - 1, y):
            l.append((x - 1, y))   
        if not Walls.Walls.isThereWall((x + 1, y)) and not Walls.Walls.isTherePerson(x + 1, y):
            l.append((x + 1, y))
        if not Walls.Walls.isThereWall((x, y - 1)) and not Walls.Walls.isTherePerson(x, y - 1):
            l.append ((x, y - 1))
        if not Walls.Walls.isThereWall((x, y + 1)) and not Walls.Walls.isTherePerson(x, y + 1):
            l.append ((x, y + 1))
        if not Walls.Walls.isThereWall((x + 1, y - 1)) and not Walls.Walls.isTherePerson(x + 1, y - 1):
            l.append ((x + 1, y - 1))
        if not Walls.Walls.isThereWall((x + 1, y + 1)) and not Walls.Walls.isTherePerson(x + 1, y + 1):
            l.append ((x + 1, y + 1))
        if not Walls.Walls.isThereWall((x - 1, y + 1)) and not Walls.Walls.isTherePerson(x - 1, y + 1):
            l.append ((x - 1, y + 1))
        if not Walls.Walls.isThereWall((x - 1, y - 1)) and not Walls.Walls.isTherePerson(x - 1, y - 1):
            l.append ((x - 1, y - 1))

        return l
    
    @staticmethod
    def manhattanDistance ((x0, y0), (x1, y1)):
        return math.fabs (x0 - x1) + math.fabs (y0 - y1)
	
    @staticmethod
    def euclidianDistance ((x0, y0), (x1, y1)):
        return math.sqrt ((x0 - x1) ** 2 + (y0 - y1) ** 2)

    @staticmethod
    def aStar((x0, y0), (x1, y1), precise = False):
        
        loops = 0
        
        x_final, y_final = x0, y0

        parent_map = {}
        cost = {}
        
        parent_map[(x0, y0)] = (x0, y0)
        cost[(x0, y0)] = 0
        
        q = Queue.PriorityQueue()

        q.put ( (0, (x0, y0) ) )
        
        while (not q.empty()):
            
            loops += 1
            print loops
            
            x0, y0 = q.get()[1]
            
            if (not precise):
                if (PathFind.euclidianDistance( (x0, y0), (x1, y1) ) <= PathFind.CONST_BOT_MIN_DISTANCE):
                    x_final, y_final = x0, y0
                    break;
            
            
            
            neighbors = PathFind.neighbors((x0, y0))
            
            #parent_cost = cost[(x0, y0)] is best-first search more faster than AStar for our problem? 
            parent_cost = 0
            for x, y in neighbors:
                
                if ( parent_map.get((x, y)) == None or cost[(x, y)] > parent_cost + 1):
                    parent_map[(x, y)] = (x0, y0)
                    priority = parent_cost + 1 + PathFind.manhattanDistance((x1, y1), (x, y))
                    cost[(x, y)] = parent_cost + 1
                    q.put( (priority, (x, y)) )
                    
        return (x_final, y_final, parent_map)
    
    
    # There is no memory for recursive solution
    @staticmethod    
    def buildPath (deque_path, parent_map, xy):

        while (parent_map[xy] != xy):
            deque_path.appendleft(xy)
            xy = parent_map[xy]
            
    @staticmethod
    def getPath ((x0, y0), (x1, y1), ):
        
        x_final, y_final, parent_map = PathFind.aStar((x0, y0), (x1, y1), False)
        
        path_deque = deque()
        PathFind.buildPath (path_deque, parent_map, (x_final, y_final))
        
        return path_deque
        
