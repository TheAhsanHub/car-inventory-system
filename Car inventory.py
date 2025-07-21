# === Car Inventory Management System ===
# =====================================================================
# This Python application is designed for a car dealership to digitally manage their car inventory and sales.
# It offers two modes:
# - Users can browse, search, and purchase cars.
# - Admins can add, update, delete car details and view sales history.
# Data persistence is handled using CSV files for easy record-keeping.
#I used Python for logic and file handling, and Tkinter for the GUI.
#Data is stored in two CSV files: one for cars and another for sales


# STEP 1: Import all necessary modules
# These libraries are needed for file operations (CSV),
# building the GUI (Tkinter), and handling dates and system paths.

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
print("Saving files to:", os.getcwd())

# STEP 2: Define constants for file names and CSV headers
# We use two files:
# 1. cars.csv to store available car inventory.
# 2. sales.csv to record car sales history.
# Headers define the structure of these CSV files.

DATABASE_FILE = "cars.csv"
SALES_FILE = "sales.csv"
HEADERS = ["Brand", "Model", "Year", "Cost", "Shade", "Status"]
SALES_HEADERS = ["Date", "SalesID", "Brand", "CustomerName", "PriceSold", "Salesperson"]

# STEP 3: Initialize database files if they don't exist
# This ensures the application can create necessary CSV files with correct headers
# when launched for the very first time.

def setup_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(HEADERS)
    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, "w", newline="") as f:
            csv.writer(f).writerow(SALES_HEADERS)

# STEP 4: Define functions to handle database operations
# These functions read car data, write updated car lists,
# and append new sales into their respective CSV files.
#The system uses modular programming principles.
#All the core operations — such as reading and writing to CSV files,
#searching, updating, and appending sales — are handled using
#dedicated functions like read_data(), write_data(), and
#append_sale().

def read_data():
    with open(DATABASE_FILE, "r") as f:
        return list(csv.reader(f))[1:]  # Skip header line

def write_data(data):
    with open(DATABASE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(data)

def append_sale(sale):
    with open(SALES_FILE, "a", newline="") as f:
        csv.writer(f).writerow(sale)

# STEP 5: Create the main application class
# This sets up the GUI using Tkinter,
#For the GUI, I’ve encapsulated everything inside a class
# This Class makes the code organized and scalable
class CarManagerApp:
    def __init__(self, root, start_tab="user"):
        self.root = root
        self.root.title("Car Management System")
        self.root.geometry("1000x650")

        # STEP 5.1: Create two tabs inside the GUI: User and Admin
        tab_control = ttk.Notebook(root)
        self.user_tab = ttk.Frame(tab_control)
        self.admin_tab = ttk.Frame(tab_control)
        tab_control.add(self.user_tab, text="User")
        tab_control.add(self.admin_tab, text="Admin")
        tab_control.pack(expand=1, fill="both")

        # STEP 5.2: Set which tab to open first (default is user)
        if start_tab == "admin":
            tab_control.select(self.admin_tab)
        else:
            tab_control.select(self.user_tab)

        self.create_user_tab()
        self.create_admin_tab()

    # STEP 6: Build the User Panel
    # Users can search for cars, view car listings, and make purchases.

    def create_user_tab(self):
        frame = ttk.Frame(self.user_tab, padding=10)
        frame.pack(fill="both", expand=True)

        # Search section

        ttk.Label(frame, text="Search by:").pack(anchor="w")
        self.search_criteria = ttk.Combobox(frame, values=HEADERS[:-1])
        self.search_criteria.current(0)
        self.search_criteria.pack(anchor="w")

        self.search_entry = ttk.Entry(frame)
        self.search_entry.pack(anchor="w")

        ttk.Button(frame, text="Search / Sort", command=self.search_cars).pack(anchor="w", pady=5)

        # Car listing table

        self.user_tree = ttk.Treeview(frame, columns=HEADERS, show="headings")
        for col in HEADERS:
            self.user_tree.heading(col, text=col)
        self.user_tree.pack(fill="both", expand=True)

        # Customer information inputs

        ttk.Label(frame, text="Customer Name:").pack(anchor="w")
        self.customer_entry = ttk.Entry(frame)
        self.customer_entry.pack(anchor="w")

        ttk.Label(frame, text="Salesperson Name:").pack(anchor="w")
        self.salesperson_entry = ttk.Entry(frame)
        self.salesperson_entry.pack(anchor="w")

        ttk.Button(frame, text="Buy Car", command=self.buy_car).pack(pady=10)

        # Load all available cars into the User Panel

        self.load_table(self.user_tree, read_data())

    # STEP 7: Build the Admin Panel
    # Admins can add new cars, edit details, delete cars, and view inventory and sales history.

    def create_admin_tab(self):
        frame = ttk.Frame(self.admin_tab, padding=10)
        frame.pack(fill="both", expand=True)

        # Car entry form

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(fill="x", pady=10)

        self.entries = []
        for idx, label in enumerate(HEADERS):
            ttk.Label(entry_frame, text=label).grid(row=0, column=idx)
            entry = ttk.Entry(entry_frame, width=15)
            entry.grid(row=1, column=idx)
            self.entries.append(entry)

        # Admin actions

        ttk.Button(frame, text="Add Car", command=self.add_car).pack(pady=5)
        ttk.Button(frame, text="Update Car", command=self.update_car).pack(pady=5)
        ttk.Button(frame, text="Delete Car", command=self.delete_car).pack(pady=5)

        # Car listing table for admin

        self.admin_tree = ttk.Treeview(frame, columns=HEADERS, show="headings")
        for col in HEADERS:
            self.admin_tree.heading(col, text=col)
        self.admin_tree.pack(fill="both", expand=True)
        self.admin_tree.bind("<<TreeviewSelect>>", self.fill_form)
        self.load_table(self.admin_tree, read_data())

        # Sales history display

        sales_frame = ttk.LabelFrame(frame, text="Inventory & Sales Overview")
        sales_frame.pack(fill="both", expand=True, pady=10)

        self.sales_tree = ttk.Treeview(sales_frame, columns=SALES_HEADERS, show="headings")
        for col in SALES_HEADERS:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=120)
        self.sales_tree.pack(fill="both", expand=True)
        self.load_sales_data()

    # STEP 8: Utility function to populate data into Treeview tables

    def load_table(self, tree, data):
        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            tree.insert("", "end", values=row)

    def load_sales_data(self):
        if os.path.exists(SALES_FILE):
            with open(SALES_FILE, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    self.sales_tree.insert("", "end", values=row)

    # STEP 9: Search or sort cars based on user input

    def search_cars(self):
            try:
                column_name = self.search_criteria.get()
                key = HEADERS.index(column_name)
                value = self.search_entry.get().lower()
                results = read_data()

                # Filter results if user typed something
                if value:
                    results = [car for car in results if value in car[key].lower()]
                else:
                    results = sorted(results, key=lambda x: x[key])

                self.load_table(self.user_tree, results)

                if not results:
                    messagebox.showwarning("No Results", f"No matching cars found for {column_name}.")
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
    # STEP 10: Populate admin form with selected car details
    # When an admin clicks a car, its details fill the input fields.

    def fill_form(self, event):
        selected = self.admin_tree.selection()
        if selected:
            values = self.admin_tree.item(selected[0])["values"]
            for entry, value in zip(self.entries, values):
                entry.delete(0, tk.END)
                entry.insert(0, value)

    # STEP 11: Admin-side functionalities: Add, Update, and Delete cars

    def add_car(self):
        new_car = [entry.get() for entry in self.entries]
        if all(new_car):
            cars = read_data()
            cars.append(new_car)
            write_data(cars)
            self.load_table(self.admin_tree, cars)
            messagebox.showinfo("Success", "Car added successfully.")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields before adding.")

    def update_car(self):
        selected = self.admin_tree.selection()
        if not selected:
            return
        index = self.admin_tree.index(selected[0])
        cars = read_data()
        updated_car = [entry.get() for entry in self.entries]
        if all(updated_car):
            cars[index] = updated_car
            write_data(cars)
            self.load_table(self.admin_tree, cars)
            messagebox.showinfo("Updated", "Car details updated successfully.")
        else:
            messagebox.showwarning("Error", "Please fill all fields before updating.")

    def delete_car(self):
        selected = self.admin_tree.selection()
        if not selected:
            return
        index = self.admin_tree.index(selected[0])
        cars = read_data()
        cars.pop(index)
        write_data(cars)
        self.load_table(self.admin_tree, cars)
        messagebox.showinfo("Deleted", "Car removed from inventory.")

    # STEP 12: User-side function to buy a car
    # When a user buys a car, it marks the car as 'Sold' and records the sale.

    def buy_car(self):
        selected = self.user_tree.selection()
        if not selected:
            return
        customer = self.customer_entry.get()
        salesperson = self.salesperson_entry.get()
        if not customer or not salesperson:
            messagebox.showwarning("Missing Info", "Please enter both customer and salesperson names.")
            return

        car_data = self.user_tree.item(selected[0])["values"]
        if car_data[-1].lower() == "sold":
            messagebox.showwarning("Unavailable", "Car is already sold.")
            return

        # Create a new sales record

        sale_id = f"S{datetime.now().strftime('%Y%m%d%H%M%S')}"
        date = datetime.now().strftime("%Y-%m-%d")
        sale = [date, sale_id, car_data[0], customer, car_data[3], salesperson]
        append_sale(sale)

        # Update car status to 'Sold'

        cars = read_data()
        for i, row in enumerate(cars):
            if row == car_data:
                cars[i][-1] = "Sold"
                break
        write_data(cars)

        self.load_table(self.user_tree, cars)
        self.load_table(self.admin_tree, cars)
        self.load_sales_data()
        messagebox.showinfo("Success", "Car purchased successfully.")

# STEP 13: Create a main menu window
# Allows the user to choose between User Panel or Admin Panel at the program start.

def open_main_menu():
    def open_admin():
        win.destroy()
        root = tk.Tk()
        app = CarManagerApp(root, start_tab="admin")
        root.mainloop()

    def open_user():
        win.destroy()
        root = tk.Tk()
        app = CarManagerApp(root, start_tab="user")
        root.mainloop()

    win = tk.Tk()
    win.title("Car Inventory Management System")
    win.geometry("400x300")

    tk.Label(win, text="Welcome to Car Inventory System", font=("Arial", 14)).pack(pady=40)
    tk.Button(win, text="Admin Panel", width=20, command=open_admin).pack(pady=10)
    tk.Button(win, text="User Panel", width=20, command=open_user).pack(pady=10)
    win.mainloop()

# STEP 14: Program entry point
# Setup the database and launch the main menu window.

if __name__ == "__main__":
    setup_database()
    open_main_menu()