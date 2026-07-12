import os
import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
from pytesseract import Output


def automate_form_processing(image_path):
    """
    Loads an invoice/form image, applies preprocessing to optimize OCR accuracy,
    extracts the text using PyTesseract, and highlights the detected text zones.
    """
    if not image_path:
        print("[!] No file selected. Exiting pipeline.")
        return
    if not os.path.exists(image_path):
        print(f"[!] Error: Target image file not found at {image_path}")
        return

    print(f"[+] Processing document: {image_path}\n")

    image = cv2.imread(image_path)
    if image is None:
        print(f"[!] Error: Unable to read image at {image_path}")
        return

    highlighted_image = image.copy()

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    custom_config = r"--oem 3 --psm 6"
    ocr_data = pytesseract.image_to_data(binary_image, config=custom_config, output_type=Output.DICT)

    extracted_text_list = []
    total_boxes = len(ocr_data["text"])

    for i in range(total_boxes):
        text = (ocr_data["text"][i] or "").strip()
        if not text:
            continue

        try:
            confidence = int(ocr_data["conf"][i])
        except (ValueError, TypeError):
            confidence = -1

        if confidence > 60:
            x = ocr_data["left"][i]
            y = ocr_data["top"][i]
            w = ocr_data["width"][i]
            h = ocr_data["height"][i]

            cv2.rectangle(highlighted_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            extracted_text_list.append(text)

    print("================ EXTRACTED TEXT ================")
    print(" ".join(extracted_text_list))
    print("================================================")

    output_path = "highlighted_output.png"
    success = cv2.imwrite(output_path, highlighted_image)
    if success:
        print(f"\n[+] Visualization successfully saved to: {output_path}")
    else:
        print(f"[!] Failed to save visualization to: {output_path}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("[*] Launching system file explorer... Please select an invoice image.")
    target_image = filedialog.askopenfilename(
        title="Select an Image for OCR & Highlighting",
        filetypes=[
            ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),
            ("All Files", "*.*"),
        ],
    )

    automate_form_processing(target_image)
    root.destroy()
