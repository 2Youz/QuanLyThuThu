import json
import os
from datetime import datetime, timedelta
from QuanLy import MuonTraSach, Book
from Book_QuanLy import get_all_books, update_book

MUONTRA_FILE = "muontra.json"

def tinh_phat(muon_tra_obj, ngay_hien_tai):
    """Tính tiền phạt nếu trả sách muộn"""
    if muon_tra_obj.trangThai == "Đã trả":
        return muon_tra_obj.phat
        
    try:
        ngay_tra = datetime.strptime(muon_tra_obj.ngayTra, "%Y-%m-%d")
        ngay_ht = datetime.strptime(ngay_hien_tai, "%Y-%m-%d")
        
        if ngay_ht > ngay_tra:
            so_ngay_tre = (ngay_ht - ngay_tra).days
            # Phạt 5000 VND/ngày trễ
            muon_tra_obj.phat = so_ngay_tre * 5000
            muon_tra_obj.trangThai = "Quá hạn"
            return muon_tra_obj.phat
        else:
            muon_tra_obj.phat = 0
            return 0
    except Exception as e:
        print(f"Lỗi tính phạt: {e}")
        return 0

def load_muon_tra():
    """Load danh sách mượn/trả từ file JSON"""
    if not os.path.exists(MUONTRA_FILE) or os.path.getsize(MUONTRA_FILE) == 0:
        return []
    with open(MUONTRA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        muon_tra_list = []
        for mt_data in data:
            muon_tra = MuonTraSach(
                mt_data["maKhach"],
                mt_data["tenKhach"],
                mt_data["soDienThoai"],
                mt_data["email"],
                mt_data["diaChi"],
                mt_data["IDSach"],
                mt_data["tenSach"],
                mt_data["ngayMuon"],
                mt_data["ngayTra"],
                mt_data.get("trangThai", "Đang mượn"),
                mt_data.get("phat", 0)
            )
            muon_tra_list.append(muon_tra)
        return muon_tra_list

def save_muon_tra(muon_tra_list):
    """Lưu danh sách mượn/trả vào file JSON"""
    with open(MUONTRA_FILE, "w", encoding="utf-8") as f:
        json.dump([mt.to_dict() for mt in muon_tra_list], f, indent=4, ensure_ascii=False)

def get_all_muon_tra():
    """Lấy tất cả danh sách mượn/trả"""
    return load_muon_tra()

def them_muon_sach(muon_tra):
    """Thêm bản ghi mượn sách mới"""
    muon_tra_list = load_muon_tra()
    
    # Kiểm tra sách có tồn tại và còn không
    books = get_all_books()
    book_found = None
    for book in books:
        if book.BookID == muon_tra.IDSach:
            book_found = book
            break
    
    if not book_found:
        raise ValueError("Sách không tồn tại")
    
    if book_found.Quantity <= 0:
        raise ValueError("Sách đã hết")
    
    # Kiểm tra khách hàng đã mượn sách này chưa trả
    for mt in muon_tra_list:
        if (mt.maKhach == muon_tra.maKhach and 
            mt.IDSach == muon_tra.IDSach and 
            mt.trangThai == "Đang mượn"):
            raise ValueError("Khách hàng đã mượn sách này và chưa trả")
    
    # Thêm bản ghi mượn
    muon_tra_list.append(muon_tra)
    
    # Giảm số lượng sách
    update_book(muon_tra.IDSach, {"Quantity": book_found.Quantity - 1})
    
    save_muon_tra(muon_tra_list)

def tra_sach(ma_khach, id_sach, ngay_tra_thuc_te):
    """Trả sách"""
    muon_tra_list = load_muon_tra()
    found = False
    
    for mt in muon_tra_list:
        if (mt.maKhach == ma_khach and 
            mt.IDSach == id_sach and 
            mt.trangThai in ["Đang mượn", "Quá hạn"]):
            
            # Tính phạt nếu trả muộn
            tinh_phat(mt, ngay_tra_thuc_te)
            mt.trangThai = "Đã trả"
            
            # Tăng số lượng sách
            books = get_all_books()
            for book in books:
                if book.BookID == id_sach:
                    update_book(id_sach, {"Quantity": book.Quantity + 1})
                    break
            
            found = True
            break
    
    if not found:
        raise ValueError("Không tìm thấy bản ghi mượn sách")
    
    save_muon_tra(muon_tra_list)
    return mt.phat

def cap_nhat_trang_thai():
    """Cập nhật trạng thái các sách quá hạn"""
    muon_tra_list = load_muon_tra()
    ngay_hien_tai = datetime.now().strftime("%Y-%m-%d")
    
    for mt in muon_tra_list:
        if mt.trangThai == "Đang mượn":
            tinh_phat(mt, ngay_hien_tai)
    
    save_muon_tra(muon_tra_list)

def tim_kiem_muon_tra(tu_khoa):
    """Tìm kiếm trong danh sách mượn/trả"""
    muon_tra_list = load_muon_tra()
    ket_qua = []
    
    for mt in muon_tra_list:
        if (tu_khoa.lower() in mt.maKhach.lower() or
            tu_khoa.lower() in mt.tenKhach.lower() or
            tu_khoa.lower() in mt.IDSach.lower() or
            tu_khoa.lower() in mt.tenSach.lower() or
            tu_khoa.lower() in mt.trangThai.lower()):
            ket_qua.append(mt)
    
    return ket_qua

def get_sach_qua_han():
    """Lấy danh sách sách quá hạn"""
    cap_nhat_trang_thai()
    muon_tra_list = load_muon_tra()
    return [mt for mt in muon_tra_list if mt.trangThai == "Quá hạn"]

def get_khach_hang_by_ma(ma_khach):
    """Lấy thông tin khách hàng theo mã"""
    muon_tra_list = load_muon_tra()
    for mt in muon_tra_list:
        if mt.maKhach == ma_khach:
            return {
                'tenKhach': mt.tenKhach,
                'soDienThoai': mt.soDienThoai,
                'email': mt.email,
                'diaChi': mt.diaChi
            }
    return None

def thong_ke_muon_tra():
    """Thống kê tổng quan mượn/trả sách"""
    muon_tra_list = load_muon_tra()
    
    tong_muon = len(muon_tra_list)
    dang_muon = len([mt for mt in muon_tra_list if mt.trangThai == "Đang mượn"])
    da_tra = len([mt for mt in muon_tra_list if mt.trangThai == "Đã trả"])
    qua_han = len([mt for mt in muon_tra_list if mt.trangThai == "Quá hạn"])
    
    tong_phat = sum([mt.phat for mt in muon_tra_list])
    
    return {
        'tong_muon': tong_muon,
        'dang_muon': dang_muon,
        'da_tra': da_tra,
        'qua_han': qua_han,
        'tong_phat': tong_phat
    }