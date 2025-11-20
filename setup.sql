DROP TABLE IF EXISTS Compte;

CREATE TABLE Compte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    
    UNIQUE(username)
);

INSERT INTO Compte (username,password) VALUES ('test','1234')