
import sys, os, traceback, logging, hashlib


from typing import Any, Self
from os.path import basename, dirname, abspath

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QTimer

from py.Model.CheckLists import CheckListsRepository
from py.Model.CheckedTarget import CheckedTargetsRepository
from py.Persistence.Repositories import SQLAlchemyCheckListsRepository, SQLAlchemyCheckedTargetsRepository
from py.Widgets.IssueListingWindow import IssueListingWindow
from py.Widgets.TrayIcon import TrayIcon, TrayIconOpenMainWindowClicked
from py.Log import Log
from py.Events import EventDispatcher

class Application(QtWidgets.QApplication):
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
        self._databaseEngine = None
        self._databaseConnection = None
        self._orm = None
        self.eventDispatcher = EventDispatcher()
        
        self.eventDispatcher.subscribe(
            self.onTrayIconOpenMainWindowClicked,
            TrayIconOpenMainWindowClicked
        )
        
    def run(self, argv: list[str]) -> None:
        self.trayIcon = TrayIcon(
            self.checklistRepository(),
            self.eventDispatcher
        )
        self.window = IssueListingWindow(
            self.eventDispatcher,
            self.checklistRepository(),
            self.baseDir()
        )
        
    def execQt(self) -> int:
        exitCode = self.exec() # Qt execution loop
        Log.info("Qt exited with code " + str(exitCode))
        return exitCode
        
    def onTrayIconOpenMainWindowClicked(self):
        self.window.show()
        
    def checklistRepository(self) -> CheckListsRepository:
        return SQLAlchemyCheckListsRepository(self.orm())
        
    def checkedTargetsRepository(self) -> CheckedTargetsRepository:
        return SQLAlchemyCheckedTargetsRepository(self.orm())
        
    def databaseEngine(self) -> Engine:
        if self._databaseEngine == None:
            self._databaseEngine = create_engine(
                url="sqlite://" + self.databasePath()
            )
        return self._databaseEngine
        
    def databaseConnection(self) -> Connection:
        if self._databaseConnection == None:
            self._databaseConnection = self.databaseEngine().connect()
        return self._databaseConnection
        
    def orm() -> Session:
        if self._orm == None:
            self._orm = sessionmaker(bind=self.databaseConnection())
        return self._orm
             
    def databasePath(self) -> str:
        return os.path.expanduser('~/.local/share/qchecklists.sqlite')
        
    def _bashScript(self) -> str:
        return self.baseDir() + "/bin/qchecklists.sh"
        
    def baseDir(self) -> str:
        return dirname(dirname(abspath(__file__)))