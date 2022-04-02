DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS hoursPlayed;
DROP TABLE IF EXISTS purchaseInfo;

PRAGMA foreign_keys = ON;

CREATE TABLE games (
    gid INTEGER,
    name VARCHAR,
    storelink VARCHAR,
    PRIMARY KEY (gid)
);

CREATE TABLE hoursPlayed (
    gid INTEGER,
    hours REAL,
    PRIMARY KEY (gid),
    FOREIGN KEY (gid) REFERENCES games
);

CREATE TABLE purchaseInfo (
    gid INTEGER,
    retailer VARCHAR,
    fullPrice REAL,
    purchasePrice REAL,
    isBundle BOOLEAN,
    system VARCHAR,
    purchaseDate DATE,
    PRIMARY KEY (gid),
    FOREIGN KEY (gid) REFERENCES games
);
