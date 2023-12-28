# Car Rental
## Tables

### Users

```sqlite
CREATE TABLE IF NOT EXISTS Users (
    nationalId TEXT PRIMARY KEY CHECK (LENGTH(nationalId) = 11),
    passHash TEXT NOT NULL CHECK (LENGTH(passHash) = 32),
    fullname TEXT NOT NULL
);
```

### Cars

``` sqlite
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
```