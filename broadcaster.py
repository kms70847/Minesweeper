class Broadcaster:
    def __init__(self):
        self.callbacks = []
    def bind(self, func):
        self.callbacks.append(func)
    def unbind(self, func):
        self.callbacks.remove(func)
    def broadcast(self, *args, **kargs):
        for func in self.callbacks:
            func(*args, **kargs)