"""
Word Converter Module - Chuyển đổi PDF sang Word (.docx)
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import pandas as pd
import logging
from typing import List, Optional, Dict
import os

logger = logging.getLogger(__name__)


class WordConverter:
    """Chuyển đổi nội dung sang tài liệu Word"""
    
    def __init__(self, title: str = "Converted Document"):
        """
        Khởi tạo Word Converter
        
        Args:
            title: Tiêu đề của tài liệu
        """
        self.document = Document()
        self.title = title
        self._setup_document()
        
    def _setup_document(self):
        """Thiết lập cấu hình tài liệu"""
        # Thêm tiêu đề
        heading = self.document.add_heading(self.title, level=0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Thiết lập font mặc định
        style = self.document.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(11)
        
    def add_text(self, text: str, heading_level: int = 0, 
                 bold: bool = False, italic: bool = False):
        """
        Thêm văn bản vào tài liệu
        
        Args:
            text: Nội dung văn bản
            heading_level: Mức độ heading (0=body, 1=H1, 2=H2, etc.)
            bold: In đậm
            italic: In nghiêng
        """
        try:
            if heading_level > 0:
                paragraph = self.document.add_heading(text, level=heading_level)
            else:
                paragraph = self.document.add_paragraph(text)
            
            # Định dạng
            for run in paragraph.runs:
                run.bold = bold
                run.italic = italic
                
            logger.info(f"Thêm văn bản: {text[:50]}...")
        except Exception as e:
            logger.error(f"Lỗi thêm văn bản: {str(e)}")
    
    def add_table(self, dataframe: pd.DataFrame, title: Optional[str] = None):
        """
        Thêm bảng dữ liệu vào tài liệu
        
        Args:
            dataframe: Dữ liệu bảng (DataFrame)
            title: Tiêu đề bảng (optional)
        """
        try:
            if title:
                self.add_text(title, heading_level=2)
            
            # Tạo bảng
            rows, cols = dataframe.shape
            table = self.document.add_table(rows=rows + 1, cols=cols)
            table.style = 'Light Grid Accent 1'
            
            # Thêm header
            header_cells = table.rows[0].cells
            for col_idx, column in enumerate(dataframe.columns):
                header_cells[col_idx].text = str(column)
                # Format header
                for paragraph in header_cells[col_idx].paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                # Màu nền header
                shading_elm = OxmlElement('w:shd')
                shading_elm.set(qn('w:fill'), '4472C4')
                header_cells[col_idx]._element.get_or_add_tcPr().append(shading_elm)
            
            # Thêm dữ liệu
            for row_idx, row in dataframe.iterrows():
                row_cells = table.rows[row_idx + 1].cells
                for col_idx, value in enumerate(row):
                    row_cells[col_idx].text = str(value)
            
            self.document.add_paragraph()  # Thêm khoảng trắng
            logger.info(f"Thêm bảng: {rows}x{cols}")
        except Exception as e:
            logger.error(f"Lỗi thêm bảng: {str(e)}")
    
    def add_image(self, image_path: str, width: Optional[float] = None):
        """
        Thêm hình ảnh vào tài liệu
        
        Args:
            image_path: Đường dẫn hình ảnh
            width: Chiều rộng hình ảnh (inches)
        """
        try:
            if not os.path.exists(image_path):
                logger.warning(f"Hình ảnh không tìm thấy: {image_path}")
                return
            
            if width:
                self.document.add_picture(image_path, width=Inches(width))
            else:
                self.document.add_picture(image_path, width=Inches(5))
            
            # Căn giữa
            last_paragraph = self.document.paragraphs[-1]
            last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            self.document.add_paragraph()  # Khoảng trắng
            logger.info(f"Thêm hình ảnh: {image_path}")
        except Exception as e:
            logger.error(f"Lỗi thêm hình ảnh: {str(e)}")
    
    def add_line_break(self, count: int = 1):
        """Thêm dòng trống"""
        for _ in range(count):
            self.document.add_paragraph()
    
    def add_page_break(self):
        """Thêm xuống trang"""
        self.document.add_page_break()
    
    def save(self, output_path: str) -> bool:
        """
        Lưu tài liệu Word
        
        Args:
            output_path: Đường dẫn lưu file
            
        Returns:
            True nếu lưu thành công
        """
        try:
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            
            self.document.save(output_path)
            logger.info(f"Lưu Word thành công: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Lỗi lưu Word: {str(e)}")
            return False


class PDFToWordConverter:
    """Chuyên đổi PDF sang Word"""
    
    def __init__(self, pdf_text: str, pdf_tables: List[pd.DataFrame] = None,
                 pdf_images: List[str] = None, title: str = "Converted Document"):
        """
        Khởi tạo converter
        
        Args:
            pdf_text: Văn bản từ PDF
            pdf_tables: Danh sách bảng từ PDF
            pdf_images: Danh sách đường dẫn hình ảnh
            title: Tiêu đề tài liệu
        """
        self.pdf_text = pdf_text
        self.pdf_tables = pdf_tables or []
        self.pdf_images = pdf_images or []
        self.title = title
        self.word_converter = WordConverter(title)
        
    def convert(self, keep_formatting: bool = True, 
               include_images: bool = True) -> bool:
        """
        Thực hiện chuyển đổi
        
        Args:
            keep_formatting: Giữ nguyên định dạng
            include_images: Bao gồm hình ảnh
            
        Returns:
            True nếu chuyển đổi thành công
        """
        try:
            # Thêm văn bản
            if self.pdf_text:
                # Xử lý văn bản để tách headings
                lines = self.pdf_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Phát hiện heading (văn bản viết hoa)
                    if len(line) > 0 and line.isupper() and len(line) < 80:
                        self.word_converter.add_text(line, heading_level=2)
                    else:
                        self.word_converter.add_text(line)
            
            # Thêm bảng
            for idx, table in enumerate(self.pdf_tables):
                self.word_converter.add_table(table, title=f"Table {idx + 1}")
            
            # Thêm hình ảnh
            if include_images:
                for image_path in self.pdf_images:
                    self.word_converter.add_image(image_path)
            
            logger.info("Chuyển đổi PDF sang Word thành công")
            return True
        except Exception as e:
            logger.error(f"Lỗi chuyển đổi: {str(e)}")
            return False
    
    def save(self, output_path: str) -> bool:
        """
        Lưu tài liệu Word
        
        Args:
            output_path: Đường dẫn lưu file
            
        Returns:
            True nếu lưu thành công
        """
        return self.word_converter.save(output_path)
