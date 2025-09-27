
import os, threading, time

from sqlalchemy.orm import Session

from py.Entity import Entity, EntityCreated
from py.Events import Event, EventDispatcher

class PersistenceEventListener:
    def __init__(
        self, 
        dispatcher: EventDispatcher,
        orm: Session
    ):
        self._orm = orm
        self._eventCounter = 0
        dispatcher.subscribe(self.onCreated, EntityCreated)
        dispatcher.subscribeToAll(self.onEvent)

    def onCreated(self, event: EntityCreated):
        self._orm.add(event.entity())

    def onEvent(self, event: Event):
        self._eventCounter += 1
        counter = self._eventCounter
        threading.Thread(
            target=self._checkCommit,
            args=(counter, )
        )
        
    def _checkCommit(self, counter):
        time.sleep(5)
        if counter == self._eventCounter:
            self._orm.commit()