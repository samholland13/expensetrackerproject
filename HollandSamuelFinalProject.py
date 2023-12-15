import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import os


# Class representing an expense item
class Expense:
    def __init__(self, name, amount, category, timestamp=None):
        # Initialize expense attributes
        self.name = name
        self.amount = amount
        self.category = category
        self.timestamp = timestamp or datetime.now()


# Main application class
class ExpenseTrackerApp:
    def __init__(self, root):
        # Initialize the application with the main window
        self.root = root
        self.root.title("Expense Tracker")

        # Lists to store expenses and budgets
        self.expenses = []
        self.budgets = {}

        # Load existing data or initialize
        self.load_data()

        # Create the user interface
        self.create_widgets()

    # Method to create the main user interface
    def create_widgets(self):
        # Create menu bar
        self.create_menu()

        # Header label
        header_label = tk.Label(self.root, text="Expense Tracker", font=("Helvetica", 16))
        header_label.pack(pady=10)

        # Display current date and time
        self.date_label = tk.Label(self.root, text="", font=("Helvetica", 10))
        self.date_label.pack()
        self.update_datetime()

        # Entry fields for expense details
        self.expense_entry = self.create_entry_with_default_text("Enter Expense")
        self.expense_entry.pack(pady=5)

        self.amount_entry = self.create_entry_with_default_text("Enter Amount")
        self.amount_entry.pack(pady=5)

        # Category-related widgets
        self.create_category_widgets()

        # Buttons to perform actions
        self.create_button("Add Expense", self.add_expense).pack(pady=5)
        self.create_button("Edit Budget", self.edit_budget).pack(pady=5)
        self.create_button("Show Expenses", self.show_expenses).pack(pady=5)
        self.create_button("Show Graph", self.show_graph_options).pack(pady=5)
        self.create_button("Show Budgets", self.show_budgets).pack(pady=5)
        self.create_search_widgets()
        self.create_button("Open Calculator", self.open_calculator).pack(pady=5)
        self.create_button("Quit", self.root.destroy).pack(pady=10)

    # Method to create the menu bar
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Save As", command=self.save_data_as)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    # Method to update the displayed date and time
    def update_datetime(self):
        now = datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date_label.config(text=formatted_date_time)
        self.root.after(1000, self.update_datetime)

    # Method to create category-related widgets
    def create_category_widgets(self):
        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.pack(pady=5)

        # Dropdown menu for selecting expense category
        self.category_combobox = ttk.Combobox(self.root, values=list(self.budgets.keys()))
        self.category_combobox.pack(pady=5)

        # Button to add a new category
        self.create_button("Add Category", self.add_category).pack(pady=5)

    # Method to create search-related widgets
    def create_search_widgets(self):
        # Entry field for searching expenses
        self.search_entry = self.create_entry("Search Expenses", width=20)
        self.search_entry.pack(pady=5)

        # Button to initiate expense search
        self.create_button("Search Expenses", self.search_expenses).pack(pady=5)

    # Method to create an entry field with default text
    def create_entry_with_default_text(self, default_text):
        entry = tk.Entry(self.root, width=30, font=("Helvetica", 10))
        entry.insert(0, default_text)
        entry.bind("<FocusIn>", self.clear_default_text)
        return entry

    # Method to create a regular entry field
    def create_entry(self, placeholder, **kwargs):
        entry = tk.Entry(self.root, **kwargs)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", self.clear_default_text)
        return entry

    # Method to clear default text from entry fields
    def clear_default_text(self, event):
        default_texts = ('Enter Expense', 'Enter Amount', 'Search Expenses')
        if event.widget.get() in default_texts:
            event.widget.delete(0, tk.END)

    # Method to create a button
    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command, font=("Helvetica", 12), width=15)
        return button

    # Method to add a new expense
    def add_expense(self):
        # Retrieve expense details from entry fields
        expense_name = self.expense_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combobox.get()

        # Validate and process the expense
        if expense_name and amount and category:
            amount = float(amount)
            expense = Expense(expense_name, amount, category)

            # Check if the category has a budget, and if so, whether the expense exceeds it
            if category not in self.budgets:
                self.budgets[category] = 0

            if amount <= self.budgets[category] or self.budgets[category] == 0:
                # Add the expense and update the budget
                self.expenses.append(expense)
                self.budgets[category] -= amount
                self.expense_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.save_data()
                messagebox.showinfo("Expense Tracker", "Expense added successfully.")
            else:
                # Alert if the budget is exceeded
                messagebox.showwarning("Expense Tracker", f"Budget exceeded for category {category}.")
        else:
            # Alert if any field is missing
            messagebox.showwarning("Expense Tracker", "Please enter an expense, amount, and select a category.")

    # Method to display a list of all expenses
    def show_expenses(self):
        expenses_window = tk.Toplevel(self.root)
        expenses_window.title("Expenses")

        # Display each expense with a delete button
        for expense in self.expenses:
            expense_label = tk.Label(expenses_window,
                                     text=f"{expense.name}: ${expense.amount:.2f} ({expense.category}) - {expense.timestamp}")
            expense_label.pack(pady=5)

            delete_button = tk.Button(expenses_window, text="Delete",
                                      command=lambda exp=expense: self.delete_expense(exp))
            delete_button.pack(pady=2)

    # Method to delete an expense
    def delete_expense(self, expense):
        confirmation = messagebox.askyesno("Delete Expense", f"Do you want to delete the expense '{expense.name}'?")
        if confirmation:
            # Remove the expense and update the budget
            self.expenses.remove(expense)
            self.budgets[expense.category] += expense.amount
            self.save_data()
            messagebox.showinfo("Expense Tracker", f"Expense '{expense.name}' deleted successfully.")
            self.show_expenses()

    # Method to edit the budget for a category
    def edit_budget(self):
        selected_category = self.category_combobox.get()

        if selected_category not in self.budgets:
            # Alert if the category does not exist
            messagebox.showwarning("Expense Tracker", f"Category '{selected_category}' not found.")
            return

        # Prompt the user for a new budget
        new_budget = simpledialog.askfloat("Edit Budget", f"Enter new budget for {selected_category}:")

        if new_budget is not None:
            # Update the budget and save data
            self.budgets[selected_category] = new_budget
            self.save_data()
            messagebox.showinfo("Expense Tracker", f"Budget for category '{selected_category}' updated successfully.")

    # Method to display options for graphical representation of expenses
    def show_graph_options(self):
        graph_options_window = tk.Toplevel(self.root)
        graph_options_window.title("Graph Options")

        tk.Label(graph_options_window, text="Select Graph Type:", font=("Helvetica", 12)).pack(pady=5)

        graph_types = ["Bar Graph", "Pie Chart", "Scatter Plot"]

        # Create buttons for different graph types
        for graph_type in graph_types:
            tk.Button(graph_options_window, text=graph_type, command=lambda gt=graph_type: self.show_graph(gt),
                      font=("Helvetica", 10)).pack(pady=5)

        tk.Button(graph_options_window, text="Close", command=graph_options_window.destroy,
                  font=("Helvetica", 10)).pack(pady=10)

    # Method to display a graph based on the selected type
    def show_graph(self, graph_type):
        if not self.expenses:
            # Alert if there are no expenses to display
            messagebox.showinfo("Expense Tracker", "No expenses to display.")
            return

        if graph_type == "Bar Graph":
            self.show_bar_graph()
        elif graph_type == "Pie Chart":
            self.show_pie_chart()
        elif graph_type == "Scatter Plot":
            self.show_scatter_plot()

    # Method to display a bar graph of expense distribution by category
    def show_bar_graph(self):
        categories = set(expense.category for expense in self.expenses)
        category_totals = {category: sum(expense.amount for expense in self.expenses if expense.category == category)
                           for category in categories}

        # Create and display the bar graph
        plt.figure(figsize=(8, 6))
        plt.bar(category_totals.keys(), category_totals.values())
        plt.title("Expense Distribution by Category - Bar Graph")

        self.show_matplotlib_graph(plt)

    # Method to display a pie chart of expense distribution by category
    def show_pie_chart(self):
        categories = set(expense.category for expense in self.expenses)
        category_totals = {category: sum(expense.amount for expense in self.expenses if expense.category == category)
                           for category in categories}

        # Create and display the pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category - Pie Chart")

        self.show_matplotlib_graph(plt)

    # Method to display a scatter plot of expense distribution by category
    def show_scatter_plot(self):
        categories = set(expense.category for expense in self.expenses)
        category_totals = {category: sum(expense.amount for expense in self.expenses if expense.category == category)
                           for category in categories}

        # Extract x and y values for the scatter plot
        x_values = list(categories)
        y_values = list(category_totals.values())

        # Create and display the scatter plot
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_values)
        plt.title("Expense Distribution by Category - Scatter Plot")

        self.show_matplotlib_graph(plt)

    # Method to display a matplotlib graph in a new window
    def show_matplotlib_graph(self, plt_instance):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Expense Distribution Graph")

        # Embed the matplotlib graph in the Tkinter window
        canvas = FigureCanvasTkAgg(plt_instance.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = tk.Frame(graph_window)
        toolbar.pack()

        # Button to close the graph window
        tk.Button(toolbar, text="Close", command=graph_window.destroy, font=("Helvetica", 12)).pack(side=tk.LEFT)

    # Method to display budgets for each category
    def show_budgets(self):
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Budgets")

        # Display each category's budget
        for category, budget in self.budgets.items():
            budget_label = tk.Label(budget_window, text=f"{category} Budget: ${budget:.2f}", font=("Helvetica", 12))
            budget_label.pack(pady=5)

    # Method to search for expenses based on user input
    def search_expenses(self):
        search_text = self.search_entry.get().lower()

        # Find expenses that match the search criteria
        search_results = [expense for expense in self.expenses if
                          search_text in expense.name.lower() or
                          search_text in str(expense.amount) or
                          search_text in expense.category.lower()]

        if not search_results:
            # Alert if no matching expenses are found
            messagebox.showinfo("Expense Tracker", "No matching expenses found.")
            return

        search_window = tk.Toplevel(self.root)
        search_window.title("Search Results")

        # Display search results
        for expense in search_results:
            expense_label = tk.Label(search_window,
                                     text=f"{expense.name}: ${expense.amount:.2f} ({expense.category}) - {expense.timestamp}",
                                     font=("Helvetica", 10))
            expense_label.pack(pady=5)

    # Method to open a simple calculator within the application
    def open_calculator(self):
        result = simpledialog.askstring("Calculator", "Enter an arithmetic expression:")
        if result:
            try:
                # Evaluate the expression and display the result
                calculated_result = eval(result)
                messagebox.showinfo("Calculator Result", f"Result: {calculated_result}")
            except Exception as e:
                # Alert if there is an error in the calculation
                messagebox.showerror("Calculator Error", f"Error: {e}")

    # Method to add a new expense category
    def add_category(self):
        new_category = simpledialog.askstring("Add Category", "Enter the new category:")
        if new_category and new_category not in self.budgets:
            # Add the new category and update the dropdown menu
            self.budgets[new_category] = 0

            self.category_combobox['values'] = list(self.budgets.keys())
            self.category_combobox.set(new_category)
            self.save_data()
            messagebox.showinfo("Expense Tracker", f"Category '{new_category}' added successfully.")
        elif new_category in self.budgets:
            # Alert if the category already exists
            messagebox.showwarning("Expense Tracker", f"Category '{new_category}' already exists.")
        else:
            # Alert if the input is invalid
            messagebox.showwarning("Expense Tracker", "Please enter a valid category.")

    # Method to save data to a specified file path
    def save_data_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.save_data(file_path)

    # Method to create a new file, clearing all current data
    def new_file(self):
        confirmation = messagebox.askyesno("New File", "Creating a new file will clear all current data. Are you sure?")
        if confirmation:
            self.expenses = []
            self.budgets = {}
            self.save_data()

    # Method to save expenses and budgets to text files
    def save_data(self, file_path="expenses.txt"):
        with open(file_path, "w") as file:
            for expense in self.expenses:
                file.write(f"{expense.name}|{expense.amount}|{expense.category}|{expense.timestamp}\n")

        with open("budgets.txt", "w") as file:
            for category, remaining_budget in self.budgets.items():
                file.write(f"{category}|{remaining_budget}\n")

    # Method to load existing data from files
    def load_data(self):
        self.load_expenses()
        self.load_budgets()

    # Method to load expenses from the "expenses.txt" file
    def load_expenses(self):
        if os.path.exists("expenses.txt"):
            with open("expenses.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        name, amount, category, timestamp = parts
                        self.expenses.append(Expense(name, float(amount), category, timestamp))

    # Method to load budgets from the "budgets.txt" file
    def load_budgets(self):
        if os.path.exists("budgets.txt"):
            with open("budgets.txt", "r") as file:
                for line in file:
                    category, remaining_budget = line.strip().split("|")
                    self.budgets[category] = float(remaining_budget)

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.geometry("600x400")
    root.mainloop()

if __name__ == "__main__":
    main()



