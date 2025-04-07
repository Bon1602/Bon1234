import tkinter as tk
from tkinter import messagebox
import openpyxl

def check_credentials(username, password):
    wb = openpyxl.load_workbook("users.xlsx")
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == username and row[1] == password:
            return True
    return False

def show_login_window(on_success):
    login = tk.Tk()
    login.title("Đăng nhập")

    tk.Label(login, text="Tên đăng nhập").grid(row=0, column=0)
    username_entry = tk.Entry(login)
    username_entry.grid(row=0, column=1)

    tk.Label(login, text="Mật khẩu").grid(row=1, column=0)
    password_entry = tk.Entry(login, show="*")
    password_entry.grid(row=1, column=1)

    def login_action():
        u = username_entry.get()
        p = password_entry.get()
        if check_credentials(u, p):
            login.destroy()
            on_success()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")

    tk.Button(login, text="Đăng nhập", command=login_action).grid(row=2, column=0, columnspan=2, pady=10)
    login.mainloop()