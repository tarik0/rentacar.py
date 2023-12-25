import customtkinter
from PIL import Image

from db import CarDatabase
from gui.login import LoginApp
from gui.test import MainApp

if __name__ == '__main__':
    # set appearance mode to dark
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("./assets/theme.json")

    # create the database
    db = CarDatabase("rentacar.db", overwrite=True)

    # load logo
    logo = Image.open("assets/logo.png")

    def on_login_success():
        print("Login success")

        # start main
        _app = MainApp(db=db, logo=logo)
        _app.mainloop()

    # start login
    #app = LoginApp(db=db, logo=logo, on_success=on_login_success)
    #app.mainloop()

    # todo: remove this
    on_login_success()


