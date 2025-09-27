
from PySide6.QtCore import SignalInstance

class Event:
    pass

class EventDispatcher:
    def __init__(self):
        self._listener = {}
        self._allListener = []
        
    def subscribe(self, listener: callable, name: type):
        if name not in self._listener:
            self._listener[name] = []
        self._listener[name].append(listener)

    def subscribeToAll(self, listener: callable):
        self._allListener.append(listener)

    def dispatch(self, event: Event):
        name = type(event)
        if name in self._listener:
            for listener in self._listener[name]:
                listener(event)
        for listener in self._allListener:
            listener(event)
        
class SafeHandler:
    _instances: list[Self] = []
    
    def __init__(self, event: SignalInstance, handler: Callable) -> None:
        SafeHandler._instances.append(self)
        self.event = event
        self.handler = handler
        event.connect(self.receive)
         
    def receive(self, *args: list) -> None:
        try:
            Log.debug("Notified " + str(self.handler) + " about Qt event " + str(self.event))
            self.handler(*args)
        except:
            exception = sys.exc_info()[1]
            Log.error(exception) 
         
def connect_safely(event: SignalInstance, handler: Callable):
    SafeHandler(event, handler)
  
