import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import json
import os
from datetime import datetime

# Module database
class Database:
    def __init__(self):
        self.invoices_file = "invoices.json"
        self.transactions_file = "transactions.json"
        self.inventory_file = "inventory.json"
        
    def create_files(self):
        """Tạo file JSON nếu chưa tồn tại"""
        for file in [self.invoices_file, self.transactions_file, self.inventory_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump([], f)
    
    # Các hàm xử lý hóa đơn
    def add_invoice(self, customer, total):
        invoices = self._read_data(self.invoices_file)
        invoice_id = len(invoices) + 1
        new_invoice = {
            "id": invoice_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer": customer,
            "total": total
        }
        invoices.append(new_invoice)
        self._write_data(self.invoices_file, invoices)
    
    def get_invoices(self):
        return self._read_data(self.invoices_file)
    
    def search_invoices(self, keyword="", start_date="", end_date=""):
        invoices = self.get_invoices()
        results = []
        
        for inv in invoices:
            # Kiểm tra keyword
            keyword_match = not keyword or keyword.lower() in inv["customer"].lower()
            
            # Kiểm tra ngày
            date_match = True
            if start_date:
                date_match &= inv["date"] >= start_date
            if end_date:
                date_match &= inv["date"] <= end_date + " 23:59:59"
            
            if keyword_match and date_match:
                results.append((inv["id"], inv["date"], inv["customer"], inv["total"]))
        
        return results
    
    # Các hàm xử lý giao dịch
    def add_transaction(self, t_type, amount, description):
        transactions = self._read_data(self.transactions_file)
        trans_id = len(transactions) + 1
        new_trans = {
            "id": trans_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": t_type,
            "amount": amount,
            "description": description
        }
        transactions.append(new_trans)
        self._write_data(self.transactions_file, transactions)
    
    def get_transactions(self):
        return self._read_data(self.transactions_file)
    
    def search_transactions(self, t_type="", keyword="", start_date="", end_date=""):
        transactions = self.get_transactions()
        results = []
        
        for trans in transactions:
            # Kiểm tra loại giao dịch
            type_match = not t_type or trans["type"].lower() == t_type.lower()
            
            # Kiểm tra keyword
            keyword_match = not keyword or keyword.lower() in trans["description"].lower()
            
            # Kiểm tra ngày
            date_match = True
            if start_date:
                date_match &= trans["date"] >= start_date
            if end_date:
                date_match &= trans["date"] <= end_date + " 23:59:59"
            
            if type_match and keyword_match and date_match:
                results.append((
                    trans["id"], 
                    trans["date"], 
                    trans["type"], 
                    trans["amount"], 
                    trans["description"]
                ))
        
        return results
    
    # Các hàm thống kê
    def get_inventory_summary(self):
        # Giả lập dữ liệu tồn kho
        return 150, 45000000  # (số lượng, giá trị)
    
    def get_sales_summary(self):
        invoices = self.get_invoices()
        return sum(inv["total"] for inv in invoices)
    
    def get_accounting_summary(self):
        transactions = self.get_transactions()
        income = sum(t["amount"] for t in transactions if t["type"].lower() == "thu")
        expense = sum(t["amount"] for t in transactions if t["type"].lower() == "chi")
        return income, expense
    
    # Hàm hỗ trợ
    def _read_data(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)
    
    def _write_data(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# Tạo instance database toàn cục
database = Database()

# Phần GUI (giữ nguyên như code trước)
class MisaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm quản lý bán hàng Misa")
        self.root.geometry("1000x700")
        
        # Cấu hình style
        self.configure_styles()
        
        # Tạo notebook (tabs)
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Xây dựng các tab
        self.build_sales_tab()
        self.build_accounting_tab()
        self.build_statistics_tab()
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.default_font = Font(family="Helvetica", size=10)
        self.title_font = Font(family="Helvetica", size=12, weight="bold")
        self.mono_font = Font(family="Consolas", size=10)
        
        style.configure('TNotebook.Tab', font=self.title_font, padding=[10, 5])
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', font=self.default_font, padding=5)
        style.configure('TLabel', font=self.default_font, background='#f0f0f0')
        style.configure('Treeview', font=self.mono_font, rowheight=25)
        style.configure('Treeview.Heading', font=self.default_font)
        style.map('TButton', foreground=[('active', 'black')], background=[('active', '#e6e6e6')])
    
    def get_products(self):
        return self._read_data(self.inventory_file)
    
    def add_product(self, name, quantity, price):
        products = self._read_data(self.inventory_file)
        new_id = max([p['id'] for p in products], default=0) + 1
        products.append({
            "id": new_id,
            "name": name,
            "quantity": quantity,
            "price": price
        })
        self._write_data(self.inventory_file, products)
        return new_id
    
    def update_product(self, product_id, name=None, quantity=None, price=None):
        products = self._read_data(self.inventory_file)
        for product in products:
            if product['id'] == product_id:
                if name is not None:
                    product['name'] = name
                if quantity is not None:
                    product['quantity'] = quantity
                if price is not None:
                    product['price'] = price
                self._write_data(self.inventory_file, products)
                return True
        return False
    
    def delete_product(self, product_id):
        products = self._read_data(self.inventory_file)
        products = [p for p in products if p['id'] != product_id]
        self._write_data(self.inventory_file, products)
    
    def search_products(self, keyword=""):
        products = self.get_products()
        if not keyword:
            return products
        
        results = []
        for product in products:
            if keyword.lower() in product['name'].lower():
                results.append(product)
        return results
    
    def get_inventory_summary(self):
        products = self.get_products()
        total_quantity = sum(p['quantity'] for p in products)
        total_value = sum(p['quantity'] * p['price'] for p in products)
        return total_quantity, total_value
    
    def build_sales_tab(self):
        self.sales_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.sales_tab, text="Bán hàng")
        
        form_frame = ttk.LabelFrame(self.sales_tab, text="Tạo hóa đơn mới", padding=(15, 10))
        form_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ttk.Label(form_frame, text="Khách hàng:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.customer_entry = ttk.Entry(form_frame, width=30)
        self.customer_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Tổng tiền:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.total_entry = ttk.Entry(form_frame, width=30)
        self.total_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn_frame, text="Tạo hóa đơn", command=self.add_invoice, style='Accent.TButton').pack(pady=5)
        
        tree_frame = ttk.LabelFrame(self.sales_tab, text="Danh sách hóa đơn", padding=(15, 10))
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.invoice_tree = ttk.Treeview(tree_frame, columns=("ID", "Ngày", "Khách", "Tổng"), show="headings")
        self.invoice_tree.pack(fill="both", expand=True)
        
        self.invoice_tree.column("ID", width=50, anchor="center")
        self.invoice_tree.column("Ngày", width=120, anchor="center")
        self.invoice_tree.column("Khách", width=200)
        self.invoice_tree.column("Tổng", width=100, anchor="e")
        
        for col in ("ID", "Ngày", "Khách", "Tổng"):
            self.invoice_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.invoice_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        search_frame = ttk.LabelFrame(self.sales_tab, text="Tìm kiếm hóa đơn", padding=(15, 10))
        search_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        ttk.Label(search_frame, text="Khách hàng:").grid(row=0, column=0, padx=5, pady=5)
        self.invoice_search_entry = ttk.Entry(search_frame, width=20)
        self.invoice_search_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Từ ngày:").grid(row=0, column=2, padx=5, pady=5)
        self.invoice_start_entry = ttk.Entry(search_frame, width=12)
        self.invoice_start_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Đến ngày:").grid(row=0, column=4, padx=5, pady=5)
        self.invoice_end_entry = ttk.Entry(search_frame, width=12)
        self.invoice_end_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(search_frame, text="Lọc", command=self.filter_invoices).grid(row=0, column=6, padx=10, pady=5)
        
        self.load_invoices()
    
    def build_accounting_tab(self):
        self.accounting_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.accounting_tab, text="Kế toán")
        
        form_frame = ttk.LabelFrame(self.accounting_tab, text="Thêm giao dịch mới", padding=(15, 10))
        form_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ttk.Label(form_frame, text="Loại giao dịch:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.type_entry = ttk.Combobox(form_frame, values=["Thu", "Chi"], width=27)
        self.type_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Số tiền:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = ttk.Entry(form_frame, width=30)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Mô tả:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn_frame, text="Thêm giao dịch", command=self.add_transaction, style='Accent.TButton').pack(pady=5)
        
        tree_frame = ttk.LabelFrame(self.accounting_tab, text="Danh sách giao dịch", padding=(15, 10))
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.trans_tree = ttk.Treeview(tree_frame, columns=("ID", "Ngày", "Loại", "Số tiền", "Mô tả"), show="headings")
        self.trans_tree.pack(fill="both", expand=True)
        
        self.trans_tree.column("ID", width=50, anchor="center")
        self.trans_tree.column("Ngày", width=120, anchor="center")
        self.trans_tree.column("Loại", width=80, anchor="center")
        self.trans_tree.column("Số tiền", width=120, anchor="e")
        self.trans_tree.column("Mô tả", width=250)
        
        for col in ("ID", "Ngày", "Loại", "Số tiền", "Mô tả"):
            self.trans_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.trans_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.trans_tree.configure(yscrollcommand=scrollbar.set)
        
        search_frame = ttk.LabelFrame(self.accounting_tab, text="Tìm kiếm giao dịch", padding=(15, 10))
        search_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        ttk.Label(search_frame, text="Loại:").grid(row=0, column=0, padx=5, pady=5)
        self.trans_type_filter = ttk.Combobox(search_frame, values=["", "Thu", "Chi"], width=8)
        self.trans_type_filter.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Từ ngày:").grid(row=0, column=2, padx=5, pady=5)
        self.trans_start_entry = ttk.Entry(search_frame, width=12)
        self.trans_start_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Đến ngày:").grid(row=0, column=4, padx=5, pady=5)
        self.trans_end_entry = ttk.Entry(search_frame, width=12)
        self.trans_end_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Từ khóa:").grid(row=0, column=6, padx=5, pady=5)
        self.trans_keyword_entry = ttk.Entry(search_frame, width=20)
        self.trans_keyword_entry.grid(row=0, column=7, padx=5, pady=5)
        
        ttk.Button(search_frame, text="Lọc", command=self.filter_transactions).grid(row=0, column=8, padx=10, pady=5)
        
        self.load_transactions()
    
    def build_statistics_tab(self):
        self.stats_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.stats_tab, text="Thống kê")
        
        btn_frame = ttk.Frame(self.stats_tab)
        btn_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ttk.Button(btn_frame, text="Làm mới thống kê", command=self.load_statistics, style='Accent.TButton').pack(pady=5)
        
        stats_frame = ttk.LabelFrame(self.stats_tab, text="Thống kê tổng quan", padding=(15, 10))
        stats_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=15, width=70, font=self.mono_font, 
                                bg='white', padx=10, pady=10, wrap=tk.WORD)
        self.stats_text.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        
        self.load_statistics()
    
    def filter_invoices(self):
        keyword = self.invoice_search_entry.get()
        start_date = self.invoice_start_entry.get()
        end_date = self.invoice_end_entry.get()

        results = database.search_invoices(keyword, start_date, end_date)

        self.invoice_tree.delete(*self.invoice_tree.get_children())
        for row in results:
            self.invoice_tree.insert("", "end", values=row)

    def add_invoice(self):
        customer = self.customer_entry.get()
        total = self.total_entry.get()
        if customer and total:
            try:
                total = float(total)
                database.add_invoice(customer, total)
                messagebox.showinfo("Thành công", "Hóa đơn đã được tạo thành công!")
                self.load_invoices()
                self.customer_entry.delete(0, tk.END)
                self.total_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Lỗi", "Tổng tiền phải là số hợp lệ!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin khách hàng và tổng tiền!")

    def load_invoices(self):
        for row in self.invoice_tree.get_children():
            self.invoice_tree.delete(row)
        for invoice in database.get_invoices():
            self.invoice_tree.insert("", "end", values=(
                invoice["id"],
                invoice["date"],
                invoice["customer"],
                f"{invoice['total']:,.0f} VND"
            ))

    def filter_transactions(self):
        t_type = self.trans_type_filter.get()
        keyword = self.trans_keyword_entry.get()
        start = self.trans_start_entry.get()
        end = self.trans_end_entry.get()

        results = database.search_transactions(t_type, keyword, start, end)

        self.trans_tree.delete(*self.trans_tree.get_children())
        for row in results:
            self.trans_tree.insert("", "end", values=row)

    def add_transaction(self):
        t_type = self.type_entry.get()
        amount = self.amount_entry.get()
        desc = self.desc_entry.get()
        if t_type and amount and desc:
            try:
                amount = float(amount)
                database.add_transaction(t_type, amount, desc)
                messagebox.showinfo("Thành công", "Giao dịch đã được thêm thành công!")
                self.load_transactions()
                self.type_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Lỗi", "Số tiền phải là số hợp lệ!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin giao dịch!")

    def load_transactions(self):
        for row in self.trans_tree.get_children():
            self.trans_tree.delete(row)
        for trans in database.get_transactions():
            self.trans_tree.insert("", "end", values=(
                trans["id"],
                trans["date"],
                trans["type"],
                f"{trans['amount']:,.0f} VND",
                trans["description"]
            ))

    def load_statistics(self):
        inventory_qty, inventory_value = database.get_inventory_summary()
        sales_total = database.get_sales_summary()
        income, expense = database.get_accounting_summary()

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "═"*50 + " TỒN KHO " + "═"*50 + "\n\n")
        self.stats_text.insert(tk.END, f" • Tổng số lượng: {inventory_qty}\n")
        self.stats_text.insert(tk.END, f" • Tổng giá trị:  {inventory_value:,.0f} VND\n\n")
        
        self.stats_text.insert(tk.END, "═"*50 + " DOANH THU " + "═"*47 + "\n\n")
        self.stats_text.insert(tk.END, f" • Tổng doanh thu: {sales_total:,.0f} VND\n\n")
        
        self.stats_text.insert(tk.END, "═"*50 + " KẾ TOÁN " + "═"*49 + "\n\n")
        self.stats_text.insert(tk.END, f" • Tổng THU:       {income:,.0f} VND\n")
        self.stats_text.insert(tk.END, f" • Tổng CHI:       {expense:,.0f} VND\n")
        self.stats_text.insert(tk.END, f" • CHÊNH LỆCH:    {income - expense:,.0f} VND\n")
        
        balance = income - expense
        self.stats_text.tag_configure("positive", foreground="green")
        self.stats_text.tag_configure("negative", foreground="red")
        
        last_line_start = self.stats_text.search("CHÊNH LỆCH:", "1.0", stopindex=tk.END)
        last_line_end = last_line_start + " + 1 line"
        
        if balance >= 0:
            self.stats_text.tag_add("positive", last_line_start, last_line_end)
        else:
            self.stats_text.tag_add("negative", last_line_start, last_line_end)

if __name__ == "__main__":
    # Khởi tạo database
    database = Database()
    database.create_files()
    
    root = tk.Tk()
    
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'), foreground='white', background='#4a6baf')
    style.map('Accent.TButton', 
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '#3a5a9f'), ('active', '#5a7bbf')])
    
    app = MisaApp(root)
    root.mainloop()