
-- add table to store transcript from movies

CREATE TABLE "transcript" (
	"id"	INTEGER,
	"meta"	TEXT,
	"transcript"	TEXT NOT NULL,
	"is_monolog"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
)