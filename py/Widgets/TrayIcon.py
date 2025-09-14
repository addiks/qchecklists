import os

from PySide6.QtWidgets import QSystemTrayIcon, QMenu

class TrayIcon(QSystemTrayIcon):
    def __init__(self, eventDispatcher: EventDispatcher):
        super(QSystemTrayIcon).__init__(self)
        self.eventDispatcher = eventDispatcher
        self.setContextMenu(self.createMenu())
        

    def createMenu(self) -> QMenu:
        menu = QMenu()