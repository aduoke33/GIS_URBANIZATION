r"""
scripts/standardize_report_docx.py
==================================
Tự động chuẩn hóa toàn diện tài liệu báo cáo Word (.docx) để nộp học thuật:
- Đọc nội dung gốc từ BAO_CAO_THUYET_MINH_HOAN_CHINH.md
- Xuất ra file mới hoàn chỉnh: BAO_CAO_THUYET_MINH_HOAN_CHINH_CHUAN_HOA.docx
- Tuân thủ nghiêm ngặt 10 nguyên tắc định dạng học thuật Việt Nam:
  1. Phong cách tối giản, nghiêm túc, chữ đen tuyệt đối (RGB 0,0,0).
  2. Trang bìa chính thức trang trọng của Trường Đại học Phenikaa (SV Ngô Đặng Nhật Dũng, GV Trịnh Thành).
  3. Tất cả bảng biểu NỀN TRẮNG 100%, không màu trang trí, không tô xen kẽ, lặp lại hàng tiêu đề (tblHeader), chống vỡ hàng (cantSplit).
  4. Chú thích Bảng đặt PHÍA TRÊN bảng ("Bảng X.X. ..."), chú thích Hình đặt PHÍA DƯỚI hình ("Hình X.X. ...").
  5. Thiết lập Heading styles thực sự (Heading 1, Heading 2, Heading 3) liên kết trường TOC của Word.
  6. Mục lục và các Danh mục đầu báo cáo có dấu chấm dóng hàng (dot leader) chuyên nghiệp.
  7. Ngắt trang (Page Break) trước mỗi chương và danh mục lớn.
  8. Chân trang có số trang tự động (PAGE field) căn giữa, không đánh số trang bìa.
  9. Nhúng trực tiếp toàn bộ 14 bản đồ & biểu đồ chất lượng cao 300 DPI.
  10. Xóa sạch các dấu phân cách trang trí (---) và hộp ghi chú emoji kiểu slide quảng cáo.
"""

import os
import sys
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MD_PATH = os.path.join(PROJ_ROOT, 'BAO_CAO_THUYET_MINH_HOAN_CHINH.md')
OUTPUT_DOCX_PATH = os.path.join(PROJ_ROOT, 'BAO_CAO_THUYET_MINH_HOAN_CHINH_CHUAN_HOA.docx')

# ─────────────────────────────────────────────────────────────
# XML HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def set_cell_margins(cell, top=70, bottom=70, left=90, right=90):
    """Thiết lập padding đệm bên trong ô bảng (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                       f'<w:top w:w="{top}" w:type="dxa"/>'
                       f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                       f'<w:left w:w="{left}" w:type="dxa"/>'
                       f'<w:right w:w="{right}" w:type="dxa"/>'
                       f'</w:tcMar>')
    tc_pr.append(tc_mar)

def set_cell_width(cell, width_cm):
    """Thiết lập độ rộng cột cố định cho ô."""
    width_dxa = int(width_cm * 567.0)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width_dxa}" w:type="dxa"/>')
    tc_pr.append(tc_w)

def set_academic_table_borders(table):
    """
    Kẻ viền bảng chuẩn phong cách học thuật quốc tế (APA / IEEE):
    - Viền trên cùng (top): nét đơn mảnh màu đen (0.5 pt)
    - Viền dưới cùng (bottom): nét đơn mảnh màu đen (0.5 pt)
    - Viền ngang phân cách giữa các dòng (insideH): nét mảnh xám trung tính (0.5 pt)
    - Không kẻ viền dọc (left, right, insideV = none) giúp bảng thoáng đãng, dễ đọc
    """
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="B0B0B0"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_table_robust(table):
    """Lặp lại tiêu đề khi qua trang (tblHeader) và chống xé đôi dòng (cantSplit)."""
    if len(table.rows) > 0:
        trPr = table.rows[0]._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def add_page_number_to_footer(section):
    """Thêm trường số trang tự động vào chân trang (Footer), căn giữa, Times New Roman 10pt."""
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    p._p.append(fld)
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def add_toc_field(paragraph):
    """Thêm trường mục lục tự động của Word (TOC Field)."""
    fld = parse_xml(r'<w:fldSimple %s w:instr="TOC \o &quot;1-3&quot; \h \z \u"/>' % nsdecls('w'))
    paragraph._p.append(fld)

def add_dot_leader_line(doc, title, page_str, level=1):
    """Thêm một dòng mục lục hoặc danh mục có dấu chấm dóng hàng (tab stop dot leader) đến lề phải 16.0 cm."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)

    # 16.0 cm = 9071 dxa (right aligned tab with dot leader)
    pPr = p._p.get_or_add_pPr()
    tabs = parse_xml(r'<w:tabs %s><w:tab w:val="right" w:leader="dot" w:pos="9071"/></w:tabs>' % nsdecls('w'))
    pPr.append(tabs)

    if level == 1:
        p.paragraph_format.left_indent = Cm(0)
        r1 = p.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0, 0, 0)
    elif level == 2:
        p.paragraph_format.left_indent = Cm(0.6)
        r1 = p.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = RGBColor(0, 0, 0)
    else:
        p.paragraph_format.left_indent = Cm(1.2)
        r1 = p.add_run(title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.italic = True
        r1.font.color.rgb = RGBColor(0, 0, 0)

    r2 = p.add_run(f"\t{page_str}")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.font.bold = (level == 1)
    r2.font.color.rgb = RGBColor(0, 0, 0)

def insert_figure(doc, rel_path, caption_text, width_in=5.6):
    """Chèn hình ảnh căn giữa kèm chú thích chuẩn học thuật đặt PHÍA DƯỚI hình."""
    full_path = os.path.join(PROJ_ROOT, rel_path.replace('/', os.sep))
    if os.path.exists(full_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        r = p_img.add_run()
        r.add_picture(full_path, width=Inches(width_in))

        # Chú thích hình: Times New Roman 10.5pt, in nghiêng, căn giữa
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        
        match = re.match(r'^(Hình\s+[\d\.]+[a-c]?:?\.?)\s*(.*)', caption_text)
        if match:
            r_bold = p_cap.add_run(match.group(1).rstrip(':') + '. ')
            r_bold.font.name = 'Times New Roman'
            r_bold.font.size = Pt(10.5)
            r_bold.font.bold = True
            r_bold.font.italic = True
            r_bold.font.color.rgb = RGBColor(0, 0, 0)

            r_text = p_cap.add_run(match.group(2))
            r_text.font.name = 'Times New Roman'
            r_text.font.size = Pt(10.5)
            r_text.font.italic = True
            r_text.font.color.rgb = RGBColor(0, 0, 0)
        else:
            r_text = p_cap.add_run(caption_text)
            r_text.font.name = 'Times New Roman'
            r_text.font.size = Pt(10.5)
            r_text.font.italic = True
            r_text.font.color.rgb = RGBColor(0, 0, 0)

        print(f"  [OK Hình] {rel_path} -> {caption_text[:50]}...")
        return True
    else:
        print(f"  [THIẾU TỆP HÌNH] Không tìm thấy: {full_path}")
        return False

def add_table_caption(doc, caption_text):
    """Thêm chú thích bảng chuẩn học thuật đặt PHÍA TRÊN bảng."""
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(14)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True

    match = re.match(r'^(Bảng\s+[\d\.]+:?\.?)\s*(.*)', caption_text)
    if match:
        r_bold = p_cap.add_run(match.group(1).rstrip(':') + '. ')
        r_bold.font.name = 'Times New Roman'
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(0, 0, 0)

        r_text = p_cap.add_run(match.group(2))
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(11)
        r_text.font.bold = True
        r_text.font.color.rgb = RGBColor(0, 0, 0)
    else:
        r_text = p_cap.add_run(caption_text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(11)
        r_text.font.bold = True
        r_text.font.color.rgb = RGBColor(0, 0, 0)

def clean_inline_math(text):
    """Làm sạch các ký hiệu LaTeX toán học thành văn bản thông thường dễ đọc trong Word."""
    t = text
    t = t.replace('$', '')
    t = t.replace(r'\text{', '').replace(r'}', '')
    t = t.replace(r'\mu\text{m}', 'µm')
    t = t.replace(r'\mu m', 'µm')
    t = t.replace(r'\approx', '≈')
    t = t.replace(r'\ge', '≥')
    t = t.replace(r'\le', '≤')
    t = t.replace(r'\times', '×')
    t = t.replace(r'\to', '→')
    t = t.replace(r'\xrightarrow', '→')
    t = t.replace(r'\ln', 'ln')
    t = t.replace(r'\exp', 'exp')
    t = t.replace(r'\kappa', 'κ')
    t = t.replace(r'\sum', '∑')
    t = t.replace(r'\prod', '∏')
    t = t.replace(r'\sqrt', '√')
    t = t.replace(r'\cdot', '·')
    t = t.replace(r'\sim', '~')
    t = t.replace(r'\%', '%')
    t = t.replace(r'\pm', '±')
    t = t.replace(r'^\circ', '°')
    t = t.replace(r'\quad', '   ')
    t = t.replace(r'\;', ' ')
    t = t.replace(r'\,', ' ')
    t = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1 / \2)', t)
    return t

# ─────────────────────────────────────────────────────────────
# MAIN BUILDER FUNCTION
# ─────────────────────────────────────────────────────────────

def build_standardized_docx():
    print(f"\n=========================================================")
    print(f"BẮT ĐẦU CHUẨN HÓA BÁO CÁO HỌC THUẬT DOCX")
    print(f"Nguồn markdown: {MD_PATH}")
    print(f"Đầu ra chuẩn hóa: {OUTPUT_DOCX_PATH}")
    print(f"=========================================================")

    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = Document()

    # ──────────────────────────────────────────────────────────
    # 1. CẤU HÌNH SECTION 1: TRANG BÌA (A4, LỀ CHUẨN, KHÔNG SỐ TRANG)
    # ──────────────────────────────────────────────────────────
    sec_cover = doc.sections[0]
    sec_cover.page_width = Cm(21.0)
    sec_cover.page_height = Cm(29.7)
    sec_cover.top_margin = Cm(2.0)
    sec_cover.bottom_margin = Cm(2.0)
    sec_cover.left_margin = Cm(3.0)   # 3.0 cm đóng gáy
    sec_cover.right_margin = Cm(2.0)
    sec_cover.different_first_page_header_footer = True

    # Cấu hình styles chuẩn toàn tài liệu
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.35
    style_normal.paragraph_format.space_after = Pt(5)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Heading 1 (Chương / Danh mục lớn)
    style_h1 = doc.styles['Heading 1']
    style_h1.font.name = 'Times New Roman'
    style_h1.font.size = Pt(15)
    style_h1.font.bold = True
    style_h1.font.color.rgb = RGBColor(0, 0, 0)
    style_h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_h1.paragraph_format.space_before = Pt(14)
    style_h1.paragraph_format.space_after = Pt(8)
    style_h1.paragraph_format.keep_with_next = True

    # Heading 2 (Mục cấp 1, ví dụ: 1.1, 1.2)
    style_h2 = doc.styles['Heading 2']
    style_h2.font.name = 'Times New Roman'
    style_h2.font.size = Pt(13)
    style_h2.font.bold = True
    style_h2.font.color.rgb = RGBColor(0, 0, 0)
    style_h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    style_h2.paragraph_format.space_before = Pt(10)
    style_h2.paragraph_format.space_after = Pt(4)
    style_h2.paragraph_format.keep_with_next = True

    # Heading 3 (Mục cấp 2, ví dụ: 1.1.1, 2.3.1)
    style_h3 = doc.styles['Heading 3']
    style_h3.font.name = 'Times New Roman'
    style_h3.font.size = Pt(12)
    style_h3.font.bold = True
    style_h3.font.color.rgb = RGBColor(0, 0, 0)
    style_h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    style_h3.paragraph_format.space_before = Pt(6)
    style_h3.paragraph_format.space_after = Pt(2)
    style_h3.paragraph_format.keep_with_next = True

    # ──────────────────────────────────────────────────────────
    # 2. XÂY DỰNG TRANG BÌA CHÍNH THỨC (TRƯỜNG ĐẠI HỌC PHENIKAA)
    # ──────────────────────────────────────────────────────────
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(3)
    p_inst.paragraph_format.line_spacing = 1.15
    r = p_inst.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    r2 = p_inst.add_run("TRƯỜNG ĐẠI HỌC PHENIKAA\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13.5)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0, 0, 0)

    r3 = p_inst.add_run("KHOA CÔNG NGHỆ THÔNG TIN")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(12.5)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(0, 0, 0)

    # Đường phân cách ngang đen mảnh thanh lịch
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(4)
    p_div.paragraph_format.space_after = Pt(28)
    r_div = p_div.add_run("━━━━━━━━━━━━━━━━━━━")
    r_div.font.name = 'Times New Roman'
    r_div.font.size = Pt(10)
    r_div.font.color.rgb = RGBColor(0, 0, 0)

    # Tiêu đề loại tài liệu
    p_report_type = doc.add_paragraph()
    p_report_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_report_type.paragraph_format.space_before = Pt(0)
    p_report_type.paragraph_format.space_after = Pt(24)
    p_report_type.paragraph_format.line_spacing = 1.2
    r_rt = p_report_type.add_run("BÁO CÁO THUYẾT MINH BÀI TẬP LỚN\n")
    r_rt.font.name = 'Times New Roman'
    r_rt.font.size = Pt(14)
    r_rt.font.bold = True
    r_rt.font.color.rgb = RGBColor(0, 0, 0)

    r_sub = p_report_type.add_run("HỌC PHẦN: XỬ LÝ DỮ LIỆU GIS THÔNG MINH (GeoAI)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0, 0, 0)

    # Tên đề tài (Chữ đen 16.5pt, đậm, căn giữa)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(14)
    p_title.paragraph_format.line_spacing = 1.25
    r_title_lbl = p_title.add_run("ĐỀ TÀI:\n")
    r_title_lbl.font.name = 'Times New Roman'
    r_title_lbl.font.size = Pt(14)
    r_title_lbl.font.bold = True
    r_title_lbl.font.color.rgb = RGBColor(0, 0, 0)

    r_title_main = p_title.add_run("ỨNG DỤNG GIS THÔNG MINH VÀ VIỄN THÁM LANDSAT\nPHÂN TÍCH, ĐÁNH GIÁ BIẾN ĐỘNG THẢM PHỦ ĐẤT CÔNG NGHIỆP\nVÀ MỞ RỘNG ĐÔ THỊ GIAI ĐOẠN 2015 – 2025")
    r_title_main.font.name = 'Times New Roman'
    r_title_main.font.size = Pt(16.5)
    r_title_main.font.bold = True
    r_title_main.font.color.rgb = RGBColor(0, 0, 0)

    # Địa bàn nghiên cứu
    p_area = doc.add_paragraph()
    p_area.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_area.paragraph_format.space_before = Pt(4)
    p_area.paragraph_format.space_after = Pt(45)
    r_area = p_area.add_run("Địa bàn nghiên cứu: Huyện Bình Xuyên, tỉnh Vĩnh Phúc\n(Cụm liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên)")
    r_area.font.name = 'Times New Roman'
    r_area.font.size = Pt(12.5)
    r_area.font.italic = True
    r_area.font.color.rgb = RGBColor(0, 0, 0)

    # Bảng thông tin sinh viên & giảng viên (Không viền, trang trọng)
    tbl_info = doc.add_table(rows=4, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info_data = [
        ("Giảng viên hướng dẫn:", "TRỊNH THÀNH"),
        ("Sinh viên thực hiện:", "NGÔ ĐẶNG NHẬT DŨNG"),
        ("Mã số sinh viên (MSSV):", "23010329"),
        ("Lớp học phần:", "Xử lý dữ liệu GIS thông minh"),
    ]
    for row_idx, (lbl, val) in enumerate(tbl_info_data):
        cell_lbl, cell_val = tbl_info.rows[row_idx].cells
        set_cell_width(cell_lbl, 5.8)
        set_cell_width(cell_val, 8.2)
        set_cell_margins(cell_lbl, top=40, bottom=40, left=40, right=40)
        set_cell_margins(cell_val, top=40, bottom=40, left=40, right=40)

        p_l = cell_lbl.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_l.paragraph_format.space_after = Pt(2)
        p_l.paragraph_format.line_spacing = 1.2
        r_l = p_l.add_run(lbl)
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(12.5)
        r_l.font.color.rgb = RGBColor(0, 0, 0)

        p_v = cell_val.paragraphs[0]
        p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_v.paragraph_format.space_after = Pt(2)
        p_v.paragraph_format.line_spacing = 1.2
        r_v = p_v.add_run(val)
        r_v.font.name = 'Times New Roman'
        r_v.font.size = Pt(12.5)
        r_v.font.bold = True
        r_v.font.color.rgb = RGBColor(0, 0, 0)

    # Chân trang bìa
    p_footer_cover = doc.add_paragraph()
    p_footer_cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_footer_cover.paragraph_format.space_before = Pt(50)
    p_footer_cover.paragraph_format.space_after = Pt(0)
    r_fc = p_footer_cover.add_run("HÀ NỘI – THÁNG 10/2026")
    r_fc.font.name = 'Times New Roman'
    r_fc.font.size = Pt(12.5)
    r_fc.font.bold = True
    r_fc.font.color.rgb = RGBColor(0, 0, 0)

    # ──────────────────────────────────────────────────────────
    # 3. CẤU HÌNH SECTION 2: BẮT ĐẦU ĐÁNH SỐ TRANG TỪ SAU TRANG BÌA
    # ──────────────────────────────────────────────────────────
    sec_body = doc.add_section()
    sec_body.page_width = Cm(21.0)
    sec_body.page_height = Cm(29.7)
    sec_body.top_margin = Cm(2.0)
    sec_body.bottom_margin = Cm(2.0)
    sec_body.left_margin = Cm(3.0)
    sec_body.right_margin = Cm(2.0)
    sec_body.different_first_page_header_footer = False
    add_page_number_to_footer(sec_body)

    # ──────────────────────────────────────────────────────────
    # 4. PARSE NỘI DUNG MARKDOWN
    # ──────────────────────────────────────────────────────────
    lines = md_text.split('\n')
    i = 0
    in_meta_header = True

    # Helper xử lý bảng Markdown thành bảng Word chuẩn học thuật
    def render_markdown_table(table_lines_block, caption_text=""):
        if not table_lines_block:
            return
        
        parsed_rows = []
        for l in table_lines_block:
            s = l.strip()
            if not s or re.match(r'^\s*\|?\s*:?-+:?\s*\|', s):
                continue
            cols = [c.strip() for c in s.strip('|').split('|')]
            if cols:
                parsed_rows.append(cols)

        if not parsed_rows:
            return

        n_cols = max(len(r) for r in parsed_rows)
        for r in parsed_rows:
            while len(r) < n_cols:
                r.append("")

        # Nếu có chú thích bảng, in chú thích PHÍA TRÊN bảng
        if caption_text:
            add_table_caption(doc, caption_text)

        # Tạo bảng Word
        tbl = doc.add_table(rows=len(parsed_rows), cols=n_cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_academic_table_borders(tbl)
        make_table_robust(tbl)

        # Tính toán phân bổ độ rộng cột (Tổng cộng = 16.0 cm)
        col_widths = []
        if n_cols == 3:
            col_widths = [2.5, 7.0, 6.5]
        elif n_cols == 4:
            if "toạ độ" in caption_text.lower() or "khống chế" in caption_text.lower():
                col_widths = [4.2, 4.2, 4.2, 3.4]
            elif "thông số" in caption_text.lower() or "cảnh ảnh" in caption_text.lower():
                col_widths = [4.6, 3.8, 3.8, 3.8]
            elif "chỉ số" in caption_text.lower():
                col_widths = [2.0, 4.5, 4.5, 5.0]
            else:
                col_widths = [4.0, 4.0, 4.0, 4.0]
        elif n_cols == 5:
            col_widths = [1.8, 5.2, 3.0, 3.0, 3.0]
        elif n_cols == 6:
            if "kênh phổ" in caption_text.lower():
                col_widths = [1.8, 2.5, 2.5, 2.0, 4.0, 3.2]
            else:
                col_widths = [1.8, 4.2, 2.5, 2.5, 2.5, 2.5]
        elif n_cols == 7:
            col_widths = [3.4, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1]
        elif n_cols == 9:
            # Bảng 5.1 so sánh 4 thuật toán
            col_widths = [3.0, 1.3, 1.3, 1.6, 1.6, 1.8, 1.8, 1.8, 1.8]
        elif n_cols == 10:
            # Bảng 6.1 thống kê diện tích
            col_widths = [0.8, 3.5, 1.5, 1.2, 1.5, 1.2, 1.5, 1.2, 1.8, 1.8]
        else:
            w_each = 16.0 / n_cols
            col_widths = [w_each] * n_cols

        # Đổ dữ liệu vào ô
        for r_idx, row_vals in enumerate(parsed_rows):
            is_header = (r_idx == 0)
            for c_idx, val in enumerate(row_vals):
                cell = tbl.rows[r_idx].cells[c_idx]
                if c_idx < len(col_widths):
                    set_cell_width(cell, col_widths[c_idx])
                set_cell_margins(cell, top=55, bottom=55, left=70, right=70)

                # Nền TRẮNG tuyệt đối
                tc_pr = cell._tc.get_or_add_tcPr()
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFFFFF"/>')
                tc_pr.append(shd)

                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2)

                clean_val = clean_inline_math(val.replace('**', '').replace('`', ''))
                run = p.add_run(clean_val)
                run.font.name = 'Times New Roman'
                run.font.color.rgb = RGBColor(0, 0, 0)

                if n_cols >= 9:
                    run.font.size = Pt(8.5)
                elif n_cols >= 6:
                    run.font.size = Pt(9.5)
                else:
                    run.font.size = Pt(10.5)

                if is_header:
                    run.font.bold = True
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    s_clean = clean_val.strip()
                    if s_clean.replace('.', '').replace('-', '').replace('+', '').replace('%', '').replace('ha', '').replace('s', '').replace('px', '').isdigit():
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if ('ha' in s_clean or '%' in s_clean) else WD_ALIGN_PARAGRAPH.CENTER
                    elif any(c in s_clean for c in ['%', 'ha', 's', 'px']):
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    elif c_idx == 0 and n_cols > 3:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_before = Pt(2)
        p_spacer.paragraph_format.space_after = Pt(6)

    # ──────────────────────────────────────────────────────────
    # PARSE VÒNG LẶP DÒNG MARKDOWN
    # ──────────────────────────────────────────────────────────
    pending_table_caption = ""
    table_buffer = []
    in_table_mode = False

    while i < len(lines):
        line = lines[i]
        line_strip = line.strip()

        # Bỏ qua phần bìa thô đầu file markdown
        if in_meta_header:
            if line.startswith("# MỤC LỤC TỔNG QUÁT") or line.startswith("# DANH MỤC") or line.startswith("# CHƯƠNG 1"):
                in_meta_header = False
            else:
                i += 1
                continue

        # Xóa các dòng phân cách trang trí ---
        if line_strip == '---':
            i += 1
            continue

        # Kiểm tra bảng Markdown
        if line_strip.startswith('|') and '|' in line_strip[1:]:
            in_table_mode = True
            table_buffer.append(line)
            i += 1
            continue
        elif in_table_mode:
            render_markdown_table(table_buffer, pending_table_caption)
            table_buffer = []
            pending_table_caption = ""
            in_table_mode = False

        # Kiểm tra tiêu đề bảng Markdown: ### Bảng X.X: ...
        if line_strip.startswith('### Bảng ') or line_strip.startswith('## Bảng '):
            pending_table_caption = re.sub(r'^#+\s*', '', line_strip)
            i += 1
            continue

        # Xử lý khối code block (```)
        if line_strip.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1
            block_content = "\n".join(code_lines).strip()

            # 1. Khối chứa lệnh chèn hình: [VỊ TRÍ CHÈN HÌNH...]
            img_match = re.search(r'\[VỊ TRÍ CHÈN HÌNH[^:]*:\s*([^\]]+)\]', block_content)
            if img_match:
                img_path = img_match.group(1).strip()
                cap_match = re.search(r'(\*Hình[^*]+\*)', block_content)
                cap = cap_match.group(1).strip('*') if cap_match else "Hình minh họa"
                insert_figure(doc, img_path, cap, width_in=5.6)
                continue

            # 2. Khối ghi chú bổ sung bản đồ: chuyển thành ghi chú học thuật thanh lịch
            if "BẢN ĐỒ HÀNH CHÍNH HUYỆN BÌNH XUYÊN" in block_content:
                p_note = doc.add_paragraph()
                p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_note.paragraph_format.space_before = Pt(8)
                p_note.paragraph_format.space_after = Pt(12)
                r_nt = p_note.add_run("*(Ghi chú của tác giả: Vị trí dành để chèn bổ sung Hình 3.2 - Bản đồ hành chính chính quy huyện Bình Xuyên theo quy định học phần khi thu thập được ảnh scan chính thức).*")
                r_nt.font.name = 'Times New Roman'
                r_nt.font.size = Pt(11)
                r_nt.font.italic = True
                r_nt.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
                continue

            # 3. Code block thông thường / diagram ASCII (sơ đồ kiến trúc lai)
            p_code = doc.add_paragraph()
            p_code.paragraph_format.left_indent = Cm(0.8)
            p_code.paragraph_format.right_indent = Cm(0.8)
            p_code.paragraph_format.space_before = Pt(6)
            p_code.paragraph_format.space_after = Pt(8)
            p_code.paragraph_format.line_spacing = 1.05
            r_c = p_code.add_run(block_content)
            r_c.font.name = 'Consolas'
            r_c.font.size = Pt(9.5)
            r_c.font.color.rgb = RGBColor(0, 0, 0)
            continue

        # Tiêu đề cấp 1: # CHƯƠNG hoặc # DANH MỤC / MỤC LỤC -> Heading 1 (Ngắt trang mới)
        if line.startswith('# '):
            h_text = line[2:].strip()
            # Bắt đầu trang mới trước mỗi chương và danh mục lớn
            doc.add_page_break()
            p_h1 = doc.add_paragraph(h_text, style='Heading 1')

            # Nếu là MỤC LỤC TỔNG QUÁT:
            if "MỤC LỤC" in h_text.upper():
                p_toc = doc.add_paragraph()
                p_toc.paragraph_format.space_before = Pt(4)
                p_toc.paragraph_format.space_after = Pt(8)
                add_toc_field(p_toc)

                toc_items = [
                    ("DANH MỤC TỪ VIẾT TẮT", "ii", 1),
                    ("DANH MỤC HÌNH VẼ & BẢN ĐỒ", "iii", 1),
                    ("DANH MỤC BẢNG BIỂU THỐNG KÊ", "iv", 1),
                    ("CHƯƠNG 1: GIỚI THIỆU & ĐẶT VẤN ĐỀ NGHIÊN CỨU", "1", 1),
                    ("1.1. Tính cấp thiết của đề tài", "1", 2),
                    ("1.2. Mục tiêu nghiên cứu", "2", 2),
                    ("1.3. Trọng tâm nghiên cứu: Động thái biến động đất công nghiệp", "2", 2),
                    ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & TỔNG QUAN PHƯƠNG PHÁP", "3", 1),
                    ("2.1. Tổng quan công nghệ viễn thám quang học đa thời gian", "3", 2),
                    ("2.2. Lý thuyết phân loại ảnh viễn thám có giám sát (Supervised Classification)", "4", 2),
                    ("2.3. Nguyên lý toán học của 4 thuật toán phân loại đối chứng", "4", 2),
                    ("2.4. Phương pháp phân tích biến động sau phân loại (PCC)", "6", 2),
                    ("2.5. Cơ sở toán học đánh giá độ chính xác phân loại độc lập", "7", 2),
                    ("CHƯƠNG 3: KHU VỰC NGHIÊN CỨU & DỮ LIỆU ĐẦU VÀO", "8", 1),
                    ("3.1. Vị trí địa lý và điều kiện tự nhiên - kinh tế xã hội", "8", 2),
                    ("3.2. Toạ độ khống chế không gian & Bản đồ chỉ dẫn vị trí", "9", 2),
                    ("3.3. Nguồn tư liệu viễn thám Landsat 8/9 Level-2 Surface Reflectance", "10", 2),
                    ("3.4. Bảng mô tả chi tiết tính chất 11 kênh phổ của hệ thống Landsat 8/9", "11", 2),
                    ("3.5. Trích xuất 13 kênh đặc trưng quang phổ (Feature Engineering)", "12", 2),
                    ("CHƯƠNG 4: QUY TRÌNH THỰC HIỆN & PHÂN CÔNG HỆ THỐNG", "13", 1),
                    ("4.1. Sơ đồ quy trình công nghệ lai (Hybrid Workflow: QGIS & Python)", "13", 2),
                    ("4.2. Thiết kế và số hóa tập mẫu huấn luyện (Training Set)", "14", 2),
                    ("4.3. Kỹ thuật cân bằng mẫu phân tầng (Stratified Capping)", "15", 2),
                    ("4.4. Xây dựng bộ mẫu kiểm chứng không gian độc lập (FPS 200 điểm)", "16", 2),
                    ("CHƯƠNG 5: THỰC NGHIỆM ĐỐI CHỨNG CÁC THUẬT TOÁN PHÂN LOẠI", "17", 1),
                    ("5.1. Bảng tổng hợp độ chính xác giữa 4 thuật toán (RF, MLC, NB, MDC)", "17", 2),
                    ("5.2. Đánh giá chuyên sâu độ chính xác của lớp Mặt nước (Water Body)", "19", 2),
                    ("5.3. Đánh giá độ chính xác bóc tách Đất công nghiệp và Đất dân cư", "20", 2),
                    ("5.4. Đánh giá hiệu năng và thời gian tính toán", "21", 2),
                    ("5.5. Luận giải khoa học: Tại sao Random Forest là lựa chọn tối ưu cho bản đồ?", "22", 2),
                    ("CHƯƠNG 6: KẾT QUẢ BIẾN ĐỘNG SỬ DỤNG ĐẤT & BÙNG NỔ ĐẤT CÔNG NGHIỆP", "23", 1),
                    ("6.1. Thống kê biến động diện tích 5 lớp phủ (2015, 2020, 2025)", "23", 2),
                    ("6.2. Động thái bùng nổ diện tích đất công nghiệp (2015 – 2025)", "24", 2),
                    ("6.3. Ma trận chuyển dịch đất đai (Transition Matrix 2015 → 2025)", "25", 2),
                    ("6.4. So sánh và kiểm chứng thực địa với ảnh Google Earth", "26", 2),
                    ("6.5. Hệ thống bản đồ chuyên đề thành lập", "27", 2),
                    ("CHƯƠNG 7: KẾT LUẬN & KIẾN NGHỊ", "29", 1),
                    ("7.1. Kết luận", "29", 2),
                    ("7.2. Khuyến nghị ứng dụng", "30", 2),
                    ("TÀI LIỆU THAM KHẢO", "31", 1),
                    ("PHỤ LỤC: HƯỚNG DẪN THAO TÁC PHẦN MỀM QGIS & MÃ NGUỒN PYTHON", "33", 1),
                ]
                for title_t, pg_t, lvl_t in toc_items:
                    add_dot_leader_line(doc, title_t, pg_t, level=lvl_t)

            i += 1
            continue

        # Tiêu đề cấp 2: ## Mục lớn (ví dụ 1.1, 2.1) -> Heading 2
        if line.startswith('## '):
            h_text = line[3:].strip()
            doc.add_paragraph(h_text, style='Heading 2')
            i += 1
            continue

        # Tiêu đề cấp 3: ### Tiểu mục -> Heading 3
        if line.startswith('### '):
            h_text = line[4:].strip()
            if "Ảnh chỉ dẫn" in h_text:
                i += 1
                continue
            doc.add_paragraph(h_text, style='Heading 3')
            i += 1
            continue

        # Danh mục Hình vẽ & Danh mục Bảng biểu (dóng hàng dot leader)
        if re.match(r'^\d+\.\s+\*?\*?(Hình|Bảng)\s+[\d\.]+', line_strip):
            m_item = re.match(r'^\d+\.\s+\*?\*?((?:Hình|Bảng)\s+[\d\.]+[a-c]?:?)\s*(.*?)(?:\s*\(([^)]+)\))?$', line_strip)
            if m_item:
                tag = m_item.group(1).rstrip(':')
                desc = m_item.group(2).strip('*').strip()
                add_dot_leader_line(doc, f"{tag}: {desc}", "", level=2)
                i += 1
                continue

        # Danh sách gạch đầu dòng / bullet
        if line_strip.startswith('* ') or line_strip.startswith('- '):
            bullet_text = line_strip[2:].strip()
            
            # Bỏ qua liên kết markdown thô
            if bullet_text.startswith('[') and '](#danh-mục' in bullet_text:
                i += 1
                continue
            if bullet_text.startswith('[') and ')(#' in bullet_text:
                i += 1
                continue

            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.left_indent = Cm(0.75)
            p_b.paragraph_format.space_before = Pt(0)
            p_b.paragraph_format.space_after = Pt(3.5)
            p_b.paragraph_format.line_spacing = 1.3

            parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', bullet_text)
            for part in parts:
                clean_p = clean_inline_math(part)
                if part.startswith('**') and part.endswith('**'):
                    r = p_b.add_run(clean_p[2:-2])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(13)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 0, 0)
                elif part.startswith('*') and part.endswith('*'):
                    r = p_b.add_run(clean_p[1:-1])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(13)
                    r.font.italic = True
                    r.font.color.rgb = RGBColor(0, 0, 0)
                elif part.startswith('`') and part.endswith('`'):
                    r = p_b.add_run(clean_p[1:-1])
                    r.font.name = 'Consolas'
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    r = p_b.add_run(clean_p)
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(13)
                    r.font.color.rgb = RGBColor(0, 0, 0)

            i += 1
            continue

        # Đoạn văn thông thường
        if line_strip:
            if any(sym in line_strip for sym in [r'\text{OA} =', r'\kappa =', r'\text{Gini}', r'g_k(X) =', r'P(X |', r'd_k(X) =', r'\text{Change Code} =']):
                p_math = doc.add_paragraph()
                p_math.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_math.paragraph_format.space_before = Pt(6)
                p_math.paragraph_format.space_after = Pt(6)
                clean_eq = clean_inline_math(line_strip)
                r_m = p_math.add_run(clean_eq)
                r_m.font.name = 'Times New Roman'
                r_m.font.size = Pt(12)
                r_m.font.italic = True
                r_m.font.color.rgb = RGBColor(0, 0, 0)
                i += 1
                continue

            p_text = doc.add_paragraph()
            p_text.paragraph_format.line_spacing = 1.35
            p_text.paragraph_format.space_before = Pt(0)
            p_text.paragraph_format.space_after = Pt(5)
            p_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

            if not line_strip.startswith('1.') and not line_strip.startswith('2.') and not line_strip.startswith('3.') and not line_strip.startswith('4.') and not line_strip.startswith('5.'):
                p_text.paragraph_format.first_line_indent = Cm(1.0)
            else:
                p_text.paragraph_format.left_indent = Cm(0.75)

            parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', line_strip)
            for part in parts:
                clean_p = clean_inline_math(part)
                if part.startswith('**') and part.endswith('**'):
                    r = p_text.add_run(clean_p[2:-2])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(13)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 0, 0)
                elif part.startswith('*') and part.endswith('*'):
                    r = p_text.add_run(clean_p[1:-1])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(13)
                    r.font.italic = True
                    r.font.color.rgb = RGBColor(0, 0, 0)
                elif part.startswith('`') and part.endswith('`'):
                    r = p_text.add_run(clean_p[1:-1])
                    r.font.name = 'Consolas'
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    r = p_text.add_run(clean_p)
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(13)
                    r.font.color.rgb = RGBColor(0, 0, 0)

        i += 1

    if in_table_mode and table_buffer:
        render_markdown_table(table_buffer, pending_table_caption)

    # Lưu tài liệu mới
    doc.save(OUTPUT_DOCX_PATH)
    file_size_mb = os.path.getsize(OUTPUT_DOCX_PATH) / (1024 * 1024)
    print(f"\n=========================================================")
    print(f"BÁO CÁO ĐÃ ĐƯỢC CHUẨN HÓA THÀNH CÔNG!")
    print(f"Đường dẫn file mới: {OUTPUT_DOCX_PATH}")
    print(f"Dung lượng tệp: {file_size_mb:.2f} MB")
    print(f"=========================================================")

if __name__ == '__main__':
    build_standardized_docx()

