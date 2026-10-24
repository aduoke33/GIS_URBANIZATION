r"""
scripts/convert_report_to_docx.py
=================================
Convert BAO_CAO_THUYET_MINH_HOAN_CHINH.md into a beautifully formatted,
submission-ready Microsoft Word document (.docx) adhering to Vietnamese academic standards:
  - Font: Times New Roman (13pt, 1.3 line spacing, 6pt after, Justified)
  - Margins: Top 2cm, Bottom 2cm, Left 3cm (binding), Right 2cm
  - Formal Academic Cover Page with border
  - Formatted Headings (H1: 15pt Bold, H2: 13.5pt Bold, H3: 13pt Bold)
  - Styled Tables with header shading (#EBF1F5) and clean grid borders
  - All 14 high-res Maps and Charts automatically embedded with centered italic captions
  - Distinct highlighted Callout Boxes for [GHI CHÚ BỔ SUNG]
"""

import os
import sys
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MD_PATH = os.path.join(PROJ_ROOT, 'BAO_CAO_THUYET_MINH_HOAN_CHINH.md')
DOCX_PATH = os.path.join(PROJ_ROOT, 'BAO_CAO_THUYET_MINH_HOAN_CHINH.docx')

def set_cell_background(cell, fill_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                       f'<w:top w:w="{top}" w:type="dxa"/>'
                       f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                       f'<w:left w:w="{left}" w:type="dxa"/>'
                       f'<w:right w:w="{right}" w:type="dxa"/>'
                       f'</w:tcMar>')
    tc_pr.append(tc_mar)

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def insert_figure(doc, rel_path, caption, width=5.8):
    full_path = os.path.join(PROJ_ROOT, rel_path.replace('/', os.sep))
    if os.path.exists(full_path):
        w = width
        if 'chart_training_time' in rel_path:
            w = 5.2
        elif 'radar' in rel_path:
            w = 5.5
        elif 'map_landcover_20' in rel_path:
            w = 5.4

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(14)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        r = p_img.add_run()
        r.add_picture(full_path, width=Inches(w))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        r_c = p_cap.add_run(caption)
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(11)
        r_c.font.italic = True
        r_c.font.bold = True
        print(f"  [EMBEDDED] {rel_path} -> {caption[:60]}...")
        return True
    else:
        print(f"  [WARNING: FILE NOT FOUND] {full_path}")
        return False

def build_docx():
    print(f"Reading markdown from: {MD_PATH}")
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = Document()

    # ──────────────────────────────────────────────────────────
    # PAGE SETUP (A4 & Standard Vietnamese Thesis Margins)
    # ──────────────────────────────────────────────────────────
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)   # 3 cm for binding
        section.right_margin = Cm(2.0)

    # ──────────────────────────────────────────────────────────
    # DEFAULT STYLES
    # ──────────────────────────────────────────────────────────
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ──────────────────────────────────────────────────────────
    # 1. TRANG BÌA CHÍNH THỨC (COVER PAGE)
    # ──────────────────────────────────────────────────────────
    p_header1 = doc.add_paragraph()
    p_header1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_header1.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC [GHI CHÚ: TÊN TRƯỜNG CỦA BẠN]\nKHOA CÔNG NGHỆ THÔNG TIN / ĐỊA KỸ THUẬT & GIS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    p_header1.paragraph_format.space_after = Pt(36)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("━━━━━━━━━━━━━━━━━━━━━")
    r_line.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    p_line.paragraph_format.space_after = Pt(48)

    p_title_sub = doc.add_paragraph()
    p_title_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_title_sub.add_run("BÁO CÁO THUYẾT MINH BÀI TẬP LỚN\nHỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO TRONG GIS (GeoAI)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    p_title_sub.paragraph_format.space_after = Pt(24)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("ỨNG DỤNG GIS THÔNG MINH VÀ VIỄN THÁM LANDSAT PHÂN TÍCH, ĐÁNH GIÁ BIẾN ĐỘNG THẢM PHỦ ĐẤT CÔNG NGHIỆP VÀ MỞ RỘNG ĐÔ THỊ GIAI ĐOẠN 2015 – 2025")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0xB2, 0x22, 0x22)
    p_title.paragraph_format.space_after = Pt(18)

    p_area = doc.add_paragraph()
    p_area.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_area = p_area.add_run("Địa bàn nghiên cứu: Huyện Bình Xuyên, tỉnh Vĩnh Phúc\n(Cụm liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên)")
    r_area.font.name = 'Times New Roman'
    r_area.font.size = Pt(13)
    r_area.font.italic = True
    p_area.paragraph_format.space_after = Pt(80)

    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Sinh viên thực hiện:", "[GHI CHÚ: Điền Họ và tên sinh viên]"),
        ("Mã số sinh viên (MSSV):", "[GHI CHÚ: Điền MSSV]"),
        ("Lớp học phần:", "[GHI CHÚ: Điền tên lớp]"),
        ("Giảng viên hướng dẫn:", "[GHI CHÚ: Điền tên Thầy/Cô hướng dẫn]"),
    ]
    for row_idx, (label, val) in enumerate(info_data):
        cell_lbl, cell_val = info_table.rows[row_idx].cells
        cell_lbl.width = Cm(6.0)
        cell_val.width = Cm(9.5)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_l = p_l.add_run(label)
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(13)
        r_l.font.bold = True

        p_v = cell_val.paragraphs[0]
        p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_v = p_v.add_run(val)
        r_v.font.name = 'Times New Roman'
        r_v.font.size = Pt(13)
        if "[GHI CHÚ" in val:
            r_v.font.color.rgb = RGBColor(0xD9, 0x53, 0x4F)

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(60)
    r_bot = p_bottom.add_run("HÀ NỘI – THÁNG 10/2026")
    r_bot.font.name = 'Times New Roman'
    r_bot.font.size = Pt(13)
    r_bot.font.bold = True

    doc.add_page_break()

    # ──────────────────────────────────────────────────────────
    # PARSE MARKDOWN BODY
    # ──────────────────────────────────────────────────────────
    lines = md_text.split('\n')
    i = 0
    in_cover_meta = True
    in_table = False
    table_lines = []

    def flush_table(tbl_lines):
        if not tbl_lines:
            return
        rows_data = []
        for line in tbl_lines:
            if not line.strip() or re.match(r'^\s*\|?\s*:?-+:?\s*\|', line):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells:
                rows_data.append(cells)
        if not rows_data:
            return

        n_cols = max(len(r) for r in rows_data)
        for r in rows_data:
            while len(r) < n_cols:
                r.append("")

        word_tbl = doc.add_table(rows=len(rows_data), cols=n_cols)
        word_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(word_tbl)

        for r_idx, row in enumerate(rows_data):
            for c_idx, val in enumerate(row):
                cell = word_tbl.rows[r_idx].cells[c_idx]
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)

                clean_val = val.replace('**', '').replace('`', '').replace('$', '')
                run = p.add_run(clean_val)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)

                if r_idx == 0:
                    set_cell_background(cell, "EBF1F5")
                    run.font.bold = True
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    if r_idx % 2 == 1:
                        set_cell_background(cell, "FAFAFA")
                    if c_idx == 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    elif any(c in clean_val for c in ['%', 'ha', 's', 'm']) or clean_val.replace('.', '').replace('-', '').isdigit():
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_before = Pt(4)
        p_spacer.paragraph_format.space_after = Pt(6)

    while i < len(lines):
        line = lines[i]

        if line.startswith("# BÁO CÁO THUYẾT MINH") or line.startswith("## ĐỀ TÀI:") or line.startswith("### THÔNG TIN HỌC PHẦN"):
            i += 1
            continue
        if in_cover_meta:
            if line.startswith("# MỤC LỤC TỔNG QUÁT") or line.startswith("# DANH MỤC"):
                in_cover_meta = False
            else:
                i += 1
                continue

        # Check table
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            flush_table(table_lines)
            table_lines = []
            in_table = False

        # Code block handling
        if line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1
            block_text = "\n".join(code_lines)

            # Check if block contains image directive
            inner_img_match = re.search(r'\[VỊ TRÍ CHÈN HÌNH[^:]*:\s*([^\]]+)\]', block_text)
            if inner_img_match:
                img_rel = inner_img_match.group(1).strip()
                cap_match = re.search(r'(\*Hình[^*]+\*)', block_text)
                caption = cap_match.group(1).strip('*') if cap_match else "Hình minh họa"
                insert_figure(doc, img_rel, caption, width=5.8)
                continue

            # Check if block is Callout note
            if "[GHI CHÚ BỔ SUNG" in block_text:
                tbl_box = doc.add_table(rows=1, cols=1)
                tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell_box = tbl_box.rows[0].cells[0]
                cell_box.width = Cm(16.0)
                set_cell_background(cell_box, "FFF3CD")
                set_cell_margins(cell_box, top=140, bottom=140, left=200, right=200)

                p_box = cell_box.paragraphs[0]
                p_box.paragraph_format.space_after = Pt(0)
                p_box.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r_box = p_box.add_run("📌 " + block_text.strip().strip('*').strip())
                r_box.font.name = 'Times New Roman'
                r_box.font.size = Pt(11.5)
                r_box.font.bold = True
                r_box.font.color.rgb = RGBColor(0x85, 0x64, 0x04)

                p_sp = doc.add_paragraph()
                p_sp.paragraph_format.space_after = Pt(6)
                continue

            # Normal code block
            p_code = doc.add_paragraph()
            p_code.paragraph_format.left_indent = Cm(0.8)
            p_code.paragraph_format.right_indent = Cm(0.8)
            p_code.paragraph_format.space_before = Pt(6)
            p_code.paragraph_format.space_after = Pt(8)
            r_code = p_code.add_run(block_text)
            r_code.font.name = 'Consolas'
            r_code.font.size = Pt(9.5)
            r_code.font.color.rgb = RGBColor(0x2E, 0x40, 0x53)
            continue

        # Check callout outside code blocks
        if "[GHI CHÚ BỔ SUNG" in line:
            tbl_box = doc.add_table(rows=1, cols=1)
            tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell_box = tbl_box.rows[0].cells[0]
            cell_box.width = Cm(16.0)
            set_cell_background(cell_box, "FFF3CD")
            set_cell_margins(cell_box, top=140, bottom=140, left=200, right=200)

            p_box = cell_box.paragraphs[0]
            p_box.paragraph_format.space_after = Pt(0)
            p_box.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r_box = p_box.add_run("📌 " + line.strip().strip('*').strip())
            r_box.font.name = 'Times New Roman'
            r_box.font.size = Pt(11.5)
            r_box.font.bold = True
            r_box.font.color.rgb = RGBColor(0x85, 0x64, 0x04)

            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_after = Pt(6)
            i += 1
            continue

        # Headings
        if line.startswith('# '):
            h_text = line[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
            i += 1
            continue
        elif line.startswith('## '):
            h_text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
            i += 1
            continue
        elif line.startswith('### '):
            h_text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            i += 1
            continue

        # Bullets
        if line.strip().startswith('* ') or line.strip().startswith('- '):
            b_text = line.strip()[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.left_indent = Cm(0.7)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.25

            parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', b_text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.font.bold = True
                elif part.startswith('*') and part.endswith('*'):
                    r = p.add_run(part[1:-1])
                    r.font.italic = True
                elif part.startswith('`') and part.endswith('`'):
                    r = p.add_run(part[1:-1])
                    r.font.name = 'Consolas'
                    r.font.size = Pt(11)
                else:
                    p.add_run(part.replace('$', ''))
            i += 1
            continue

        # Regular paragraph
        clean_line = line.strip()
        if clean_line:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.3
            p.paragraph_format.space_after = Pt(6)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

            if not clean_line.startswith('*Hình') and not clean_line.startswith('*Bảng'):
                p.paragraph_format.first_line_indent = Cm(0.75)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(10)

            parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', clean_line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.font.bold = True
                elif part.startswith('*') and part.endswith('*'):
                    r = p.add_run(part[1:-1])
                    r.font.italic = True
                elif part.startswith('`') and part.endswith('`'):
                    r = p.add_run(part[1:-1])
                    r.font.name = 'Consolas'
                    r.font.size = Pt(11)
                else:
                    p.add_run(part.replace('$', ''))

        i += 1

    if in_table and table_lines:
        flush_table(table_lines)

    doc.save(DOCX_PATH)
    size_mb = os.path.getsize(DOCX_PATH) / (1024 * 1024)
    print(f"\n=========================================================")
    print(f"DOCUMENT SAVED SUCCESSFULLY: {DOCX_PATH}")
    print(f"File size: {size_mb:.2f} MB")
    print(f"=========================================================")

if __name__ == '__main__':
    build_docx()
