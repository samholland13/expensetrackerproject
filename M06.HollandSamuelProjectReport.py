import tkinter as tk
from tkinter import messagebox, ttk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Sam's Personal Finance")

        # Variables
        self.expenses = []
        self.load_expenses()

        # GUI components
        self.label = tk.Label(root, text="Expense Tracker", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.expense_entry = tk.Entry(root, width=30)
        self.expense_entry.pack(pady=5)

        self.amount_entry = tk.Entry(root, width=10)
        self.amount_entry.pack(pady=5)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.pack(pady=5)

        self.category_combobox = ttk.Combobox(root, values=["General", "Groceries", "Utilities", "Entertainment"])
        self.category_combobox.pack(pady=5)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=5)

        self.show_expenses_button = tk.Button(root, text="Show Expenses", command=self.show_expenses)
        self.show_expenses_button.pack(pady=5)

        self.show_graph_button = tk.Button(root, text="Show Graph", command=self.show_graph)
        self.show_graph_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Quit", command=root.destroy)
        self.quit_button.pack(pady=10)

    def add_expense(self):
        expense = self.expense_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combobox.get()

        if expense and amount and category:
            self.expenses.append({"expense": expense, "amount": float(amount), "category": category})
            self.expense_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.save_expenses()
            messagebox.showinfo("Sam's Personal Finance", "Expense added successfully.")
        else:
            messagebox.showwarning("Sam's Personal Finance", "Please enter an expense, amount, and select a category.")

    def show_expenses(self):
        total_amount = sum(expense["amount"] for expense in self.expenses)

        expenses_window = tk.Toplevel(self.root)
        expenses_window.title("Expenses")

        for expense in self.expenses:
            expense_label = tk.Label(expenses_window,
                                     text=f"{expense['expense']}: ${expense['amount']:.2f} ({expense['category']})")
            expense_label.pack(pady=5)

            edit_button = tk.Button(expenses_window, text="Edit", command=lambda exp=expense: self.edit_expense(exp))
            edit_button.pack(pady=2)

            delete_button = tk.Button(expenses_window, text="Delete",
                                      command=lambda exp=expense: self.delete_expense(exp))
            delete_button.pack(pady=2)

    def edit_expense(self, expense):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")

        tk.Label(edit_window, text="Edit Expense").grid(row=0, column=0, columnspan=2)

        tk.Label(edit_window, text="Expense:").grid(row=1, column=0, sticky=tk.E)
        tk.Entry(edit_window, textvariable=tk.StringVar(value=expense["expense"]), state="readonly").grid(row=1,
                                                                                                          column=1)

        tk.Label(edit_window, text="Amount:").grid(row=2, column=0, sticky=tk.E)
        tk.Entry(edit_window, textvariable=tk.DoubleVar(value=expense["amount"])).grid(row=2, column=1)

        tk.Label(edit_window, text="Category:").grid(row=3, column=0, sticky=tk.E)
        tk.Entry(edit_window, textvariable=tk.StringVar(value=expense["category"])).grid(row=3, column=1)

        tk.Button(edit_window, text="Save", command=lambda: self.save_edited_expense(expense, edit_window)).grid(row=4,
                                                                                                                 column=0,
                                                                                                                 columnspan=2)

    def save_edited_expense(self, original_expense, edit_window):
        new_expense = {
            "expense": original_expense["expense"],
            "amount": float(edit_window.children['!entry2'].get()),
            "category": edit_window.children['!entry4'].get()
        }
        self.expenses.remove(original_expense)
        self.expenses.append(new_expense)
        self.save_expenses()
        edit_window.destroy()
        messagebox.showinfo("Sam's Personal Finance", "Expense edited successfully.")

    def delete_expense(self, expense):
        self.expenses.remove(expense)
        self.save_expenses()
        messagebox.showinfo("Sam's Personal Finance", f"Expense '{expense['expense']}' deleted successfully.")

    def show_graph(self):
        categories = set(expense["category"] for expense in self.expenses)
        category_totals = {
            category: sum(expense["amount"] for expense in self.expenses if expense["category"] == category) for
            category in categories}

        plt.figure(figsize=(8, 6))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category")

        # Embed the Matplotlib plot in the Tkinter window
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Expense Distribution Graph")

        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = tk.Frame(graph_window)
        toolbar.pack()

        tk.Button(toolbar, text="Close", command=graph_window.destroy).pack(side=tk.LEFT)

        plt.show()

    def save_expenses(self):
        with open("expenses.txt", "w") as file:
            for expense in self.expenses:
                file.write(f"{expense['expense']}|{expense['amount']}|{expense['category']}\n")

    def load_expenses(self):
        if os.path.exists("expenses.txt"):
            with open("expenses.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        expense, amount, category = parts
                        self.expenses.append({"expense": expense, "amount": float(amount), "category": category})


def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()



