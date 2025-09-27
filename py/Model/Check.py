
from py.Model.Entity import Entity
from py.Events import Event, EventDispatcher

class Check(Entity):
    def __init__(
        self, 
        dispatcher: EventDispatcher, 
        title: str
    ):
        super().__init__(dispatcher)
        self._title = title
        self._checked = False
        
    def title(self) -> str:
        return self._title
        
    def check(self):
        self._checked = True
        self._notify(CheckToggled(self))

    def uncheck(self):
        self._checked = False
        self._notify(CheckToggled(self))
        
    def isChecked(self) -> bool:
        return self._checked

class CheckToggled(Event):
    def __init__(self, check: Check):
        self.check = check
        