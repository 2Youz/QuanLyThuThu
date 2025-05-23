import tkinter as tk
from tkinter import ttk, messagebox
from QuanLy import User
from User_QuanLy import get_all_users, add_user, update_user, delete_user

class GiaoDienQuanLyNguoiDung(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.tao_giao_dien()
        self.tai_lai()

    def tao_giao_dien(self):
        tk.Label(self, text="Tên đăng nhập").place(x=20, y=20)
        tk.Label(self, text="Mật khẩu").place(x=20, y=60)
        tk.Label(self, text="Chức vụ").place(x=20, y=100)

        self.tenDN = tk.StringVar()
        self.matKhau = tk.StringVar()
        self.chucVu = tk.StringVar()

        tk.Entry(self, textvariable=self.tenDN).place(x=120, y=20, width=200)
        tk.Entry(self, textvariable=self.matKhau, show="*").place(x=120, y=60, width=200)

        self.cbChucVu = ttk.Combobox(self, textvariable=self.chucVu, values=["Thủ Thư", "Quản Lý"], state="readonly")
        self.cbChucVu.place(x=120, y=100, width=200)
        self.cbChucVu.set("Thủ Thư")

        tk.Button(self, text="Thêm", command=self.them).place(x=350, y=20, width=100)
        tk.Button(self, text="Sửa", command=self.sua).place(x=350, y=60, width=100)
        tk.Button(self, text="Xóa", command=self.xoa).place(x=350, y=100, width=100)

        self.tree = ttk.Treeview(self, columns=("username", "role"), show="headings")
        self.tree.heading("username", text="Tên đăng nhập")
        self.tree.heading("role", text="Chức vụ")
        self.tree.place(x=20, y=150, width=430, height=250)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def tai_lai(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for user in get_all_users():
            self.tree.insert("", "end", values=(user.username, user.role))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.tenDN.set(values[0])
            self.chucVu.set(values[1])
            self.matKhau.set("")  # không hiển thị mật khẩu

    def them(self):
        try:
            user = User(self.tenDN.get().strip(), self.matKhau.get().strip(), self.chucVu.get())
            if not user.username or not user.password:
                raise ValueError("Tên đăng nhập và mật khẩu không được để trống.")
            if user.username in [u.username for u in get_all_users()]:
                raise ValueError("Tên đăng nhập đã tồn tại.")
            if user.role == "Quản Lý":
                user.permission = True
            add_user(user)
            messagebox.showinfo("Thành công", "Đã thêm người dùng.")
            self.tai_lai()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def sua(self):
        try:
            update_user(self.tenDN.get().strip(), {
                "password": self.matKhau.get().strip(),
                "role": self.chucVu.get()
            })
            messagebox.showinfo("Thành công", "Đã cập nhật người dùng.")
            self.tai_lai()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def xoa(self):
        username = self.tenDN.get().strip()
        if not username:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn người dùng để xóa.")
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{username}' không?"):
            try:
                delete_user(username)
                messagebox.showinfo("Thành công", "Đã xóa người dùng.")
                self.tai_lai()
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x450")
    root.title("Quản lý người dùng")
    app = GiaoDienQuanLyNguoiDung(root)
    app.mainloop()
