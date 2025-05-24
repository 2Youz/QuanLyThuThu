import json
import os
from QuanLy import ThuThu

THUTHU_FILE = "thuthu_data.json"

def load_thuthu():
    """Tải danh sách thủ thư từ file"""
    if not os.path.exists(THUTHU_FILE):
        return []
    
    try:
        with open(THUTHU_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            thuthu_list = []
            for item in data:
                thuthu = ThuThu(
                    item['maTT'],
                    item['tenTT'], 
                    item['soDienthoai'],
                    item['email'],
                    item['diaChi'],
                    item['luong'],
                    item['calamViec']
                )
                thuthu_list.append(thuthu)
            return thuthu_list
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Lỗi đọc file thủ thư: {e}")
        return []

def save_thuthu(thuthu_list):
    """Lưu danh sách thủ thư vào file"""
    try:
        data = [thuthu.to_dict() for thuthu in thuthu_list]
        with open(THUTHU_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi lưu file thủ thư: {e}")

def get_all_thuthu():
    """Lấy tất cả thủ thư"""
    return load_thuthu()

def add_thuthu(thuthu):
    """Thêm thủ thư mới"""
    thuthu_list = load_thuthu()
    
    # Kiểm tra trùng mã thủ thư
    for tt in thuthu_list:
        if tt.maTT == thuthu.maTT:
            raise ValueError(f"Mã thủ thư {thuthu.maTT} đã tồn tại!")
    
    thuthu_list.append(thuthu)
    save_thuthu(thuthu_list)

def update_thuthu(ma_thuthu, new_data):
    """Cập nhật thông tin thủ thư"""
    thuthu_list = load_thuthu()
    
    for thuthu in thuthu_list:
        if thuthu.maTT == ma_thuthu:
            # Cập nhật các trường
            if 'tenTT' in new_data:
                thuthu.tenTT = new_data['tenTT']
            if 'soDienthoai' in new_data:
                thuthu.soDienthoai = new_data['soDienthoai']
            if 'email' in new_data:
                thuthu.email = new_data['email']
            if 'diaChi' in new_data:
                thuthu.diaChi = new_data['diaChi']
            if 'luong' in new_data:
                thuthu.luong = new_data['luong']
            if 'calamViec' in new_data:
                thuthu.calamViec = new_data['calamViec']
            
            save_thuthu(thuthu_list)
            return
    
    raise ValueError(f"Không tìm thấy thủ thư có mã {ma_thuthu}")

def delete_thuthu(ma_thuthu):
    """Xóa thủ thư"""
    thuthu_list = load_thuthu()
    
    for i, thuthu in enumerate(thuthu_list):
        if thuthu.maTT == ma_thuthu:
            thuthu_list.pop(i)
            save_thuthu(thuthu_list)
            return
    
    raise ValueError(f"Không tìm thấy thủ thư có mã {ma_thuthu}")

def search_thuthu(keyword):
    """Tìm kiếm thủ thư theo từ khóa"""
    thuthu_list = load_thuthu()
    result = []
    
    keyword = keyword.lower()
    for thuthu in thuthu_list:
        if (keyword in thuthu.maTT.lower() or 
            keyword in thuthu.tenTT.lower() or
            keyword in thuthu.email.lower() or
            keyword in thuthu.soDienthoai.lower()):
            result.append(thuthu)
    
    return result

def get_thuthu_by_ma(ma_thuthu):
    """Lấy thông tin thủ thư theo mã"""
    thuthu_list = load_thuthu()
    
    for thuthu in thuthu_list:
        if thuthu.maTT == ma_thuthu:
            return thuthu
    
    return None