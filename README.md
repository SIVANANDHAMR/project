# OCR Image Processor

This project provides a simple Python script that opens an image file dialog, runs OCR with Tesseract, and highlights detected text regions on the original image.

## Requirements

- Python 3.9+
- Tesseract OCR installed and available on your PATH

## Install dependencies

```bash
pip install -r requirements.txt
```

## Install Tesseract OCR

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y tesseract-ocr
```

### Windows

Install Tesseract from the official installer and make sure the `tesseract` executable is added to your PATH.

## Run the script

```bash
python OCR.py
```

Select an image file when prompted. The script will print extracted text and save a highlighted output image as `highlighted_output.png`.
