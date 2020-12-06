import domain.user as ouser

class SUser(ouser.User):
    tag = "USR"

    def __init__(self,name=None,password=None,display_name=None,history=None):
        super().__init__(name,password,display_name,history)
    def __str__(self):
        msg = "{ name: "+self.name+', password:'+self.password+', display_name:'+self.display_name+'history:'+self.history.__str__() + " }"
        return msg
    def __repr__(self):
        return self.__str__()
    @staticmethod
    def build(_,tag):
        r = SUser()
        b = r.from_tag(tag) == 3
        if b == True:
            return (r,b,(0,"OK"))
        return (r,b,(1,"INVALID USER REQUEST"))

    def from_tag(self,taga):
        i = 0
        for it in taga:
            if i == 0:
                self.name = it
            elif i == 1:
                self.password = it
            elif i ==2:
                self.display_name = it
            else:
                break
            i+=1
        return i

    @staticmethod
    def hooks():
        return (SUser.tag,SUser.build)
