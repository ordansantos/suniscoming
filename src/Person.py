
import Character
import Walls

class Person:
    
    CONST_MAX_WH = 7200
    person_list = []
    
    @staticmethod
    def getNewPerson(x, y, image = '../characters/kauan.png'):
        if (x > Person.CONST_MAX_WH / 4 or y > Person.CONST_MAX_WH / 4):
            return None
        
        p = Character.Character(image)
        p.setPosition((x, y))
        p.setId(len(Person.person_list))
        if (Walls.Walls.pushPerson(x, y, p)):
            Person.person_list.append(p)

            return p

        return None
        
    @staticmethod
    def getPersonById(p_id):
        
        for p in Person.person_list:
            if (p_id == p.getId()):
                return p
    
        return None
  
    
    @staticmethod
    def getPersonByPosition (x, y):
        if (not Walls.Walls.isTherePerson(x, y)):
            return None;
        
        return Person.getPersonById(Walls.Walls.getIdPosition(x, y))
    
    
    @staticmethod
    def changePersonLocation (p, x, y):
        return Walls.Walls.changePersonLocation(p, x, y)
    
    @staticmethod
    def cmp ((x1, y1), (x2, y2)):
    
        if (y1 < y2):
            return True
        if (y1 == y2):
            if (x1 < x2):
                return True
        return False
    
    @staticmethod
    def getPersons():
        for i in xrange (1, len(Person.person_list)):
            j = i
            while (j > 0 and Person.cmp(Person.person_list[j].getPosition(), Person.person_list[j - 1].getPosition())):
                Person.person_list[j], Person.person_list[j - 1] = Person.person_list[j - 1], Person.person_list[j]
                j -= 1
                    
        return Person.person_list
    
    @staticmethod
    def getMaster():
        
        for p in Person.person_list:
            if (p.id == Person.id_master):
                return p
        return None
    
    
    @staticmethod
    def setMaster(id_master):
        Person.id_master = id_master
    
        
        