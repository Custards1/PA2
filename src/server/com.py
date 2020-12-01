import socket as sock
class CommunicationNode:
    def __init__(self,socket,hooks = None):
        self.socket = socket
        if hooks is None:
            self._hooks = dict()
        else:
            self._hooks = hooks
    def add_hook(self,hook_key,hook):
        self._hooks[hook_key] =hook;
    def run_hook(self,hook,args):
        if hook in self._hooks:
            self._hooks[hook](args)
            return True
        return False
    def parse(self):
        pass
