
import Character
import Walls

class Person:
    
    person_list = []
    
    @staticmethod
    def getNewPerson(x, y):
        p = Character.Character()
        p.setPosition((x, y))
        p.setId(len(Person.person_list))
        if (Walls.Walls.pushPerson(x, y, p)):
            Person.person_list.append(p)
            return p
        return None
        
    @staticmethod
    def getPersonById(p_id):
        
        if (len(Person.person_list) <= p_id):
            return None
        return Person.person_list[p_id]
    
    @staticmethod
    def getPersonByPosition (x, y):
        if (not Walls.Walls.isTherePerson(x, y)):
            return None;
        
        return Person.getPersonById(Walls.Walls.getIdPosition(x, y))
    
    
    @staticmethod
    def changePersonLocation (p, x, y):
        return Walls.Walls.changePersonLocation(p, x, y)
        
        