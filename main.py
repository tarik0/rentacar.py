import base64
from hashlib import md5
from io import BytesIO
from tkinter import messagebox

import customtkinter
from PIL import Image

from db import CarDatabase
from gui.login import LoginApp
from gui.main import MainApp
import os


def setup_dev_env():
    def img_to_base64(path):
        buff = BytesIO()
        Image.open(path).save(buff, format="JPEG")
        buff.seek(0)
        return base64.b64encode(buff.read()).decode()

    # remove old database
    if os.path.exists("rentacar.db"):
        os.remove("rentacar.db")

    # create the database
    db = CarDatabase("rentacar.db", overwrite=True)

    # insert some users
    pass_hash = md5("123".encode()).hexdigest()
    db.insert_user(
        national_id="12345678900",
        pass_hash=pass_hash,
        fullname="admin",
        is_admin=1
    )
    db.insert_user(
        national_id="12345678901",
        pass_hash=pass_hash,
        fullname="Özgür"
    )
    db.insert_user(
        national_id="12345678902",
        pass_hash=pass_hash,
        fullname="Sabri"
    )
    db.insert_user(
        national_id="12345678903",
        pass_hash=pass_hash,
        fullname="Tayfun"
    )
    db.insert_user(
        national_id="12345678904",
        pass_hash=pass_hash,
        fullname="Ganyotçu"
    )
    db.insert_user(
        national_id="12345678905",
        pass_hash=pass_hash,
        fullname="Şahin"
    )

    # insert some cars
    db.insert_car(
        plate="06AG5825",
        occupied_until="0000-00-00",
        occupied_to=None,
        daily_price=500,
        production_date="1997-01-01",
        production_name="BMW 320i",
        image_url=img_to_base64("assets/cars/e36.jpg")
    )
    db.insert_car(
        plate="06COY110",
        occupied_until="0000-00-00",
        occupied_to=None,
        daily_price=250,
        production_date="1997-05-08",
        production_name="Hyundai Accent",
        image_url=img_to_base64("assets/cars/accent.jpg")
    )
    db.insert_car(
        plate="06AC600",
        occupied_until="0000-00-00",
        occupied_to=None,
        daily_price=700,
        production_date="1995-02-10",
        production_name="Mercedes S500",
        image_url=img_to_base64("assets/cars/s600.jpg")
    )
    db.insert_car(
        plate="06TRK06",
        occupied_until="0000-00-00",
        occupied_to=None,
        daily_price=350,
        production_date="2020-07-10",
        production_name="Fiat Egea",
        image_url=img_to_base64("assets/cars/egea.jpg")
    )
    db.insert_car(
        plate="34TK053",
        occupied_until="0000-00-00",
        occupied_to=None,
        daily_price=650,
        production_date="1998-10-22",
        production_name="BMW 740iL",
        image_url=img_to_base64("assets/cars/e38.jpg")
    )

    # assign some cars to users
    db.assign_car_to_user(
        plate="06AG5825",
        end_date="2025-10-10",
        national_id="12345678900"
    )

    messagebox.showinfo("Dev setup", f"Development environment setup complete.\n\nUser: 12345678900\nPassword: 123")


if __name__ == '__main__':
    # set appearance mode to dark
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("./assets/theme.json")

    # Dev setup
    setup_dev_env()

    # create the database
    db = CarDatabase("rentacar.db", overwrite=True)

    # load logo
    logo = Image.open("assets/logo.png")

    def on_login_success(info):
        print("Login success", info)

        # start main
        _app = MainApp(db=db, logo=logo)
        _app.mainloop()


    # start login
    app = LoginApp(db=db, logo=logo, on_success=on_login_success)
    app.mainloop()
