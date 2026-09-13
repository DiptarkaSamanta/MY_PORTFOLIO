import os
import sys
import re
import shutil
import json
from pathlib import Path

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# Category Keyword Mapping Rules
CATEGORY_KEYWORDS = {
    "horror": [
        "horror", "dracula", "frankenstein", "vampire", "ghost", "gothic", "terror",
        "spooky", "haunted", "haunting", "witch", "demon", "zombie", "curse", "macabre",
        "stoker", "poe", "king", "lovecraft"
    ],
    "detective": [
        "detective", "sherlock", "holmes", "mystery", "crime", "investigation", "murder",
        "clue", "sleuth", "watson", "doyle", "christie", "poirot", "marple", "byomkesh",
        "satyanweshi", "sharadindu", "bakshi", "noir", "casebook"
    ],
    "romance": [
        "romance", "romantic", "love", "pride and prejudice", "austen", "passion",
        "shesher kobita", "heart", "bride", "darcy", "bennet", "emma", "sensibility",
        "affection", "desire", "lover"
    ],
    "novels": [
        "novel", "fiction", "classic", "gatsby", "fitzgerald", "pather panchali",
        "bibhutibhushan", "tagore", "chowringhee", "1984", "orwell", "mockingbird",
        "literature", "story", "chronicle"
    ],
    "fantasy": [
        "fantasy", "hobbit", "tolkien", "magic", "ring", "wizard", "dragon", "narnia",
        "potter", "spell", "myth", "beast", "realm", "legend", "middle-earth", "orc"
    ],
    "scifi": [
        "scifi", "sci-fi", "science fiction", "dune", "space", "planet", "galaxy", "asimov",
        "shonku", "satyajit", "robot", "future", "star", "cyber", "martian", "alien",
        "time machine", "wells", "verne"
    ],
    "adventure": [
        "adventure", "treasure", "island", "voyage", "pirate", "ship", "sea", "tintin",
        "herge", "kakababu", "sunil", "journey", "exploration", "savage", "safari"
    ],
    "short-stories": [
        "short story", "short stories", "tales", "collection", "anthology", "poe",
        "o henry", "galpaguchha", "fables", "sketches"
    ]
}

def detect_category(filename, title="", text_sample=""):
    """
    Detect category based strictly on the filename and title written on the PDF.
    Filename & Title matches are given 10x higher priority than background text.
    """
    name_content = (filename + " " + title).lower()
    full_content = (name_content + " " + text_sample).lower()
    
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            kw_pattern = r'\b' + re.escape(kw) + r'\b'
            
            # Highest priority: Exact word match in PDF Filename or Title (10 points)
            if re.search(kw_pattern, name_content):
                scores[cat] += 10
            # Partial match in PDF Filename or Title (5 points)
            elif kw in name_content:
                scores[cat] += 5
            # Fallback: Match in document text content (1 point)
            elif re.search(kw_pattern, full_content):
                scores[cat] += 1

    best_cat = max(scores, key=scores.get)
    if scores[best_cat] > 0:
        return best_cat
    
    return "novels"  # General fiction & novels as default fallback


def extract_pdf_info(pdf_path):
    """
    Extract basic PDF info & metadata using PyMuPDF (fitz) or fallback header.
    """
    info = {
        "filename": os.path.basename(pdf_path),
        "filepath": str(pdf_path),
        "filesize_mb": round(os.path.getsize(pdf_path) / (1024 * 1024), 2),
        "pages": 0,
        "title": os.path.splitext(os.path.basename(pdf_path))[0].replace("_", " ").replace("-", " ").title(),
        "author": "Unknown Author",
        "category": "novels",
        "text_sample": ""
    }

    try:
        import pymupdf as fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        info["pages"] = len(doc)
        
        meta = doc.metadata
        if meta.get("title") and len(meta["title"].strip()) > 2:
            info["title"] = meta["title"].strip()
        if meta.get("author") and len(meta["author"].strip()) > 2:
            info["author"] = meta["author"].strip()

        # Extract text sample from first 3 pages
        sample_text = ""
        for page_num in range(min(3, len(doc))):
            sample_text += doc[page_num].get_text() + " "
        info["text_sample"] = sample_text[:1000]
        doc.close()
    except Exception as e:
        print(f"Warning reading metadata for {pdf_path}: {e}")

    # Determine category based strictly on filename & title written on the PDF
    info["category"] = detect_category(info["filename"], info["title"], info.get("text_sample", ""))
    return info

def extract_series_or_group_name(filename):
    """
    Extracts core book series or title name by stripping volume numbers, edition markers,
    part numbers, and noise characters (e.g. 'Sherlock Holmes Vol 1' -> 'Sherlock Holmes').
    """
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ")
    
    # Strip parenthetical annotations like (Book 1), [Vol 2]
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)

    # Strip common volume, edition, and part suffixes
    patterns = [
        r'\b(vol|volume|part|book|ch|chapter|v|ed|edition)\s*\d+.*$',
        r'\b\d+(st|nd|rd|th)?\s*(ed|edition).*$',
        r'\b\d+$'
    ]
    for p in patterns:
        name = re.sub(p, '', name, flags=re.IGNORECASE)
        
    name = name.strip(" ()[]-_.,")
    return name.title() if len(name) >= 3 else os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title()



def cluster_pdf_files_by_title_similarity(pdf_files_info):
    """
    Groups PDF files by common matching title parts or phrases.
    Ignores common website watermarks like (BDeBooks.Com), www, download, pdf.
    """
    IGNORE_WORDS = {
        "the", "a", "an", "and", "or", "of", "in", "on", "at", "to", "for", "with",
        "by", "from", "part", "vol", "volume", "book", "edition", "ed", "ch", "chapter",
        "pdf", "complete", "series", "guide", "handbook", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "bdebooks", "com", "bdebooks.com", "www", "org", "net", "download", "free", "ebook", "ebooks",
        "official", "drive", "blog", "wordpress", "http", "https", "bdebook"
    }

    # 1. Collect phrase frequencies across all PDF filenames
    phrase_counts = {}
    for info in pdf_files_info:
        # Strip parenthetical watermarks like (BDeBooks.Com) or [BDeBooks.Com]
        fn_clean = os.path.splitext(info["filename"])[0].lower()
        fn_clean = re.sub(r'\(.*?\)', '', fn_clean)
        fn_clean = re.sub(r'\[.*?\]', '', fn_clean)
        fn_clean = re.sub(r'[^a-z0-9\s]', ' ', fn_clean)
        
        tokens = [t for t in fn_clean.split() if t not in IGNORE_WORDS and len(t) >= 3]
        
        # Single significant words
        for t in set(tokens):
            phrase_counts[t] = phrase_counts.get(t, 0) + 1

        # Two-word sequence phrases (e.g. "Masud Rana", "Sherlock Holmes", "Data Science")
        for i in range(len(tokens) - 1):
            phrase = f"{tokens[i]} {tokens[i+1]}"
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

    # 2. Keep phrases shared by at least 2 files
    valid_clusters = {phrase: count for phrase, count in phrase_counts.items() if count >= 2}
    
    # Sort phrases: Prefer multi-word phrases over single words (e.g. 'Masud Rana' > 'Masud')
    sorted_phrases = sorted(valid_clusters.keys(), key=lambda x: (len(x.split()), len(x)), reverse=True)

    # 3. Assign files to their matching group folder
    assignments = {}
    for info in pdf_files_info:
        filepath = info["filepath"]
        fn_clean = os.path.splitext(info["filename"])[0].lower()
        fn_clean = re.sub(r'\(.*?\)', '', fn_clean)
        fn_clean = re.sub(r'\[.*?\]', '', fn_clean)
        fn_clean = re.sub(r'[^a-z0-9\s]', ' ', fn_clean)
        
        matched_folder = None
        for phrase in sorted_phrases:
            if re.search(r'\b' + re.escape(phrase) + r'\b', fn_clean):
                matched_folder = phrase.title()
                break

        if not matched_folder:
            matched_folder = "Single_Books"

        assignments[filepath] = matched_folder

    return assignments



def sanitize_folder_name(name):
    """
    Sanitizes folder name for Windows filesystem compatibility.
    Removes invalid characters: \\ / : * ? " < > | and trailing dots/spaces.
    """
    clean = re.sub(r'[\/:*?"<>|\\]', '_', name)
    clean = re.sub(r'\s+', ' ', clean).strip(' ._')
    if not clean or len(clean) < 2:
        return "Single_Books"
    return clean[:60]


def scan_and_sort_pdfs(input_dirs, output_dir="D:\\Sorted_PDF_Library", copy_files=True, clean_existing=True):
    """
    Scans input directories for PDFs, clusters files with matching title parts into shared folders,
    and builds a clean JSON catalog index.
    """
    print(f"\n🔍 Starting PDF Title Clustering & Auto-Sorter...")
    print(f"Input directories: {input_dirs}")
    print(f"Output directory: {output_dir}\n")

    # Delete existing output directory if clean_existing is True to start fresh
    if clean_existing and os.path.exists(output_dir):
        print(f"🧹 Cleaning up existing '{output_dir}' directory...")
        try:
            shutil.rmtree(output_dir)
        except Exception as e:
            print(f"⚠️ Warning cleaning directory: {e}")

    os.makedirs(output_dir, exist_ok=True)

    pdf_files = []
    for input_dir in input_dirs:
        if not os.path.exists(input_dir):
            print(f"⚠️ Warning: Directory '{input_dir}' not found. Skipping...")
            continue
        
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))

    print(f"📚 Discovered {len(pdf_files)} PDF files total.\n")

    # Pass 1: Extract PDF metadata for all discovered files
    print("⚡ Analyzing title patterns across all PDF files...")
    all_info = []
    for idx, pdf_path in enumerate(pdf_files, 1):
        try:
            info = extract_pdf_info(pdf_path)
            all_info.append(info)
        except Exception as e:
            print(f"⚠️ Error reading {pdf_path}: {e}")

    # Pass 2: Perform Title Phrase Clustering to match similar names
    print("🧩 Grouping books by common title parts and shared series names...")
    cluster_assignments = cluster_pdf_files_by_title_similarity(all_info)

    # Pass 3: Copy / Move files into organized cluster folders
    catalog = []
    for idx, info in enumerate(all_info, 1):
        pdf_path = info["filepath"]
        raw_folder_name = cluster_assignments.get(pdf_path, "Single_Books")
        folder_name = sanitize_folder_name(raw_folder_name)
        
        info["group_folder"] = folder_name
        target_group_dir = os.path.join(output_dir, folder_name)
        os.makedirs(target_group_dir, exist_ok=True)

        target_file_path = os.path.join(target_group_dir, info["filename"])

        if copy_files:
            try:
                if not os.path.exists(target_file_path):
                    shutil.copy2(pdf_path, target_file_path)
                    print(f"[{idx}/{len(all_info)}] -> Placed into Folder [{folder_name}]: {info['filename']}")
                else:
                    print(f"[{idx}/{len(all_info)}] -> Already exists in Folder [{folder_name}]: {info['filename']}")
            except Exception as copy_err:
                print(f"❌ Copy error for {info['filename']}: {copy_err}")
        
        info["sorted_filepath"] = target_file_path
        catalog.append(info)


    # Save Catalog Index JSON
    catalog_json_path = os.path.join(output_dir, "library_catalog_index.json")
    with open(catalog_json_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Title Similarity Clustering Complete!")
    print(f"Organized {len(catalog)} books into grouped folders inside '{output_dir}'")
    print(f"Saved catalog index to: {catalog_json_path}\n")
    return catalog



if __name__ == "__main__":
    # Test directories as requested by user
    target_sources = ["D:\\pdf 2", "D:\\pdfs"]
    output_location = "D:\\Sorted_PDF_Library"
    scan_and_sort_pdfs(target_sources, output_location, copy_files=True)
