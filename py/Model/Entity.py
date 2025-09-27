
from uuid import UUID, uuid4

from py.Events import Event, EventDispatcher

class Entity:
    def __init__(self, dispatcher: EventDispatcher):
        self._id = uuid4().hex
        self._dispatcher = dispatcher
        dispatcher.dispatch(EntityCreated(self))

    def id(self) -> str:
        return self._id
        
    def _notify(self, event: Event):
        if self._dispatcher != None:
            self._dispatcher.dispatch(event)

class EntityCreated(Event):
    def __init__(self, entity: Entity):
        super().__init__("entity-created")
        self._entity = entity
        
    def entity(self): Entity:
        return self._entity