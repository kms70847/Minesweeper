class Broadcaster:
    """
    An event-broadcasting object.
    Interested listeners can register callbacks that get executed
    when the object has something to broadcast.
    """

    def __init__(self):
        self.callbacks = []

    def bind(self, func):
        """Register `func` as a callback."""

        self.callbacks.append(func)

    def unbind(self, func):
        """
        Unregister `func` as a callback.
        Note: `func` must be referentially equal to the object
        used to bind in the first place.
        Particular care must be taken for anonymous lambdas.
        """

        self.callbacks.remove(func)

    def broadcast(self, *args, **kargs):
        """Call each registered callback with the given arguments."""

        for func in self.callbacks:
            func(*args, **kargs)
