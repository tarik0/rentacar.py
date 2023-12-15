import customtkinter
from db import CarDatabase
from gui import LoginApp, MainApp



if __name__ == '__main__':
    # set appearance mode to dark
    customtkinter.set_default_color_theme("green")

    # create the database
    db = CarDatabase("rentacar.db", overwrite=True)

     #Start the MainApp class
    app = MainApp(db=db)
    app.mainloop()