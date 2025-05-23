import tkinter as tk
from kiemtra import kiemTraHoacTaoUserMacDinh, kiemTraQuyen
from GiaoDien_DangNhap import GiaoDienDangNhap

def main():
    kiemTraHoacTaoUserMacDinh()
    root = tk.Tk()
    app = GiaoDienDangNhap(root, kiemTraQuyen)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()