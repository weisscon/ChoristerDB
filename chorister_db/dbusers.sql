/*******************************
Begin by dropping old data:
*******************************/

DROP TABLE IF EXISTS allowed;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS permissions;

/******************************
Create Tables
******************************/

CREATE TABLE account (
	accountId INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
    userset INTEGER NOT NULL
);

CREATE TABLE permissions (
    permissionId INTEGER PRIMARY KEY AUTOINCREMENT,
    permissionDesc TEXT NOT NULL
);

CREATE TABLE allowed (
    accountId INTEGER NOT NULL,
    permissionId INTEGER NOT NULL,
    FOREIGN KEY (accountId) REFERENCES account(accountId),
    FOREIGN KEY (permissionId) REFERENCES permissions(permissionId) 
);

/*******************************
Populate validation tables
*******************************/

INSERT INTO permissions (permissionDesc) VALUES ('DB Admin');
INSERT INTO permissions (permissionDesc) VALUES ('Chorister Admin');
INSERT INTO permissions (permissionDesc) VALUES ('Attendance');
INSERT INTO permissions (permissionDesc) VALUES ('Treasurer');

INSERT INTO account (username, password, userset) VALUES ('admin','scrypt:32768:8:1$BaSGxICnXT51pijn$11b653ffe01d91c8d0da7531831d84addc28002a8f14a6ad51d462fb57fce257f9f9b62f3ca8170a0a94a151d6e58e1d740c10589e2d2d87c17999648b4ac258', '0');

INSERT INTO allowed (accountId, permissionId) VALUES ('1','1');
INSERT INTO allowed (accountId, permissionId) VALUES ('1','2');
INSERT INTO allowed (accountId, permissionId) VALUES ('1','3');
INSERT INTO allowed (accountId, permissionId) VALUES ('1','4');