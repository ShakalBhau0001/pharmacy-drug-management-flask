CREATE TABLE customer (
            uid TEXT PRIMARY KEY,
            pass_hash TEXT NOT NULL,
            fname TEXT,
            lname TEXT,
            email TEXT,
            address TEXT,
            phno TEXT
        );

CREATE TABLE seller (
            sid TEXT PRIMARY KEY,
            sname TEXT,
            pass_hash TEXT NOT NULL,
            address TEXT,
            phno TEXT
        );

CREATE TABLE product (
            pid TEXT PRIMARY KEY,
            pname TEXT UNIQUE,
            manufacturer TEXT,
            mfg TEXT,
            exp TEXT,
            price INTEGER
        );

CREATE TABLE inventory (
            pid TEXT NOT NULL,
            sid TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            PRIMARY KEY (pid, sid),
            FOREIGN KEY (pid) REFERENCES product (pid) ON DELETE CASCADE,
            FOREIGN KEY (sid) REFERENCES seller (sid) ON DELETE CASCADE
        );

CREATE TABLE orders (
            oid INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT,
            sid TEXT,
            uid TEXT,
            orderdatetime TEXT DEFAULT (datetime('now', 'localtime')),
            quantity INTEGER,
            price INTEGER,
            FOREIGN KEY (pid) REFERENCES product (pid) ON DELETE CASCADE,
            FOREIGN KEY (sid) REFERENCES seller (sid) ON DELETE CASCADE,
            FOREIGN KEY (uid) REFERENCES customer (uid) ON DELETE CASCADE
        );
