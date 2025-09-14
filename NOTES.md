
# Model / Entities
* Check (Quasi eine benannte Checkbox)
* Checklist
    * isDoing "Wird daran gerade aktiv gearbeitet?"
    * isDone
    * Lifecycle: "Created" -> "Doing" -> "Done" / "Canceled"
    * [n:m] ChecklistEntry [1:1] Check
* ChecklistTemplate
    * [n:m] ChecklistTemplateEntry [1:1] Checks
* Events
    * CheckChangeEvent
    * ChecklistLifecycleChange
    * ChecklistStructureChange
    * TemplateStructureChange
* RemoteIntegration (z.B. GitLab oder Markdown-Dateien)
* CheckedTarget (Das was gecheckt werden soll: Ticket, Werk, Reise, ...)
    * Type ("Ticket", "Task", ... / Abhängig von Integration)
    * [n:m] Checklist
    * [n:1] RemoteIntegration

# Windows:
* Checklist List
    * New Checklist
    * "Show Done Checklists"
    * "Show Canceled Checklists"
* Checklist View
* Checklist-Template List
    * Import/Export
    * "New Template" / "Template from Checklist"
* Integrations (GitLab, ...)
* History

* TrayIcon
    * Open Checklist List Window
    * New Checklist
    * Access active Checklists (State = DOING)
    
# Architecture
[DB] <=> [ORM] <=> [Model (Entities)] <=> [Events] <=> [UI]

* [DB]:     SqLite (~/.local/share/qchecklists.sqlite)
* [ORM]:    SQLAlchemy (separat definiertes Mapping; Yoyo-Migrations)
* [Events]: Kommunikation zwischen anderen Layern. Selbst-Gebaut
* [UI]:     Qt-Widgets / Pyside6