import PyPDF2
import docx
from pathlib import Path

def extract_text(file_path: str) -> str:
    """Read raw text from PDF, DOCX, or TXT files."""
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif ext == ".txt":
        return path.read_text(encoding="utf-8")

    else:
        raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks.
    
    WHY OVERLAP? If a sentence is cut in half between two chunks,
    the overlap ensures neither chunk loses the full context.
    
    Example: chunk_size=500 means each chunk is ~500 characters.
    overlap=50 means the last 50 chars of chunk 1 appear at the
    start of chunk 2.
    """
    words = text.split()
    chunks = []
    
    i = 0
    while i < len(words):
        # Take a slice of words
        chunk_words = words[i : i + chunk_size]
        chunks.append(" ".join(chunk_words))
        # Move forward but step back by 'overlap' to create the overlap
        i += chunk_size - overlap

    return chunks