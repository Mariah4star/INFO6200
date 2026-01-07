#importing libraries for a calculator app in python 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  

import math

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
    
    #create a CLI interface for the calculator  
    def cli_interface(self):
        print("Welcome to the CLI Calculator!")
        print("Type 'exit' to quit.")
        while True:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                print("Exiting the calculator. Goodbye!")
                break
            try:
                result = eval(user_input)
                print("Result:", result)
            except Exception as e:
                print("Error: Invalid Input")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()     