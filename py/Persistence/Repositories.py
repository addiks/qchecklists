
import os

from sqlalchemy.orm import Session

from py.Model.CheckLists import CheckListsRepository, CheckList, CheckListState
from py.Model.CheckedTarget import CheckedTargetsRepository, CheckedTarget

class SQLAlchemyCheckListsRepository(CheckListsRepository):
    def __init__(self, orm: Session):
        self._orm = orm

    def findAllChecklists() -> list:
        query = self._orm.query(CheckList)
        result = self._orm.execute(query)
        return self._resultToEntities(result)

    def findDoingCheckList() -> list:
        query = self._orm.query(CheckList)
        query.filter_by(_state=CheckListState.DOING)
        result = self._orm.execute(query)
        return self._resultToEntities(result)
        
    def _resultToEntities(self, result) -> list:
        entities = []
        for row in result.all():
            entities.append(row[0])
        return entities
        
class SQLAlchemyCheckedTargetsRepository(CheckedTargetsRepository):
    def __init__(self, orm: Session):
        self._orm = orm

    def findAllCheckedTargets() -> list:
        query = self._orm.query(CheckedTarget)
        result = self._orm.execute(query)
        return self._resultToEntities(result)
        