
from enum import Enum

from py.Model.Entity import Entity
from py.Model.Check import Check
from py.Events import Event, EventDispatcher

class CheckListEntry(Check):
    def __init__(
        self, 
        dispatcher: EventDispatcher, 
        checklist: "CheckList",
        title: str,
        position: int
    ):
        super().__init__(dispatcher, title)
        self._checklist = checklist
        self._position = position
        
    def checklist(self) -> "CheckList":
        return self._checklist
        
    def delete(self):
        self._checklist.remove(self)
        
    def check(self):
        self._checklist.assertMutable()
        super().check()
        self._checklist.onCheckChecked(self)
        
    def uncheck(self):
        self._checklist.assertMutable()
        super().uncheck()
        self._checklist.onCheckUnchecked(self)
        
    def isMutable(self) -> bool:
        return self._checklist.isMutable()
        
    def position(self) -> int:
        return self._position
        
class CheckListState(Enum):
    CREATED = "Created"
    DOING = "Doing"
    DONE = "Done"
    CANCELED = "Canceled"
        
class CheckList(Entity):
    def __init__(
        self, 
        dispatcher: EventDispatcher, 
        title: str
    ):
        super().__init__(dispatcher)
        self._title = title
        self._entries = {}
        self._state = CheckListState.CREATED
        
    def entries(self) -> list:
        # TODO: Sort by position
        return self._entries.values()
        
    def add(self, title: str) -> CheckListEntry:
        self.assertMutable()
        entry = CheckListEntry(self._dispatcher, self, title, len(self._entries))
        self._entries[entry.id()] = entry
        if self._state == CheckListState.DONE:
            self._setState(CheckListState.DOING)
        self._notify(CheckAddedToList(self, entry))
        return entry
        
    def remove(self, entry: CheckListEntry):
        self.assertMutable()
        del self._entries[entry.id()]
        if self.areAllCheckChecked():
            self._setState(CheckListState.DONE)
        self._notify(CheckRemovedFromList(self, entry))
        
    def get(self, title: str) -> CheckListEntry:
        for entry in self._entries.values():
            if entry.title() == title:
                return entry
        return None
        
    def onCheckChecked(self, entry: CheckListEntry):
        if self._state == CheckListState.CREATED:
            self._setState(CheckListState.DOING)
        if self.areAllCheckChecked():
            self._setState(CheckListState.DONE)
        
    def onCheckUnchecked(self, entry: CheckListEntry):
        if self._state == CheckListState.CREATED:
            self._setState(CheckListState.DOING)
        if self._state == CheckListState.DONE:
            self._setState(CheckListState.DOING)
            
    def cancel(self):
        self._state = CheckListState.CANCELED
        
    def isMutable(self) -> bool:
        return self._state != CheckListState.CANCELED
        
    def isDoing(self) -> bool:
        return self._state == CheckListState.DOING
        
    def isDone(self) -> bool:
        return self._state == CheckListState.DONE
        
    def isCanceled(self) -> bool:
        return self._state == CheckListState.CANCELED
        
    def isFinished(self) -> bool:
        return self.isDone() or self.isCanceled()
        
    def assertMutable(self):
        if not self.isMutable():
            raise Error("Cannot mutate checklist '" + self._title + "'")
        
    def areAllCheckChecked(self) -> bool:
        areAllCheckChecked = True
        for entry in self._entries.values():
            if not entry.isChecked():
                return False
        return True
        
    def _setState(self, newState: CheckListState):
        if self._state == newState:
            return
        oldState = self._state
        self._state = newState
        self._notify(CheckListStateChange(self, oldState))
        
class CheckAddedToList(Event):
    def __init__(self, checklist: CheckList, entry: CheckListEntry):
        self.checklist = checklist
        self.entry = entry
        
class CheckRemovedFromList(Event):
    def __init__(self, checklist: CheckList, entry: CheckListEntry):
        self.checklist = checklist
        self.entry = entry
        
class CheckListStateChange(Event):
    def __init__(self, checklist: CheckList, oldState: CheckListState):
        self.checklist = checklist
        self.oldState = oldState
        
class CheckListsRepository:

    def findAllChecklists() -> list:
        raise NotImplementedError()

    def findDoingCheckList() -> list:
        raise NotImplementedError()