from hashlib import md5
from tkinter import messagebox,filedialog
from functools import partial
import customtkinter
from PIL import Image, ImageTk
import base64
from io import BytesIO
from db import CarDatabase


class MainApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase):
        super().__init__()
        self.db = db
        self.geometry("1250x720")
        self.title("RENTACAR - SYSTEM")

        # Add Car Button
        self.add_car_button = customtkinter.CTkButton(self, text="Add Car", command=self.add_car)
        self.add_car_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Remove Car Button
        self.remove_car_button = customtkinter.CTkButton(self, text="Remove Car")
        self.remove_car_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Check Users Button
        self.check_users_button = customtkinter.CTkButton(self, text="Check Users")
        self.check_users_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def add_car(self):
       
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
        
        self.add_image_button_ent = customtkinter.CTkButton(self, text="Add Image",command=self.process_image)
        self.add_image_button_ent.grid(row=6, column=6, padx=10, pady=10)

        self.submit_button_ent = customtkinter.CTkButton(self, text="Submit",command=self.add_car_callback)
        self.submit_button_ent.grid(row=7,column=6, padx=10, pady=10)


    def process_image(self):
        
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), ("All Files", "*.*")))

        # Convert the image to binary format
        with open(file_path, "rb") as file:
            image_binary = file.read()

        # Convert the image to Base64 format
        image_base64 = base64.b64encode(image_binary).decode("utf-8")

        # Decode Base64 image text
        decoded_image_binary = base64.b64decode(image_base64)

        # Open the image using Pillow
        image_pil = Image.open(BytesIO(decoded_image_binary))

            
        image_button = customtkinter.CTkImage(light_image=image_pil,size=(400,200))
        image_label = customtkinter.CTkLabel(self, image=image_button,text=None)
        image_label.grid(row=9,column=6)

        

    def add_car_callback(self):
        
        plate= self.plate_ent.get()
        occupiedUntil = self.occupiedUntil_ent.get()
        occupiedTo= self.occupiedTo_ent.get()
        dailyPrice= self.dailyPrice_ent.get()
        productionDate= self.productionDate_ent.get()
        productionName= self.productionName_ent.get()
        carImage = self.image_base64.get()

        print (plate,occupiedUntil,occupiedTo,dailyPrice,productionDate,productionName,carImage)


    
    

class LoginApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase, on_success=None):
        super().__init__()
        self.db = db
        self.on_success = on_success
        self.geometry("400x300")
        self.title("RENTACAR - Authentication")

        # Configure grid for centering widgets in the main window
        self.grid_columnconfigure(0, weight=1)  # Left padding column
        self.grid_columnconfigure(2, weight=1)  # Right padding column
        self.grid_rowconfigure(0, weight=1)  # Top padding row
        self.grid_rowconfigure(8, weight=1)  # Bottom padding row

        # Header Label
        self.header_label = customtkinter.CTkLabel(
            self, text="Authenticate", font=("Verdana", 20, "bold")
        )
        self.header_label.grid(row=1, column=1, pady=10)

        # Full Name Entry
        self.fullname_entry = customtkinter.CTkEntry(
            self, width=180, placeholder_text="Full Name"
        )
        self.fullname_entry.grid(row=2, column=1)

        # Username Entry
        self.username_entry = customtkinter.CTkEntry(
            self, width=180, placeholder_text="ID"
        )
        self.username_entry.grid(row=3, pady=5, column=1)

        # Password Entry
        self.password_entry = customtkinter.CTkEntry(
            self, width=180, placeholder_text="Password", show="*"
        )
        self.password_entry.grid(row=4, column=1)

        # Register Button
        self.register_button = customtkinter.CTkButton(
            self, text="Register", command=self.register_callback
        )
        self.register_button.grid(row=6, column=1, pady=10, sticky="ew")

        # Login Button
        self.login_button = customtkinter.CTkButton(
            self, text="Login", command=self.login_callback
        )
        self.login_button.grid(row=7, column=1, pady=0, sticky="ew")

    def login_callback(self):
        # get values from entries
        _id = self.username_entry.get()
        password = self.password_entry.get()

        # check if values are empty
        if not _id or not password:
            messagebox.showerror("Auth", "Credentials cannot be empty!")
            print("Credentials cannot be empty!")
            return

        # encrypt password with MD5
        passHash = md5(password.encode()).hexdigest()
        print("Login Callback")
        print(f"National ID: {_id}, Password: {password}, Encrypted Password: {passHash}")

        # check if db is initialized
        if not self.db:
            messagebox.showerror("Auth", "Database not initialized!")
            print("Database not initialized!")
            return

        # fetch user info
        try:
            info = self.db.check_user(_id, passHash)
        except Exception as e:
            print(e)
            messagebox.showerror("Auth", "Internal database error!")
            print("Internal database error!", e)
            return

        # check if user exists
        if not info:
            messagebox.showerror("Auth", "Invalid credentials!")
            print("Invalid credentials!")
            return

        # show message
        messagebox.showinfo("Login", f"Welcome {info[2]}!")
        print(f"Welcome {info[2]}!")

        # call on_success callback
        if self.on_success:
            self.on_success(info)

    def register_callback(self):
        _id = self.username_entry.get()
        fullname = self.fullname_entry.get()
        password = self.password_entry.get()

        # Check if values are empty
        if not _id or not password or not fullname:
            messagebox.showerror("Login", "Credentials cannot be empty! (Including Full Name)")
            print("Credentials cannot be empty!")
            return

        # encrypt password with MD5
        passHash = md5(password.encode()).hexdigest()
        print("Register Callback")
        print(f"National ID: {_id}, Password: {password}, Encrypted Password: {passHash}, Full Name: {fullname}")

        # check if db is initialized
        if not self.db:
            messagebox.showerror("Auth", "Database not initialized!")
            print("Database not initialized!")
            return

        # insert user
        try:
            self.db.insert_user(_id, passHash, fullname)
        except Exception as e:
            print(e)
            messagebox.showerror("Auth", "Unable to register user! (Make sure ID is unique and at least 11 characters)")
            print("Internal database error!", e)
            return

        messagebox.showinfo("Login", f"Welcome {fullname}!")
        print(f"Welcome {fullname}!")

        # call on_success callback
        if self.on_success:
            self.on_success({
                "nationalId": _id,
                "fullname": fullname
            })

