import base64
from io import BytesIO

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
        self.grid_columnconfigure(1, weight=1)  # Allow the second column (view_frame) to expand

        dark_color = "#1a1a1a"

        # Create the menu frame
        self.menu_frame = customtkinter.CTkFrame(self, height=720, fg_color=dark_color)
        self.menu_frame.grid_columnconfigure(0, weight=0)
        self.menu_frame.grid_rowconfigure(0, weight=0)  # Allow the menu_frame to expand vertically
        self.menu_frame.grid(row=0, column=0, sticky="news")

        self.create_menu()

        # Create view frame
        self.view_frame = customtkinter.CTkScrollableFrame(self, height=720)
        self.view_frame.grid_columnconfigure(0, weight=1)  # Allow the view_frame to expand horizontally
        self.view_frame.grid_rowconfigure(0, weight=1)  # Allow the view_frame to expand vertically
        self.view_frame.grid(row=0, column=1, sticky="news")

        self.show_view()

    def create_menu(self):
        # Create the logo label
        image = customtkinter.CTkImage(self.logo, size=(150, 150))
        self.logo_label = customtkinter.CTkLabel(self.menu_frame, image=image, text=None, width=150)
        self.logo_label.grid(row=1, column=0, pady=25, padx=25)

        # Create the menu label
        self.menu_label = customtkinter.CTkLabel(self.menu_frame, width=175, height=55, corner_radius=0, text="RENTACAR\nDATABASE", fg_color="#7c0000", text_color="white", font=("Verdana", 15, "bold"))
        self.menu_label.grid(row=2, column=0, pady=20, padx=0,  sticky="ew")

        def on_menu_button_click(buttons, active_index):
            print(self.winfo_width(), self.winfo_height())
            # reset the view frame
            for widget in self.view_frame.grid_slaves():
                widget.grid_forget()

            for index in range(len(buttons)):
                if index == active_index:
                    buttons[index].configure(fg_color="#7c0000")
                else:
                    buttons[index].configure(fg_color="transparent")

            # show the view
            if active_index == 0:
                self.show_view()

        # Create the menu buttons
        self.menu_buttons = [
            customtkinter.CTkButton(self.menu_frame, text="VIEW", corner_radius=0, command=lambda: on_menu_button_click(self.menu_buttons, 0)),
            customtkinter.CTkButton(self.menu_frame, text="MODIFY", corner_radius=0, fg_color="transparent", command=lambda: on_menu_button_click(self.menu_buttons, 1)),
        ]
        for i, button in enumerate(self.menu_buttons):
            button.grid(row=i+3, column=0, pady=5, padx=0, sticky="e")
        pass

    def show_view(self):
        self.view_frame.rowconfigure(0, minsize=75)

        # Get all available cars from the database
        available_cars_tuples = self.db.fetch_all_available_cars()

        # Convert each tuple to a dictionary
        available_cars = [dict(
            zip(["plate", "occupied_until", "occupied_to", "daily_price", "production_date", "production_name",
                 "image_url"], car)) for car in available_cars_tuples]

        # Create labels to display car information
        header_labels = ["Plate", "Occupied Until", "Occupied To", "Daily Price", "Year", "Brand", "Image"]
        for col, header in enumerate(header_labels):
            label = customtkinter.CTkLabel(self.view_frame, text=header, bg_color="#7c0000", font=("Rubik", 18, "bold"))
            label.grid(row=0, column=col, padx=10, pady=10, sticky="news")

        # Display each available car's information
        for row, car in enumerate(available_cars, start=1):
            plate_label = customtkinter.CTkLabel(self.view_frame, text=car['plate'], font=("Default", 13))
            plate_label.grid(row=row, column=0, padx=15, pady=15)

            occupied_until_label = customtkinter.CTkLabel(self.view_frame, text=car['occupied_until'],
                                                          font=("Default", 13))
            occupied_until_label.grid(row=row, column=1, padx=15, pady=15)

            occupied_to_label = customtkinter.CTkLabel(self.view_frame, text=car['occupied_to'],
                                                       font=("Default", 13))
            occupied_to_label.grid(row=row, column=2, padx=15, pady=15)

            daily_price_label = customtkinter.CTkLabel(self.view_frame, text=f"{car['daily_price']} TL",
                                                       font=("Default", 13))
            daily_price_label.grid(row=row, column=3, padx=15, pady=15)

            production_date_label = customtkinter.CTkLabel(self.view_frame, text=car['production_date'],
                                                           font=("Default", 13))
            production_date_label.grid(row=row, column=4, padx=15, pady=15)

            production_name_label = customtkinter.CTkLabel(self.view_frame, text=car['production_name'],
                                                           font=("Default", 13))
            production_name_label.grid(row=row, column=5, padx=15, pady=15)

            # Assuming you have stored images as base64 strings in the database
            image_data = base64.b64decode(car['image_url'])
            image_pil = Image.open(BytesIO(image_data))
            image_button = customtkinter.CTkImage(light_image=image_pil, size=(280, 150))
            image_label = customtkinter.CTkLabel(self.view_frame, image=image_button, text=None)
            image_label.grid(row=row, column=6, padx=10, pady=10)