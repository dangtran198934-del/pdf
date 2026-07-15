"""
Excel Converter Module - Chuyển đổi PDF sang Excel (.xlsx)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import logging
from typing import List, Optional, Dict
import os

logger = logging.getLogger(__name__)


class ExcelConverter:
    """Chuyển đổi dữ liệu sang tài liệu Excel"""
    
    def __init__(self, title: str = "Converted Data"):
        """
        Khởi tạo Excel Converter
        
        Args:
            title: Tiêu đề workbook
        """
        self.workbook = Workbook()
        self.workbook.remove(self.workbook.active)  # Xóa sheet trống
        self.title = title
        self.sheet_count = 0
        
    def add_dataframe(self, df: pd.DataFrame, sheet_name: str = None,
                     include_index: bool = False,
                     auto_adjust_columns: bool = True) -> bool:
        """
        Thêm DataFrame vào sheet
        
        Args:
            df: Dữ liệu DataFrame
            sheet_name: Tên sheet (auto generate nếu None)
            include_index: Bao gồm index
            auto_adjust_columns: Tự động điều chỉnh chiều rộng cột
            
        Returns:
            True nếu thành công
        """
        try:
            # Tạo tên sheet nếu không được cung cấp
            if sheet_name is None:
                self.sheet_count += 1
                sheet_name = f"Sheet{self.sheet_count}"
            
            # Giới hạn độ dài tên sheet (Excel giới hạn 31 ký tự)
            sheet_name = sheet_name[:31]
            
            # Tạo sheet
            ws = self.workbook.create_sheet(title=sheet_name)
            
            # Thêm dữ liệu
            for r_idx, row in enumerate(df.values, 1):
                for c_idx, value in enumerate(row, 1):
                    cell = ws.cell(row=r_idx + 1, column=c_idx)
                    cell.value = value
            
            # Thêm header
            for c_idx, column in enumerate(df.columns, 1):
                cell = ws.cell(row=1, column=c_idx)
                cell.value = column
                # Format header
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", 
                                       fill_type="solid")
                cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # Tự động điều chỉnh cột
            if auto_adjust_columns:
                for c_idx, column in enumerate(df.columns, 1):
                    column_letter = get_column_letter(c_idx)
                    max_length = 0
                    
                    for row in ws.iter_rows(min_col=c_idx, max_col=c_idx):
                        for cell in row:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                    
                    adjusted_width = min(max_length + 2, 50)
                    ws.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Thêm sheet '{sheet_name}': {df.shape[0]} hàng, {df.shape[1]} cột")
            return True
        except Exception as e:
            logger.error(f"Lỗi thêm DataFrame: {str(e)}")
            return False
    
    def add_table_data(self, table_data: List[List], sheet_name: str = None,
                      has_header: bool = True) -> bool:
        """
        Thêm dữ liệu bảng (list of lists) vào sheet
        
        Args:
            table_data: Dữ liệu bảng [[row1], [row2], ...]
            sheet_name: Tên sheet
            has_header: Hàng đầu tiên là header
            
        Returns:
            True nếu thành công
        """
        try:
            if not table_data:
                logger.warning("Dữ liệu bảng trống")
                return False
            
            # Tạo tên sheet
            if sheet_name is None:
                self.sheet_count += 1
                sheet_name = f"Sheet{self.sheet_count}"
            
            sheet_name = sheet_name[:31]
            
            # Tạo sheet
            ws = self.workbook.create_sheet(title=sheet_name)
            
            # Thêm dữ liệu
            for r_idx, row in enumerate(table_data, 1):
                for c_idx, value in enumerate(row, 1):
                    cell = ws.cell(row=r_idx, column=c_idx)
                    cell.value = value
                    
                    # Format header nếu là hàng đầu tiên
                    if has_header and r_idx == 1:
                        cell.font = Font(bold=True, color="FFFFFF")
                        cell.fill = PatternFill(start_color="4472C4", end_color="4472C4",
                                              fill_type="solid")
                        cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # Điều chỉnh cột
            for c_idx in range(1, len(table_data[0]) + 1):
                column_letter = get_column_letter(c_idx)
                ws.column_dimensions[column_letter].width = 20
            
            logger.info(f"Thêm sheet '{sheet_name}': {len(table_data)} hàng")
            return True
        except Exception as e:
            logger.error(f"Lỗi thêm dữ liệu bảng: {str(e)}")
            return False
    
    def add_summary_sheet(self, summary_text: str):
        """
        Thêm sheet tóm tắt
        
        Args:
            summary_text: Nội dung tóm tắt
        """
        try:
            ws = self.workbook.create_sheet(title="Summary", index=0)
            
            # Thêm tiêu đề
            title_cell = ws['A1']
            title_cell.value = self.title
            title_cell.font = Font(size=14, bold=True)
            
            # Thêm nội dung tóm tắt
            ws['A3'].value = summary_text
            ws['A3'].alignment = Alignment(wrap_text=True)
            
            logger.info("Thêm sheet tóm tắt")
        except Exception as e:
            logger.error(f"Lỗi thêm sheet tóm tắt: {str(e)}")
    
    def save(self, output_path: str) -> bool:
        """
        Lưu file Excel
        
        Args:
            output_path: Đường dẫn lưu file
            
        Returns:
            True nếu lưu thành công
        """
        try:
            # Tạo thư mục nếu cần
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            
            self.workbook.save(output_path)
            logger.info(f"Lưu Excel thành công: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Lỗi lưu Excel: {str(e)}")
            return False


class PDFToExcelConverter:
    """Chuyên đổi PDF sang Excel"""
    
    def __init__(self, pdf_tables: List[pd.DataFrame] = None,
                 pdf_text: str = None, title: str = "PDF Data"):
        """
        Khởi tạo converter
        
        Args:
            pdf_tables: Danh sách bảng từ PDF
            pdf_text: Văn bản từ PDF (optional)
            title: Tiêu đề
        """
        self.pdf_tables = pdf_tables or []
        self.pdf_text = pdf_text
        self.title = title
        self.excel_converter = ExcelConverter(title)
        
    def convert(self, include_summary: bool = True,
               table_names: List[str] = None) -> bool:
        """
        Thực hiện chuyển đổi
        
        Args:
            include_summary: Bao gồm sheet tóm tắt
            table_names: Danh sách tên cho các bảng
            
        Returns:
            True nếu chuyển đổi thành công
        """
        try:
            if not self.pdf_tables:
                logger.warning("Không có bảng nào để chuyển đổi")
                return False
            
            # Thêm sheet tóm tắt
            if include_summary:
                summary = f"Tài liệu chuyên đổi từ PDF\n"
                summary += f"Số bảng: {len(self.pdf_tables)}\n"
                if self.pdf_text:
                    summary += f"Có nội dung văn bản: Có\n"
                self.excel_converter.add_summary_sheet(summary)
            
            # Thêm các bảng
            for idx, table in enumerate(self.pdf_tables):
                if isinstance(table, pd.DataFrame):
                    # Xác định tên sheet
                    if table_names and idx < len(table_names):
                        sheet_name = table_names[idx]
                    else:
                        sheet_name = f"Table_{idx + 1}"
                    
                    self.excel_converter.add_dataframe(table, sheet_name=sheet_name)
            
            logger.info(f"Chuyển đổi thành công {len(self.pdf_tables)} bảng")
            return True
        except Exception as e:
            logger.error(f"Lỗi chuyển đổi: {str(e)}")
            return False
    
    def save(self, output_path: str) -> bool:
        """
        Lưu file Excel
        
        Args:
            output_path: Đường dẫn lưu file
            
        Returns:
            True nếu lưu thành công
        """
        return self.excel_converter.save(output_path)
