
import os

from PySide6 import QtCore, QtWidgets, QtGui

from py.Events import EventDispatcher, connect_safely, Event
from py.Model.CheckLists import CheckListsRepository

class IssueListingWindow(QtWidgets.QMainWindow):
    def __init__(
        self, 
        eventDispatcher: EventDispatcher, 
        checkedTargetsRepository: CheckedTargetsRepository,
        baseDir: str
    ):
        self._eventDispatcher = eventDispatcher
        self._checkedTargetsRepository = checkedTargetsRepository

        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(
            baseDir + "/resources/qchecklists-logo-v1.512.png"
        )))
        
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        
        vbox = QtWidgets.QVBoxLayout(self.centralWidget)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.centralWidget.layout = vbox
        
        buttonHBox = QtWidgets.QHboxLayout(vbox)
        vbox.addWidget(buttonHBox)

        newChecklistButton = QtWidgets.QToolButton(buttonHBox)
        buttonHBox.addWidget(newChecklistButton)
        connect_safely(newChecklistButton.triggered, self._onNewChecklistBtnPressed)
        
        templatesButton = QtWidgets.QToolButton(buttonHBox)
        buttonHBox.addWidget(templatesButton)
        connect_safely(newChecklistButton.triggered, self._onTemplatesBtnPressed)
        
        targetsTree = QtWidgets.QTreeView(vbox)
        vbox.addWidget(targetsTree)
        
        for targets in checkedTargetsRepository.findAllCheckedTargets():
            pass
        
    def _onNewChecklistBtnPressed(self):
        self._eventDispatcher.dispatch(NewChecklistButtonPressed())
       
    def _onTemplatesBtnPressed(self):
        self._eventDispatcher.dispatch(TemplatesButtonPressed())
        
class NewChecklistButtonPressed(Event):
    pass
    
class TemplatesButtonPressed(Event):
    pass