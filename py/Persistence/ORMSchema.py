
from sqlalchemy import (
    Table, Column, Integer, String, MetaData, 
    Varchar, Text, Boolean
)
from sqlalchemy.orm import registry, mapper

from py.Model.Check import Check
from py.Model.CheckLists import CheckList, CheckListEntry
from py.Model.Templates import CheckListTemplate, CheckListTemplateEntry
from py.Model.CheckedTarget import CheckedTarget

class ORMSchema:

    def declareMapping(self):
        mapper_registry = registry()
        metadata = MetaData()
        
        checkDiscriminator = Column('checktype', Varchar(16))
        checkTable = Table(
            'checks',
            metadata,
            Column('id', Varchar(32), primary_key=True),
            checkDiscriminator,
            Column('title', Text),
            Column('checked', Boolean)
        )

        mapper_registry.map_imperatively(
            Check,
            checkTable,
            polymorphic_on=checkDiscriminator,
            polymorphic_identity="check"
        )
        
        checkedTargetsToCheckListsTable = Table(
            'checked_targets_checklists',
            metadata,
            Column(
                'checked_target_id',
                Varchar(32), 
                primary_key=True,
                ForeignKey("checked_targets.id")
            ),
            Column(
                'checklist_id', 
                Varchar(32), 
                primary_key=True,
                ForeignKey("checklists.id")
            )
        )
        
        mapper_registry.map_imperatively(
            CheckList,
            Table(
                'checklists',
                metadata,
                Column('id', Varchar(32), primary_key=True),
                Column('title', Text),
                Column('state', Varchar(16))
            ),
            properties={
                "_entries": relationship(
                    "CheckListEntry", 
                    back_populates="_checklist"
                )
            }
        )
        
        mapper_registry.map_imperatively(
            CheckListEntry,
            Table(
                'checklists_entries',
                metadata,
                Column('id', Varchar(32), primary_key=True),
                Column('checklist_id', ForeignKey('checklists.id')),
                Column('position', Integer)
            ),
            properties={
                "_checklist": relationship(
                    "CheckList", 
                    back_populates="_entries"
                )
            },
            polymorphic_identity="checklist_entry"
        )
        
        mapper_registry.map_imperatively(
            CheckListTemplate,
            Table(
                'checklists_templates',
                metadata,
                Column('id', Varchar(32), primary_key=True),
                Column('title', Text)
            ),
            properties={
                "_entries": relationship(
                    "CheckList", 
                    back_populates="_template"
                )
            }
        )
        
        mapper_registry.map_imperatively(
            CheckListTemplateEntry,
            Table(
                'checklists_templates_entries',
                metadata,
                Column('id', Varchar(32), primary_key=True),
                # checks.id
                Column('position', Integer)
            ),
            polymorphic_identity="template_entry",
            properties={
                "_template": relationship(
                    "CheckList", 
                    back_populates="_entries"
                )
            }
        )
        
        mapper_registry.map_imperatively(
            CheckedTarget,
            Table(
                'checked_targets',
                metadata,
                Column('id', Varchar(32), primary_key=True),
                Column('')
            ),
            properties={
                '_checklists': relationship(
                    "CheckListTemplateEntry", 
                    secondary=checkedTargetsToCheckListsTable
                )
            }
        )
        
        