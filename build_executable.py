"""
Build Script - Đóng gói ứng dụng thành executable
Sử dụng PyInstaller để tạo file .exe standalone
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Cấu hình
PROJECT_NAME = "PDF Converter"
MAIN_SCRIPT = "main.py"
ICON_FILE = None  # Thay bằng đường dẫn icon .ico nếu có
OUTPUT_DIR = "dist"
BUILD_DIR = "build"

def check_pyinstaller():
    """Kiểm tra PyInstaller đã cài đặt"""
    try:
        import PyInstaller
        print("✓ PyInstaller đã cài đặt")
        return True
    except ImportError:
        print("✗ PyInstaller chưa cài đặt")
        print("Cài đặt: pip install pyinstaller")
        return False

def build_executable():
    """Xây dựng file executable"""
    print(f"\n{'='*50}")
    print(f"Đóng gói {PROJECT_NAME}")
    print(f"{'='*50}\n")
    
    # Kiểm tra PyInstaller
    if not check_pyinstaller():
        sys.exit(1)
    
    # Lệnh PyInstaller cơ bản
    cmd = [
        "pyinstaller",
        "--onefile",  # Tạo 1 file duy nhất
        "--windowed",  # Không có console window
        "--name", PROJECT_NAME.replace(" ", "_"),
        "--distpath", OUTPUT_DIR,
        "--buildpath", BUILD_DIR,
        "--specpath", BUILD_DIR,
    ]
    
    # Thêm icon nếu có
    if ICON_FILE and os.path.exists(ICON_FILE):
        cmd.extend(["--icon", ICON_FILE])
    
    # Thêm các thư viện/module
    cmd.extend([
        "--hidden-import=PyQt5",
        "--hidden-import=pdfplumber",
        "--hidden-import=pdf2image",
        MAIN_SCRIPT
    ])
    
    print(f"Lệnh: {' '.join(cmd)}\n")
    
    try:
        # Chạy PyInstaller
        subprocess.run(cmd, check=True)
        print("\n✓ Xây dựng thành công!")
        
        # Thông tin output
        exe_name = PROJECT_NAME.replace(" ", "_")
        exe_path = os.path.join(OUTPUT_DIR, f"{exe_name}.exe")
        
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n📦 File executable: {exe_path}")
            print(f"   Dung lượng: {size_mb:.2f} MB")
        
        # Dọn dẹp build directory
        cleanup()
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Lỗi xây dựng: {e}")
        sys.exit(1)

def cleanup():
    """Dọn dẹp file tạm"""
    print("\nDọn dẹp file tạm...")
    try:
        if os.path.exists(BUILD_DIR):
            shutil.rmtree(BUILD_DIR)
            print(f"✓ Xóa {BUILD_DIR}")
    except Exception as e:
        print(f"⚠ Lỗi dọn dẹp: {e}")

def create_installer():
    """Tạo installer NSIS (tuỳ chọn)"""
    print("\n" + "="*50)
    print("Tạo Installer (NSIS)")
    print("="*50)
    print("\nCần cài đặt NSIS từ: https://nsis.sourceforge.io/")
    print("Sau đó tạo file .nsi để đóng gói installer")

def main():
    """Hàm chính"""
    # Kiểm tra file chính tồn tại
    if not os.path.exists(MAIN_SCRIPT):
        print(f"✗ Không tìm thấy {MAIN_SCRIPT}")
        sys.exit(1)
    
    # Kiểm tra requirements.txt
    if not os.path.exists("requirements.txt"):
        print("⚠ Không tìm thấy requirements.txt")
    
    # Xây dựng executable
    build_executable()
    
    print("\n" + "="*50)
    print("Hướng dẫn sử dụng file .exe")
    print("="*50)
    print("""
1. File .exe nằm trong thư mục: dist/
2. Bạn có thể:
   - Chạy trực tiếp từ thư mục dist/
   - Copy file .exe sang bất kỳ nơi đâu
   - Tạo shortcut trên Desktop
   - Thêm vào Start Menu
   
3. Để phân phối:
   - Tạo folder chứa file .exe
   - Tạo file README.txt hướng dẫn
   - Nén thành .zip để chia sẻ
    """)

if __name__ == "__main__":
    main()
