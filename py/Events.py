
class Event:
    def __init__(self, name: str):
        self._name = name
        
    def name(self) -> str:
        return self._name

class EventDispatcher:
    def __init__(self):
        self._listener = {}
        
    def subscribe(self, listener: callable, name: str):
        if name not in self._listener:
            self._listener[name] = []
        self._listener[name].append(listener)

    def dispatch(self, event: Event):
        name = event.name()
        if name in self._listener:
            for listener in self._listener[name]:
                listener(event)
        