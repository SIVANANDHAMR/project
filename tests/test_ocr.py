import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import OCR


class OcrProcessingTests(unittest.TestCase):
    @patch("OCR.pytesseract.image_to_data")
    @patch("OCR.cv2.imwrite", return_value=True)
    @patch("OCR.cv2.rectangle")
    @patch("OCR.cv2.threshold", return_value=(None, "binary"))
    @patch("OCR.cv2.GaussianBlur", return_value="blurred")
    @patch("OCR.cv2.cvtColor", return_value="gray")
    @patch("OCR.cv2.imread")
    def test_high_confidence_text_is_returned_and_saved(
        self,
        _imread,
        _cvt_color,
        _blur,
        _threshold,
        rectangle,
        imwrite,
        image_to_data,
    ):
        image = Mock()
        image.copy.return_value = "highlighted"
        _imread.return_value = image
        image_to_data.return_value = {
            "text": ["Invoice", "noise"],
            "conf": ["95.5", "40"],
            "left": [1, 2],
            "top": [3, 4],
            "width": [20, 10],
            "height": [8, 6],
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "input.png"
            source.touch()
            destination = Path(temporary_directory) / "output.png"

            output_path, text = OCR.automate_form_processing(source, destination)

        self.assertEqual(destination, output_path)
        self.assertEqual(["Invoice"], text)
        rectangle.assert_called_once()
        imwrite.assert_called_once()


if __name__ == "__main__":
    unittest.main()
