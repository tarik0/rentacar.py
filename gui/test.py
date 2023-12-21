import customtkinter
from PIL import Image
from db import CarDatabase


class MainApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase, logo: Image):
        super().__init__()
        self.logo_label = None

        self.db, self.logo = db, logo
        self.geometry("1250x720")
        self.title("RENTACAR - SYSTEM")
        self.resizable(False, False)

        dark_color = "#1a1a1a"

        # Create the menu frame
        self.menu_frame = customtkinter.CTkFrame(self, height=720, fg_color=dark_color)
        self.menu_frame.grid(row=0, column=0, sticky="ns")

        self.create_menu()

        # Create view frame
        self.view_frame = customtkinter.CTkFrame(self, width=1050, height=720)
        self.view_frame.grid(row=0, column=1, sticky="ew")

    def create_menu(self):
        # Create the logo label
        image = customtkinter.CTkImage(self.logo, size=(150, 150))
        self.logo_label = customtkinter.CTkLabel(self.menu_frame, image=image, text=None, width=150)
        self.logo_label.grid(row=1, column=0, pady=25, padx=25)

        # Create the menu label
        self.menu_label = customtkinter.CTkLabel(self.menu_frame, text="Menu", font=("Verdana", 20, "bold"))
        self.menu_label.grid(row=2, column=0, pady=25, padx=25)

        # Create the menu buttons
        self.menu_buttons = [
            customtkinter.CTkButton(self.menu_frame, text="Add Car"),
            customtkinter.CTkButton(self.menu_frame, text="Remove Car"),
            customtkinter.CTkButton(self.menu_frame, text="List Cars"),
        ]
        for i, button in enumerate(self.menu_buttons):
            button.grid(row=i+3, column=0, pady=10, padx=25, sticky="ew")
        pass
