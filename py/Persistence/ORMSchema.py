
from sqlalchemy import (
    Table, Column, Integer, String, MetaData
)
from sqlalchemy.orm import registry

class ORMSchema:
    def __init__(self):
        pass
        
    def declareMapping(self):
        mapper_registry = registry()
        metadata = MetaData()
        mapper_registry.map_imperatively(
            Person, person_table,
            polymorphic_on=person_table.c.type,
            polymorphic_identity="person",
        )
