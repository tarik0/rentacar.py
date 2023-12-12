import customtkinter

from db import CarDatabase
from gui import LoginApp

if __name__ == '__main__':
    # set appearance mode to dark
    customtkinter.set_appearance_mode("dark")

    # create the database
    db = CarDatabase("rentacar.db", overwrite=True)

    # create the app
    app = LoginApp(db=db, on_success=lambda x: app.destroy())
    app.mainloop()
