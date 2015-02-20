

import Queue
import Walls

class PathFind():
    
    @staticmethod
    def bfs((x0, y0), (x1, y1)):
        
        parent_map = {}
        
        parent_map[(x0, y0)] = (x0, y0)
        
        q = Queue.Queue()

        q.put ( (x0, y0) )
        
        while (not q.empty()):
            x0, y0 = q.get()
            
            if ((x0, y0) == (x1, y1)):
                break
            
            x = x0 - 1
            y = y0
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))
            
            x = x0 + 1
            y = y0
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))
                
            x = x0
            y = y0 - 1
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))
                
            x = x0
            y = y0 + 1
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))

            x = x0 + 1
            y = y0 - 1
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))
                
            x = x0 + 1
            y = y0 + 1
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))
                
            x = x0 - 1
            y = y0 + 1
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))
                
            x = x0 - 1
            y = y0 - 1
            
            if (not Walls.Walls.isThereWall((x, y)) and parent_map.get((x, y)) == None):
                parent_map [(x, y)] = (x0, y0)
                q.put ((x, y))

        return parent_map
            
    @staticmethod    
    def buildPath (path, parent_map, xy):
        
        if (parent_map[xy] != xy):
            PathFind.buildPath(path, parent_map, parent_map[xy])
        
        path.put (xy)
        
    @staticmethod
    def getPath ((x0, y0), (x1, y1)):
        
        parent_map = PathFind.bfs((x0, y0), (x1, y1))
        
        path = Queue.Queue()
        
        PathFind.buildPath (path, parent_map, (x1, y1))
        
        return path
        
        
        