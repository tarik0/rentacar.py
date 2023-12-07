import sqlite3


class CarDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                nationalId TEXT PRIMARY KEY CHECK (LENGTH(nationalId) = 11),
                fullname TEXT NOT NULL
            );
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS Cars (
                plate TEXT PRIMARY KEY NOT NULL CHECK (LENGTH(plate) >= 7 AND LENGTH(plate) <= 9),
                occupiedUntil DATE NOT NULL CHECK (occupiedUntil >= '0000-00-00'),
                occupiedTo TEXT NOT NULL,
                dailyPrice REAL NOT NULL,
                productionDate DATE NOT NULL,
                productionName TEXT NOT NULL,
                imageUrl TEXT,
                FOREIGN KEY (occupiedTo) REFERENCES Users(nationalId)
            );
        """)

    def insert_user(self, national_id, fullname):
        self.conn.execute("INSERT INTO Users (nationalId, fullname) VALUES (?, ?)", (national_id, fullname))
        self.conn.commit()

    def insert_car(self, plate, occupied_until, occupied_to, daily_price, production_date, production_name, image_url):
        self.conn.execute(
            "INSERT INTO Cars (plate, occupiedUntil, occupiedTo, dailyPrice, productionDate, productionName, "
            "imageUrl) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (plate, occupied_until, occupied_to, daily_price, production_date, production_name, image_url))
        self.conn.commit()

    def remove_user(self, national_id):
        self.conn.execute("DELETE FROM Users WHERE nationalId = ?", (national_id,))
        self.conn.commit()

    def remove_car(self, plate):
        self.conn.execute("DELETE FROM Cars WHERE plate = ?", (plate,))
        self.conn.commit()

    def fetch_best_car_for_rent(self):
        cursor = self.conn.execute(
            "SELECT * FROM Cars WHERE occupiedUntil <= CURRENT_DATE ORDER BY productionDate DESC, dailyPrice ASC "
            "LIMIT 1")
        return cursor.fetchone()

    def fetch_all_available_cars(self):
        cursor = self.conn.execute("SELECT * FROM Cars WHERE occupiedUntil <= CURRENT_DATE")
        return cursor.fetchall()

    def assign_car_to_user(self, plate, end_date, national_id):
        self.conn.execute("UPDATE Cars SET occupiedUntil = ?, occupiedTo = ? WHERE plate = ?",
                          (end_date, national_id, plate))
        self.conn.commit()

    def close(self):
        self.conn.close()
