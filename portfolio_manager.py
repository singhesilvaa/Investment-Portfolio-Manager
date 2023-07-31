import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import json

class InvestmentPortfolioManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Portfolio Manager")
        
        self.investments = self.load_data()

        # Add StringVar variables for amount and buying price fields
        self.amount_var = tk.StringVar()
        self.buying_price_var = tk.StringVar()

        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):
        # Investment Entry Frame
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(padx=10, pady=5, anchor="w")

        investment_type_label = tk.Label(entry_frame, text="Investment Type:")
        investment_type_label.grid(row=0, column=0)

        self.investment_type_var = tk.StringVar()
        investment_type_combobox = ttk.Combobox(entry_frame, textvariable=self.investment_type_var, values=["Stocks", "Bonds", "Real Estate", "Mutual Funds", "Other"], width=12)
        investment_type_combobox.grid(row=0, column=1)

        amount_label = tk.Label(entry_frame, text="Amount:")
        amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(entry_frame, textvariable=self.amount_var, width=15)  # Use StringVar for amount entry
        self.amount_entry.grid(row=1, column=1)

        buying_price_label = tk.Label(entry_frame, text="Buying Price:")
        buying_price_label.grid(row=2, column=0)
        self.buying_price_entry = tk.Entry(entry_frame, textvariable=self.buying_price_var, width=15)  # Use StringVar for buying price entry
        self.buying_price_entry.grid(row=2, column=1)

        transaction_date_label = tk.Label(entry_frame, text="Transaction Date:")
        transaction_date_label.grid(row=3, column=0)

        # Use DateEntry from tkcalendar for the date picker
        self.transaction_date_entry = DateEntry(entry_frame, date_pattern="YYYY-MM-DD", width=12)
        self.transaction_date_entry.grid(row=3, column=1)

        add_button = tk.Button(entry_frame, text="Add Investment", command=self.add_investment, padx=1, pady=1, width=15)
        add_button.grid(row=4, column=0, columnspan=2)

        # Investments List Frame
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=10, pady=5, anchor="w")

        self.investments_listbox = tk.Listbox(list_frame, height=10, selectmode=tk.SINGLE)
        self.investments_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.investments_listbox.bind("<<ListboxSelect>>", self.on_investment_selected)  # Bind the selection event

        scrollbar = tk.Scrollbar(list_frame, command=self.investments_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.investments_listbox.config(yscrollcommand=scrollbar.set)

        # Add a label or text widget to display investment details
        self.investment_details_label = tk.Label(list_frame, text="Select an investment \n to view details:", padx=5, pady=10)
        self.investment_details_label.pack()

        # Remove List item
        remove_button = tk.Button(entry_frame, text="Remove Investment", command=self.remove_investment, padx=1, pady=1, width=15)
        remove_button.grid(row=5, column=0, columnspan=2)

        # Filter Frame
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(padx=10, pady=5, anchor="w")

        filter_label = tk.Label(filter_frame, text="Filter Investments:")
        filter_label.grid(row=0, column=0)

        self.filter_type_var = tk.StringVar()
        filter_type_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["All", "Stocks", "Bonds", "Real Estate", "Mutual Funds", "Other"], width=12)
        filter_type_combobox.grid(row=0, column=1)
        filter_type_combobox.set("All")
        filter_type_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

        self.filter_date_var = tk.StringVar()
        filter_date_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_date_var, values=["All", "Last 7 Days", "Last 30 Days", "Last 90 Days"], width=12)
        filter_date_combobox.grid(row=0, column=2)
        filter_date_combobox.set("All")
        filter_date_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

        # Metrics Frame
        metrics_frame = tk.Frame(self.root)
        metrics_frame.pack(padx=10, pady=5, anchor="w")

        self.metrics_label = tk.Label(metrics_frame, text="Portfolio Metrics:")
        self.metrics_label.pack()

        self.update_metrics()

    def add_investment(self):
        investment_type = self.investment_type_var.get()
        amount_str = self.amount_var.get()
        buying_price_str = self.buying_price_var.get()
        transaction_date_str = self.transaction_date_entry.get()

        if investment_type and amount_str and buying_price_str and transaction_date_str:
            try:
                amount = float(amount_str)
                buying_price = float(buying_price_str)
                mount_str = "{:.2f}".format(amount)  # Format to display cents
                buying_price_str = "{:.2f}".format(buying_price)  # Format to display cents
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric value. Please enter valid numeric data for amount and buying price.")
                return
        
            try:
                transaction_date = datetime.strptime(transaction_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return
            
            new_investment = {
                "type": investment_type,
                "amount": amount,
                "buying_price": buying_price,
                "transaction_date": transaction_date.strftime("%Y-%m-%d")
            }

            self.investments.append(new_investment)
            self.update_listbox()
            self.update_metrics()

            # Clear the entries
            self.amount_entry.delete(0, tk.END)
            self.buying_price_entry.delete(0, tk.END)
            self.transaction_date_entry.set_date(datetime.now())

            # Clear the StringVar variables
            self.amount_var.set("")
            self.buying_price_var.set("")

            self.save_data()
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")

    def remove_investment(self):
        selected_index = self.investments_listbox.curselection()
        if selected_index:
            self.investments.pop(selected_index[0])
            self.update_listbox()
            self.update_metrics()
            self.save_data()
        else:
            messagebox.showerror("Error", "Please select an investment to remove.")

    def update_listbox(self):
        self.investments_listbox.delete(0, tk.END)
        for investment in self.investments:
            self.investments_listbox.insert(tk.END, investment["type"])

    def clear_entries(self):
        self.investment_type_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.buying_price_entry.delete(0, tk.END)
        self.transaction_date_entry.delete(0, tk.END)

    def apply_filter(self, event):
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_var.get()

        if filter_type == "All" and filter_date == "All":
            # If both filter options are "All", display all investments
            self.investments = self.load_data()
        else:
            filtered_investments = []

            for investment in self.load_data():
                if (filter_type == "All" or investment["type"] == filter_type) and \
                    (filter_date == "All" or self.check_date_within_range(investment["transaction_date"], filter_date)):
                    filtered_investments.append(investment)

            self.investments = filtered_investments

        self.update_listbox()
        self.update_metrics()

    def check_date_within_range(self, transaction_date_str, filter_date):
        today = datetime.today().date()
        transaction_date = datetime.strptime(transaction_date_str, "%Y-%m-%d").date()

        if filter_date == "Last 7 Days":
            delta = today - transaction_date
            return delta.days <= 7
        elif filter_date == "Last 30 Days":
            delta = today - transaction_date
            return delta.days <= 30
        elif filter_date == "Last 90 Days":
            delta = today - transaction_date
            return delta.days <= 90

        return False

    def update_metrics(self):
        total_investment_value = sum(investment["amount"] * investment["buying_price"] for investment in self.investments)
        total_investment_cost = sum(investment["amount"] * investment["buying_price"] for investment in self.investments)
        total_returns = total_investment_value - total_investment_cost
        percentage_returns = (total_returns / total_investment_cost) * 100 if total_investment_cost != 0 else 0

        # Calculate diversification percentages for all investment types
        diversification_percentages = {}
        total_investment_amount = sum(investment["amount"] for investment in self.investments)

        for investment in self.investments:
            investment_type = investment["type"]
            investment_amount = investment["amount"]
            percentage = (investment_amount / total_investment_amount) * 100
            diversification_percentages[investment_type] = "{:.2f}".format(percentage)

        # Include investment types with 0% diversification if not present in self.investments
        all_investment_types = {"Stocks", "Bonds", "Real Estate", "Mutual Funds", "Other"}
        for investment_type in all_investment_types:
            diversification_percentages.setdefault(investment_type, 0)

        self.metrics_label.config(text=f"Portfolio Metrics:\n"
                                    f"Total Investment Value: ${total_investment_value:.2f}\n"
                                    f"Total Returns: ${total_returns:.2f}\n"
                                    f"Percentage Returns: {percentage_returns:.2f}%\n"
                                    f"Diversification: {diversification_percentages}")

    def load_data(self):
        try:
            with open("investments.json", "r") as file:
                investments = json.load(file)
                # Validate and remove invalid investments
                valid_investments = []
                for investment in investments:
                    try:
                        investment["amount"] = float(investment["amount"])
                        investment["buying_price"] = float(investment["buying_price"])
                        valid_investments.append(investment)
                    except ValueError:
                        # Handle invalid float values (e.g., non-numeric strings)
                        print(f"Warning: Invalid investment data for {investment['type']}. Skipping...")
                        # You can choose to remove the invalid data or handle it in some other way
                return valid_investments
        except FileNotFoundError:
            return []

    def save_data(self):
        with open("investments.json", "w") as file:
            json.dump(self.investments, file)

    # Implement the remove_investment method
    def remove_investment(self):
        selected_index = self.investments_listbox.curselection()
        if selected_index:
            index_to_remove = selected_index[0]
            self.investments.pop(index_to_remove)
            self.update_listbox()
            self.update_metrics()
            self.save_data()
        else:
            messagebox.showerror("Error", "Please select an investment to remove.")

    def on_investment_selected(self, event):
        selected_index = self.investments_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_investment = self.investments[index]

            # Update the investment details label with the selected investment's information
            investment_type = selected_investment["type"]
            amount = selected_investment["amount"]
            buying_price = selected_investment["buying_price"]
            transaction_date = selected_investment["transaction_date"]

            details_text = (
                f"Investment Type: {investment_type}\n"
                f"Amount: {amount:.2f}\n"
                f"Buying Price: {buying_price:.2f}\n"
                f"Transaction Date: {transaction_date}"
            )

            self.investment_details_label.config(text=details_text)

        else:
            # If no investment is selected, display a default message
            self.investment_details_label.config(text="Select an investment to view details:")

def main():
    root = tk.Tk()
    app = InvestmentPortfolioManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
