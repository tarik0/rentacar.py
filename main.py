import customtkinter
from PIL import Image

from db import CarDatabase
from gui.login import LoginApp
from gui.test import MainApp

if __name__ == '__main__':
    # set appearance mode to dark
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    # create the database
    db = CarDatabase("rentacar.db", overwrite=True)

    # load logo
    logo = Image.open("./gui/assets/logo.png")

    # start login
    app = LoginApp(db=db, logo=logo)
    app.mainloop()

    # start main
    app = MainApp(db=db, logo=logo)
    app.mainloop()
