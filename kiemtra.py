import json
import os
from QuanLy import User
import tkinter as tk
from tkinter import messagebox, ttk

# Hàm kiểm tra và tạo user mặc định nếu cần
def kiemTraHoacTaoUserMacDinh():
    filepath = "users.json"
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        admin_user = [{
            "username": "admin",
            "password": "123",
            "role": "Quản Lý",
            "permission": True
        }]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(admin_user, f, indent=4, ensure_ascii=False)

# Hàm kiểm tra quyền đăng nhập
def kiemTraQuyen(username, password, role):
    filepath = "users.json"
    with open(filepath, "r", encoding="utf-8") as f:
        ds_user = json.load(f)
        for u in ds_user:
            if u["username"] == username and u["password"] == password and u["role"] == role:
                quyen = u.get("permission", False)
                return User(u["username"], u["password"], u["role"], quyen)
    return None