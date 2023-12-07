from db import CarDatabase

if __name__ == '__main__':

    db = CarDatabase("rentacar.db")
    db.insert_car("06AG5825", 100, 100, 100, 100, 100, None)


    print(db.fetch_all_available_cars())