import sqlite3
from os.path import exists


class CarDatabase:
    def __init__(self, db_path, overwrite=False):
        if not exists(db_path) and overwrite:
            open(db_path, "w").close()

        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                nationalId TEXT PRIMARY KEY CHECK (LENGTH(nationalId) = 11),
                passHash TEXT NOT NULL CHECK (LENGTH(passHash) = 32),
                fullname TEXT NOT NULL,
                isAdmin INTEGER DEFAULT 0 CHECK (isAdmin = 0 OR isAdmin = 1)
            );
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Cars (
                plate TEXT PRIMARY KEY NOT NULL CHECK (LENGTH(plate) >= 7 AND LENGTH(plate) <= 9),
                occupiedUntil DATE NOT NULL CHECK (occupiedUntil >= '0000-00-00'),
                occupiedTo TEXT,
                dailyPrice REAL NOT NULL,
                productionDate DATE NOT NULL,
                productionName TEXT NOT NULL,
                imageUrl TEXT,
                FOREIGN KEY (occupiedTo) REFERENCES Users(nationalId)
            );
        """)

    def check_user(self, national_id, pass_hash):
        cursor = self.conn.execute("SELECT * FROM Users WHERE nationalId = ? AND passHash = ?",
                                   (national_id, pass_hash))
        return cursor.fetchone()

    def insert_user(self, national_id, pass_hash, fullname, is_admin=0):
        self.conn.execute(
            "INSERT INTO Users (nationalId, passHash, fullname, isAdmin) VALUES (?, ?, ?, ?)",
            (national_id, pass_hash, fullname, is_admin)
        )
        self.conn.commit()

    def insert_car(self, plate, occupied_until, occupied_to, daily_price, production_date, production_name, image_url):
        self.conn.execute(
            "INSERT INTO Cars (plate, occupiedUntil, occupiedTo, dailyPrice, productionDate, productionName, "
            "imageUrl) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (plate, occupied_until, occupied_to, daily_price, production_date, production_name, image_url))
        self.conn.commit()

    def return_car(self, plate):
        self.conn.execute("UPDATE Cars SET occupiedUntil = '0000-00-00', occupiedTo = NULL WHERE plate = ?", (plate,))
        self.conn.commit()

    def remove_user(self, national_id):
        self.conn.execute("DELETE FROM Users WHERE nationalId = ?", (national_id,))
        self.conn.commit()

    def remove_car(self, plate):
        self.conn.execute("DELETE FROM Cars WHERE plate = ?", (plate,))
        self.conn.commit()
    
    def check_car(self, plate):
        cursor = self.conn.execute("SELECT * FROM Cars WHERE plate = ?" , (plate,))
        return cursor.fetchone()

    def fetch_best_car_for_rent(self):
        cursor = self.conn.execute(
            "SELECT * FROM Cars WHERE occupiedUntil <= CURRENT_DATE ORDER BY productionDate DESC, dailyPrice ASC "
            "LIMIT 1")
        return cursor.fetchone()

    def fetch_cars(self):
        cursor = self.conn.execute("SELECT * FROM Cars")
        return cursor.fetchall()

    def assign_car_to_user(self, plate, end_date, national_id):
        self.conn.execute("UPDATE Cars SET occupiedUntil = ?, occupiedTo = ? WHERE plate = ?",(end_date, national_id, plate))
        self.conn.commit()

    def close(self):
        self.conn.close()
