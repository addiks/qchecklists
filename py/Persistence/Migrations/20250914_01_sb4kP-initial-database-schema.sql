-- Initial Database Schema
-- depends: 

CREATE TABLE checks (
    id VARCHAR(32) PRIMARY KEY,
    checktype VARCHAR(16),
    title TEXT,
    checked BOOLEAN DEFAULT 0
) WITHOUT ROWID;

CREATE TABLE checklists (
    id VARCHAR(32) PRIMARY KEY,
    title TEXT,
    state VARCHAR(16)
) WITHOUT ROWID;

CREATE TABLE checklists_entries (
    id VARCHAR(32) PRIMARY KEY,
    checklist_id VARCHAR(32),
    position INTEGER,
    FOREIGN KEY (id) REFERENCES checks(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE checklists_templates (
    id VARCHAR(32) PRIMARY KEY,
    title TEXT
) WITHOUT ROWID;

CREATE TABLE checklists_templates_entries (
    id VARCHAR(32) PRIMARY KEY,
    template_id VARCHAR(32),
    position INTEGER,
    FOREIGN KEY (id) REFERENCES checks(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE checked_targets (
    id VARCHAR(32) PRIMARY KEY,
    title TEXT
) WITHOUT ROWID;

CREATE TABLE checked_targets_checklists (
    checked_target_id VARCHAR(32),
    checklist_id VARCHAR(32),
    PRIMARY KEY (checked_target_id, checklist_id),
    FOREIGN KEY (checked_target_id) REFERENCES checked_targets(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) WITHOUT ROWID;