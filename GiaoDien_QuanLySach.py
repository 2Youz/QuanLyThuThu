import tkinter as tk
from tkinter import ttk, messagebox
from QuanLy import Book
from Book_QuanLy import get_all_books, add_book, update_book, delete_book

class GiaoDienQuanLySach(tk.Frame):
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
        
        # Frame cho form nhập liệu (CỐ ĐỊNH - không giãn nở)
        form_frame = tk.Frame(main_container, bg="white")
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Row 1: Mã sách và Tên sách
        row1_frame = tk.Frame(form_frame, bg="white")
        row1_frame.pack(fill="x", pady=5)
        
        tk.Label(row1_frame, text="Mã sách:", bg="white", font=("Arial", 10)).pack(side="left")
        self.maSach = tk.StringVar()
        tk.Entry(row1_frame, textvariable=self.maSach, width=15, font=("Arial", 10)).pack(side="left", padx=(5, 20))

        tk.Label(row1_frame, text="Tên sách:", bg="white", font=("Arial", 10)).pack(side="left")
        self.tenSach = tk.StringVar()
        tk.Entry(row1_frame, textvariable=self.tenSach, width=35, font=("Arial", 10)).pack(side="left", padx=(5, 0))

        # Row 2: Tác giả và Thể loại
        row2_frame = tk.Frame(form_frame, bg="white")
        row2_frame.pack(fill="x", pady=5)
        
        tk.Label(row2_frame, text="Tác giả:", bg="white", font=("Arial", 10)).pack(side="left")
        self.tacGia = tk.StringVar()
        tk.Entry(row2_frame, textvariable=self.tacGia, width=20, font=("Arial", 10)).pack(side="left", padx=(5, 20))

        tk.Label(row2_frame, text="Thể loại:", bg="white", font=("Arial", 10)).pack(side="left")
        self.theLoai = tk.StringVar()
        self.cbTheLoai = ttk.Combobox(row2_frame, textvariable=self.theLoai, width=25, font=("Arial", 10))
        self.cbTheLoai['values'] = ["Literature", "Science", "Technology", "Education", "Fiction", "History", "Philosophy", "General"]
        self.cbTheLoai.set("General")
        self.cbTheLoai.pack(side="left", padx=(5, 0))

        # Row 3: Số lượng
        row3_frame = tk.Frame(form_frame, bg="white")
        row3_frame.pack(fill="x", pady=5)
        
        tk.Label(row3_frame, text="Số lượng:", bg="white", font=("Arial", 10)).pack(side="left")
        self.soLuong = tk.StringVar()
        tk.Entry(row3_frame, textvariable=self.soLuong, width=15, font=("Arial", 10)).pack(side="left", padx=(5, 0))

        # Frame cho các nút chức năng (CỐ ĐỊNH)
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

        # Frame tìm kiếm (CỐ ĐỊNH)
        search_frame = tk.Frame(main_container, bg="white")
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(search_frame, text="Tìm kiếm:", bg="white", font=("Arial", 10, "bold")).pack(side="left")
        self.tuKhoa = tk.StringVar()
        self.entry_tim_kiem = tk.Entry(search_frame, textvariable=self.tuKhoa, width=30, font=("Arial", 10))
        self.entry_tim_kiem.pack(side="left", padx=(5, 10))
        self.entry_tim_kiem.bind('<Return>', lambda event: self.tim_kiem())
        
        tk.Button(search_frame, text="Tìm", command=self.tim_kiem, bg="#9C27B0", fg="white", 
                 font=("Arial", 10), width=10).pack(side="left")

        # Frame cho Treeview (CHỈ CÁI NÀY GIÃN NỞ)
        tree_frame = tk.Frame(main_container, bg="white")
        tree_frame.pack(fill="both", expand=True)

        # Treeview với scrollbars
        self.tree = ttk.Treeview(tree_frame, columns=("BookID", "BookName", "Author", "Category", "Quantity"), show="headings")
        
        # Cấu hình headers
        self.tree.heading("BookID", text="Mã sách")
        self.tree.heading("BookName", text="Tên sách")
        self.tree.heading("Author", text="Tác giả")
        self.tree.heading("Category", text="Thể loại")
        self.tree.heading("Quantity", text="Số lượng")
        
        # Cấu hình độ rộng cột
        self.tree.column("BookID", width=100, minwidth=80)
        self.tree.column("BookName", width=300, minwidth=200)
        self.tree.column("Author", width=200, minwidth=150)
        self.tree.column("Category", width=120, minwidth=100)
        self.tree.column("Quantity", width=100, minwidth=80)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack Treeview và scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # CHỈ tree_frame giãn nở
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind sự kiện
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Style cho Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def tai_lai(self):
        """Tải lại danh sách"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for book in get_all_books():
            self.tree.insert("", "end", values=(
                book.BookID, book.BookName, book.Author, 
                book.Category, book.Quantity
            ))

    def on_select(self, event):
        """Chọn sách từ danh sách"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.maSach.set(values[0])
            self.tenSach.set(values[1])
            self.tacGia.set(values[2])
            self.theLoai.set(values[3])
            self.soLuong.set(values[4])

    def them(self):
        """Thêm sách"""
        try:
            if not all([self.maSach.get().strip(), self.tenSach.get().strip(), self.tacGia.get().strip()]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return

            try:
                so_luong = int(self.soLuong.get().strip())
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên.")
                return
            
            the_loai = self.theLoai.get() if self.theLoai.get() else "General"
            
            book = Book(
                self.maSach.get().strip(),
                self.tenSach.get().strip(),
                self.tacGia.get().strip(),
                the_loai,
                so_luong
            )
            
            add_book(book)
            messagebox.showinfo("Thành công", "Đã thêm sách!")
            self.tai_lai()
            self.lam_moi()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def sua(self):
        """Sửa sách"""
        try:
            if not self.maSach.get().strip():
                messagebox.showerror("Lỗi", "Vui lòng chọn sách để sửa.")
                return

            try:
                so_luong = int(self.soLuong.get().strip())
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên.")
                return
            
            new_data = {
                "BookName": self.tenSach.get().strip(),
                "Author": self.tacGia.get().strip(),
                "Category": self.theLoai.get(),
                "Quantity": so_luong
            }
            
            update_book(self.maSach.get().strip(), new_data)
            messagebox.showinfo("Thành công", "Đã cập nhật sách!")
            self.tai_lai()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def xoa(self):
        """Xóa sách"""
        if not self.maSach.get().strip():
            messagebox.showerror("Lỗi", "Vui lòng chọn sách để xóa.")
            return
            
        if messagebox.askyesno("Xác nhận", f"Xóa sách {self.maSach.get()}?"):
            try:
                delete_book(self.maSach.get().strip())
                messagebox.showinfo("Thành công", "Đã xóa sách!")
                self.tai_lai()
                self.lam_moi()
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

    def tim_kiem(self):
        """Tìm kiếm sách"""
        keyword = self.tuKhoa.get().lower().strip()
        if not keyword:
            self.tai_lai()
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        found = False
        for book in get_all_books():
            if (keyword in book.BookID.lower() or 
                keyword in book.BookName.lower() or 
                keyword in book.Author.lower() or
                keyword in book.Category.lower()):
                self.tree.insert("", "end", values=(
                    book.BookID, book.BookName, book.Author, 
                    book.Category, book.Quantity
                ))
                found = True
        
        if not found:
            messagebox.showinfo("Kết quả", "Không tìm thấy sách nào phù hợp.")

    def lam_moi(self):
        """Làm mới form"""
        self.maSach.set("")
        self.tenSach.set("")
        self.tacGia.set("")
        self.theLoai.set("General")
        self.soLuong.set("")
        self.tuKhoa.set("")
        self.tai_lai()