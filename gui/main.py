import base64
import time
import tkinter
from datetime import datetime
from io import BytesIO
from tkinter import messagebox, filedialog
from tkinter.constants import BOTH

import customtkinter
from PIL import Image, ImageDraw

from db import CarDatabase


class MainApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase, logo: Image):
        super().__init__()
        self.menu_buttons = None
        self.logo_label = None

        self.db, self.logo = db, logo
        self.geometry("1250x700")
        self.title("RENTACAR - SYSTEM")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)  # Allow the second column (view_frame) to expand

        dark_color = "#1a1a1a"

        # Create the menu frame
        self.menu_frame = customtkinter.CTkFrame(self, height=720, fg_color=dark_color)
        self.menu_frame.grid_columnconfigure(0, weight=0)
        self.menu_frame.grid_rowconfigure(0, weight=0)  # Allow the menu_frame to expand vertically
        self.menu_frame.pack(fill="y", side="left")

        self.create_menu()

        # Create view frame
        self.view_frame = customtkinter.CTkFrame(self, height=720, fg_color=dark_color)
        self.view_frame.grid_columnconfigure(0, weight=1)  # Allow the view_frame to expand horizontally
        self.view_frame.grid_rowconfigure(0, weight=1)  # Allow the view_frame to expand vertically
        self.view_frame.pack(fill="both", expand=True, side="right", padx=10, pady=10)

        self.show_cars()

    def create_menu(self):
        # Create the logo label
        image = customtkinter.CTkImage(self.logo, size=(150, 150))
        self.logo_label = customtkinter.CTkLabel(self.menu_frame, image=image, text=None, width=150)
        self.logo_label.grid(row=1, column=0, pady=25, padx=25)

        # Create the menu label
        self.menu_label = customtkinter.CTkLabel(self.menu_frame, width=175, height=55, corner_radius=0,
                                                 text="RENTACAR\nDATABASE", fg_color="#7c0000", text_color="white",
                                                 font=("Verdana", 15, "bold"))
        self.menu_label.grid(row=2, column=0, pady=20, padx=0, sticky="ew")

        def on_menu_button_click(buttons, active_index):
            # reset the view frame
            for widget in self.view_frame.grid_slaves():
                widget.grid_forget()
            for widget in self.view_frame.pack_slaves():
                widget.pack_forget()

            for index in range(len(buttons)):
                if index == active_index:
                    buttons[index].configure(fg_color="#7c0000")
                else:
                    buttons[index].configure(fg_color="transparent")

            # show the view
            if active_index == 0:
                self.show_cars()
            elif active_index == 1:
                self.show_users()

        # Create the menu buttons
        self.menu_buttons = [
            customtkinter.CTkButton(self.menu_frame, text="CARS", corner_radius=0,
                                    command=lambda: on_menu_button_click(self.menu_buttons, 0)),
            customtkinter.CTkButton(self.menu_frame, text="USERS", corner_radius=0, fg_color="transparent",
                                    command=lambda: on_menu_button_click(self.menu_buttons, 1)),
        ]
        for i, button in enumerate(self.menu_buttons):
            button.grid(row=i + 3, column=0, pady=5, padx=0, sticky="e")
        pass

    @staticmethod
    def round_image(image_pil, border_radius=20, border_width=5, border_color=(0, 0, 0)):
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

    def view_rent_menu(self, car):
        # check if the car availability date is in the past
        if car['occupied_until'] != "0000-00-00":
            availability_date = datetime.strptime(car['occupied_until'], "%Y-%m-%d")
            if availability_date > datetime.now(availability_date.tzinfo):
                # show an error message
                messagebox.showerror("Error", "This car is not available for rent.")
                return

        # show inputs for the renter's national id and the rent date
        input_window = customtkinter.CTkToplevel(self, width=400, height=200)
        input_window.title("Rent")
        input_window.resizable(False, False)

        # center the window
        input_window.update_idletasks()
        input_window.geometry(f"+{self.winfo_x() + self.winfo_width() // 2 - input_window.winfo_width() // 2}+"
                              f"{self.winfo_y() + self.winfo_height() // 2 - input_window.winfo_height() // 2}")

        # create the input frame
        input_frame = customtkinter.CTkFrame(input_window, fg_color="#3a3a3a")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=1)
        input_frame.grid_rowconfigure(2, weight=1)

        # create the input labels
        national_id_label = customtkinter.CTkLabel(input_frame, text="National ID", text_color="#ff3838",
                                                   font=("Default", 15, "bold"))
        rent_date_label = customtkinter.CTkLabel(input_frame, text="Return Date", text_color="#ff3838",
                                                 font=("Default", 15, "bold"))
        national_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        rent_date_label.grid(row=1, column=0, padx=10, pady=10, sticky="news")

        # create the input entries
        national_id_entry = customtkinter.CTkEntry(input_frame, width=180, placeholder_text="National ID")
        rent_date_entry = customtkinter.CTkEntry(input_frame, width=180, placeholder_text="Return Date (YYYY-MM-DD)")
        national_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="news")
        rent_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="news")

        # create the rent button
        def rent_callback():
            # get the values from the entries
            national_id = national_id_entry.get()
            rent_date = rent_date_entry.get()

            # check if the user exists
            user = self.db.check_user_exists(national_id)
            if user is None:
                messagebox.showerror("Error", "User not found.")
                return

            # check if the rent date is valid
            try:
                datetime.strptime(rent_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid rent date.")
                return

            # check if date is in the past
            if datetime.strptime(rent_date, "%Y-%m-%d") < datetime.now():
                messagebox.showerror("Error", "Rent date cannot be in the past.")
                return

            # rent the car
            self.db.assign_car_to_user(car['plate'], rent_date, national_id)
            messagebox.showinfo("Success", "Car rented successfully.")
            input_window.destroy()
            self.show_cars()

        rent_button = customtkinter.CTkButton(input_frame, text="Rent", command=rent_callback)
        rent_button.grid(row=2, column=1, padx=10, pady=10, sticky="news")

        # show the input frame
        input_frame.pack(fill="both", expand=True)

    def view_delete_menu(self, car):
        # delete the car from the database
        self.db.remove_car(car['plate'])
        messagebox.showinfo("Success", "Car deleted successfully.")
        self.show_cars()

    def view_return_menu(self, car):
        # set car availability date to default
        self.db.return_car(car['plate'])
        messagebox.showinfo("Success", "Car returned successfully.")
        self.show_cars()

    def create_cars_frame(self, master, available_cars, height=400):
        # frame to show the list of available cars
        frame = customtkinter.CTkScrollableFrame(master, fg_color="#1a1a1a", height=height, corner_radius=5)

        # set the column weights
        for i in range(7):
            frame.columnconfigure(i, weight=1)
        frame.columnconfigure(7, weight=0)

        # create the header labels
        header_labels = ["Plate", "Availability Date", "Driver ID", "Price", "Year", "Brand", "Picture", "Actions"]
        for col, header in enumerate(header_labels):
            label = customtkinter.CTkLabel(frame, text=header, text_color="#ff3838", font=("Default", 15, "bold"))
            label.grid(row=0, pady=15, column=col)

        # callbacks for the actions
        callbacks = []
        for car in available_cars:
            def action_callback(choice, _car=car):
                if choice == "Actions":
                    return

                print("dropdown clicked:", choice)
                print("plate:", _car['plate'])

                if choice == "Rent":
                    self.view_rent_menu(_car)
                elif choice == "Return":
                    self.view_return_menu(_car)
                elif choice == "Remove":
                    self.view_delete_menu(_car)

            callbacks.append(action_callback)

        # display cars
        all_decoded_cars = []
        for row, car in enumerate(available_cars, start=1):
            # show plate
            plate_label = customtkinter.CTkLabel(frame, fg_color="#3c3c3c", text=car['plate'].upper().replace("-", " "),
                                                 font=("Consolas", 13, "bold"))
            plate_label.grid(row=row, column=0)

            # show available date
            availability_date = "Available" if car['occupied_until'] == "0000-00-00" else car['occupied_until']
            occupation_color = "#32ff7e" if car['occupied_until'] == "0000-00-00" else None
            occupied_until_label = customtkinter.CTkLabel(
                frame, text=availability_date, text_color=occupation_color, font=("Default", 13, "bold"))
            occupied_until_label.grid(row=row, padx=50, column=1)

            # show driver
            driver = "None" if car['occupied_to'] is None else car['occupied_to']
            boldness = "normal" if car['occupied_to'] is None else "bold"
            occupied_to_label = customtkinter.CTkLabel(frame, text=driver, font=("Default", 13, boldness))
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
            image_pil = Image.open(BytesIO(base64.urlsafe_b64decode(car['image_url'])))

            # add rounding to the image
            output = self.round_image(image_pil, border_radius=10, border_width=15, border_color=(255, 255, 255))
            image_button = customtkinter.CTkImage(light_image=output, size=(100, 75))
            image_label = customtkinter.CTkLabel(frame, image=image_button, corner_radius=50, text=None)
            image_label.grid(row=row, column=6, pady=5, sticky="news")

            # deserialize the car
            decoded_car = dict(zip(["plate", "occupied_until", "occupied_to", "daily_price", "production_date",
                                    "production_name", "image_url"], car.values()))
            all_decoded_cars.append(decoded_car)

            # show actions
            combobox = customtkinter.CTkOptionMenu(
                frame,
                values=["Actions", "Rent", "Return", "Remove"],
                command=callbacks[row - 1],
                width=100,
                fg_color="#ff3030",
                text_color="white",
                dynamic_resizing=False
            )
            combobox.grid(row=row, column=7, padx=10, sticky="e")

        return frame

    def show_cars(self):
        # Get all available cars from the database
        available_cars_tuples = self.db.fetch_cars()

        # Convert each tuple to a dictionary
        available_cars = [dict(
            zip(["plate", "occupied_until", "occupied_to", "daily_price", "production_date", "production_name",
                 "image_url"], car)) for car in available_cars_tuples]

        # reset the view frame
        for widget in self.view_frame.grid_slaves():
            widget.grid_forget()
        for widget in self.view_frame.pack_slaves():
            widget.pack_forget()

        # create table frame
        table_frame = self.create_cars_frame(self.view_frame, available_cars)
        table_frame.pack(fill="both", pady=10, expand=True)

        # create the add car button
        def add_car_callback():
            # create a new window
            add_car_window = customtkinter.CTkToplevel(self, width=400, height=500)
            add_car_window.title("Add Car")
            add_car_window.resizable(False, False)

            # center the window
            add_car_window.update_idletasks()
            add_car_window.geometry(f"+{self.winfo_x() + self.winfo_width() // 2 - add_car_window.winfo_width() // 2}+"
                                    f"{self.winfo_y() + self.winfo_height() // 2 - add_car_window.winfo_height() // 2}")

            # create the input frame
            input_frame = customtkinter.CTkFrame(add_car_window, fg_color="#3a3a3a")
            input_frame.grid_columnconfigure(0, weight=1)
            input_frame.grid_columnconfigure(1, weight=1)
            input_frame.grid_rowconfigure(0, weight=1)
            input_frame.grid_rowconfigure(1, weight=1)
            input_frame.grid_rowconfigure(2, weight=1)
            input_frame.grid_rowconfigure(3, weight=1)
            input_frame.grid_rowconfigure(4, weight=1)

            # create the input labels
            plate_label = customtkinter.CTkLabel(input_frame, text="Plate", text_color="#ff3838",
                                                 font=("Default", 15, "bold"))
            daily_price_label = customtkinter.CTkLabel(input_frame, text="Daily Price", text_color="#ff3838",
                                                       font=("Default", 15, "bold"))
            production_date_label = customtkinter.CTkLabel(input_frame, text="Production Date", text_color="#ff3838",
                                                           font=("Default", 15, "bold"))
            production_name_label = customtkinter.CTkLabel(input_frame, text="Production Name", text_color="#ff3838",
                                                           font=("Default", 15, "bold"))
            image_label = customtkinter.CTkLabel(input_frame, text="Image File", text_color="#ff3838",
                                                 font=("Default", 15, "bold"))
            plate_label.grid(row=0, column=0, padx=10, pady=10, sticky="news")
            daily_price_label.grid(row=1, column=0, padx=10, pady=10, sticky="news")
            production_date_label.grid(row=2, column=0, padx=10, pady=10, sticky="news")
            production_name_label.grid(row=3, column=0, padx=10, pady=10, sticky="news")
            image_label.grid(row=4, column=0, padx=10, pady=10, sticky="news")

            def on_select_image():
                # open a file dialog
                file_path = filedialog.askopenfilename(parent=add_car_window, title="Select Image",
                                                       filetypes=[("Image Files", "*.png *.jpg, *.jpeg")])
                if file_path == "":
                    return

                # set the image url
                image_entry_var.set(file_path)

            # create the input entries
            plate_entry = customtkinter.CTkEntry(input_frame, width=180, placeholder_text="Plate")
            daily_price_entry = customtkinter.CTkEntry(input_frame, width=180, placeholder_text="Daily Price")
            production_date_entry = customtkinter.CTkEntry(input_frame, width=180,
                                                           placeholder_text="Production (YYYY-MM-DD)")
            production_name_entry = customtkinter.CTkEntry(input_frame, width=180, placeholder_text="Name")
            image_entry_var = customtkinter.StringVar()
            image_entry = customtkinter.CTkEntry(input_frame, width=180, placeholder_text="Image URL",
                                                 textvariable=image_entry_var)
            select_image_button = customtkinter.CTkButton(input_frame, text="Select Image", command=on_select_image)

            # place the input entries
            plate_entry.grid(row=0, column=1, padx=10, pady=10, sticky="news")
            daily_price_entry.grid(row=1, column=1, padx=10, pady=10, sticky="news")
            production_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="news")
            production_name_entry.grid(row=3, column=1, padx=10, pady=10, sticky="news")
            image_entry.grid(row=4, column=1, padx=10, pady=10, sticky="news")
            select_image_button.grid(row=5, column=1, padx=10, pady=10, sticky="news")

            # create the add button
            def add_callback():
                # focus
                add_car_window.focus()

                # get the values from the entries
                plate = plate_entry.get()
                occupied_until = "0000-00-00"
                daily_price = daily_price_entry.get()
                production_date = production_date_entry.get()
                production_name = production_name_entry.get()
                image_url = image_entry.get()

                # check if the plate is valid
                if len(plate) < 7 or len(plate) > 9:
                    messagebox.showerror(parent=add_car_window, title="Error", message="Invalid plate.")
                    return

                # check if the daily price is valid
                try:
                    float(daily_price)
                except ValueError:
                    messagebox.showerror(parent=add_car_window, title="Error", message="Invalid price.")
                    return

                # check if the production date is valid
                try:
                    datetime.strptime(production_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(parent=add_car_window, title="Error", message="Invalid production date.")
                    return

                # read the image and convert it to base64
                try:
                    image = Image.open(image_url)
                    image = image.resize((100, 75))
                    image = image.convert("RGB")
                    buffered = BytesIO()
                    image.save(buffered, format="JPEG")
                    image_url = base64.b64encode(buffered.getvalue()).decode()
                except Exception as e:
                    print(e)
                    messagebox.showerror(parent=add_car_window, title="Error", message="Unable to read image.")
                    return

                # add the car
                self.db.insert_car(plate, occupied_until, None, daily_price, production_date, production_name,
                                   image_url)
                messagebox.showinfo(parent=add_car_window, title="Success", message="Car added successfully.")
                add_car_window.destroy()
                self.show_cars()

            # create the add button
            add_button = customtkinter.CTkButton(input_frame, text="Add", command=add_callback)
            add_button.grid(row=7, column=1, padx=10, pady=10, sticky="news")

            # show input frame
            input_frame.pack(fill="both", expand=True)

        # add button frame
        add_button_frame = customtkinter.CTkFrame(self.view_frame, fg_color="#1a1a1a")
        add_car_button = customtkinter.CTkButton(add_button_frame, text="Add Car", command=add_car_callback)
        add_button_frame.pack(fill="x", side="bottom")
        add_car_button.pack(padx=10, pady=10, fill="x", side="bottom")

    def show_users(self):
        # Get all users from the database
        users = self.db.fetch_users()

        # reset the view frame
        for widget in self.view_frame.grid_slaves():
            widget.grid_forget()
        for widget in self.view_frame.pack_slaves():
            widget.pack_forget()

        # deserialize the users
        users = [dict(zip(["nationalId", "passHash", "fullname", "isAdmin"], user)) for user in users]

        # create table frame
        table_frame = self.create_users_frame(self.view_frame, users)
        table_frame.pack(fill="both", expand=True)

    def create_users_frame(self, view_frame, users):
        # frame to show the list of users
        frame = customtkinter.CTkScrollableFrame(view_frame, fg_color="#1a1a1a", height=400, corner_radius=5)

        # set the column weights
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        frame.columnconfigure(4, weight=0)
        frame.columnconfigure(5, weight=0)

        # create the header labels
        header_labels = ["National ID", "Full Name", "Role", "Picture", "Actions"]
        for col, header in enumerate(header_labels):
            label = customtkinter.CTkLabel(frame, text=header, text_color="#ff3838", font=("Default", 15, "bold"))
            label.grid(row=0, pady=15, column=col)

        # load the user images
        user_image = Image.open("assets/user.png")
        admin_image = Image.open("assets/admin.png")

        # callbacks for the actions
        callbacks = []
        for user in users:
            def action_callback(choice, _user=user):
                if choice == "Actions":
                    return

                print("dropdown clicked:", choice)
                print("national id:", _user['nationalId'])

                if choice == "Remove":
                    self.db.remove_user(_user['nationalId'])
                    messagebox.showinfo("Success", "User deleted successfully.")
                    self.show_users()
                elif choice == "Set As Admin":
                    self.db.set_user_admin(_user['nationalId'], 1)
                    messagebox.showinfo("Success", "User is now an admin.")
                    self.show_users()
                elif choice == "Revoke Admin":
                    self.db.set_user_admin(_user['nationalId'], 0)
                    messagebox.showinfo("Success", "User is no longer an admin.")
                    self.show_users()

            callbacks.append(action_callback)

        # display users
        for row, user in enumerate(users, start=1):
            # show national id
            national_id_label = customtkinter.CTkLabel(frame, fg_color="#3c3c3c", text=user['nationalId'],
                                                       font=("Consolas", 13, "bold"))
            national_id_label.grid(row=row, column=0)

            # show full name
            fullname_label = customtkinter.CTkLabel(frame, text=user['fullname'], font=("Default", 13))
            fullname_label.grid(row=row, column=1)

            # show is admin
            is_admin_text = "Admin" if user['isAdmin'] == 1 else "User"
            is_admin_color = "#32ff7e" if user['isAdmin'] == 1 else None
            is_admin_boldness = "bold" if user['isAdmin'] == 1 else "normal"
            is_admin_label = customtkinter.CTkLabel(frame, text=is_admin_text, text_color=is_admin_color,
                                                    font=("Default", 13, is_admin_boldness))
            is_admin_label.grid(row=row, column=2)

            # show user image
            image = user_image if user['isAdmin'] == 0 else admin_image
            image = customtkinter.CTkImage(light_image=image, size=(64, 64))
            image_label = customtkinter.CTkLabel(frame, image=image, corner_radius=50, text=None)
            image_label.grid(row=row, column=3, pady=5, sticky="news")

            # show actions
            combobox = customtkinter.CTkOptionMenu(
                frame,
                values=["Actions", "Remove", "Set As Admin", "Revoke Admin"],
                command=lambda choice, _user=user: action_callback(choice, _user),
                width=100,
                fg_color="#ff3030",
                text_color="white",
                dynamic_resizing=False
            )
            combobox.grid(row=row, column=4, padx=10, sticky="e")

        return frame
