import tkinter as tk
from tkinter import messagebox, ttk
from QuanLy import User
from GiaoDien_Chinh import GiaoDienChinh

class GiaoDienDangNhap(tk.Frame):
    def __init__(self, master, kiemTraQuyen):
        super().__init__(master)
        self.master = master
        self.kiemTraQuyen = kiemTraQuyen  # Hàm kiểm tra quyền truy cập
        self.master.title("Đăng Nhập")
        self.GiaoDien()

    def GiaoDien(self):
        # Kích thước cửa sổ
        form_width = 400
        form_height = 400
        
        # Thiết lập kích thước cửa sổ
        self.master.geometry(f"{form_width}x{form_height}")
        
        # Căn giữa cửa sổ trên màn hình
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - form_width) // 2
        y = (screen_height - form_height) // 2
        self.master.geometry(f"{form_width}x{form_height}+{x}+{y}")
        
        # Không cho phép thay đổi kích thước
        self.master.resizable(False, False)
        
        # Đặt frame chiếm toàn bộ cửa sổ
        self.pack(fill="both", expand=True)
        
        # Tọa độ bắt đầu cho các widget (tương đối với frame)
        startX = 50
        startY = 50

        # Tiêu đề
        tk.Label(
            self, text="Đăng Nhập",
            font=("Arial", 20, "bold"),
            anchor="center"
        ).place(x=0, y=startY, width=form_width, height=30)

        # Tên đăng nhập - label
        tk.Label(self, text="Tên đăng nhập:", anchor="w").place(
            x=startX, y=startY + 60, width=300, height=20
        )

        # Tên đăng nhập - entry
        self.tendn = tk.StringVar()
        self.nhapTenDN = tk.Entry(self, textvariable=self.tendn, width=30)
        self.nhapTenDN.place(x=startX, y=startY + 90, width=300, height=30)

        # Mật khẩu - label
        tk.Label(self, text="Mật khẩu:", anchor="w").place(
            x=startX, y=startY + 130, width=300, height=20
        )

        # Mật khẩu - entry
        self.matkhau = tk.StringVar()
        self.nhapMK = tk.Entry(self, textvariable=self.matkhau, width=30, show="*")
        self.nhapMK.place(x=startX, y=startY + 160, width=300, height=30)

        # Chức vụ - label
        tk.Label(self, text="Chức vụ:", anchor="w").place(
            x=startX, y=startY + 200, width=300, height=20
        )

        # Chức vụ - combobox
        self.chucvu = tk.StringVar()
        self.cbChucVu = ttk.Combobox(
            self, textvariable=self.chucvu,
            values=["Thủ Thư", "Quản Lý"],
            state="readonly"
        )
        self.cbChucVu.place(x=startX, y=startY + 230, width=300, height=30)
        self.cbChucVu.set("Thủ Thư")  # Giá trị mặc định

        # Nút đăng nhập
        tk.Button(
            self, text="Đăng nhập",
            command=self.DangNhap,
            bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold")
        ).place(x=startX + 50, y=startY + 280, width=200, height=35)
        # Focus
        self.nhapTenDN.focus()

        # Binding Enter key
        self.nhapTenDN.bind("<Tab>", lambda event: self.nhapMK.focus())
        self.nhapMK.bind("<Tab>", lambda event: self.cbChucVu.focus())
        self.cbChucVu.bind("<Return>", lambda event: self.DangNhap())

    def DangNhap(self):  # Hàm đăng nhập
        username = self.tendn.get().strip()
        password = self.matkhau.get()
        role = self.chucvu.get()

        if not username or not password:    
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        user = self.kiemTraQuyen(username, password, role)
        if user:    
            messagebox.showinfo("Thành công", f"Đăng nhập thành công với vai trò: {role}")

        # Ẩn cửa sổ đăng nhập
            self.master.withdraw()

        # Tạo cửa sổ mới là giao diện chính
            new_win = tk.Toplevel(self.master)
            new_win.geometry("1000x600")
            new_win.title("Giao diện chính")

            app = GiaoDienChinh(new_win, user)
            app.pack(fill="both", expand=True)

        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập, mật khẩu hoặc vai trò không chính xác")
