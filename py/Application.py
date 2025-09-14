
import sys, os, traceback, logging, hashlib


from typing import Any, Self
from os.path import basename, dirname, abspath

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer

from py.Widgets.IssueListingWindow import IssueListingWindow
from py.Widgets.TrayIcon import TrayIcon, TrayIconEventReceiver
from py.Log import Log
from py.Events import EventDispatcher

class Application(QtWidgets.QApplication, TrayIconEventReceiver):
    _instance = None

    @staticmethod
    def main(argv: list[str]) -> int:
        try:
            app = Application.instance()
            app.run(argv)
            return app.execQt()
            
        except SystemExit:
            sys.exit(0)
        
        except:
            exception = sys.exc_info()[0]
            Log.error(exception)
            Log.error(traceback.format_exc())
            
        return -2
        
    @staticmethod
    def instance() -> Self:
        if Application._instance == None:
            Application._instance = Application()
        return Application._instance
        
    def __init__(self):
        self._isReadyForInteraction = False
        super().__init__([])
        self.setApplicationDisplayName("QCheckLists")
        self.setDesktopFileName("qchecklists")
        self.eventDispatcher = EventDispatcher()
        self.trayIcon = TrayIcon(self.eventDispatcher)
        self.window = IssueListingWindow(self.eventDispatcher)
        
    def run(self, argv: list[str]) -> None:
        pass
        # self.window.show()
        
    def execQt(self) -> int:
        exitCode = self.exec() # Qt execution loop
        Log.info("Qt exited with code " + str(exitCode))
        return exitCode
             
    def _bashScript(self) -> str:
        return self.baseDir() + "/bin/qchecklists.sh"
        
    def baseDir(self) -> str:
        return dirname(dirname(abspath(__file__)))
        
