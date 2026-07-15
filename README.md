# PDF Converter - Desktop Application

Ứng dụng desktop chuyên nghiệp chuyển đổi file PDF sang Word (.docx) và Excel (.xlsx) với các tính năng nâng cao.

## ✨ Tính năng chính

- ✅ **Chuyển đổi bảng dữ liệu PDF → Excel** - Trích xuất bảng từ PDF và lưu sang Excel
- ✅ **Chuyển đổi văn bản PDF → Word** - Chuyển nội dung PDF thành tài liệu Word
- ✅ **Giữ nguyên định dạng** - Bảo toàn font, màu sắc, kích thước chữ
- ✅ **Xử lý hàng loạt** - Chuyển đổi nhiều file cùng một lúc
- ✅ **Giao diện thân thiện** - Giao diện đồ họa dễ sử dụng (PyQt5)
- ✅ **Hỗ trợ OCR** - Nhận diện văn bản từ PDF hình ảnh
- ✅ **Theo dõi tiến trình** - Hiển thị tiến độ xử lý real-time

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- Windows 10+ / macOS / Linux
- Tesseract OCR (tùy chọn, cho PDF hình ảnh)

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/dangtran198934-del/pdf.git
cd pdf
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cài đặt Tesseract (tùy chọn, cho OCR)

**Windows:**
- Download từ: https://github.com/UB-Mannheim/tesseract/wiki
- Cài đặt mặc định

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## 💻 Sử dụng

### Chạy ứng dụng
```bash
python main.py
```

### Giao diện chính

1. **Select Files** - Chọn file PDF cần chuyển đổi
2. **Choose Output Format** - Chọn định dạng output (Word/Excel)
3. **Configure Options** - Cấu hình tùy chọn xử lý
4. **Convert** - Bắt đầu chuyển đổi
5. **View Progress** - Xem tiến độ và kết quả

## 📁 Cấu trúc dự án

```
pdf/
├── main.py                 # Ứng dụng chính, giao diện PyQt5
├── pdf_processor.py        # Module xử lý PDF
├── word_converter.py       # Module chuyển đổi sang Word
├── excel_converter.py      # Module chuyển đổi sang Excel
├── ocr_handler.py          # Module xử lý OCR
├── ui/
│   ├── main_window.py      # Cửa sổ chính
│   ├── dialogs.py          # Các dialog hỗ trợ
│   └── styles.py           # CSS/Stylesheet
├── utils/
│   ├── file_utils.py       # Tiện ích xử lý file
│   ├── logger.py           # Logging
│   └── config.py           # Cấu hình
├── requirements.txt        # Dependencies
└── README.md              # Tài liệu này
```

## 🎯 Các tính năng chi tiết

### Chuyển đổi PDF → Excel
- Phát hiện tự động bảng trong PDF
- Giữ nguyên cấu trúc bảng
- Hỗ trợ nhiều bảng trong một file
- Export thành sheet riêng biệt

### Chuyển đổi PDF → Word
- Giữ nguyên định dạng văn bản
- Hỗ trợ header/footer
- Bảo toàn hình ảnh
- Tạo mục lục tự động

### Xử lý hàng loạt
- Chọn nhiều file PDF cùng lúc
- Chuyển đổi song song
- Báo cáo tóm tắt sau khi hoàn thành
- Tùy chọn ghi đè hoặc bỏ qua file tồn tại

## 📝 Ví dụ sử dụng

### Lập trình (API)
```python
from pdf_processor import PDFProcessor
from excel_converter import ExcelConverter

# Tạo processor
processor = PDFProcessor('input.pdf')

# Trích xuất bảng
tables = processor.extract_tables()

# Chuyển sang Excel
converter = ExcelConverter()
converter.save_tables(tables, 'output.xlsx')
```

## 🐛 Troubleshooting

### Lỗi: "Tesseract not found"
- Cài đặt Tesseract OCR từ link ở phần "Cài đặt"

### Lỗi: "Module not found"
- Chạy lại: `pip install -r requirements.txt`

### PDF không chuyển đổi được
- Kiểm tra file PDF không bị mã hóa
- Thử chuyển đổi file khác
- Xem log file để biết chi tiết

## 📄 Giấy phép

MIT License - xem file LICENSE

## 👨‍💻 Tác giả

Dang Tran

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork repository
2. Tạo branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo Issue trên GitHub hoặc liên hệ tác giả.
