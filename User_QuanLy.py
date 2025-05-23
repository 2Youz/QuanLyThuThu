import json
import os
from QuanLy import User

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [User(u["username"], u["password"], u["role"], u.get("permission", False)) for u in data]

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump([u.__dict__ for u in users], f, indent=4, ensure_ascii=False)

def get_all_users():
    return load_users()

def add_user(user):
    users = load_users()
    for u in users:
        if u.username == user.username:
            raise ValueError("Tên đăng nhập đã tồn tại")
    users.append(user)
    save_users(users)

def update_user(username, new_data):
    users = load_users()
    found = False
    for u in users:
        if u.username == username:
            u.password = new_data.get("password", u.password)
            u.role = new_data.get("role", u.role)
            u.permission = new_data.get("permission", u.permission)
            found = True
            break
    if not found:
        raise ValueError("Không tìm thấy người dùng")
    save_users(users)

def delete_user(username):
    users = load_users()
    new_users = [u for u in users if u.username != username]
    if len(new_users) == len(users):
        raise ValueError("Không tìm thấy người dùng để xóa")
    save_users(new_users)