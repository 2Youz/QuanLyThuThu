class User:
    def __init__(self, tenDN, matKhau, chucvu, quyen = False):
        self.username = tenDN
        self.password = matKhau
        self.role = chucvu
        self.permission = quyen
class Book:
    def __init__(self, maSach, tenSach, tacGia, theLoai, soLuong):
        self.BookID = maSach
        self.BookName = tenSach
        self.Author = tacGia
        self.Category = theLoai
        self.Quantity = soLuong
    def to_dict(self):
        return {
            'BookID': self.BookID,
            'BookName': self.BookName,
            'Author': self.Author,
            'Category': self.Category,
            'Quantity': self.Quantity,
        }
    def from_dict(self, data):
        self.BookID = data['BookID']
        self.BookName = data['BookName']
        self.Author = data['Author']
        self.Category = data['Category']
        self.Quantity = data['Quantity']
class MuonTraSach:
    def __init__(self, maKhach, tenKhach, soDienThoai, email, diaChi, IDSach, tenSach, ngayMuon, ngayTra, trangThai="Đang mượn", phat=0):
        # Thông tin khách hàng
        self.maKhach = maKhach
        self.tenKhach = tenKhach
        self.soDienThoai = soDienThoai
        self.email = email
        self.diaChi = diaChi
        
        # Thông tin sách mượn
        self.IDSach = IDSach
        self.tenSach = tenSach
        self.ngayMuon = ngayMuon
        self.ngayTra = ngayTra
        
        # Trạng thái và phạt
        self.trangThai = trangThai  # "Đang mượn", "Đã trả", "Quá hạn"
        self.phat = phat  # Số tiền phạt nếu trả muộn
    
    def to_dict(self):
        return {
            'maKhach': self.maKhach,
            'tenKhach': self.tenKhach,
            'soDienThoai': self.soDienThoai,
            'email': self.email,
            'diaChi': self.diaChi,
            'IDSach': self.IDSach,
            'tenSach': self.tenSach,
            'ngayMuon': self.ngayMuon,
            'ngayTra': self.ngayTra,
            'trangThai': self.trangThai,
            'phat': self.phat
        }
    
    def from_dict(self, data):
        self.maKhach = data['maKhach']
        self.tenKhach = data['tenKhach']
        self.soDienThoai = data['soDienThoai']
        self.email = data['email']
        self.diaChi = data['diaChi']
        self.IDSach = data['IDSach']
        self.tenSach = data['tenSach']
        self.ngayMuon = data['ngayMuon']
        self.ngayTra = data['ngayTra']
        self.trangThai = data['trangThai']
        self.phat = data['phat']
class ThuThu: # Thủ thư quản lý thư viện
    def __init__(self, maTT, tenTT, soDienthoai, email, diaChi, luong, calamViec):
        self.maTT = maTT
        self.tenTT = tenTT
        self.soDienthoai = soDienthoai
        self.email = email
        self.diaChi = diaChi
        self.luong = luong
        self.calamViec = calamViec
    def to_dict(self):
        return {
            'maTT': self.maTT,
            'tenTT': self.tenTT,
            'soDienthoai': self.soDienthoai,
            'email': self.email,
            'diaChi': self.diaChi,
            'luong': self.luong,
            'calamViec': self.calamViec
        }
    def from_dict(self, data):
        self.maTT = data['maTT']
        self.tenTT = data['tenTT']
        self.soDienthoai = data['soDienthoai']
        self.email = data['email']
        self.diaChi = data['diaChi']
        self.luong = data['luong']
        self.calamViec = data['calamViec']
        