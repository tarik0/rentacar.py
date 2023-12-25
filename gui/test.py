import base64
from io import BytesIO

import customtkinter
from PIL import Image, ImageDraw, ImageOps, ImageTk

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

    def round_image(self, image_pil, border_radius=20, border_width=5, border_color=(0, 0, 0)):
        # Create a mask for the rounded corners
        mask = Image.new("L", image_pil.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image_pil.size], radius=border_radius, fill=255)

        # Apply the mask to the image
        image_pil.putalpha(mask)

        # Create a new image with a transparent background
        bordered_image = Image.new("RGBA", image_pil.size, (0, 0, 0, 0))

        # Paste the masked image onto the transparent background
        bordered_image.paste(image_pil, (0, 0), image_pil)

        # Add a border with a corner radius
        border_image = Image.new("RGBA", bordered_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(border_image)
        draw.rounded_rectangle([(0, 0), bordered_image.size], radius=border_radius, outline=border_color,
                               width=border_width)

        # Composite the bordered image with the border
        final_image = Image.alpha_composite(border_image, bordered_image)

        return final_image

    def create_table_frame(self, master, available_cars, height=400):
        # frame to show the list of available cars
        frame = customtkinter.CTkScrollableFrame(master, fg_color="#1a1a1a", height=height, corner_radius=5)

        # set the column weights
        for i in range(6):
            frame.columnconfigure(i, weight=1)
        frame.columnconfigure(6, weight=0)

        # create the header labels
        header_labels = ["Plate", "Available Date", "Driver", "Price", "Year", "Brand", "Picture"]
        for col, header in enumerate(header_labels):
            label = customtkinter.CTkLabel(frame, text=header, text_color="#ff3838", font=("Default", 15, "bold"))
            label.grid(row=0, pady=15, column=col)

        # display cars
        for row, car in enumerate(available_cars, start=1):
            # show plate
            plate_label = customtkinter.CTkLabel(frame, text=car['plate'].upper(), font=("Default", 13, "bold"))
            plate_label.grid(row=row, column=0)

            # show available date
            occupied_until_label = customtkinter.CTkLabel(frame, text=car['occupied_until'], font=("Default", 13))
            occupied_until_label.grid(row=row, column=1)

            # show driver
            occupied_to_label = customtkinter.CTkLabel(frame, text=car['occupied_to'], font=("Default", 13))
            occupied_to_label.grid(row=row, column=2)

            # show price
            daily_price_label = customtkinter.CTkLabel(frame, text=f"{car['daily_price']} TL", font=("Default", 13))
            daily_price_label.grid(row=row, column=3)

            # show year
            production_date_label = customtkinter.CTkLabel(frame, text=car['production_date'], font=("Default", 13))
            production_date_label.grid(row=row, column=4)

            # show brand
            production_name_label = customtkinter.CTkLabel(frame, text=car['production_name'], font=("Default", 13))
            production_name_label.grid(row=row, column=5)

            # show image
            image_data = base64.b64decode(car['image_url'])
            image_pil = Image.open(BytesIO(image_data))

            # add rounding to the image
            output = self.round_image(image_pil, border_radius=10, border_width=15, border_color=(255, 255, 255))
            image_button = customtkinter.CTkImage(light_image=output, size=(100, 75))
            image_label = customtkinter.CTkLabel(frame, image=image_button, corner_radius=50, text=None)
            image_label.grid(row=row, column=6, pady=5, sticky="ens")

        return frame



    def show_view(self):
        # Get all available cars from the database
        available_cars_tuples = self.db.fetch_all_available_cars()

        # Convert each tuple to a dictionary
        available_cars = [dict(
            zip(["plate", "occupied_until", "occupied_to", "daily_price", "production_date", "production_name",
                 "image_url"], car)) for car in available_cars_tuples]

        # Create the table frame
        frame = self.create_table_frame(self.view_frame, available_cars)

        frame.grid(row=0, column=0, pady=15, padx=15, sticky="news")