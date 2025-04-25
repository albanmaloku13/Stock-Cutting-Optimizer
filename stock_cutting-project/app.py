from tkinter import Tk, Label, Button, Entry, Text, END, messagebox
from src.cutting_logic import process_cuts
from src.stock_manager import load_stock, add_stock, remove_stock

class CuttingStockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Cutting Optimizer")

        # Set background color
        self.root.configure(bg="#6d63c7")

        # Title
        self.title_label = Label(root, text="Stock Cutting Optimizer", font=("Trebuchet MS", 26, "bold"), bg="#6d63c7", fg="black")
        self.title_label.pack(pady=12)

        # Stock display
        self.stock_label = Label(root, text="Available Stock:", font=("Arial", 16), bg="#6d63c7", fg="white")
        self.stock_label.pack()

        self.stock_display = Text(root, height=10, width=50, wrap="word", font=("Arial", 12), bg="#f0f0f0", fg="black")
        self.stock_display.pack(padx=10, pady=10)
        self.update_stock_display()

        # Add stock entry and button
        self.add_label = Label(root, text="Add Stock (length x quantity):", font=("Arial", 12), bg="#6d63c7", fg="white")
        self.add_label.pack(pady=3)

        self.add_entry = Entry(root, width=30, font=("Arial", 12))
        self.add_entry.insert(0, "e.g. 13.5x2")
        self.add_entry.pack(pady=5)

        self.add_button = Button(root, text="Add Stock", command=self.add_stock_action, bg="green", fg="white", font=("Arial", 12))
        self.add_button.pack(pady=5)

        # Remove stock entry and button
        self.remove_label = Label(root, text="Remove Stock (length x quantity):", font=("Arial", 12), bg="#6d63c7", fg="white")
        self.remove_label.pack(pady=5)

        self.remove_entry = Entry(root, width=30, font=("Arial", 12))
        self.remove_entry.insert(0, "e.g. 13.5x1")
        self.remove_entry.pack(pady=5)

        self.remove_button = Button(root, text="Remove Stock", command=self.remove_stock_action, bg="red", fg="white", font=("Arial", 12))
        self.remove_button.pack(pady=5)

        # Required cuts entry
        self.cuts_label = Label(root, text="Input your required cuts (length x quantity):", font=("Arial", 12), bg="#6d63c7", fg="white")
        self.cuts_label.pack(pady=5)

        self.cuts_entry = Entry(root, width=50, font=("Arial", 12))
        self.cuts_entry.insert(0, "e.g. 4.7x8, 3.38x8, 3.08x7")
        self.cuts_entry.pack(pady=5)

        # Generate Cutting Plan button
        self.generate_button = Button(root, text="Generate Cutting Plan", command=self.generate_cutting_plan, bg="blue", fg="white", font=("Arial", 12))
        self.generate_button.pack(pady=50)

        # Result area
        self.result_label = Label(root, text="Cutting Plan:", font=("Arial", 16), bg="#6d63c7", fg="white")
        self.result_label.pack(pady=5)

        self.result_display = Text(root, height=15, width=80, wrap="word", font=("Arial", 12), bg="#f0f0f0", fg="black")
        self.result_display.pack(padx=20, pady=10)

    def update_stock_display(self):
        """ Updates the stock display area with current available stock. """
        self.stock_display.delete("1.0", END)
        stock = load_stock()
        for length, qty in stock.items():
            self.stock_display.insert(END, f"{length}m x {qty}\n")

    def add_stock_action(self):
        """ Adds new stock to the available stock list. """
        try:
            value = self.add_entry.get()
            length, qty = value.lower().split("x")
            add_stock(float(length), int(qty))
            self.update_stock_display()
        except Exception as e:
            messagebox.showerror("Invalid Input", "Please enter stock as 'length x quantity', e.g., 13.5x2.\nError: " + str(e))

    def remove_stock_action(self):
        """ Removes stock from the available stock list. """
        try:
            value = self.remove_entry.get()
            length, qty = value.lower().split("x")
            remove_stock(float(length), int(qty))
            self.update_stock_display()
        except Exception as e:
            messagebox.showerror("Invalid Input", "Please enter stock as 'length x quantity', e.g., 13.5x1.\nError: " + str(e))

    def generate_cutting_plan(self):
        """ Generates the cutting plan based on required cuts. """
        input_cuts = self.cuts_entry.get()  # Getting input from the entry field
        print(f"Received input: {input_cuts}")  # Debugging step

        try:
            # Process cuts, assuming input is in correct format
            output = process_cuts(input_cuts)  # Pass input directly to process_cuts
            self.result_display.delete("1.0", END)
            self.result_display.insert(END, output)
            self.update_stock_display()

        except Exception as e:
            print("Error parsing cuts:", e)
            messagebox.showerror("Invalid Input", "Please enter required cuts in the format: 'length x quantity', e.g., 4.7x8, 3.38x8.")

# Launch the application
root = Tk()
app = CuttingStockApp(root)
root.mainloop()