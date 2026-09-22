"""Extract text from an image and save a visualization of detected text."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import cv2
import pytesseract
from pytesseract import Output


def automate_form_processing(
    image_path: str | os.PathLike[str],
    output_path: str | os.PathLike[str] = "highlighted_output.png",
    confidence_threshold: float = 60.0,
) -> tuple[Path, list[str]]:
    """Run OCR, draw high-confidence text boxes, and return the output and text."""
    if not image_path:
        raise ValueError("An image path is required.")

    source_path = Path(image_path).expanduser()
    if not source_path.is_file():
        raise FileNotFoundError(f"Image file not found: {source_path}")

    image = cv2.imread(str(source_path))
    if image is None:
        raise ValueError(f"Unable to read image: {source_path}")

    highlighted_image = image.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, binary_image = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    ocr_data: dict[str, Any] = pytesseract.image_to_data(
        binary_image,
        config="--oem 3 --psm 6",
        output_type=Output.DICT,
    )

    extracted_text: list[str] = []
    for index, raw_text in enumerate(ocr_data.get("text", [])):
        text = (raw_text or "").strip()
        if not text:
            continue

        try:
            confidence = float(ocr_data["conf"][index])
        except (KeyError, IndexError, TypeError, ValueError):
            confidence = -1

        if confidence < confidence_threshold:
            continue

        x = int(ocr_data["left"][index])
        y = int(ocr_data["top"][index])
        width = int(ocr_data["width"][index])
        height = int(ocr_data["height"][index])
        cv2.rectangle(
            highlighted_image,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2,
        )
        extracted_text.append(text)

    destination = Path(output_path).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(destination), highlighted_image):
        raise OSError(f"Unable to write output image: {destination}")

    return destination, extracted_text


def choose_image() -> str:
    """Open a file chooser for users running the script without an image argument."""
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return filedialog.askopenfilename(
            title="Select an image for OCR",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All files", "*.*"),
            ],
        )
    finally:
        root.destroy()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "image",
        nargs="?",
        help="Path to an image. Opens a file chooser when omitted.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="highlighted_output.png",
        help="Output image path (default: highlighted_output.png).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=60.0,
        help="Minimum OCR confidence to highlight (default: 60).",
    )
    args = parser.parse_args()

    image_path = args.image or choose_image()
    if not image_path:
        parser.error("No image selected.")

    try:
        output_path, extracted_text = automate_form_processing(
            image_path,
            args.output,
            args.threshold,
        )
    except (FileNotFoundError, OSError, ValueError, pytesseract.TesseractError) as error:
        parser.error(str(error))

    print("Extracted text:")
    print(" ".join(extracted_text) or "(no high-confidence text found)")
    print(f"Highlighted image saved to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
