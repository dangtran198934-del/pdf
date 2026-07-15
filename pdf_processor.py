"""
PDF Processor Module - Xử lý trích xuất dữ liệu từ PDF
"""

import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import logging
from typing import List, Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Xử lý và trích xuất dữ liệu từ file PDF"""
    
    def __init__(self, pdf_path: str, use_ocr: bool = False):
        """
        Khởi tạo PDF Processor
        
        Args:
            pdf_path: Đường dẫn tới file PDF
            use_ocr: Sử dụng OCR cho PDF hình ảnh (mặc định: False)
        """
        self.pdf_path = pdf_path
        self.use_ocr = use_ocr
        self.pdf = None
        self.text_content = ""
        self.tables = []
        self.images = []
        
    def load_pdf(self) -> bool:
        """
        Tải file PDF
        
        Returns:
            True nếu tải thành công, False nếu thất bại
        """
        try:
            if not os.path.exists(self.pdf_path):
                logger.error(f"File không tồn tại: {self.pdf_path}")
                return False
                
            self.pdf = pdfplumber.open(self.pdf_path)
            logger.info(f"PDF tải thành công: {self.pdf_path}")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi tải PDF: {str(e)}")
            return False
    
    def extract_text(self, page_num: Optional[int] = None) -> str:
        """
        Trích xuất văn bản từ PDF
        
        Args:
            page_num: Số trang cụ thể (None = tất cả trang)
            
        Returns:
            Văn bản trích xuất
        """
        if self.pdf is None:
            self.load_pdf()
            
        try:
            text = ""
            pages = [self.pdf.pages[page_num]] if page_num else self.pdf.pages
            
            for page in pages:
                text += page.extract_text() or ""
                text += "\n"
                
            self.text_content = text
            logger.info(f"Trích xuất văn bản thành công: {len(text)} ký tự")
            return text
        except Exception as e:
            logger.error(f"Lỗi trích xuất văn bản: {str(e)}")
            return ""
    
    def extract_tables(self, page_num: Optional[int] = None) -> List[pd.DataFrame]:
        """
        Trích xuất bảng từ PDF
        
        Args:
            page_num: Số trang cụ thể (None = tất cả trang)
            
        Returns:
            Danh sách DataFrame chứa các bảng
        """
        if self.pdf is None:
            self.load_pdf()
            
        try:
            tables = []
            pages = [self.pdf.pages[page_num]] if page_num else self.pdf.pages
            
            for idx, page in enumerate(pages):
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)
                        logger.info(f"Trích xuất bảng từ trang {idx+1}: {df.shape}")
                        
            self.tables = tables
            logger.info(f"Tổng cộng trích xuất {len(tables)} bảng")
            return tables
        except Exception as e:
            logger.error(f"Lỗi trích xuất bảng: {str(e)}")
            return []
    
    def extract_images(self, output_dir: str = "extracted_images", 
                      page_num: Optional[int] = None) -> List[str]:
        """
        Trích xuất hình ảnh từ PDF
        
        Args:
            output_dir: Thư mục lưu hình ảnh
            page_num: Số trang cụ thể (None = tất cả trang)
            
        Returns:
            Danh sách đường dẫn hình ảnh
        """
        if self.pdf is None:
            self.load_pdf()
            
        try:
            os.makedirs(output_dir, exist_ok=True)
            image_paths = []
            pages = [self.pdf.pages[page_num]] if page_num else self.pdf.pages
            
            for page_idx, page in enumerate(pages):
                images = page.images
                for img_idx, image in enumerate(images):
                    # Lưu hình ảnh
                    img_name = f"page_{page_idx+1}_img_{img_idx+1}.png"
                    img_path = os.path.join(output_dir, img_name)
                    # Tạo hình ảnh từ crop
                    im = page.crop(image["top_left"] + image["bottom_right"]).to_image()
                    im.save(img_path)
                    image_paths.append(img_path)
                    
            self.images = image_paths
            logger.info(f"Trích xuất {len(image_paths)} hình ảnh")
            return image_paths
        except Exception as e:
            logger.error(f"Lỗi trích xuất hình ảnh: {str(e)}")
            return []
    
    def ocr_text(self) -> str:
        """
        Sử dụng OCR để nhận diện văn bản từ PDF hình ảnh
        
        Returns:
            Văn bản nhận diện được
        """
        try:
            # Chuyển PDF sang hình ảnh
            images = convert_from_path(self.pdf_path)
            text = ""
            
            for page_num, image in enumerate(images):
                # Nhận diện văn bản
                page_text = pytesseract.image_to_string(image, lang='vie+eng')
                text += f"--- Page {page_num + 1} ---\n"
                text += page_text + "\n"
                logger.info(f"OCR trang {page_num + 1} thành công")
                
            self.text_content = text
            return text
        except Exception as e:
            logger.error(f"Lỗi OCR: {str(e)}")
            return ""
    
    def get_pdf_info(self) -> Dict[str, Any]:
        """
        Lấy thông tin về PDF
        
        Returns:
            Dictionary chứa thông tin PDF
        """
        if self.pdf is None:
            self.load_pdf()
            
        try:
            info = {
                "file_name": os.path.basename(self.pdf_path),
                "file_size": os.path.getsize(self.pdf_path) / 1024,  # KB
                "num_pages": len(self.pdf.pages),
                "metadata": self.pdf.metadata or {}
            }
            return info
        except Exception as e:
            logger.error(f"Lỗi lấy thông tin PDF: {str(e)}")
            return {}
    
    def close(self):
        """Đóng file PDF"""
        if self.pdf:
            self.pdf.close()
            logger.info("PDF đã đóng")
    
    def __enter__(self):
        """Context manager support"""
        self.load_pdf()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.close()


class BatchPDFProcessor:
    """Xử lý hàng loạt nhiều file PDF"""
    
    def __init__(self, pdf_paths: List[str], use_ocr: bool = False):
        """
        Khởi tạo Batch PDF Processor
        
        Args:
            pdf_paths: Danh sách đường dẫn PDF
            use_ocr: Sử dụng OCR cho PDF hình ảnh
        """
        self.pdf_paths = pdf_paths
        self.use_ocr = use_ocr
        self.results = []
        
    def process_all(self, callback=None) -> List[Dict]:
        """
        Xử lý tất cả file PDF
        
        Args:
            callback: Hàm callback để cập nhật tiến độ (optional)
            
        Returns:
            Danh sách kết quả xử lý
        """
        results = []
        
        for idx, pdf_path in enumerate(self.pdf_paths):
            try:
                processor = PDFProcessor(pdf_path, self.use_ocr)
                processor.load_pdf()
                
                result = {
                    "file": pdf_path,
                    "success": True,
                    "text": processor.extract_text(),
                    "tables": processor.extract_tables(),
                    "info": processor.get_pdf_info(),
                    "error": None
                }
                processor.close()
                
                results.append(result)
                logger.info(f"Xử lý thành công {idx+1}/{len(self.pdf_paths)}: {pdf_path}")
                
            except Exception as e:
                logger.error(f"Lỗi xử lý {pdf_path}: {str(e)}")
                results.append({
                    "file": pdf_path,
                    "success": False,
                    "error": str(e)
                })
            
            # Gọi callback để cập nhật tiến độ
            if callback:
                callback(idx + 1, len(self.pdf_paths))
                
        self.results = results
        return results
