
from py.Model.Entity import Entity
from py.Model.CheckLists import CheckList
from py.Events import Event


class CheckedTarget(Entity):
    def __init__(self, title: str):
        self._title = title
        self._checklists = {}
        self._parent = None
        self._children = []
        
    def title(self):
        return self._title
        
    def parent(self) -> CheckedTarget:
        return self._parent
        
    def children(self) -> list:
        return self._children
        
    def add(self, checklist: CheckList):
        self._checklists[checklist.id()] = checklist
        
    def remove(self, checklist: CheckList):
        del self._checklists[checklist.id()]
        
class CheckedTargetsRepository:

    def findAllCheckedTargets() -> list:
        raise NotImplementedError()
        