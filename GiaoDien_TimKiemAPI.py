import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Button, Entry, Text, Scrollbar
from API_Sach import APIBook, OpenLibraryAPI
from QuanLy import Book
from Book_QuanLy import add_book, get_all_books
import threading
from PIL import Image, ImageTk
import requests
from io import BytesIO

class GiaoDienTimKiemAPI(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.pack(fill="both", expand=True)
        
        # API instances
        self.google_api = APIBook()
        self.openlibrary_api = OpenLibraryAPI()
        
        # Dữ liệu tìm kiếm
        self.search_results = []
        self.selected_book = None
        
        self.tao_giao_dien()

    def tao_giao_dien(self):
        """Tạo giao diện tìm kiếm API"""
        # Container chính
        main_container = Frame(self, bg="white")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = Frame(main_container, bg="#3498db", height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        Label(
            header_frame,
            text="🔍 TÌM KIẾM SÁCH QUA API",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=15)
        
        # Frame tìm kiếm
        search_frame = Frame(main_container, bg="white")
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Tìm kiếm
        Label(search_frame, text="Từ khóa tìm kiếm:", bg="white", 
              font=("Arial", 10, "bold")).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_entry = Entry(search_frame, textvariable=self.search_var, 
                                width=40, font=("Arial", 10))
        self.search_entry.pack(side="left", padx=(10, 10))
        self.search_entry.bind('<Return>', lambda e: self.tim_kiem_sach())
        
        # Nút tìm kiếm
        self.btn_search = Button(
            search_frame,
            text="🔍 Tìm kiếm",
            command=self.tim_kiem_sach,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.btn_search.pack(side="left", padx=5)
        
        # Chọn API
        Label(search_frame, text="API:", bg="white", font=("Arial", 10)).pack(side="left", padx=(20, 5))
        self.api_var = tk.StringVar(value="Google Books")
        api_combo = ttk.Combobox(search_frame, textvariable=self.api_var, 
                               values=["Google Books", "Open Library"], 
                               width=15, state="readonly")
        api_combo.pack(side="left")
        
        # Frame chính chia 2 cột
        content_frame = Frame(main_container, bg="white")
        content_frame.pack(fill="both", expand=True)
        
        # Cột trái - Danh sách kết quả
        left_frame = Frame(content_frame, bg="white")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        Label(left_frame, text="📚 Kết quả tìm kiếm:", bg="white", 
              font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        
        # Treeview cho kết quả
        tree_frame = Frame(left_frame, bg="white")
        tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Title", "Author", "Year"), 
                                show="headings", height=15)
        
        self.tree.heading("Title", text="Tiêu đề")
        self.tree.heading("Author", text="Tác giả") 
        self.tree.heading("Year", text="Năm XB")
        
        self.tree.column("Title", width=300, minwidth=200)
        self.tree.column("Author", width=200, minwidth=150)
        self.tree.column("Year", width=80, minwidth=60)
        
        # Scrollbar cho tree
        tree_scroll = Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # Bind event
        self.tree.bind("<<TreeviewSelect>>", self.on_select_book)
        
        # Cột phải - Chi tiết sách
        right_frame = Frame(content_frame, bg="white", width=400)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        right_frame.pack_propagate(False)
        
        Label(right_frame, text="📖 Chi tiết sách:", bg="white", 
              font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Frame thông tin chi tiết
        detail_frame = Frame(right_frame, bg="#f8f9fa", relief="solid", bd=1)
        detail_frame.pack(fill="both", expand=True, padx=5)
        
        # Hình ảnh sách (nếu có)
        self.image_label = Label(detail_frame, bg="#f8f9fa", text="📚\nKhông có hình", 
                               font=("Arial", 10), width=20, height=8)
        self.image_label.pack(pady=10)
        
        # Thông tin chi tiết
        self.detail_text = Text(detail_frame, wrap="word", font=("Arial", 9), 
                              height=20, width=45, bg="#f8f9fa")
        detail_scroll = Scrollbar(detail_frame, orient="vertical", command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=detail_scroll.set)
        
        self.detail_text.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        detail_scroll.pack(side="right", fill="y", pady=10)
        
        # Frame nút thêm
        button_frame = Frame(right_frame, bg="white")
        button_frame.pack(fill="x", pady=10)
        
        self.btn_add = Button(
            button_frame,
            text="➕ Thêm vào thư viện",
            command=self.them_sach_vao_thu_vien,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            cursor="hand2",
            state="disabled"
        )
        self.btn_add.pack(fill="x", padx=5)
        
        # Status label
        self.status_label = Label(main_container, text="Sẵn sàng tìm kiếm...", 
                                bg="white", fg="#7f8c8d", font=("Arial", 9))
        self.status_label.pack(pady=5)

    def tim_kiem_sach(self):
        """Tìm kiếm sách qua API"""
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        
        # Disable nút tìm kiếm
        self.btn_search.config(state="disabled", text="🔄 Đang tìm...")
        self.status_label.config(text="Đang tìm kiếm...", fg="#f39c12")
        
        # Xóa kết quả cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.xoa_chi_tiet()
        
        # Tìm kiếm trong thread riêng
        def search_thread():
            try:
                api_choice = self.api_var.get()
                
                if api_choice == "Google Books":
                    self.search_results = self.google_api.tim_kiem_sach(keyword, 30)
                else:
                    self.search_results = self.openlibrary_api.tim_kiem_sach(keyword, 30)
                
                # Cập nhật UI trong main thread
                self.master.after(0, self.hien_thi_ket_qua)
                
            except Exception as e:
                self.master.after(0, lambda: self.xu_ly_loi(str(e)))
        
        # Chạy trong thread
        threading.Thread(target=search_thread, daemon=True).start()

    def hien_thi_ket_qua(self):
        """Hiển thị kết quả tìm kiếm"""
        try:
            if self.search_results:
                for book in self.search_results:
                    self.tree.insert("", "end", values=(
                        book.get('title', '')[:50] + ('...' if len(book.get('title', '')) > 50 else ''),
                        book.get('author', '')[:30] + ('...' if len(book.get('author', '')) > 30 else ''),
                        book.get('published_date', '')
                    ))
                
                self.status_label.config(text=f"Tìm thấy {len(self.search_results)} kết quả", fg="#27ae60")
            else:
                self.status_label.config(text="Không tìm thấy kết quả nào", fg="#e74c3c")
        
        except Exception as e:
            self.xu_ly_loi(str(e))
        
        finally:
            # Enable lại nút tìm kiếm
            self.btn_search.config(state="normal", text="🔍 Tìm kiếm")

    def on_select_book(self, event):
        """Khi chọn sách từ danh sách"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            index = self.tree.index(selection[0])
            
            if index < len(self.search_results):
                self.selected_book = self.search_results[index]
                self.hien_thi_chi_tiet()
                self.btn_add.config(state="normal")

    def hien_thi_chi_tiet(self):
        """Hiển thị chi tiết sách đã chọn"""
        if not self.selected_book:
            return
        
        # Xóa nội dung cũ
        self.detail_text.delete(1.0, tk.END)
        
        # Hiển thị thông tin
        book = self.selected_book
        detail_info = f"""📚 THÔNG TIN CHI TIẾT

📖 Tiêu đề: {book.get('title', 'N/A')}

✍️ Tác giả: {book.get('author', 'N/A')}

📂 Thể loại: {book.get('category', 'N/A')}

📅 Năm xuất bản: {book.get('published_date', 'N/A')}

📄 Số trang: {book.get('page_count', 'N/A')}

🔢 ISBN: {book.get('isbn', 'N/A')}

📝 Mô tả:
{book.get('description', 'Không có mô tả')}
"""
        
        self.detail_text.insert(1.0, detail_info)
        
        # Tải hình ảnh nếu có
        if book.get('thumbnail'):
            self.tai_hinh_anh(book['thumbnail'])
        else:
            self.image_label.config(image="", text="📚\nKhông có hình")

    def tai_hinh_anh(self, url):
        """Tải và hiển thị hình ảnh sách"""
        def load_image():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    # Resize ảnh
                    image = image.resize((120, 160), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Cập nhật UI trong main thread
                    self.master.after(0, lambda: self.cap_nhat_hinh_anh(photo))
            except Exception as e:
                print(f"Lỗi tải hình ảnh: {e}")
        
        threading.Thread(target=load_image, daemon=True).start()

    def cap_nhat_hinh_anh(self, photo):
        """Cập nhật hình ảnh trong UI"""
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # Giữ reference

    def xoa_chi_tiet(self):
        """Xóa thông tin chi tiết"""
        self.detail_text.delete(1.0, tk.END)
        self.image_label.config(image="", text="📚\nKhông có hình")
        self.btn_add.config(state="disabled")
        self.selected_book = None

    def them_sach_vao_thu_vien(self):
        """Thêm sách đã chọn vào thư viện"""
        if not self.selected_book:
            return
        
        try:
            book = self.selected_book
            
            # Tạo dialog để nhập thông tin bổ sung
            dialog = tk.Toplevel(self.master)
            dialog.title("Thêm sách vào thư viện")
            dialog.geometry("500x400")
            dialog.configure(bg="white")
            dialog.transient(self.master)
            dialog.grab_set()
            
            # Căn giữa dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() - 500) // 2
            y = (dialog.winfo_screenheight() - 400) // 2
            dialog.geometry(f"500x400+{x}+{y}")
            
            # Frame cho form
            form_frame = Frame(dialog, bg="white")
            form_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            Label(form_frame, text="📚 THÊM SÁCH VÀO THƯ VIỆN", 
                  font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))
            
            # Các trường nhập liệu
            fields = {}
            
            # Mã sách
            Label(form_frame, text="Mã sách:", bg="white", font=("Arial", 10)).pack(anchor="w")
            fields['ma_sach'] = tk.StringVar(value=f"BK{len(get_all_books()) + 1:04d}")
            Entry(form_frame, textvariable=fields['ma_sach'], width=50).pack(fill="x", pady=(0, 10))
            
            # Tên sách
            Label(form_frame, text="Tên sách:", bg="white", font=("Arial", 10)).pack(anchor="w")
            fields['ten_sach'] = tk.StringVar(value=book.get('title', ''))
            Entry(form_frame, textvariable=fields['ten_sach'], width=50).pack(fill="x", pady=(0, 10))
            
            # Tác giả
            Label(form_frame, text="Tác giả:", bg="white", font=("Arial", 10)).pack(anchor="w")
            fields['tac_gia'] = tk.StringVar(value=book.get('author', ''))
            Entry(form_frame, textvariable=fields['tac_gia'], width=50).pack(fill="x", pady=(0, 10))
            
            # Thể loại
            Label(form_frame, text="Thể loại:", bg="white", font=("Arial", 10)).pack(anchor="w")
            fields['the_loai'] = tk.StringVar(value=book.get('category', 'General'))
            combo_theloai = ttk.Combobox(form_frame, textvariable=fields['the_loai'], 
                                       values=["Literature", "Science", "Technology", "Education", 
                                             "Fiction", "History", "Philosophy", "General"], width=47)
            combo_theloai.pack(fill="x", pady=(0, 10))
            
            # Số lượng
            Label(form_frame, text="Số lượng:", bg="white", font=("Arial", 10)).pack(anchor="w")
            fields['so_luong'] = tk.StringVar(value="1")
            Entry(form_frame, textvariable=fields['so_luong'], width=50).pack(fill="x", pady=(0, 20))
            
            # Nút
            button_frame = Frame(form_frame, bg="white")
            button_frame.pack(fill="x")
            
            def luu_sach():
                try:
                    # Kiểm tra dữ liệu
                    if not all([fields['ma_sach'].get().strip(), fields['ten_sach'].get().strip(),
                              fields['tac_gia'].get().strip()]):
                        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                        return
                    
                    so_luong = int(fields['so_luong'].get().strip())
                    if so_luong <= 0:
                        raise ValueError("Số lượng phải lớn hơn 0")
                    
                    # Tạo đối tượng sách
                    new_book = Book(
                        fields['ma_sach'].get().strip(),
                        fields['ten_sach'].get().strip(),
                        fields['tac_gia'].get().strip(),
                        fields['the_loai'].get(),
                        so_luong
                    )
                    
                    # Thêm vào database
                    add_book(new_book)
                    
                    messagebox.showinfo("Thành công", "Đã thêm sách vào thư viện!")
                    dialog.destroy()
                    
                except ValueError as e:
                    messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {str(e)}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            
            Button(button_frame, text="💾 Lưu sách", command=luu_sach,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side="left", padx=(0, 10))
            
            Button(button_frame, text="❌ Hủy", command=dialog.destroy,
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=15).pack(side="left")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

    def xu_ly_loi(self, error_msg):
        """Xử lý lỗi"""
        self.status_label.config(text=f"Lỗi: {error_msg}", fg="#e74c3c")
        self.btn_search.config(state="normal", text="🔍 Tìm kiếm")
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {error_msg}")