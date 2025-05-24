import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from QuanLy import MuonTraSach
from MuonTra_QuanLy import (get_all_muon_tra, them_muon_sach, tra_sach, 
                           tim_kiem_muon_tra, cap_nhat_trang_thai, 
                           get_khach_hang_by_ma)
from Book_QuanLy import get_all_books

class GiaoDienMuonTra(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.pack(fill="both", expand=True)
        self.tao_giao_dien()
        self.tai_lai()
        cap_nhat_trang_thai()  # Cập nhật trạng thái khi mở

    def tao_giao_dien(self):
        # Container chính
        main_container = tk.Frame(self, bg="white")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Notebook để chia tab
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab mượn sách
        self.tab_muon = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_muon, text="📖 Mượn sách")
        
        # Tab trả sách
        self.tab_tra = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_tra, text="📚 Trả sách")
        
        # Tab danh sách
        self.tab_danh_sach = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_danh_sach, text="📋 Danh sách mượn/trả")
        
        self.tao_tab_muon()
        self.tao_tab_tra()
        self.tao_tab_danh_sach()

    def tao_tab_muon(self):
        """Tạo giao diện tab mượn sách"""
        # Frame thông tin khách hàng
        frame_khach = tk.LabelFrame(self.tab_muon, text="Thông tin khách hàng", 
                                   bg="white", font=("Arial", 10, "bold"))
        frame_khach.pack(fill="x", padx=10, pady=5)
        
        # Row 1
        row1 = tk.Frame(frame_khach, bg="white")
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="Mã khách:", bg="white").pack(side="left")
        self.ma_khach = tk.StringVar()
        entry_ma_khach = tk.Entry(row1, textvariable=self.ma_khach, width=15)
        entry_ma_khach.pack(side="left", padx=(5, 20))
        entry_ma_khach.bind('<FocusOut>', self.load_khach_hang_info)
        
        tk.Label(row1, text="Tên khách:", bg="white").pack(side="left")
        self.ten_khach = tk.StringVar()
        tk.Entry(row1, textvariable=self.ten_khach, width=30).pack(side="left", padx=(5, 0))
        
        # Row 2
        row2 = tk.Frame(frame_khach, bg="white")
        row2.pack(fill="x", pady=5)
        
        tk.Label(row2, text="SĐT:", bg="white").pack(side="left")
        self.sdt = tk.StringVar()
        tk.Entry(row2, textvariable=self.sdt, width=15).pack(side="left", padx=(5, 20))
        
        tk.Label(row2, text="Email:", bg="white").pack(side="left")
        self.email = tk.StringVar()
        tk.Entry(row2, textvariable=self.email, width=35).pack(side="left", padx=(5, 0))
        
        # Row 3
        row3 = tk.Frame(frame_khach, bg="white")
        row3.pack(fill="x", pady=5)
        
        tk.Label(row3, text="Địa chỉ:", bg="white").pack(side="left")
        self.dia_chi = tk.StringVar()
        tk.Entry(row3, textvariable=self.dia_chi, width=50).pack(side="left", padx=(5, 0))
        
        # Frame thông tin sách
        frame_sach = tk.LabelFrame(self.tab_muon, text="Thông tin sách mượn", 
                                  bg="white", font=("Arial", 10, "bold"))
        frame_sach.pack(fill="x", padx=10, pady=5)
        
        # Row sách
        row_sach = tk.Frame(frame_sach, bg="white")
        row_sach.pack(fill="x", pady=5)
        
        tk.Label(row_sach, text="Mã sách:", bg="white").pack(side="left")
        self.id_sach = tk.StringVar()
        cb_sach = ttk.Combobox(row_sach, textvariable=self.id_sach, width=15)
        cb_sach.pack(side="left", padx=(5, 20))
        cb_sach.bind('<<ComboboxSelected>>', self.load_ten_sach)
        
        tk.Label(row_sach, text="Tên sách:", bg="white").pack(side="left")
        self.ten_sach = tk.StringVar()
        tk.Entry(row_sach, textvariable=self.ten_sach, width=40, state="readonly").pack(side="left", padx=(5, 0))
        
        # Load danh sách sách vào combobox
        self.update_sach_combobox(cb_sach)
        
        # Frame ngày tháng
        frame_ngay = tk.LabelFrame(self.tab_muon, text="Thông tin mượn", 
                                  bg="white", font=("Arial", 10, "bold"))
        frame_ngay.pack(fill="x", padx=10, pady=5)
        
        row_ngay = tk.Frame(frame_ngay, bg="white")
        row_ngay.pack(fill="x", pady=5)
        
        tk.Label(row_ngay, text="Ngày mượn:", bg="white").pack(side="left")
        self.ngay_muon = tk.StringVar()
        self.ngay_muon.set(datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(row_ngay, textvariable=self.ngay_muon, width=12).pack(side="left", padx=(5, 20))
        
        tk.Label(row_ngay, text="Ngày trả:", bg="white").pack(side="left")
        self.ngay_tra = tk.StringVar()
        ngay_tra_mac_dinh = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        self.ngay_tra.set(ngay_tra_mac_dinh)
        tk.Entry(row_ngay, textvariable=self.ngay_tra, width=12).pack(side="left", padx=(5, 0))
        
        # Nút chức năng
        frame_btn = tk.Frame(self.tab_muon, bg="white")
        frame_btn.pack(fill="x", padx=10, pady=10)
        
        tk.Button(frame_btn, text="Mượn sách", command=self.muon_sach, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                 width=15, height=2).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Làm mới", command=self.lam_moi_muon, 
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"), 
                 width=15, height=2).pack(side="left", padx=5)

    def tao_tab_tra(self):
        """Tạo giao diện tab trả sách"""
        frame_tra = tk.LabelFrame(self.tab_tra, text="Thông tin trả sách", 
                                 bg="white", font=("Arial", 10, "bold"))
        frame_tra.pack(fill="x", padx=10, pady=10)
        
        row1 = tk.Frame(frame_tra, bg="white")
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="Mã khách:", bg="white").pack(side="left")
        self.ma_khach_tra = tk.StringVar()
        tk.Entry(row1, textvariable=self.ma_khach_tra, width=15).pack(side="left", padx=(5, 20))
        
        tk.Label(row1, text="Mã sách:", bg="white").pack(side="left")
        self.id_sach_tra = tk.StringVar()
        tk.Entry(row1, textvariable=self.id_sach_tra, width=15).pack(side="left", padx=(5, 20))
        
        tk.Label(row1, text="Ngày trả:", bg="white").pack(side="left")
        self.ngay_tra_thuc_te = tk.StringVar()
        self.ngay_tra_thuc_te.set(datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(row1, textvariable=self.ngay_tra_thuc_te, width=12).pack(side="left", padx=(5, 0))
        
        # Nút trả sách
        frame_btn_tra = tk.Frame(self.tab_tra, bg="white")
        frame_btn_tra.pack(fill="x", padx=10, pady=10)
        
        tk.Button(frame_btn_tra, text="Trả sách", command=self.tra_sach, 
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                 width=15, height=2).pack(side="left", padx=5)

    def tao_tab_danh_sach(self):
        """Tạo giao diện tab danh sách"""
        # Frame tìm kiếm
        frame_tim_kiem = tk.Frame(self.tab_danh_sach, bg="white")
        frame_tim_kiem.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_tim_kiem, text="Tìm kiếm:", bg="white", font=("Arial", 10, "bold")).pack(side="left")
        self.tu_khoa_ds = tk.StringVar()
        tk.Entry(frame_tim_kiem, textvariable=self.tu_khoa_ds, width=30).pack(side="left", padx=(5, 10))
        tk.Button(frame_tim_kiem, text="Tìm", command=self.tim_kiem_ds, 
                 bg="#9C27B0", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(frame_tim_kiem, text="Tải lại", command=self.tai_lai, 
                 bg="#607D8B", fg="white", width=10).pack(side="left", padx=5)
        
        # Treeview
        frame_tree = tk.Frame(self.tab_danh_sach, bg="white")
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(frame_tree, columns=(
            "MaKhach", "TenKhach", "IDSach", "TenSach", 
            "NgayMuon", "NgayTra", "TrangThai", "Phat"
        ), show="headings")
        
        # Cấu hình headers
        headers = {
            "MaKhach": "Mã khách",
            "TenKhach": "Tên khách",
            "IDSach": "Mã sách",
            "TenSach": "Tên sách",
            "NgayMuon": "Ngày mượn",
            "NgayTra": "Ngày trả",
            "TrangThai": "Trạng thái",
            "Phat": "Phạt (VND)"
        }
        
        for col, text in headers.items():
            self.tree.heading(col, text=text)
            if col in ["MaKhach", "IDSach"]:
                self.tree.column(col, width=80, minwidth=60)
            elif col in ["NgayMuon", "NgayTra"]:
                self.tree.column(col, width=100, minwidth=80)
            elif col in ["TrangThai", "Phat"]:
                self.tree.column(col, width=100, minwidth=80)
            else:
                self.tree.column(col, width=200, minwidth=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)

    def update_sach_combobox(self, combobox):
        """Cập nhật danh sách sách có sẵn"""
        books = get_all_books()
        sach_co_san = [f"{book.BookID}" for book in books if book.Quantity > 0]
        combobox['values'] = sach_co_san

    def load_ten_sach(self, event):
        """Load tên sách khi chọn mã sách"""
        id_sach = self.id_sach.get()
        books = get_all_books()
        for book in books:
            if book.BookID == id_sach:
                self.ten_sach.set(book.BookName)
                break

    def load_khach_hang_info(self, event):
        """Load thông tin khách hàng nếu đã từng mượn"""
        ma_khach = self.ma_khach.get().strip()
        if ma_khach:
            from MuonTra_QuanLy import get_khach_hang_by_ma
            khach_info = get_khach_hang_by_ma(ma_khach)
            if khach_info:
                self.ten_khach.set(khach_info['tenKhach'])
                self.sdt.set(khach_info['soDienThoai'])
                self.email.set(khach_info['email'])
                self.dia_chi.set(khach_info['diaChi'])

    def muon_sach(self):
        """Xử lý mượn sách"""
        try:
            if not all([self.ma_khach.get().strip(), self.ten_khach.get().strip(), 
                       self.id_sach.get().strip()]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc.")
                return
            
            muon_tra = MuonTraSach(
                self.ma_khach.get().strip(),
                self.ten_khach.get().strip(),
                self.sdt.get().strip(),
                self.email.get().strip(),
                self.dia_chi.get().strip(),
                self.id_sach.get().strip(),
                self.ten_sach.get().strip(),
                self.ngay_muon.get(),
                self.ngay_tra.get()
            )
            
            them_muon_sach(muon_tra)
            messagebox.showinfo("Thành công", "Đã ghi nhận mượn sách!")
            self.lam_moi_muon()
            self.tai_lai()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def tra_sach(self):
        """Xử lý trả sách"""
        try:
            if not all([self.ma_khach_tra.get().strip(), self.id_sach_tra.get().strip()]):
                messagebox.showerror("Lỗi", "Vui lòng nhập mã khách và mã sách.")
                return
            
            phat = tra_sach(
                self.ma_khach_tra.get().strip(),
                self.id_sach_tra.get().strip(),
                self.ngay_tra_thuc_te.get()
            )
            
            if phat > 0:
                messagebox.showinfo("Thành công", 
                                   f"Đã ghi nhận trả sách!\nPhí phạt: {phat:,} VND")
            else:
                messagebox.showinfo("Thành công", "Đã ghi nhận trả sách!")
            
            self.ma_khach_tra.set("")
            self.id_sach_tra.set("")
            self.tai_lai()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def tim_kiem_ds(self):
        """Tìm kiếm trong danh sách"""
        tu_khoa = self.tu_khoa_ds.get().strip()
        if not tu_khoa:
            self.tai_lai()
            return
        
        ket_qua = tim_kiem_muon_tra(tu_khoa)
        self.hien_thi_danh_sach(ket_qua)

    def tai_lai(self):
        """Tải lại danh sách"""
        muon_tra_list = get_all_muon_tra()
        self.hien_thi_danh_sach(muon_tra_list)

    def hien_thi_danh_sach(self, danh_sach):
        """Hiển thị danh sách lên treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for mt in danh_sach:
            # Định dạng trạng thái với màu sắc
            tag = ""
            if mt.trangThai == "Quá hạn":
                tag = "qua_han"
            elif mt.trangThai == "Đã trả":
                tag = "da_tra"
            else:
                tag = "dang_muon"
            
            self.tree.insert("", "end", values=(
                mt.maKhach, mt.tenKhach, mt.IDSach, mt.tenSach,
                mt.ngayMuon, mt.ngayTra, mt.trangThai, f"{mt.phat:,}"
            ), tags=(tag,))
        
        # Cấu hình màu sắc cho các trạng thái
        self.tree.tag_configure("qua_han", background="#ffebee", foreground="#c62828")
        self.tree.tag_configure("da_tra", background="#e8f5e8", foreground="#2e7d32")
        self.tree.tag_configure("dang_muon", background="#fff3e0", foreground="#ef6c00")

    def lam_moi_muon(self):
        """Làm mới form mượn sách"""
        self.ma_khach.set("")
        self.ten_khach.set("")
        self.sdt.set("")
        self.email.set("")
        self.dia_chi.set("")
        self.id_sach.set("")
        self.ten_sach.set("")
        self.ngay_muon.set(datetime.now().strftime("%Y-%m-%d"))
        self.ngay_tra.set((datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))