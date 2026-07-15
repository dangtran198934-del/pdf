"""
Main Application - Ứng dụng Desktop chuyển đổi PDF
"""

import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QListWidget,
    QListWidgetItem, QComboBox, QCheckBox, QMessageBox, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor
from datetime import datetime
from pdf_processor import PDFProcessor, BatchPDFProcessor
from word_converter import PDFToWordConverter
from excel_converter import PDFToExcelConverter
import traceback

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_converter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ConversionWorker(QThread):
    """Worker thread cho xử lý chuyển đổi"""
    progress_updated = pyqtSignal(int, str)
    conversion_complete = pyqtSignal(bool, str)
    
    def __init__(self, pdf_files, output_format, output_dir, use_ocr=False):
        super().__init__()
        self.pdf_files = pdf_files
        self.output_format = output_format
        self.output_dir = output_dir
        self.use_ocr = use_ocr
        
    def run(self):
        """Chạy quá trình chuyển đổi"""
        try:
            total_files = len(self.pdf_files)
            successful = 0
            failed = 0
            
            for idx, pdf_file in enumerate(self.pdf_files):
                try:
                    self.progress_updated.emit(int((idx / total_files) * 100), 
                                             f"Đang xử lý: {os.path.basename(pdf_file)}")
                    
                    # Tạo processor
                    processor = PDFProcessor(pdf_file, use_ocr=self.use_ocr)
                    processor.load_pdf()
                    
                    # Xác định tên output
                    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                    
                    if self.output_format == "Word":
                        # Chuyển sang Word
                        text = processor.extract_text()
                        tables = processor.extract_tables()
                        
                        converter = PDFToWordConverter(
                            pdf_text=text,
                            pdf_tables=tables,
                            title=base_name
                        )
                        converter.convert(keep_formatting=True)
                        
                        output_path = os.path.join(self.output_dir, f"{base_name}.docx")
                        if converter.save(output_path):
                            successful += 1
                            logger.info(f"Chuyển đổi Word thành công: {output_path}")
                        else:
                            failed += 1
                            
                    elif self.output_format == "Excel":
                        # Chuyển sang Excel
                        tables = processor.extract_tables()
                        
                        if tables:
                            converter = PDFToExcelConverter(
                                pdf_tables=tables,
                                title=base_name
                            )
                            converter.convert()
                            
                            output_path = os.path.join(self.output_dir, f"{base_name}.xlsx")
                            if converter.save(output_path):
                                successful += 1
                                logger.info(f"Chuyển đổi Excel thành công: {output_path}")
                            else:
                                failed += 1
                        else:
                            failed += 1
                            logger.warning(f"Không tìm thấy bảng trong: {pdf_file}")
                    
                    processor.close()
                    
                except Exception as e:
                    failed += 1
                    logger.error(f"Lỗi xử lý {pdf_file}: {str(e)}\n{traceback.format_exc()}")
            
            # Cập nhật tiến độ hoàn thành
            self.progress_updated.emit(100, "Hoàn thành!")
            
            message = f"Chuyển đổi hoàn thành:\n✓ Thành công: {successful}\n✗ Thất bại: {failed}"
            self.conversion_complete.emit(True, message)
            
        except Exception as e:
            error_msg = f"Lỗi: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            self.conversion_complete.emit(False, error_msg)


class PDFConverterApp(QMainWindow):
    """Ứng dụng chính"""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.output_directory = os.path.expanduser("~/Documents")
        self.conversion_worker = None
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("PDF Converter - Chuyển đổi PDF sang Word/Excel")
        self.setGeometry(100, 100, 900, 700)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("PDF Converter")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_conversion_tab(), "Chuyển đổi")
        tabs.addTab(self.create_settings_tab(), "Cài đặt")
        main_layout.addWidget(tabs)
        
        central_widget.setLayout(main_layout)
        
    def create_conversion_tab(self):
        """Tạo tab chuyển đổi"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Nút chọn file
        btn_select = QPushButton("📁 Chọn file PDF")
        btn_select.setStyleSheet("padding: 10px; font-size: 12px;")
        btn_select.clicked.connect(self.select_files)
        layout.addWidget(btn_select)
        
        # Danh sách file đã chọn
        layout.addWidget(QLabel("Danh sách file:"))
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        # Nút xóa file
        btn_remove = QPushButton("❌ Xóa file đã chọn")
        btn_remove.clicked.connect(self.remove_selected_file)
        layout.addWidget(btn_remove)
        
        # Output format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Định dạng output:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Word (.docx)", "Excel (.xlsx)"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # Output directory
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Thư mục output:"))
        self.dir_label = QLabel(self.output_directory)
        dir_layout.addWidget(self.dir_label)
        btn_browse = QPushButton("Chọn thư mục")
        btn_browse.clicked.connect(self.select_output_directory)
        dir_layout.addWidget(btn_browse)
        layout.addLayout(dir_layout)
        
        # Options
        self.ocr_checkbox = QCheckBox("🔍 Sử dụng OCR (cho PDF hình ảnh)")
        layout.addWidget(self.ocr_checkbox)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng")
        layout.addWidget(self.status_label)
        
        # Convert button
        btn_convert = QPushButton("🚀 Bắt đầu chuyển đổi")
        btn_convert.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_convert.clicked.connect(self.start_conversion)
        layout.addWidget(btn_convert)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Tạo tab cài đặt"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Cài đặt ứng dụng:"))
        
        # Version
        layout.addWidget(QLabel("Phiên bản: 1.0.0"))
        
        # Author
        layout.addWidget(QLabel("Tác giả: Dang Tran"))
        
        # Thông tin
        info = QLabel(
            "PDF Converter - Công cụ chuyển đổi chuyên nghiệp\n\n"
            "Tính năng:\n"
            "• Chuyển đổi PDF → Word\n"
            "• Chuyển đổi PDF → Excel\n"
            "• Xử lý hàng loạt\n"
            "• Hỗ trợ OCR\n\n"
            "Hỗ trợ: Liên hệ tác giả qua GitHub"
        )
        layout.addWidget(info)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def select_files(self):
        """Chọn file PDF"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Chọn file PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if files:
            self.selected_files = files
            self.update_file_list()
            self.status_label.setText(f"Đã chọn {len(files)} file")
    
    def update_file_list(self):
        """Cập nhật danh sách file"""
        self.file_list.clear()
        for file in self.selected_files:
            item = QListWidgetItem(os.path.basename(file))
            self.file_list.addItem(item)
    
    def remove_selected_file(self):
        """Xóa file đã chọn"""
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            self.selected_files.pop(current_row)
            self.update_file_list()
    
    def select_output_directory(self):
        """Chọn thư mục output"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục lưu"
        )
        
        if directory:
            self.output_directory = directory
            self.dir_label.setText(directory)
    
    def start_conversion(self):
        """Bắt đầu chuyển đổi"""
        if not self.selected_files:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ít nhất một file PDF!")
            return
        
        # Lấy định dạng output
        output_format = "Word" if "Word" in self.format_combo.currentText() else "Excel"
        use_ocr = self.ocr_checkbox.isChecked()
        
        # Tạo worker thread
        self.conversion_worker = ConversionWorker(
            self.selected_files,
            output_format,
            self.output_directory,
            use_ocr
        )
        self.conversion_worker.progress_updated.connect(self.update_progress)
        self.conversion_worker.conversion_complete.connect(self.conversion_finished)
        self.conversion_worker.start()
        
        self.status_label.setText("Đang xử lý...")
    
    def update_progress(self, value, message):
        """Cập nhật thanh tiến độ"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def conversion_finished(self, success, message):
        """Chuyển đổi hoàn thành"""
        if success:
            QMessageBox.information(self, "Thành công", message)
        else:
            QMessageBox.critical(self, "Lỗi", message)
        
        self.progress_bar.setValue(0)
        self.status_label.setText("Sẵn sàng")


def main():
    """Hàm chính"""
    app = QApplication(sys.argv)
    window = PDFConverterApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
