"""
Hướng dẫn chi tiết: Đóng gói ứng dụng PDF Converter thành file .exe
"""

# ============================================================================
# PHẦN 1: CHUẨN BỊ MÔI TRƯỜNG
# ============================================================================

"""
Bước 1.1: Cài đặt Python (nếu chưa có)
  - Tải từ: https://www.python.org/downloads/
  - Phiên bản: Python 3.9 trở lên
  - ⚠️ QUAN TRỌNG: Chọn "Add Python to PATH" khi cài đặt
  
Bước 1.2: Kiểm tra Python đã cài đặt
  - Mở Command Prompt (Windows) hoặc Terminal (Mac/Linux)
  - Gõ: python --version
  - Kết quả: Python 3.x.x (ví dụ: Python 3.11.5)

Bước 1.3: Cài đặt dependencies
  - Mở Command Prompt tại thư mục project
  - Gõ: pip install -r requirements.txt
  - Đợi cài đặt hoàn tất (có thể mất vài phút)
"""

# ============================================================================
# PHẦN 2: CỘNG CỤ VÀ THƯ VIỆN CẦN THIẾT
# ============================================================================

"""
2.1 PyInstaller - Công cụ chính để tạo .exe
  Cài đặt: pip install pyinstaller
  
2.2 Các thư viện phụ thuộc
  - PyQt5 (giao diện)
  - pdfplumber (xử lý PDF)
  - python-docx (tạo Word)
  - openpyxl (tạo Excel)
  - pytesseract (OCR - tùy chọn)
  - Pillow (xử lý hình ảnh)
  
2.3 Tesseract OCR (tùy chọn, cho tính năng OCR)
  Cài đặt:
  - Windows: Tải từ https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: brew install tesseract
  - Linux: sudo apt-get install tesseract-ocr
"""

# ============================================================================
# PHẦN 3: PHƯƠNG PHÁP 1 - DÙNG PYINSTALLER (Dễ nhất)
# ============================================================================

"""
📋 BƯỚC CẢ CHI TIẾT:

BƯỚC 1: Cài đặt PyInstaller
  $ pip install pyinstaller

BƯỚC 2: Mở Command Prompt tại thư mục project
  - Nhấn Windows + R
  - Gõ: cmd
  - Nhấn Enter
  - Gõ: cd "C:\đường\dẫn\đến\pdf\project"
  
BƯỚC 3: Chạy lệnh tạo .exe
  $ pyinstaller --onefile --windowed --name "PDF_Converter" main.py
  
  Giải thích các tham số:
  - --onefile: Tạo 1 file .exe duy nhất (thay vì nhiều file)
  - --windowed: Ẩn console window (chỉ hiển thị GUI)
  - --name: Tên của file .exe
  - main.py: File Python chính
  
BƯỚC 4: Chờ quá trình hoàn thành
  - Mất khoảng 1-5 phút
  - Sẽ thấy thông báo "completed successfully"
  
BƯỚC 5: Tìm file .exe
  - File nằm trong thư mục: dist/
  - Tên file: PDF_Converter.exe
  - Kích thước: ~150-200 MB
  
✅ XONG! Bạn có thể chạy file .exe ngay lập tức
"""

# ============================================================================
# PHẦN 4: PHƯƠNG PHÁP 2 - DÙNG SCRIPT TỰ ĐỘNG
# ============================================================================

"""
📋 CÁCH DÙNG SCRIPT TỰ ĐỘNG:

BƯỚC 1: Chạy script tự động
  $ python build_executable.py
  
BƯỚC 2: Script sẽ tự động:
  ✓ Kiểm tra PyInstaller
  ✓ Chạy lệnh tạo .exe
  ✓ Dọn dẹp file tạm
  ✓ Hiển thị đường dẫn file .exe
  
BƯỚC 3: Tìm file trong thư mục dist/

ℹ️ LỢI ÍCH:
  - Tiết kiệm thời gian
  - Tự động xử lý các tham số phức tạp
  - Dọn dẹp file tạm tự động
"""

# ============================================================================
# PHẦN 5: PHƯƠNG PHÁP 3 - NÂNG CAO VỚI ICON & CÀI ĐẶT TỰ ĐỘNG
# ============================================================================

"""
📋 THÊM ICON CHO ỨNG DỤNG:

BƯỚC 1: Chuẩn bị icon
  - Tạo file icon có đuôi .ico
  - Kích thước: 256x256 pixel hoặc lớn hơn
  - Công cụ tạo icon: 
    • https://convertio.co/png-ico/ (online)
    • https://icoconvert.com/ (online)
    • Adobe Photoshop, GIMP, v.v.
  
BƯỚC 2: Lệnh với icon
  $ pyinstaller --onefile --windowed --icon="app_icon.ico" --name "PDF_Converter" main.py
  
Lưu ý: 
  - Đặt file icon cùng thư mục với main.py
  - Hoặc cung cấp đường dẫn đầy đủ

BƯỚC 3: Kết quả
  - File .exe sẽ có icon bạn đã chọn
"""

# ============================================================================
# PHẦN 6: TẠO CÀI ĐẶT INSTALLER (.MSI hoặc .NSIS)
# ============================================================================

"""
📋 PHƯƠNG PHÁP A: TỰ CÀI ĐẶT CHO NGƯỜI DÙNG

Sử dụng NSIS (Nullsoft Scriptable Install System)

BƯỚC 1: Tải NSIS
  - Tải từ: https://nsis.sourceforge.io/
  - Cài đặt bình thường
  
BƯỚC 2: Tạo file .nsi
  - Tạo file mới: installer.nsi
  - Nội dung:

---
; Installer Script cho PDF Converter
; NSIS Installer Script

!include "MUI2.nsh"

; Cấu hình cơ bản
Name "PDF Converter"
OutFile "PDF_Converter_Setup.exe"
InstallDir "$PROGRAMFILES\PDFConverter"

; Trang chào mừng
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Vietnamese"

; Cài đặt
Section "Cài đặt"
  SetOutPath "$INSTDIR"
  File "dist\PDF_Converter.exe"
  
  ; Tạo shortcut
  CreateDirectory "$SMPROGRAMS\PDF Converter"
  CreateShortcut "$SMPROGRAMS\PDF Converter\PDF Converter.lnk" "$INSTDIR\PDF_Converter.exe"
  CreateShortcut "$DESKTOP\PDF Converter.lnk" "$INSTDIR\PDF_Converter.exe"
SectionEnd

; Gỡ cài đặt
Section "Uninstall"
  Delete "$INSTDIR\PDF_Converter.exe"
  Delete "$SMPROGRAMS\PDF Converter\PDF Converter.lnk"
  Delete "$DESKTOP\PDF Converter.lnk"
  RMDir "$SMPROGRAMS\PDF Converter"
  RMDir "$INSTDIR"
SectionEnd
---

BƯỚC 3: Biên dịch installer
  - Mở file installer.nsi bằng NSIS Editor
  - Nhấn Ctrl+F11 hoặc Compile > Compile NSI Script
  - Kết quả: PDF_Converter_Setup.exe (cài đặt tự động)

✅ Người dùng chỉ cần chạy Setup file này!
"""

# ============================================================================
# PHẦN 7: PHÂN PHỐI ỨNG DỤNG
# ============================================================================

"""
📦 CÁCH PHÂN PHỐI CHO NGƯỜI DÙNG:

CÁCH 1: Chia sẻ file .exe trực tiếp
  ✓ Lợi ích: Đơn giản, chạy ngay
  ✗ Nhược điểm: File lớn (~200MB)
  
  Các bước:
  1. Tìm file: dist/PDF_Converter.exe
  2. Copy file này
  3. Tạo folder: "PDF_Converter_v1.0"
  4. Paste file vào folder
  5. Thêm file README.txt hướng dẫn sử dụng
  6. Nén thành .zip
  7. Chia sẻ file .zip

CÁCH 2: Tạo installer setup
  ✓ Lợi ích: Chuyên nghiệp, tự động cài đặt
  ✗ Nhược điểm: Phức tạp hơn
  
  Các bước:
  1. Tạo file NSIS như phần 6
  2. Biên dịch thành PDF_Converter_Setup.exe
  3. Chia sẻ file Setup này
  4. Người dùng chạy → cài đặt tự động → có shortcut trên Desktop

CÁCH 3: Upload lên GitHub Release
  1. Tạo GitHub Repository
  2. Commit code
  3. Tạo Release mới
  4. Upload file .exe hoặc .zip
  5. Chia sẻ link download

CÁCH 4: Tạo website/landing page
  - Tạo website để download
  - Hiển thị hướng dẫn sử dụng
  - Cung cấp support
"""

# ============================================================================
# PHẦN 8: GỠ LỖI & TỐI ƯU HÓA
# ============================================================================

"""
🔧 KHẮC PHỤC SỰ CỐ:

Lỗi 1: "ModuleNotFoundError: No module named..."
  Giải pháp:
  - Cài đặt lại requirements: pip install -r requirements.txt
  - Thêm tham số --hidden-import vào lệnh PyInstaller
  
  Ví dụ:
  $ pyinstaller --onefile --windowed \\
    --hidden-import=PyQt5 \\
    --hidden-import=pdfplumber \\
    --hidden-import=pytesseract \\
    main.py

Lỗi 2: File .exe chạy nhưng không có giao diện
  Giải pháp:
  - Kiểm tra xem đã dùng --windowed chưa
  - Xem log file: pdf_converter.log
  
Lỗi 3: File .exe chạy chậm khi khởi động
  Nguyên nhân: File lớn, cần load thư viện
  Giải pháp:
  - Bình thường, chỉ cần chờ một chút
  - Lần sau sẽ nhanh hơn

⚡ TỐI ƯU HÓA:

1. Giảm kích thước file:
   - Dùng UPX (Ultimate Packer for eXecutables)
   - Cài: pip install upx
   - Lệnh: pyinstaller --upx-dir=/path/to/upx --onefile main.py

2. Giảm thời gian khởi động:
   - Chỉ include các module cần thiết
   - Loại bỏ các module không dùng
"""

# ============================================================================
# PHẦN 9: KIỂM TRA & KIỂM NGHIỆM
# ============================================================================

"""
✅ CHECKLIST TRƯỚC KHI PHÂN PHỐI:

□ File .exe tạo thành công
□ File .exe chạy được trên máy mình
□ Kiểm tra tất cả tính năng:
  □ Chọn file PDF
  □ Chuyển sang Word - thành công
  □ Chuyển sang Excel - thành công
  □ Xử lý hàng loạt - thành công
  □ OCR (nếu có) - thành công
  
□ Thử chạy trên máy khác (nếu có)
□ Tạo README hướng dẫn sử dụng
□ Chuẩn bị tệp hỗ trợ/liên hệ
□ Test installer (nếu có)
□ Chuẩn bị thông tin phiên bản

✔️ XONG! Sẵn sàng phân phối
"""

# ============================================================================
# PHẦN 10: LỆNH NHANH THAM KHẢO
# ============================================================================

"""
📝 BỘSƯU TẬP LỆNH NHANH:

Lệnh cơ bản (đơn giản):
  $ pyinstaller --onefile --windowed main.py

Lệnh với icon:
  $ pyinstaller --onefile --windowed --icon=icon.ico main.py

Lệnh nâng cao (với hidden imports):
  $ pyinstaller --onefile --windowed \\
    --hidden-import=PyQt5 \\
    --hidden-import=pdfplumber \\
    --name="PDF_Converter" \\
    main.py

Lệnh với console (để debug):
  $ pyinstaller --onefile --name="PDF_Converter" main.py
  (bỏ --windowed để giữ console)

Xóa build files cũ:
  $ rm -r build dist *.spec  (Mac/Linux)
  $ rmdir /s build dist      (Windows)

Kiểm tra file .exe được tạo:
  Windows: dir dist\\
  Mac/Linux: ls dist/
"""

# ============================================================================
# PHẦN 11: VIDEO HƯỚNG DẪN (THAM KHẢO)
# ============================================================================

"""
Nếu cần hướng dẫn trực quan, bạn có thể tìm:
- YouTube: "PyInstaller tutorial"
- YouTube: "Create exe from Python"
- YouTube: "NSIS installer tutorial"
"""

# ============================================================================
# PHẦN 12: HỖ TRỢ & CÂU HỎI THƯỜNG GẶP
# ============================================================================

"""
Q: File .exe bao lớn?
A: Khoảng 150-200 MB (thông thường cho PyQt5 + các thư viện)

Q: Có thể giảm kích thước không?
A: Có thể, dùng UPX hoặc loại bỏ các module không cần

Q: Cần cài đặt Python trên máy khác không?
A: Không, .exe là standalone (tự chứa tất cả)

Q: Hoạt động trên Mac/Linux không?
A: Chỉ hoạt động trên Windows (nếu build trên Windows)
  Để chạy trên Mac/Linux, cần build trên hệ điều hành đó

Q: Có thể cập nhật ứng dụng không?
A: Có, tạo version mới và phân phối lại file .exe

Q: Cần license gì không?
A: PyInstaller: GPLv2+
  PyQt5: LGPLv3
  Xem tài liệu từng thư viện để chi tiết
"""

# ============================================================================
# KẾT LUẬN
# ============================================================================

"""
🎉 HOÀN THÀNH!

Bạn đã có ứng dụng desktop hoàn chỉnh:
✓ Mã nguồn Python
✓ Giao diện PyQt5
✓ File .exe thực thi
✓ Installer (tuỳ chọn)

Tiếp theo:
1. Test kỹ trước khi phân phối
2. Chuẩn bị tài liệu hướng dẫn
3. Chia sẻ với người dùng
4. Thu thập feedback
5. Cập nhật và cải thiện

Chúc bạn thành công! 🚀
"""
