DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS hoursPlayed;
DROP TABLE IF EXISTS prices;

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS games (
    gid INTEGER,
    name VARCHAR,
    storelink VARCHAR,
    PRIMARY KEY (gid)
);

CREATE TABLE IF NOT EXISTS hoursPlayed (
    gid INTEGER,
    hours REAL,
    PRIMARY KEY (gid),
    FOREIGN KEY (gid) REFERENCES games ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS prices (
    gid INTEGER,
    price REAL,
    PRIMARY KEY (gid),
    FOREIGN KEY (gid) REFERENCES games ON DELETE CASCADE
);

