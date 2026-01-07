#importing libraries for a calculator app in python 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  

import math

# This script includes both a command-line calculator and an GUI calculator extension.

# GUI Calculator
#class for Calculator Application
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("420x500")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        self.create_widgets()

    #create a frame for the input field and buttons
    def create_widgets(self):
        input_frame = tk.Frame(self.root, width=420, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        input_frame.pack(side=tk.TOP)

        input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=35, bg="#eee", bd=0, justify=tk.RIGHT)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=10)

        btns_frame = tk.Frame(self.root, width=420, height=450, bg="grey")
        btns_frame.pack()

        # First row
        clear = tk.Button(btns_frame, text="C", fg="black", width=23, height=2, bd=0, bg="#eee", cursor="hand2", command=self.clear).grid(row=0, column=0, columnspan=3, padx=1, pady=1)
        divide = tk.Button(btns_frame, text="/", fg="black", width=7, height=2, bd=0, bg="#eee", cursor="hand2", command=lambda: self.button_click("/")).grid(row=0, column=3, padx=1, pady=1)

        # Second row
        seven = tk.Button(btns_frame, text="7", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("7")).grid(row=1, column=0, padx=1, pady=1)
        eight = tk.Button(btns_frame, text="8", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("8")).grid(row=1, column=1, padx=1, pady=1)
        nine = tk.Button(btns_frame, text="9", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("9")).grid(row=1, column=2, padx=1, pady=1)
        multiply = tk.Button(btns_frame, text="*", fg="black", width=7, height=2, bd=0, bg="#eee", cursor="hand2", command=lambda: self.button_click("*")).grid(row=1, column=3, padx=1, pady=1)

        # Third row
        four = tk.Button(btns_frame, text="4", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("4")).grid(row=2, column=0, padx=1, pady=1)
        five = tk.Button(btns_frame, text="5", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("5")).grid(row=2, column=1, padx=1, pady=1)
        six = tk.Button(btns_frame, text="6", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("6")).grid(row=2, column=2, padx=1, pady=1)
        minus = tk.Button(btns_frame, text="-", fg="black", width=7, height=2, bd=0, bg="#eee", cursor="hand2", command=lambda: self.button_click("-")).grid(row=2, column=3, padx=1, pady=1)

        # Fourth row
        one = tk.Button(btns_frame, text="1", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("1")).grid(row=3, column=0, padx=1 , pady=1)
        two = tk.Button(btns_frame, text="2", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("2")).grid(row=3, column=1, padx=1 , pady=1)
        three = tk.Button(btns_frame, text="3", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("3")).grid(row=3, column=2, padx=1 , pady=1)
        plus = tk.Button(btns_frame, text="+", fg="black", width=7, height=2, bd=0, bg="#eee", cursor="hand2", command=lambda: self.button_click("+")).grid(row=3, column=3, padx=1 , pady=1)      

        # Fifth row
        zero = tk.Button(btns_frame, text="0", fg="black", width=15, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click("0")).grid(row=4, column=0, columnspan=2, padx=1 , pady=1)
        point = tk.Button(btns_frame, text=".", fg="black", width=7, height=2, bd=0, bg="#fff", cursor="hand2", command=lambda: self.button_click(".")).grid(row=4, column=2, padx=1 , pady=1)
        equals = tk.Button(btns_frame, text="=", fg="black", width=7, height=2, bd=0, bg="#eee", cursor="hand2", command=self.evaluate).grid(row=4, column=3, padx=1 , pady=1)

    #function to handle button clicks
    def button_click(self, item):
        self.expression += str(item)
        self.input_text.set(self.expression)    
    
    #function to clear the input field
    def clear(self):
        self.expression = ""
        self.input_text.set("")    

    #function to evaluate the expression
    def evaluate(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            self.expression = ""
            self.input_text.set("")     

#command-line calculator function
def command_line_calculator():
    """
    Command-line calculator that prompts for first number, operation, and second number.
    Handles non-numeric input and division by zero gracefully.
    Allows user to continue or exit after each calculation.
    """
    print("\nWelcome to the Command-Line Calculator!")
    print("=" * 50)
    
    while True:
        # Get first number
        while True:
            try:
                first_number = float(input("Enter the first number: "))
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        
        # Get operation
        while True:
            operation = input("Enter an operation (+, -, *, /): ")
            if operation in ['+', '-', '*', '/']:
                break
            else:
                print("Error: Please enter a valid operation (+, -, *, /).")
        
        # Get second number
        while True:
            try:
                second_number = float(input("Enter the second number: "))
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        
        # Perform calculation
        try:
            if operation == '+':
                result = first_number + second_number
            elif operation == '-':
                result = first_number - second_number
            elif operation == '*':
                result = first_number * second_number
            elif operation == '/':
                if second_number == 0:
                    print("\nError: Cannot divide by zero. Please try again.")
                    print("=" * 50)
                    continue
                result = first_number / second_number
            
            # Display result
            print("=" * 50)
            print(f"Result: {first_number} {operation} {second_number} = {result}")
            print("=" * 50)
        except Exception as e:
            print(f"\nError: An unexpected error occurred: {e}")
            print("=" * 50)
        
        # Ask user if they want to continue
        while True:
            continue_choice = input("\nDo you want to perform another calculation? (yes/no): ").lower()
            if continue_choice in ['yes', 'y']:
                print("\n" + "=" * 50)
                break
            elif continue_choice in ['no', 'n']:
                print("\nThank you for using the calculator. Goodbye!")
                print("=" * 50)
                return
            else:
                print("Error: Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    print("\nCalculator Application")
    print("=" * 50)
    choice = input("Choose calculator mode:\n1. Command-Line Calculator\n2. GUI Calculator\nEnter 1 or 2: ")
    
    if choice == '1':
        command_line_calculator()
    elif choice == '2':
        root = tk.Tk()
        app = CalculatorApp(root)
        root.mainloop()
    else:
        print("Invalid choice. Defaulting to GUI Calculator...")
        root = tk.Tk()
        app = CalculatorApp(root)
        root.mainloop()