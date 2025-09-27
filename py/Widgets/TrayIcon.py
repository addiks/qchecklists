import os

from PySide6.QtWidgets import QSystemTrayIcon, QMenu

from py.Model.CheckLists import CheckListsRepository, CheckList, CheckListEntry, CheckListState

from py.Model.CheckLists import CheckAddedToList, CheckRemovedFromList, CheckListStateChange
from py.Events import Event, EventDispatcher, connect_safely

class TrayIcon(QSystemTrayIcon):
    def __init__(
        self, 
        checklistRepository: CheckListsRepository,
        eventDispatcher: EventDispatcher
    ):
        super(QSystemTrayIcon).__init__(self)
        self._checklistRepository = checklistRepository
        self._eventDispatcher = eventDispatcher
        self._menus = {}
        self._actions = {}
        self._menu = None
        self.setContextMenu(self.createMenu())
        eventDispatcher.subscribe(self._onChecklistStateChange, CheckListStateChange)
        eventDispatcher.subscribe(self._onCheckAdded, CheckAddedToList)
        eventDispatcher.subscribe(self._onCheckRemoved, CheckRemovedFromList)
        
    def createMenu(self) -> QMenu:
        self._menu = QMenu()
        
        openListingWindowAction = self._menu.addAction('Open Main Window')
        openListingWindowAction.setShortcut('Ctrl+M')
        connect_safely(openListingWindowAction.triggered, self._onOpenMainWindow)
        # Open Checklist Listing Window
        
        self._menu.addSeparator()
        
        for checklist in self._checklistRepository.findDoingCheckList():
            self._addChecklist(checklist)
        
    def _onOpenMainWindow(self):
        eventDispatcher.dispatch(TrayIconOpenMainWindowClicked())
        
    def _onChecklistStateChange(self, event: CheckListStateChange):
        checklistId = event.checklist.id()
        if event.oldState == CheckListState.DOING:
            if checklistId in self._actions:
                self._menu.removeAction(self._actions[checklistId])
                del self._actions[checklistId]
        elif event.checklist.isDoing():
            self._addChecklist(checklist)
        
    def _addChecklist(self, checklist: CheckList):
        checklistMenu = QMenu(checklist.title())
        self._menus[checklist.id()] = checklistMenu
        for checklistEntry in checklist.entries():
            self._addCheckEntry(checklistEntry)
        checklistMenuAction = self._menu.addMenu(checklistMenu)
        self._actions[checklistEntry.id()] = checklistMenuAction
        
    def _onCheckAdded(self, event: CheckAddedToList):
        if event.entry.checklist().isDoing():
            self._addCheckEntry(event.entry)
        
    def _onCheckRemoved(self, event: CheckRemovedFromList):
        entry = event.entry
        if entry.id() in self._actions:
            self._menus[entry.checklist().id()].removeAction(self._actions[entry.id()])
            del self._actions[entry.id()]
        
    def _addCheckEntry(self, entry: CheckListEntry):
        checklistMenu = self._menus[entry.checklist().id()]
        checklistEntryAction = checklistMenu.addAction(checklistEntry.title())
        self._actions[checklistEntry.id()] = checklistEntryAction
        
        
            
        
class TrayIconOpenMainWindowClicked(Event):
    pass