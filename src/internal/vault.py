from internal import suser
import threading
import json
class Vault:
    login_tag = "LOG"
    def __init__(self,storage = None):
        if storage is None:
            self._storage = dict()
        else:
            self._storage = storage
        self._lock = threading.Lock()
    def __contains__(self, item : suser.SUser):
        with self._lock:
            if item.name in self._storage:
                return item.password == self._storage[item.name].password
            return False
    def __getitem__(self, item):
        with self._lock:
            return self._storage[item.name]
    def __setitem__(self, key : suser.SUser, value: suser.SUser):
            if not self.append(key):
                with self._lock:
                    self._storage[key.name] = value
    def __str__(self):
        return self._storage.__str__()
    def get(self,name : str):
        with self._lock:
            try:
                return self._storage[name]
            except:
                return None
    def append(self,user):

        with self._lock:

            if user.name not in self._storage:
                self._storage[user.name] = user

                return True
            return False
    def exists(self,name):
        return self.get(name) == None
    @staticmethod
    def build_login_user(vaults,tag):
        r = suser.SUser()
        b = r.from_tag(tag)

        b = b == 2
        if b == True:
            if r in vaults.user_data:

                if not vaults.user_data[r].logged_in:
                    vaults.user_data[r].logged_in = True
                    vaults.connected_user = vaults.user_data[r]
                    return (vaults.user_data[r],b,(0,"OK"))
                return (r,b,(2,"Already Logged In"))

        return (r,b,(1,"Invalid Credentials"))
    @staticmethod
    def debuild_login_user(vaults,tag):
        vaults.user_data[vaults.connected_user].logged_in = False
        return (vaults.connected_user,None,(0,"Ok"))
    @staticmethod
    def login_tag_hook(self,user,com):
        if user in self:
            com.connected_user = self[user]
            return True
        return False
    @staticmethod
    def login_register_hook(self,user,com):
        if user in self:
            com.connected_user = self[user]
            return True
        return False

    @staticmethod
    def user_creation_hook(self,user,com):
        if self.append(user):
            com.connected_user = user
            return True
        return False
    def from_json(self,file):
        self._storage = dict()
        with open(file, "r") as data_file:
            a = data_file.read()
            objs = json.loads(a,object_hook=as_complex)
            for i in objs:
                self._storage[i] = objs[i]
    def to_json(self):
        msg = dict()
        for (j) in self._storage:
            if isinstance(self._storage[j],suser.SUser):
                msg[j]= self._storage[j].as_dct()
        return json.dumps(msg)

def as_complex(dct):
    if dct.get('name') is not None and dct.get('password') is not None:
        return suser.SUser(dct.get('name'),dct.get('password'),dct.get('display_name'),dct.get('history'))
    return dct


