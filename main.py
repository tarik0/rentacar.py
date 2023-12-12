from hashlib import md5
from tkinter import messagebox

import customtkinter

from db import CarDatabase

customtkinter.set_appearance_mode("dark")


class LoginApp(customtkinter.CTk):
    def __init__(self, db: CarDatabase):
        super().__init__()
        self.db = db
        self.geometry("400x300")
        self.title("RENTACAR - Authentication")

        # Frame for the form
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(padx=65, pady=25, expand=True, fill="both")

        # Configure grid for centering in form_frame
        self.form_frame.grid_columnconfigure((0, 3), weight=1)  # Columns for padding
        self.form_frame.grid_rowconfigure((0, 6), weight=1)  # Rows for padding (added one extra for the empty row)

        # Header Label
        self.header_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Authenticate",
            font=("Verdana", 20, "bold")
        )
        self.header_label.grid(row=0, column=1, pady=10)

        # Username Entry
        self.fullname_entry = customtkinter.CTkEntry(self.form_frame, width=180, placeholder_text="Full Name")
        self.fullname_entry.grid(row=1, column=1)

        # Username Entry
        self.username_entry = customtkinter.CTkEntry(self.form_frame, width=180, placeholder_text="ID")
        self.username_entry.grid(row=2, pady=5, column=1)

        # Password Entry
        self.password_entry = customtkinter.CTkEntry(self.form_frame, width=180, placeholder_text="Password",
                                                     show="*")
        self.password_entry.grid(row=3, column=1)

        # Register Button
        self.register_button = customtkinter.CTkButton(self.form_frame, text="Register", command=self.register_callback)
        self.register_button.grid(row=7, column=1, sticky="ew")

        # Login Button
        self.login_button = customtkinter.CTkButton(self.form_frame, text="Login", command=self.login_callback)
        self.login_button.grid(row=6, column=1, pady=5, sticky="ew")

        # Empty row for spacing
        self.form_frame.grid_rowconfigure(8, weight=1)

    def login_callback(self):
        _id = self.username_entry.get()
        password = self.password_entry.get()

        if not _id or not password:
            messagebox.showerror("Auth", "Invalid credentials!")
            print("Invalid credentials!")
            return

        # Encrypt password with MD5
        # This is just for demonstration purposes, you should use a more secure encryption algorithm
        # See: https://docs.python.org/3/library/hashlib.html
        passHash = md5(password.encode()).hexdigest()
        print(f"National ID: {_id}, Password: {password}, Encrypted Password: {passHash}")

        if self.db:
            info = self.db.check_user(_id, passHash)
            if info:
                # alert box
                messagebox.showinfo("Auth", f"Welcome {info[2]}!")
                print(f"Welcome {info[2]}!")
                self.destroy()
            else:
                # alert box
                messagebox.showerror("Login", "Invalid credentials!")
                print("Invalid credentials!")

    def register_callback(self):
        _id = self.username_entry.get()
        fullname = self.fullname_entry.get()
        password = self.password_entry.get()

        if not _id or not password or not fullname:
            messagebox.showerror("Auth", "Invalid inputs!")
            print("Invalid inputs!")
            return

        # Encrypt password with MD5
        passHash = md5(password.encode()).hexdigest()
        print(f"National ID: {_id}, Password: {password}, Encrypted Password: {passHash}, Full Name: {fullname}")

        if self.db:
            try:
                info = self.db.insert_user(_id, passHash, "fullname")
                messagebox.showinfo("Login", f"Welcome {info[2]}!")
                print(f"Welcome {info[2]}!")
                self.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror("Login", "Invalid inputs!")
                print("Invalid inputs!")


app = LoginApp(CarDatabase("rentacar.db", overwrite=True))
app.mainloop()
