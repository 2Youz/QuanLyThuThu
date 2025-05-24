import tkinter as tk
from tkinter import Frame, Label, Button, messagebox
from GiaoDien_QuanLyNguoiDung import GiaoDienQuanLyNguoiDung
from GiaoDien_QuanLySach import GiaoDienQuanLySach
from GiaoDien_QuanLyThuThu import GiaoDienQuanLyThuThu
from GiaoDien_TimKiemAPI import GiaoDienTimKiemAPI

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
        
        # Nút đăng xuất ở cuối sidebar
        self.create_logout_button()
        
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
        
        # Nút tìm kiếm API (cho tất cả user)
        btn_api = Button(
            self.sidebar,
            text="🔍 Tìm kiếm API",
            command=self.mo_tim_kiem_api,
            bg="#16a085",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            pady=10
        )
        btn_api.pack(fill="x", padx=10, pady=2)
        
        # Nút mượn/trả sách
        btn_muon_tra = Button(
            self.sidebar,
            text="📖 Mượn/Trả sách",
            command=self.mo_muon_tra,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            pady=10
        )
        btn_muon_tra.pack(fill="x", padx=10, pady=2)
        
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
            btn_user.pack(fill="x", padx=10, pady=2)
            
            # Nút quản lý thủ thư (chỉ admin)
            btn_thu_thu = Button(
                self.sidebar,
                text="👨‍💼 Quản lý Thủ Thư",
                command=self.mo_quan_ly_thu_thu,
                bg="#e67e22",
                fg="white",
                font=("Arial", 10),
                relief="flat",
                pady=10
            )
            btn_thu_thu.pack(fill="x", padx=10, pady=2)

    def create_logout_button(self):
        """Tạo nút đăng xuất ở cuối sidebar"""
        # Frame để đẩy nút đăng xuất xuống cuối
        spacer_frame = Frame(self.sidebar, bg="#2c3e50")
        spacer_frame.pack(fill="both", expand=True)
        
        # Separator line
        separator = Frame(self.sidebar, height=2, bg="#34495e")
        separator.pack(fill="x", padx=10, pady=10)
        
        # Nút đăng xuất
        btn_logout = Button(
            self.sidebar,
            text="🚪 Đăng xuất",
            command=self.dang_xuat,
            bg="#c0392b",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=12,
            cursor="hand2"
        )
        btn_logout.pack(fill="x", padx=10, pady=(0, 20))
        
        # Hiệu ứng hover cho nút đăng xuất
        def on_enter(event):
            btn_logout.configure(bg="#a93226")
        
        def on_leave(event):
            btn_logout.configure(bg="#c0392b")
        
        btn_logout.bind("<Enter>", on_enter)
        btn_logout.bind("<Leave>", on_leave)

    def dang_xuat(self):
        """Xử lý đăng xuất và quay về màn hình đăng nhập"""
        # Hiển thị hộp thoại xác nhận
        if messagebox.askyesno("Xác nhận đăng xuất", 
                              f"Bạn có chắc chắn muốn đăng xuất tài khoản '{self.user_login.username}'?"):
            try:
                # Xóa giao diện hiện tại
                self.destroy()
                
                # Đặt lại kích thước cửa sổ cho màn hình đăng nhập
                self.master.geometry("400x400")
                
                # Căn giữa cửa sổ
                screen_width = self.master.winfo_screenwidth()
                screen_height = self.master.winfo_screenheight()
                x = (screen_width - 400) // 2
                y = (screen_height - 400) // 2
                self.master.geometry(f"400x400+{x}+{y}")
                
                # Import và tạo lại giao diện đăng nhập
                from GiaoDien_DangNhap import GiaoDienDangNhap
                
                # Tạo hàm kiểm tra quyền (giả sử có sẵn)
                def kiem_tra_quyen(username, password, role):
                    # Import các hàm cần thiết để kiểm tra đăng nhập
                    from User_QuanLy import get_all_users
                    users = get_all_users()
                    for user in users:
                        if (user.username == username and 
                            user.password == password and 
                            user.role == role):
                            return user
                    return None
                
                # Tạo giao diện đăng nhập mới
                GiaoDienDangNhap(self.master, kiem_tra_quyen)
                
                # Hiển thị thông báo đăng xuất thành công
                messagebox.showinfo("Đăng xuất thành công", 
                                  "Bạn đã đăng xuất thành công!\nVui lòng đăng nhập lại.")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi đăng xuất: {str(e)}")

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

    def mo_tim_kiem_api(self):
        """Mở giao diện tìm kiếm sách qua API"""
        self.xoa_noi_dung_chinh()
        
        # Tạo giao diện tìm kiếm API trong khung chính
        GiaoDienTimKiemAPI(self.khungChinh)

    def mo_quan_ly_user(self):
        """Mở cửa sổ quản lý người dùng"""
        win = tk.Toplevel(self.master)
        win.geometry("500x450")
        win.title("Quản lý người dùng")
        win.configure(bg="white")
        win.transient(self.master)
        win.grab_set()
        GiaoDienQuanLyNguoiDung(win)

    def mo_quan_ly_thu_thu(self):
        """Mở giao diện quản lý thủ thư trong khung chính"""
        self.xoa_noi_dung_chinh()
        
        # Tạo giao diện quản lý thủ thư trong khung chính
        GiaoDienQuanLyThuThu(self.khungChinh)
        
    def mo_muon_tra(self):
        """Mở giao diện mượn/trả sách"""
        self.xoa_noi_dung_chinh()
    
        # Import và tạo giao diện mượn/trả sách
        from GiaoDien_MuonTra import GiaoDienMuonTra
        GiaoDienMuonTra(self.khungChinh)