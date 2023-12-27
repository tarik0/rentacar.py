# SQL Queries

## Create Tables

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

## Insert Row

### Insert New User

```sqlite
INSERT INTO Users (nationalId, passHash, fullname) VALUES ('12345678901', '...', 'John Doe');
```

### Insert New Car

```sqlite
INSERT INTO Cars (plate, occupiedUntil, occupiedTo, dailyPrice, productionDate, productionName, imageUrl) 
VALUES ('ABC1234', '2023-01-01', '12345678901', 100.0, '2020-01-01', 'Model X', 'base64url');
```

## Remove Row

### Remove User

```sqlite
DELETE FROM Users WHERE nationalId = 'nationalId_value';
```

### Remove Car

```sqlite
DELETE FROM Cars WHERE plate = 'plate_value';
```

## Simple Queries

### Fetch The Best Car For Rent (Not Occupied + Young Car + Low Price)

```sqlite
SELECT * FROM Cars
WHERE occupiedUntil <= CURRENT_DATE
ORDER BY productionDate DESC, dailyPrice ASC
LIMIT 1;
```

### Fetch All Available Cars

```sqlite
SELECT * FROM Cars
WHERE occupiedUntil <= CURRENT_DATE;
```

### Assign A Car To An User For Some Period

```sqlite
UPDATE Cars
SET occupiedUntil = 'end_date', occupiedTo = 'nationalId_value'
WHERE plate = 'plate_value';
```