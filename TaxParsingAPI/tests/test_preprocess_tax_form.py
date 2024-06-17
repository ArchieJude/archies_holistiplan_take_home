from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm, OCRPage
from pathlib import Path
from typing import Dict
def test_preprocess_tax_form_intialization(mock_pdf_path:Path):
    """
    Test the initialization of the PreprocessTaxForm class.

    This test ensures that the PreprocessTaxForm object is correctly initialized with the given mock PDF path.
    It checks the following:
    - The preprocessed_tax_form object is an instance of PreprocessTaxForm.
    - The temporary PDF file and required directories are created.
    - Image files are generated from the PDF and have the correct file extension.
    - OCR pages are correctly set and are instances of OCRPage.
    - The PDF file has the correct suffix.

    Args:
        mock_pdf_path (Path): The path to the mock PDF file.
    """
    preprocessed_tax_form = PreprocessTaxForm(file_path=mock_pdf_path)
    assert isinstance(preprocessed_tax_form, PreprocessTaxForm)

    assert preprocessed_tax_form.file_path.exists(), "The temporary PDF file was not created."
    assert preprocessed_tax_form.base_dir.exists(), "The base dir of PDF file was not created."
    assert preprocessed_tax_form.base_image_directory.exists(), "The base image dir of PDF file was not created."
    assert preprocessed_tax_form.base_annotations_directory.exists(), "The base annotations dir of PDF file was not created."
    assert preprocessed_tax_form.base_annotations_over_images_dir.exists(), "The base annotations over images dir of PDF file was not created."
    assert len(preprocessed_tax_form.image_file_paths)>0
    for image_file_path in preprocessed_tax_form.image_file_paths:
        assert isinstance(image_file_path, Path)
        assert image_file_path.suffix == '.png'
        
        
    assert isinstance(preprocessed_tax_form.ocr_pages,Dict)
    assert len(preprocessed_tax_form.ocr_pages)>0
    for page_number, ocr_page in preprocessed_tax_form.ocr_pages.items():
        assert isinstance(ocr_page, OCRPage)
    # Check if the file has the correct suffix
    assert preprocessed_tax_form.file_path.suffix == '.pdf', "The temporary file does not have a .pdf suffix."
