import os
import json
import pymupdf as fitz  # PyMuPDF
from PIL import Image

def convert_pdf_to_web_assets(pdf_path, output_dir, max_pages=None, dpi=150, quality=80):
    """
    Converts a PDF file into compressed WebP page images and extracts a 3D cover thumbnail.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    filename = os.path.basename(pdf_path)
    book_id = os.path.splitext(filename)[0].lower().replace(" ", "_").replace("-", "_")
    book_id = "".join([c for c in book_id if c.isalnum() or c == '_'])

    book_out_dir = os.path.join(output_dir, book_id)
    pages_dir = os.path.join(book_out_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    print(f"📖 Converting PDF: '{filename}' -> '{book_id}'...")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    pages_to_render = min(total_pages, max_pages) if max_pages else total_pages

    page_files = []
    zoom = dpi / 72  # scale factor for DPI
    matrix = fitz.Matrix(zoom, zoom)

    for page_idx in range(pages_to_render):
        page = doc[page_idx]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        
        # Convert PyMuPDF pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        page_file_name = f"page_{page_idx + 1}.webp"
        page_file_path = os.path.join(pages_dir, page_file_name)
        img.save(page_file_path, "WEBP", quality=quality)
        page_files.append(f"pages/{page_file_name}")

        # Page 1 is saved as cover image
        if page_idx == 0:
            cover_path = os.path.join(book_out_dir, "cover.webp")
            img.save(cover_path, "WEBP", quality=85)

    doc.close()

    # Create book metadata manifest
    manifest = {
        "id": book_id,
        "title": os.path.splitext(filename)[0].replace("_", " ").title(),
        "total_pages": total_pages,
        "rendered_pages": pages_to_render,
        "cover_url": f"processed_books/{book_id}/cover.webp",
        "page_urls": [f"processed_books/{book_id}/{p}" for p in page_files]
    }

    manifest_path = os.path.join(book_out_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"   ✅ Rendered {pages_to_render} pages to '{book_out_dir}'")
    return manifest

def batch_convert_library(catalog_index_path, output_dir="D:\\Web_Converted_Books", max_pages_per_book=10):
    """
    Batch converts sorted PDFs into web reader images.
    """
    if not os.path.exists(catalog_index_path):
        print(f"❌ Error: Catalog index file not found at '{catalog_index_path}'")
        return []

    with open(catalog_index_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"\n🚀 Batch Converting {len(catalog)} Books for Online Reader...")
    manifests = []
    for item in catalog:
        pdf_path = item.get("sorted_filepath") or item.get("filepath")
        if pdf_path and os.path.exists(pdf_path):
            try:
                m = convert_pdf_to_web_assets(pdf_path, output_dir, max_pages=max_pages_per_book)
                manifests.append(m)
            except Exception as e:
                print(f"❌ Failed to convert {pdf_path}: {e}")

    summary_path = os.path.join(output_dir, "web_library_manifest.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(manifests, f, indent=2)

    print(f"\n✅ All books converted successfully! Summary saved to {summary_path}")
    return manifests

if __name__ == "__main__":
    catalog_file = "D:\\Sorted_PDF_Library\\library_catalog_index.json"
    batch_convert_library(catalog_file, "D:\\Web_Converted_Books", max_pages_per_book=10)
