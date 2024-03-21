import sqlite3


def initialize():
    database = 'grocery.db'
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user(id INTEGER,Username TEXT,Password TEXT,Cart TEXT DEFAULT '')")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admin(id INTEGER,Username TEXT,Password TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS category(id INTEGER,Name TEXT,image TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS product(id INTEGER,Name TEXT,ManufactureDate TEXT,ExpiryDate TEXT,Categoryid INTEGER,rate INTEGER,image TEXT,cart INTEGER,quantity INTEGER,unit TEXT)")
    cur.execute("SELECT COUNT(*) FROM admin")
    result = cur.execute("SELECT COUNT(*) FROM admin").fetchone()[0]
    if result == 0:
        cur.execute(
            "INSERT INTO admin(id, Username, Password) VALUES (1, 'Admin1', '123')")
        conn.commit()
    cur.close()
    conn.close()
