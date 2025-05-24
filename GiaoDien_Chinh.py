import tkinter as tk
from tkinter import Frame, Label, Button
from GiaoDien_QuanLyNguoiDung import GiaoDienQuanLyNguoiDung
from GiaoDien_QuanLySach import GiaoDienQuanLySach

class GiaoDienChinh(tk.Frame):
    def __init__(self, master, user_login):
        super().__init__(master)
        self.master = master
        self.user_login = user_login
        self.master.title("Quản lý thư viện")
        self.master.geometry("1200x700")
        self.pack(fill="both", expand=True)
        
        # Sidebar trái (cố định)
        self.sidebar = Frame(self, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Label chào mừng
        welcome_label = Label(
            self.sidebar, 
            text=f"Chào {self.user_login.username}", 
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=20
        )
        welcome_label.pack(fill="x", padx=10, pady=(20, 10))

        # Menu buttons
        self.create_menu_buttons()
        
        # Khung chính (màu trắng)
        self.khungChinh = Frame(self, bg="white", relief="ridge", bd=2)
        self.khungChinh.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Hiển thị welcome message ban đầu
        self.hien_thi_welcome()

    def create_menu_buttons(self):
        """Tạo các nút menu"""
        # Nút quản lý sách (cho tất cả user)
        btn_sach = Button(
            self.sidebar,
            text="📚 Quản lý sách",
            command=self.mo_quan_ly_sach,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            pady=10
        )
        btn_sach.pack(fill="x", padx=10, pady=5)
        
        # Nút quản lý user (chỉ admin)
        if self.user_login.permission:
            btn_user = Button(
                self.sidebar,
                text="👤 Quản lý User",
                command=self.mo_quan_ly_user,
                bg="#e74c3c",
                fg="white",
                font=("Arial", 10),
                relief="flat",
                pady=10
            )
            btn_user.pack(fill="x", padx=10, pady=5)
            
        # Các nút khác
        buttons = [
            ("📖 Mượn/Trả sách", self.mo_muon_tra, "#9b59b6"),
            ("📊 Báo cáo", self.mo_bao_cao, "#f39c12"),
            ("⚙️ Cài đặt", self.mo_cai_dat, "#95a5a6")
        ]
        
        for text, command, color in buttons:
            btn = Button(
                self.sidebar,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 10),
                relief="flat",
                pady=10
            )
            btn.pack(fill="x", padx=10, pady=2)

    def hien_thi_welcome(self):
        """Hiển thị thông điệp chào mừng"""
        self.xoa_noi_dung_chinh()
        welcome_label = Label(
            self.khungChinh,
            text="🏛️ Chào mừng đến với Hệ thống Quản lý Thư viện",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2c3e50",
            pady=50
        )
        welcome_label.pack()
        
        info_label = Label(
            self.khungChinh,
            text=f"Đăng nhập với quyền: {self.user_login.role}",
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d"
        )
        info_label.pack()

    def xoa_noi_dung_chinh(self):
        """Xóa tất cả widget trong khung chính"""
        for widget in self.khungChinh.winfo_children():
            widget.destroy()

    def mo_quan_ly_sach(self):
        """Mở giao diện quản lý sách trong khung chính"""
        self.xoa_noi_dung_chinh()
        
        # Tạo giao diện quản lý sách trong khung chính
        GiaoDienQuanLySach(self.khungChinh)

    def mo_quan_ly_user(self):
        """Mở cửa sổ quản lý người dùng"""
        win = tk.Toplevel(self.master)
        win.geometry("500x450")
        win.title("Quản lý người dùng")
        win.configure(bg="white")
        win.transient(self.master)
        win.grab_set()
        GiaoDienQuanLyNguoiDung(win)
        
    def mo_muon_tra(self):
        """Mở giao diện mượn/trả sách"""
        self.xoa_noi_dung_chinh()
    
        # Import và tạo giao diện mượn/trả sách
        from GiaoDien_MuonTra import GiaoDienMuonTra
        GiaoDienMuonTra(self.khungChinh)
        
    def mo_bao_cao(self):
        """Placeholder cho báo cáo"""
        self.xoa_noi_dung_chinh()
        Label(
            self.khungChinh,
            text="📊 Chức năng Báo cáo\n(Đang phát triển)",
            font=("Arial", 16),
            bg="white",
            fg="#f39c12",
            pady=100
        ).pack()
        
    def mo_cai_dat(self):
        """Placeholder cho cài đặt"""
        self.xoa_noi_dung_chinh()
        Label(
            self.khungChinh,
            text="⚙️ Chức năng Cài đặt\n(Đang phát triển)",
            font=("Arial", 16),
            bg="white",
            fg="#95a5a6",
            pady=100
        ).pack()