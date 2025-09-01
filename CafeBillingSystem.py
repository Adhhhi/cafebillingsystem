import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import datetime

class ScrollableFrame(ttk.Frame):
    """A scrollable frame for item buttons inside tabs."""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=250)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Billing System")
        self.root.geometry("750x800")
        self.root.configure(bg="#f0f4f8")

        self.menu = {
            'Beverages': {'Tea': 120.0, 'Soda': 20.0},
            'Food': {'Sandwich': 250.5, 'Salad': 260.0, 'Pizza': 300.5, 'Maggi': 500.0},
            'Coffee': {'Coffee': 125.5},
            'Others': {'Cake': 350.5}
        }
        self.order = []
        self.customer_name = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Sunny Day Cafe", font=("Helvetica", 24, "bold"),
                 bg="#f0f4f8", fg="#2c3e50").pack(pady=15)

        # Customer name entry
        frame_name = tk.Frame(self.root, bg="#f0f4f8")
        frame_name.pack(pady=10)
        tk.Label(frame_name, text="Customer Name:", font=("Helvetica", 14),
                 bg="#f0f4f8", fg="#34495e").pack(side=tk.LEFT)
        tk.Entry(frame_name, textvariable=self.customer_name, font=("Helvetica", 14),
                 width=30, bd=2, relief="groove").pack(side=tk.LEFT, padx=10)

        # Top frame for notebook and add category button
        top_frame = tk.Frame(self.root, bg="#f0f4f8")
        top_frame.pack(pady=10, fill=tk.X, padx=20)

        self.notebook = ttk.Notebook(top_frame)
        self.notebook.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_add_cat = tk.Button(top_frame, text="Add Category", font=("Helvetica", 12, "bold"),
                                bg="#8e44ad", fg="white", activebackground="#9b59b6",
                                activeforeground="white", relief="raised", bd=3,
                                cursor="hand2", command=self.add_category_dialog)
        btn_add_cat.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        self.add_hover_effect(btn_add_cat, "#8e44ad", "#9b59b6")

        self.tabs = {}
        for cat in self.menu:
            self.add_tab(cat, self.menu[cat])

        # Control buttons
        control_frame = tk.Frame(self.root, bg="#f0f4f8")
        control_frame.pack(pady=15)

        btn_show = tk.Button(control_frame, text="Show Receipt", font=("Helvetica", 14, "bold"),
                             bg="#27ae60", fg="white", activebackground="#2ecc71",
                             activeforeground="white", relief="raised", bd=4, width=15,
                             cursor="hand2", command=self.show_receipt)
        btn_show.pack(side=tk.LEFT, padx=15)
        self.add_hover_effect(btn_show, "#27ae60", "#2ecc71")

        btn_clear = tk.Button(control_frame, text="Clear Order", font=("Helvetica", 14, "bold"),
                              bg="#c0392b", fg="white", activebackground="#e74c3c",
                              activeforeground="white", relief="raised", bd=4, width=15,
                              cursor="hand2", command=self.clear_order)
        btn_clear.pack(side=tk.LEFT, padx=15)
        self.add_hover_effect(btn_clear, "#c0392b", "#e74c3c")

        btn_export = tk.Button(control_frame, text="Export Bill", font=("Helvetica", 14, "bold"),
                               bg="#2980b9", fg="white", activebackground="#3498db",
                               activeforeground="white", relief="raised", bd=4, width=15,
                               cursor="hand2", command=self.export_bill)
        btn_export.pack(side=tk.LEFT, padx=15)
        self.add_hover_effect(btn_export, "#2980b9", "#3498db")

        # Receipt area with scrollbar
        receipt_frame = tk.Frame(self.root, bg="#f0f4f8")
        receipt_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        self.receipt_box = tk.Text(receipt_frame, height=15, width=70, font=("Courier New", 12),
                                   bd=2, relief="sunken", bg="#ecf0f1", fg="#2c3e50", wrap=tk.WORD)
        self.receipt_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(receipt_frame, command=self.receipt_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.receipt_box.config(yscrollcommand=scrollbar.set)

    def add_tab(self, category, items):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=category)
        self.tabs[category] = tab

        scroll_frame = ScrollableFrame(tab)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for item, price in items.items():
            btn = tk.Button(scroll_frame.scrollable_frame, text=f"{item} - Rs.{price:.2f}",
                            width=25, font=("Helvetica", 12), bg="#3498db", fg="white",
                            activebackground="#5dade2", activeforeground="white",
                            relief="raised", bd=3, cursor="hand2",
                            command=lambda i=item: self.add_item(i))
            btn.pack(pady=5)
            self.add_hover_effect(btn, "#3498db", "#5dade2")

    def add_hover_effect(self, widget, color_normal, color_hover):
        def on_enter(e): widget['background'] = color_hover
        def on_leave(e): widget['background'] = color_normal
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def add_item(self, item):
        self.order.append(item)
        messagebox.showinfo("Item Added", f"{item} added to your order.")

    def clear_order(self):
        self.order.clear()
        self.receipt_box.delete(1.0, tk.END)

    def show_receipt(self):
        if not self.order:
            messagebox.showwarning("Empty Order", "Please add some items first.")
            return

        subtotal = 0
        for item in self.order:
            for cat_items in self.menu.values():
                if item in cat_items:
                    subtotal += cat_items[item]
                    break

        tax = subtotal * 0.08
        total = subtotal + tax
        name = self.customer_name.get().strip() or "Guest"

        receipt = f"--- Receipt ---\nCustomer: {name}\n\n"
        counts = {}
        for item in self.order:
            counts[item] = counts.get(item, 0) + 1

        for item, count in counts.items():
            price = None
            for cat_items in self.menu.values():
                if item in cat_items:
                    price = cat_items[item]
                    break
            receipt += f"{item} x{count}: Rs.{price * count:.2f}\n"

        receipt += "\n-------------------------"
        receipt += f"\nSubtotal: Rs.{subtotal:.2f}"
        receipt += f"\nTax (8%): Rs.{tax:.2f}"
        receipt += "\n-------------------------"
        receipt += f"\nTotal: Rs.{total:.2f}"
        receipt += "\n-------------------------"

        self.receipt_box.delete(1.0, tk.END)
        self.receipt_box.insert(tk.END, receipt)

    def export_bill(self):
        content = self.receipt_box.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("No Receipt", "Please generate the receipt before exporting.")
            return

        now = datetime.datetime.now()
        default_filename = f"Bill_{now.strftime('%Y%m%d_%H%M%S')}.txt"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 initialfile=default_filename,
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(content)
                messagebox.showinfo("Export Successful", f"Bill exported successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export bill:\n{e}")

    def add_category_dialog(self):
        category_name = simpledialog.askstring("Add Category", "Enter new category name:", parent=self.root)
        if not category_name:
            return
        category_name = category_name.strip()
        if category_name == "":
            messagebox.showerror("Invalid Name", "Category name cannot be empty.")
            return
        if category_name in self.menu:
            messagebox.showerror("Duplicate Category", f"Category '{category_name}' already exists.")
            return

        new_items = {}
        while True:
            item_name = simpledialog.askstring("Add Item", "Enter item name (Cancel to stop):", parent=self.root)
            if not item_name:
                break
            item_name = item_name.strip()
            if item_name == "":
                messagebox.showerror("Invalid Name", "Item name cannot be empty.")
                continue
            if item_name in new_items:
                messagebox.showerror("Duplicate Item", f"Item '{item_name}' already added.")
                continue

            while True:
                price_str = simpledialog.askstring("Add Item Price", f"Enter price for '{item_name}':", parent=self.root)
                if price_str is None:
                    item_name = None
                    break
                price_str = price_str.strip()
                try:
                    price = float(price_str)
                    if price < 0:
                        raise ValueError
                    break
                except ValueError:
                    messagebox.showerror("Invalid Price", "Please enter a valid positive number for price.")
            if item_name is None:
                continue
            new_items[item_name] = price

        if not new_items:
            messagebox.showinfo("No Items", "No items were added. Category not created.")
            return

        self.menu[category_name] = new_items
        self.add_tab(category_name, new_items)
        self.notebook.select(self.tabs[category_name])
        messagebox.showinfo("Category Added", f"Category '{category_name}' added with {len(new_items)} items.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeBillingSystem(root)
    root.mainloop()
