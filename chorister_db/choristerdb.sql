/*******************************
Begin by dropping old data:
*******************************/
DROP TABLE IF EXISTS attends;
DROP TABLE IF EXISTS rehearsal;
DROP TABLE IF EXISTS attendancestatus;
DROP TABLE IF EXISTS paymentmonth;
DROP TABLE IF EXISTS month;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS paymentmethod;
DROP TABLE IF EXISTS chorister;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS status;

/******************************
Create Tables
******************************/

CREATE TABLE chorister (
	choristerId TEXT PRIMARY KEY NOT NULL,
	firstName TEXT NOT NULL,
	lastName TEXT NOT NULL,
	street1 TEXT NOT NULL,
	street2 TEXT,
	city TEXT NOT NULL,
	state TEXT NOT NULL,
	zip TEXT NOT NULL,
	email TEXT,
	phone INTEGER,
	sectionId INTEGER NOT NULL,
	statusId INTEGER NOT NULL,
	FOREIGN KEY(sectionId) REFERENCES section(sectionId)
	FOREIGN KEY(statusId) REFERENCES status(statusId)
);

CREATE TABLE section (
	sectionId INTEGER PRIMARY KEY AUTOINCREMENT,
	sectionName TEXT NOT NULL
);

CREATE TABLE status (
	statusId INTEGER PRIMARY KEY AUTOINCREMENT,
	statusName TEXT NOT NULL
);

CREATE TABLE payment (
	paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
	choristerId TEXT NOT NULL,
	methodId INTEGER NOT NULL,
	amount INTEGER NOT NULL,
	FOREIGN KEY(choristerId) REFERENCES chorister(choristerId),
	FOREIGN KEY(methodId) REFERENCES paymentmethod(methodId)
);

CREATE TABLE paymentmethod (
	methodId INTEGER PRIMARY KEY AUTOINCREMENT,
	methodDescription TEXT NOT NULL
);

CREATE TABLE paymentmonth (
	paymentId INTEGER NOT NULL,
	monthId INTEGER NOT NULL,
	FOREIGN KEY(paymentId) REFERENCES payment(paymentId),
	FOREIGN KEY(monthId) REFERENCES month(monthId)
);

CREATE TABLE month (
	monthId INTEGER PRIMARY KEY AUTOINCREMENT,
	month INTEGER NOT NULL,
	year INTEGER NOT NULL
);

CREATE TABLE attends (
	choristerId TEXT NOT NULL,
	rehearsalId INTEGER NOT NULL,
	attendanceId INTEGER NOT NULL,
	FOREIGN KEY(choristerId) REFERENCES chorister(choristerId),
	FOREIGN KEY(rehearsalId) REFERENCES rehearsal(rehearsalId),
	FOREIGN KEY(attendanceId) REFERENCES attendancestatus(attendanceId)
);

CREATE TABLE attendancestatus (
	attendanceId INTEGER PRIMARY KEY AUTOINCREMENT,
	attendanceStatus TEXT NOT NULL
);

CREATE TABLE rehearsal (
	rehearsalId INTEGER PRIMARY KEY AUTOINCREMENT,
	rehearsalDate TEXT NOT NULL
);

/*******************************
Populate validation tables
*******************************/

INSERT INTO section (sectionName) VALUES ('Soprano 1');
INSERT INTO section (sectionName) VALUES ('Soprano 2');
INSERT INTO section (sectionName) VALUES ('Alto 1');
INSERT INTO section (sectionName) VALUES ('Alto 2');
INSERT INTO section (sectionName) VALUES ('Tenor 1');
INSERT INTO section (sectionName) VALUES ('Tenor 2');
INSERT INTO section (sectionName) VALUES ('Bass 1');
INSERT INTO section (sectionName) VALUES ('Bass 2');

INSERT INTO status (statusName) VALUES ('Active');
INSERT INTO status (statusName) VALUES ('Former');
INSERT INTO status (statusName) VALUES ('Prospective');
INSERT INTO status (statusName) VALUES ('On Break');

INSERT INTO paymentmethod (methodDescription) VALUES ('Cash');
INSERT INTO paymentmethod (methodDescription) VALUES ('Check');
INSERT INTO paymentmethod (methodDescription) VALUES ('Venmo');
INSERT INTO paymentmethod (methodDescription) VALUES ('External Donor');
INSERT INTO paymentmethod (methodDescription) VALUES ('Excused');

INSERT INTO attendancestatus (attendanceStatus) VALUES ('Present');
INSERT INTO attendancestatus (attendanceStatus) VALUES ('Absent');
INSERT INTO attendancestatus (attendanceStatus) VALUES ('Notified Absence');

/********************************
Seed month data - examples
********************************/

INSERT INTO month (month, year) VALUES ('8','2024');
INSERT INTO month (month, year) VALUES ('9','2024');
INSERT INTO month (month, year) VALUES ('10','2024');
INSERT INTO month (month, year) VALUES ('11','2024');
INSERT INTO month (month, year) VALUES ('12','2024');
INSERT INTO month (month, year) VALUES ('1','2025');
INSERT INTO month (month, year) VALUES ('2','2025');
INSERT INTO month (month, year) VALUES ('3','2025');
INSERT INTO month (month, year) VALUES ('4','2025');

/********************************
Chorister data and attendance data - fake
********************************/

INSERT INTO chorister (choristerId, firstName, lastName, street1, street2, city, state, zip, email, sectionId, statusId) 
	VALUES ('T0001','John','Smith','1 Main St','Apt 1','Portland','ME','04103','johnsmith@example.com','5','2');

INSERT INTO chorister (choristerId, firstName, lastName, street1, street2, city, state, zip, email, sectionId, statusId) 
	VALUES ('A0001','Janet','Smith','1 Main St','Apt 1','Portland','ME','04103','janetsmith@example.com','3','1');

INSERT INTO chorister (choristerId, firstName, lastName, street1, city, state, zip, email, phone, sectionId, statusId) 
	VALUES ('S0001','Jane','Doe','2 Test Ave','Portland','ME','04103','janedoe@example.com','2075555555','1','1');

INSERT INTO chorister (choristerId, firstName, lastName, street1, city, state, zip, email, phone, sectionId, statusId) 
	VALUES ('T0002','Nat','Test','PO Box 1357','Portland','ME','04103','nat@test.com','2075551234','5','3');

INSERT INTO chorister (choristerId, firstName, lastName, street1, street2, city, state, zip, email, phone, sectionId, statusId) 
	VALUES ('B0001','Larry','Gordon','3 Yard Ln','Unit 7','Westbrook','ME','04092','lgordon@example.com','8025550000','8','2');

INSERT INTO chorister (choristerId, firstName, lastName, street1, city, state, zip, email, phone, sectionId, statusId) 
	VALUES ('S0002','Kristin','Chenowyth','4 Broad Way','Portland','ME','04203','diva@broadway.com','2075552020','1','4');

INSERT INTO chorister (choristerId, firstName, lastName, street1, city, state, zip, sectionId, statusId) 
	VALUES ('T0003','Placido','Domingo','5 Spain Ln','Westbrook','ME','04092','6','1');

INSERT INTO chorister (choristerId, firstName, lastName, street1, street2, city, state, zip, email, phone, sectionId, statusId) 
	VALUES ('B0002','Greg','Smalls','6 Low Rd','Apt 2','Westbrook','ME','04092','smallg@test.com','2075556666','8','1');

INSERT INTO rehearsal (rehearsalDate) VALUES ('8/1/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('8/8/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('8/15/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('8/22/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('8/29/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('9/5/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('9/12/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('9/19/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('9/26/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('10/3/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('10/10/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('10/17/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('10/24/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('10/31/24');
INSERT INTO rehearsal (rehearsalDate) VALUES ('11/7/24');

INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0002','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0001','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0001','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','1','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','2','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0002','2','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','2','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0001','2','3');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','2','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0001','2','2');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','2','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','3','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0002','3','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','3','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0001','3','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','3','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','3','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','4','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0002','4','2');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','4','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0001','4','3');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','4','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','4','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','5','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0002','5','3');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','5','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0001','5','3');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','5','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','5','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','6','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0002','6','2');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','6','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','6','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','6','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('S0001','7','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('A0001','7','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('T0003','7','1');
INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES ('B0002','7','1');

/******************************
Payment Data - fake
******************************/

INSERT INTO payment (choristerId, methodId, amount) VALUES ('T0001','1','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('A0001','1','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('S0001','2','400');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('B0001','1','50');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('S0002','3','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('T0003','4','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('B0002','2','200');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('T0001','2','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('A0001','2','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('S0002','3','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('T0003','4','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('A0001','1','100');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('T0003','5','0');
INSERT INTO payment (choristerId, methodId, amount) VALUES ('B0002','2','100');

INSERT INTO paymentmonth (paymentId, monthId) VALUES ('1','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('2','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('3','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('3','2');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('3','3');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('3','4');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('4','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('5','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('6','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('7','1');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('7','2');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('8','2');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('9','2');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('10','2');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('11','2');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('12','3');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('13','3');
INSERT INTO paymentmonth (paymentId, monthId) VALUES ('14','3');