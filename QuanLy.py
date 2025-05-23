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