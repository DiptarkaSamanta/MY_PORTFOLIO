import os
import sys

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sort_and_index import scan_and_sort_pdfs
from convert_pdf import batch_convert_library

def main():
    print("==========================================================")
    print("📚 GRAND LIBRARY - AUTOMATED PDF PIPELINE & AUTO-SORTER 📚")
    print("==========================================================")
    print("This pipeline scans your local hard drives, auto-sorts PDFs")
    print("into the 8 library categories, and converts them for web reading.\n")

    default_sources = ["D:\\pdf 2", "D:\\pdfs"]
    default_sorted_dir = "D:\\Sorted_PDF_Library"
    default_web_dir = "D:\\Web_Converted_Books"

    print("Target Input Hard Drive Folders:")
    for src in default_sources:
        status = "FOUND ✅" if os.path.exists(src) else "NOT FOUND ⚠️"
        print(f" - {src} ({status})")
    print(f"\nSorted Output Directory: {default_sorted_dir}")
    print(f"Web Converted Output Directory: {default_web_dir}\n")

    print("----------------------------------------------------------")
    print("Select an Action:")
    print(" [1] Auto-Sort PDFs into 8 Categories & Create Catalog Index")
    print(" [2] Convert Sorted PDFs into Web Page Images (WebP)")
    print(" [3] Run Complete Pipeline (Sort + Convert + Create Index)")
    print(" [4] Exit")
    print("----------------------------------------------------------")

    choice = input("Enter choice (1-4) [default: 3]: ").strip() or "3"

    if choice == "1":
        scan_and_sort_pdfs(default_sources, default_sorted_dir, copy_files=True, clean_existing=True)
    elif choice == "2":
        index_file = os.path.join(default_sorted_dir, "library_catalog_index.json")
        batch_convert_library(index_file, default_web_dir, max_pages_per_book=15)
    elif choice == "3":
        print("\n🚀 Starting Phase 1: Auto-Sorting Local PDFs...")
        catalog = scan_and_sort_pdfs(default_sources, default_sorted_dir, copy_files=True, clean_existing=True)
        
        index_file = os.path.join(default_sorted_dir, "library_catalog_index.json")
        print("\n🚀 Starting Phase 2: Converting PDF Pages to Web Images...")
        batch_convert_library(index_file, default_web_dir, max_pages_per_book=15)
        
        print("\n🎉 COMPLETE! All PDFs sorted and web reader assets generated.")
    else:
        print("Exiting pipeline tool.")

if __name__ == "__main__":
    main()
