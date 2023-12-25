from hashlib import md5
from tkinter import messagebox, filedialog
import customtkinter
from PIL import Image
import base64
from io import BytesIO
from db import CarDatabase


class MainApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase, logo: Image):
        super().__init__()
        self.db = db
        self.geometry("1250x720")
        self.title("RENTACAR - SYSTEM")

        # Import logo and center
        self.logo = customtkinter.CTkImage(
            logo,
            size=(150, 150),
        )

        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text=None)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add Car Button
        self.add_car_button = customtkinter.CTkButton(self, text="Add New Car", command=self.add_car, width=150)
        self.add_car_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Remove Car Button
        self.remove_car_button = customtkinter.CTkButton(self, text="Remove Existing Car", command=self.remove_car, width=150)
        self.remove_car_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Check Avaliable Carss Button
        self.check_cars_button = customtkinter.CTkButton(self, text="Show All Avalible Cars",
                                                         command=self.show_all_available_cars, width=150)
        self.check_cars_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    def add_car(self):
        # To stop the other buttons
        self.remove_car_button.configure(state=customtkinter.DISABLED)

        self.plate_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Plate")
        self.plate_ent.grid(row=5, column=3)

        self.occupiedUntil_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Occupied Until")
        self.occupiedUntil_ent.grid(row=5, column=4)

        self.occupiedTo_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Occupied To")
        self.occupiedTo_ent.grid(row=5, column=5)

        self.dailyPrice_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Daily Price (TL)")
        self.dailyPrice_ent.grid(row=5, column=6)

        self.productionDate_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Year")
        self.productionDate_ent.grid(row=5, column=7)

        self.productionName_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Brand")
        self.productionName_ent.grid(row=5, column=8)

        self.add_image_button_ent = customtkinter.CTkButton(self, text="Add Image", command=self.process_image)
        self.add_image_button_ent.grid(row=6, column=6, padx=10, pady=10)

        try:
            self.submit_button_ent = customtkinter.CTkButton(self, text="Submit", command=self.add_car_callback)
            self.submit_button_ent.grid(row=7, column=6, padx=10, pady=10)

        except Exception as e:
            print(e)
            messagebox.showerror("Auth", "Internal database error!")
            print("Internal database error!", e)

        self.finish_ent = customtkinter.CTkButton(self, text="Finish", command=self.close_add_car)
        self.finish_ent.grid(row=10, column=8)

    # To get info from the user
    def add_car_callback(self):

        try:
            plate = self.plate_ent.get()
            occupied_until = self.occupiedUntil_ent.get()
            occupied_to = self.occupiedTo_ent.get()
            daily_price = self.dailyPrice_ent.get()
            production_date = self.productionDate_ent.get()
            production_name = self.productionName_ent.get()
            car_image = self.image_base64

            self.db.insert_car(plate=plate, occupied_until=occupied_until,
                               occupied_to=occupied_to, daily_price=daily_price,
                               production_date=production_date, production_name=production_name, image_url=car_image
                               )

        except Exception as e:
            print(e)
            messagebox.showerror("Auth", "Internal database error!")
            print("Internal database error!", e)

    # Turn back to clean main
    def close_add_car(self):

        self.plate_ent.grid_forget()
        self.occupiedUntil_ent.grid_forget()
        self.occupiedTo_ent.grid_forget()
        self.dailyPrice_ent.grid_forget()
        self.productionDate_ent.grid_forget()
        self.productionName_ent.grid_forget()
        self.add_image_button_ent.grid_forget()
        self.submit_button_ent.grid_forget()
        self.finish_ent.grid_forget()
        try:
            self.image_label.grid_forget()

        except Exception as e:
            print(e)

        # TO ACTİVETE TO ACCES TO OTHER OTPTİONS
        self.remove_car_button.configure(state=customtkinter.NORMAL)

    # To store the image as text
    def process_image(self):

        file_path = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(
        ("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), ("All Files", "*.*")))

        # Convert the image to binary format
        with open(file_path, "rb") as file:
            image_binary = file.read()

        # Convert the image to Base64 format
        image_base64 = base64.b64encode(image_binary).decode("utf-8")
        self.image_base64 = image_base64

        # Decode Base64 image text decoded_image_binary = base64.b64decode(image_base64)

        # Open the image using Pillow
        image_pil = Image.open(BytesIO(image_binary))

        image_button = customtkinter.CTkImage(light_image=image_pil, size=(280, 150))
        self.image_label = customtkinter.CTkLabel(self, image=image_button, text=None)
        self.image_label.grid(row=7, column=1, columnspan=5, sticky='w')

    def remove_car(self):

        self.add_car_button.configure(state=customtkinter.DISABLED)

        self.plate_ent = customtkinter.CTkEntry(self, width=180, placeholder_text="Plate")
        self.plate_ent.grid(row=5, column=3)

        self.finish_ent = customtkinter.CTkButton(self, text="Finish", command=self.close_remove_car)
        self.finish_ent.grid(row=7, column=7)

        try:
            self.submit_button_ent = customtkinter.CTkButton(self, text="Remove Car", command=self.remove_car_callback)
            self.submit_button_ent.grid(row=7, column=6, padx=10, pady=10)

        except Exception as e:
            print(e)
            messagebox.showerror("Auth", "Internal database error!")
            print("Internal database error!", e)

    def remove_car_callback(self):

        plate = self.plate_ent.get()

        if self.db.check_car(plate=plate) == None:
            messagebox.showerror("DB ERROR", "There Is No Such Car!")
        else:
            self.db.remove_car(plate=plate)
            messagebox.showerror("", "Car Removed From Database!")

    def close_remove_car(self):

        self.add_car_button.configure(state=customtkinter.NORMAL)

        self.plate_ent.grid_forget()
        self.submit_button_ent.grid_forget()
        self.finish_ent.grid_forget()

    def show_all_available_cars(self):
        # Get all available cars from the database
        available_cars_tuples = self.db.fetch_all_available_cars()

        # Convert each tuple to a dictionary
        available_cars = [dict(
            zip(["plate", "occupied_until", "occupied_to", "daily_price", "production_date", "production_name",
                 "image_url"], car)) for car in available_cars_tuples]

        # Create a new window to display the available cars
        available_cars_window = customtkinter.CTkToplevel(self)
        available_cars_window.title("Available Cars")

        # Create labels to display car information
        header_labels = ["Plate", "Occupied Until", "Occupied To", "Daily Price", "Year", "Brand", "Image"]
        for col, header in enumerate(header_labels):
            label = customtkinter.CTkLabel(available_cars_window, text=header, font=("Rubik", 18, "bold"))
            label.grid(row=0, column=col, padx=10, pady=10)

        # Display each available car's information
        for row, car in enumerate(available_cars, start=1):
            plate_label = customtkinter.CTkLabel(available_cars_window, text=car['plate'], font=("Default", 13))
            plate_label.grid(row=row, column=0, padx=15, pady=15)

            occupied_until_label = customtkinter.CTkLabel(available_cars_window, text=car['occupied_until'],
                                                          font=("Default", 13))
            occupied_until_label.grid(row=row, column=1, padx=15, pady=15)

            occupied_to_label = customtkinter.CTkLabel(available_cars_window, text=car['occupied_to'],
                                                       font=("Default", 13))
            occupied_to_label.grid(row=row, column=2, padx=15, pady=15)

            daily_price_label = customtkinter.CTkLabel(available_cars_window, text=f"{car['daily_price']} TL",
                                                       font=("Default", 13))
            daily_price_label.grid(row=row, column=3, padx=15, pady=15)

            production_date_label = customtkinter.CTkLabel(available_cars_window, text=car['production_date'],
                                                           font=("Default", 13))
            production_date_label.grid(row=row, column=4, padx=15, pady=15)

            production_name_label = customtkinter.CTkLabel(available_cars_window, text=car['production_name'],
                                                           font=("Default", 13))
            production_name_label.grid(row=row, column=5, padx=15, pady=15)

            # Assuming you have stored images as base64 strings in the database
            image_data = base64.b64decode(car['image_url'])
            image_pil = Image.open(BytesIO(image_data))
            image_button = customtkinter.CTkImage(light_image=image_pil, size=(280, 150))
            image_label = customtkinter.CTkLabel(available_cars_window, image=image_button, text=None)
            image_label.grid(row=row, column=6, padx=10, pady=10)

        # Add a close button
        close_button = customtkinter.CTkButton(available_cars_window, text="Close",
                                               command=available_cars_window.destroy)
        close_button.grid(row=row + 1, column=0, columnspan=7, pady=10)
        available_cars_window.grab_set()
        available_cars_window.focus_set()
        available_cars_window.wait_window()