CREATE TABLE COURSE_OFFERING (
COURSE TEXT NOT NULL,
SESSION TEXT NOT NULL,
PRIMARY KEY (COURSE, SESSION)
);

CREATE TABLE SURVEY (
COURSE TEXT NOT NULL,
SESSION TEXT NOT NULL,
START TIME NOT NULL,
END TIME NOT NULL,
PRIMARY KEY (COURSE, SESSION),
FOREIGN KEY (COURSE, SESSION) REFERENCES COURSE_OFFERING(COURSE, SESSION)
);

CREATE TABLE USER (
ID INTEGER PRIMARY KEY NOT NULL,
PASSWORD TEXT NOT NULL,
ROLE TEXT NOT NULL
);





CREATE TABLE COURSE_OFFERING (
COURSE TEXT NOT NULL,
SESSION TEXT NOT NULL,
PRIMARY KEY (COURSE, SESSION)
);
CREATE TABLE QUESTION (
QUEST TEXT PRIMARY KEY NOT NULL,
MANDATORY INTEGER NOT NULL
);
CREATE TABLE SURVEY (
COURSE TEXT NOT NULL,
SESSION TEXT NOT NULL,
START TIME NOT NULL,
END TIME NOT NULL,
PRIMARY KEY (COURSE, SESSION),
FOREIGN KEY (COURSE, SESSION) REFERENCES COURSE_OFFERING(COURSE, SESSION)
);
CREATE TABLE SURVEY_DATA (
ID INTEGER PRIMARY KEY NOT NULL,
COURSE TEXT NOT NULL,
SESSION TEXT NOT NULL,
QUEST TEXT NOT NULL,
TYPE TEXT NOT NULL,
UNIQUE (COURSE, SESSION, QUEST)
);
CREATE TABLE USER (
ID INTEGER PRIMARY KEY NOT NULL,
PASSWORD TEXT NOT NULL,
ROLE TEXT NOT NULL
);






CREATE TABLE COURSE_OFFERING (
ID INTEGER PRIMARY KEY NOT NULL,
COURSE TEXT NOT NULL,
SESSION TEXT NOT NULL,
SURVEY_ID INTEGER,
UNIQUE (COURSE, SESSION),
FOREIGN KEY (SURVEY_ID) REFERENCES SURVEY(ID)
);
CREATE TABLE QUESTION (
ID INTEGER PRIMARY KEY NOT NULL,
QUEST TEXT NOT NULL,
MANDATORY INTEGER NOT NULL,
STATUS INTEGER NOT NULL,
UNIQUE (QUEST)
);
CREATE TABLE SURVEY (
ID INTEGER PRIMARY KEY NOT NULL,
START TIME,
END TIME
);
CREATE TABLE SURVEY_DATA (
ID INTEGER PRIMARY KEY NOT NULL,
SURVEY_ID INTEGER NOT NULL,
QUESTION_ID INTEGER NOT NULL,
FOREIGN KEY (SURVEY_ID) REFERENCES SURVEY(ID),
FOREIGN KEY (QUESTION_ID) REFERENCES QUESTION(ID)
);
CREATE TABLE USER (
ID INTEGER PRIMARY KEY NOT NULL,
PASSWORD TEXT NOT NULL,
ROLE TEXT NOT NULL
);
CREATE TABLE USER_COURSE (
ID INTEGER PRIMARY KEY NOT NULL,
USER_ID INTEGER NOT NULL,
COURSE_ID INTEGER NOT NULL,
SEEN INTEGER NOT NULL,
FOREIGN KEY (USER_ID) REFERENCES USER(ID),
FOREIGN KEY (COURSE_ID) REFERENCES COURSE_OFFERING(ID)
);
