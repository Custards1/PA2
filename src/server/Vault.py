import server.user
class Vault:
    def __init__(self,storage = None):
        if storage is None:
            self._storage = dict()
        else:
            self._storage = storage
    def __contains__(self, item : server.user.User):
        if item.name in self._storage:
            return True
        return False
    def __getitem__(self, item):
        return self._storage[item]

