import tkinter as tk
from tkinter import ttk, messagebox
from QuanLy import ThuThu
from ThuThu_QuanLy import get_all_thuthu, add_thuthu, update_thuthu, delete_thuthu, search_thuthu

class GiaoDienQuanLyThuThu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.pack(fill="both", expand=True)
        self.tao_giao_dien()
        self.tai_lai()

    def tao_giao_dien(self):
        # Container chính
        main_container = tk.Frame(self, bg="white")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame cho form nhập liệu
        form_frame = tk.Frame(main_container, bg="white")
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Row 1: Mã thủ thư và Tên thủ thư
        row1_frame = tk.Frame(form_frame, bg="white")
        row1_frame.pack(fill="x", pady=5)
        
        tk.Label(row1_frame, text="Mã thủ thư:", bg="white", font=("Arial", 10)).pack(side="left")
        self.maTT = tk.StringVar()
        tk.Entry(row1_frame, textvariable=self.maTT, width=15, font=("Arial", 10)).pack(side="left", padx=(5, 20))

        tk.Label(row1_frame, text="Tên thủ thư:", bg="white", font=("Arial", 10)).pack(side="left")
        self.tenTT = tk.StringVar()
        tk.Entry(row1_frame, textvariable=self.tenTT, width=35, font=("Arial", 10)).pack(side="left", padx=(5, 0))

        # Row 2: SĐT và Email
        row2_frame = tk.Frame(form_frame, bg="white")
        row2_frame.pack(fill="x", pady=5)
        
        tk.Label(row2_frame, text="Số điện thoại:", bg="white", font=("Arial", 10)).pack(side="left")
        self.soDienthoai = tk.StringVar()
        tk.Entry(row2_frame, textvariable=self.soDienthoai, width=20, font=("Arial", 10)).pack(side="left", padx=(5, 20))

        tk.Label(row2_frame, text="Email:", bg="white", font=("Arial", 10)).pack(side="left")
        self.email = tk.StringVar()
        tk.Entry(row2_frame, textvariable=self.email, width=30, font=("Arial", 10)).pack(side="left", padx=(5, 0))

        # Row 3: Địa chỉ
        row3_frame = tk.Frame(form_frame, bg="white")
        row3_frame.pack(fill="x", pady=5)
        
        tk.Label(row3_frame, text="Địa chỉ:", bg="white", font=("Arial", 10)).pack(side="left")
        self.diaChi = tk.StringVar()
        tk.Entry(row3_frame, textvariable=self.diaChi, width=60, font=("Arial", 10)).pack(side="left", padx=(5, 0))

        # Row 4: Lương và Ca làm việc
        row4_frame = tk.Frame(form_frame, bg="white")
        row4_frame.pack(fill="x", pady=5)
        
        tk.Label(row4_frame, text="Lương:", bg="white", font=("Arial", 10)).pack(side="left")
        self.luong = tk.StringVar()
        tk.Entry(row4_frame, textvariable=self.luong, width=15, font=("Arial", 10)).pack(side="left", padx=(5, 20))

        tk.Label(row4_frame, text="Ca làm việc:", bg="white", font=("Arial", 10)).pack(side="left")
        self.calamViec = tk.StringVar()
        self.cbCaLam = ttk.Combobox(row4_frame, textvariable=self.calamViec, width=25, font=("Arial", 10))
        self.cbCaLam['values'] = ["Ca sáng (7:00-12:00)", "Ca chiều (13:00-18:00)", "Ca tối (18:00-22:00)", "Toàn thời gian"]
        self.cbCaLam.set("Toàn thời gian")
        self.cbCaLam.pack(side="left", padx=(5, 0))

        # Frame cho các nút chức năng
        button_frame = tk.Frame(main_container, bg="white")
        button_frame.pack(fill="x", pady=(0, 10))

        # Các nút chức năng
        tk.Button(button_frame, text="Thêm", command=self.them, bg="#4CAF50", fg="white", 
                 font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Sửa", command=self.sua, bg="#2196F3", fg="white", 
                 font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=5)
        tk.Button(button_frame, text="Xóa", command=self.xoa, bg="#f44336", fg="white", 
                 font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=5)
        tk.Button(button_frame, text="Làm mới", command=self.lam_moi, bg="#FF9800", fg="white", 
                 font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=5)

        # Frame tìm kiếm
        search_frame = tk.Frame(main_container, bg="white")
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(search_frame, text="Tìm kiếm:", bg="white", font=("Arial", 10, "bold")).pack(side="left")
        self.tuKhoa = tk.StringVar()
        self.entry_tim_kiem = tk.Entry(search_frame, textvariable=self.tuKhoa, width=30, font=("Arial", 10))
        self.entry_tim_kiem.pack(side="left", padx=(5, 10))
        self.entry_tim_kiem.bind('<Return>', lambda event: self.tim_kiem())
        
        tk.Button(search_frame, text="Tìm", command=self.tim_kiem, bg="#9C27B0", fg="white", 
                 font=("Arial", 10), width=10).pack(side="left")

        # Frame cho Treeview
        tree_frame = tk.Frame(main_container, bg="white")
        tree_frame.pack(fill="both", expand=True)

        # Treeview với scrollbars
        self.tree = ttk.Treeview(tree_frame, columns=("MaTT", "TenTT", "SoDT", "Email", "DiaChi", "Luong", "CaLam"), show="headings")
        
        # Cấu hình headers
        self.tree.heading("MaTT", text="Mã thủ thư")
        self.tree.heading("TenTT", text="Tên thủ thư")
        self.tree.heading("SoDT", text="Số điện thoại")
        self.tree.heading("Email", text="Email")
        self.tree.heading("DiaChi", text="Địa chỉ")
        self.tree.heading("Luong", text="Lương")
        self.tree.heading("CaLam", text="Ca làm việc")
        
        # Cấu hình độ rộng cột
        self.tree.column("MaTT", width=100, minwidth=80)
        self.tree.column("TenTT", width=200, minwidth=150)
        self.tree.column("SoDT", width=120, minwidth=100)
        self.tree.column("Email", width=200, minwidth=150)
        self.tree.column("DiaChi", width=250, minwidth=200)
        self.tree.column("Luong", width=100, minwidth=80)
        self.tree.column("CaLam", width=150, minwidth=120)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack Treeview và scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind sự kiện
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Style cho Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def tai_lai(self):
        """Tải lại danh sách thủ thư"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for thuthu in get_all_thuthu():
            self.tree.insert("", "end", values=(
                thuthu.maTT, thuthu.tenTT, thuthu.soDienthoai, 
                thuthu.email, thuthu.diaChi, f"{thuthu.luong:,} VND", thuthu.calamViec
            ))

    def on_select(self, event):
        """Chọn thủ thư từ danh sách"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.maTT.set(values[0])
            self.tenTT.set(values[1])
            self.soDienthoai.set(values[2])
            self.email.set(values[3])
            self.diaChi.set(values[4])
            # Lấy lương (bỏ " VND" và dấu phẩy)
            luong_str = str(values[5]).replace(" VND", "").replace(",", "")
            self.luong.set(luong_str)
            self.calamViec.set(values[6])

    def them(self):
        """Thêm thủ thư"""
        try:
            if not all([self.maTT.get().strip(), self.tenTT.get().strip(), 
                       self.soDienthoai.get().strip(), self.email.get().strip()]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc.")
                return

            try:
                luong = float(self.luong.get().strip())
            except ValueError:
                messagebox.showerror("Lỗi", "Lương phải là số.")
                return
            
            thuthu = ThuThu(
                self.maTT.get().strip(),
                self.tenTT.get().strip(),
                self.soDienthoai.get().strip(),
                self.email.get().strip(),
                self.diaChi.get().strip(),
                luong,
                self.calamViec.get()
            )
            
            add_thuthu(thuthu)
            messagebox.showinfo("Thành công", "Đã thêm thủ thư!")
            self.tai_lai()
            self.lam_moi()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def sua(self):
        """Sửa thông tin thủ thư"""
        try:
            if not self.maTT.get().strip():
                messagebox.showerror("Lỗi", "Vui lòng chọn thủ thư để sửa.")
                return

            try:
                luong = float(self.luong.get().strip())
            except ValueError:
                messagebox.showerror("Lỗi", "Lương phải là số.")
                return
            
            new_data = {
                "tenTT": self.tenTT.get().strip(),
                "soDienthoai": self.soDienthoai.get().strip(),
                "email": self.email.get().strip(),
                "diaChi": self.diaChi.get().strip(),
                "luong": luong,
                "calamViec": self.calamViec.get()
            }
            
            update_thuthu(self.maTT.get().strip(), new_data)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin thủ thư!")
            self.tai_lai()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def xoa(self):
        """Xóa thủ thư"""
        if not self.maTT.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng chọn thủ thư để xóa.")
            return
            
        if messagebox.askyesno("Xác nhận", f"Xóa thủ thư {self.maTT.get()}?"):
            try:
                delete_thuthu(self.maTT.get().strip())
                messagebox.showinfo("Thành công", "Đã xóa thủ thư!")
                self.tai_lai()
                self.lam_moi()
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

    def tim_kiem(self):
        """Tìm kiếm thủ thư"""
        keyword = self.tuKhoa.get().strip()
        if not keyword:
            self.tai_lai()
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        thuthu_list = search_thuthu(keyword)
        if not thuthu_list:
            messagebox.showinfo("Kết quả", "Không tìm thấy thủ thư nào phù hợp.")
            return
        
        for thuthu in thuthu_list:
            self.tree.insert("", "end", values=(
                thuthu.maTT, thuthu.tenTT, thuthu.soDienthoai, 
                thuthu.email, thuthu.diaChi, f"{thuthu.luong:,} VND", thuthu.calamViec
            ))

    def lam_moi(self):
        """Làm mới form"""
        self.maTT.set("")
        self.tenTT.set("")
        self.soDienthoai.set("")
        self.email.set("")
        self.diaChi.set("")
        self.luong.set("")
        self.calamViec.set("Toàn thời gian")