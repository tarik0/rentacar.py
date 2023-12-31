from hashlib import md5
from tkinter import messagebox
import customtkinter
from PIL import Image

from db import CarDatabase


class LoginApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase, logo: Image, on_success=None):
        super().__init__()
        self.db = db
        self.on_success = on_success
        self.geometry("400x450")
        self.title("RENTACAR - Authentication")
        self.resizable(False, False)

        # Configure grid for centering widgets in the main window
        self.grid_columnconfigure(0, weight=1)  # Left padding column
        self.grid_columnconfigure(2, weight=1)  # Right padding column
        self.grid_rowconfigure(0, weight=1)  # Top padding row
        self.grid_rowconfigure(8, weight=1)  # Bottom padding row

        # Import logo and center
        self.logo = customtkinter.CTkImage(
            logo,
            size=(150, 150),
        )

        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text=None)
        self.logo_label.grid(row=0, column=1, padx=10, sticky="w")

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
            self.destroy()
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
