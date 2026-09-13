# 📚 Automated PDF Sorting & Processing Pipeline

This standalone Python tool scans local directories (like `D:\pdf 2` and `D:\pdfs`), automatically categorizes PDF story books into the 8 Grand Library genres, extracts metadata, and converts PDF pages into compressed `.webp` web images.

---

## 📁 Directory Location
Located in a clean standalone module folder:
`d:\projects\portfolio\pdf_pipeline\`

---

## ⚙️ Requirements
- Python 3.9+
- `PyMuPDF` (`fitz`)
- `Pillow` (`PIL`)

*(Installed automatically during setup)*

---

## 🚀 How to Run

Open your terminal or command prompt in `d:\projects\portfolio` and run:

```bash
python pdf_pipeline/run_pipeline.py
```

### 📋 Menu Options:
1. **Auto-Sort PDFs into 8 Categories & Create Catalog Index**:
   Scans `D:\pdf 2` and `D:\pdfs`, analyzes filename and content keywords, auto-categorizes books into `Horror`, `Detective`, `Romance`, `Novels`, `Fantasy`, `Science Fiction`, `Adventure`, or `Short Stories`, and creates `D:\Sorted_PDF_Library`.
2. **Convert Sorted PDFs into Web Page Images (WebP)**:
   Renders pages into lightweight `.webp` images and generates 3D cover thumbnails in `D:\Web_Converted_Books`.
3. **Run Complete Pipeline**:
   Performs full automated sorting, metadata indexing, and web page conversion in one click.

---

## 🔒 Cloud Upload Readiness
The generated `library_catalog_index.json` and `web_library_manifest.json` are formatted to be pushed directly to **Cloudflare R2** and **Supabase PostgreSQL**!
