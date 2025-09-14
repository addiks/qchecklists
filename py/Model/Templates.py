
from py.Model.Entity import Entity
from py.Model.CheckLists import CheckList, CheckListEntry
from py.Model.CheckedTarget import CheckedTarget
from py.Events import Event, EventDispatcher

class CheckListTemplateEntry(Entity):
    def __init__(self,
        dispatcher: EventDispatcher, 
        template: "CheckListTemplate",
        title: str,
        position: int
    ):
        super().__init__(dispatcher)
        self._title = title
        self._position = position
        self._template = template
        
    def template(self) -> "CheckListTemplate":
        return self._template
        
    def delete(self):
        self._template.remove(self)
        
    def title(self) -> str:
        return self._title
        
    def position(self) -> int:
        return self._position
        
class CheckListTemplate(Entity):
    def __init__(
        self, 
        dispatcher: EventDispatcher, 
        title: str
    ):
        super().__init__(dispatcher)
        self._title = title
        self._entries = {}
        
    def add(self, title: str):
        entry = CheckListTemplateEntry(self._dispatcher, self, title, len(self._entries))
        self._entries[entry.id()] = entry
        self._notify(CheckAddedToTemplate(self, entry))
        
    def remove(self, entry: CheckListEntry):
        del self._entries[entry.id()]
        self._notify(CheckRemovedFromTemplate(self, entry))
        
    def createChecklist(self) -> CheckList:
        checklist = CheckList(self._dispatcher, self._title)
        for templateEntry in self._entries.values():
            checklist.add(templateEntry.title())
        return checklist
        
    def applyTo(self, target: CheckedTarget):
        target.add(self.createChecklist())
        
class CheckAddedToTemplate(Event):
    def __init__(self, template: CheckListTemplate, entry: CheckListTemplateEntry):
        super().__init__("check-added-to-template")
        self._template = template
        self._entry = entry
        
class CheckRemovedFromTemplate(Event):
    def __init__(self, template: CheckListTemplate, entry: CheckListTemplateEntry):
        super().__init__("check-removed-from-template")
        self._template = template
        self._entry = entry