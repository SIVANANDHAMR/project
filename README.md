# OCR Image Processor

A small Python document-processing utility that preprocesses an image, extracts text with Tesseract OCR, and saves a copy with high-confidence text regions highlighted.

## Features

- Grayscale, blur, and Otsu threshold preprocessing
- Confidence-aware OCR box highlighting
- Command-line interface for scripts and automation
- Optional file chooser for desktop use
- Testable processing function with explicit return values

## Requirements

- Python 3.9+
- Tesseract OCR installed and available on `PATH`

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Install Tesseract:

- Ubuntu/Debian: `sudo apt update && sudo apt install -y tesseract-ocr`
- Windows: install Tesseract and add its installation directory to `PATH`
- macOS: `brew install tesseract`

## Usage

Process an image from the command line:

```bash
python OCR.py invoice.png --output output/highlighted.png
```

If the image path is omitted, a file chooser opens:

```bash
python OCR.py
```

Adjust the minimum OCR confidence when needed:

```bash
python OCR.py invoice.png --threshold 75
```

The command prints the extracted text and writes the highlighted image to the requested output path.

## Test

```bash
python -m unittest discover -s tests -v
```
