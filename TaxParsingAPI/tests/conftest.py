import pytest
from pathlib import Path
from django.conf import settings
from HolistiplanTakeHome.settings import MEDIA_ROOT
from fpdf import FPDF
from django.conf import settings
from TaxParsingAPI.models import TaxForm

test_file_content = [
    "Add lines 1z, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income .        |           220,640.",
    "Subtract line 10 from line 9. This is your adjusted gross income        |           220,183.",
    "Standard deduction or itemized deductions (from Schedule A)        |           27,700.",
    "Subtract line 14 from line 11. If zero or less, enter -0-. This is your taxable income        |           192,482.",
    "Add lines 22 and 23. This is your total tax        |           26,825.",
    "Add lines 25d, 26, and 32. These are your total payments        |           34,294.",
    "If line 33 is more than line 24, subtract line 24 from line 33. This is the amount you overpaid        |           7. 169.",
    "Subtract line 33 from line 24. This is the amount you owe.        |           ",
]

@pytest.fixture
def mock_pdf_path(tmp_path) -> Path:
    """
    Fixture to create a mock PDF file for testing.

    This fixture sets up a temporary directory structure and creates a mock PDF file
    with the specified content. The mock PDF is saved in a directory that simulates
    the media root of the TaxParsingAPI application. The path to the created PDF is
    returned for use in tests.

    Args:
        tmp_path (pathlib.Path): A temporary directory path provided by pytest.

    Returns:
        pathlib.Path: The path to the created mock PDF file.
    """
    FILE_NAME = "test_document.pdf"
    TAX_APP_DIR = Path(tmp_path) / "TaxParsingAPI"
    settings.MEDIA_ROOT = TAX_APP_DIR
    TAX_APP_DIR.mkdir()

    tax_forms_dir = TAX_APP_DIR / "tax_forms"
    tax_forms_dir.mkdir()

    mock_pdf_path = tax_forms_dir / FILE_NAME

    # Create a PDF with content "test content"
    pdf = FPDF()

    for file_content in test_file_content:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=file_content, ln=True, align="C")
    pdf.output(mock_pdf_path)

    return mock_pdf_path

@pytest.fixture
def tax_form_object(mock_pdf_path) -> TaxForm:
    """
    Fixture to create a mock TaxForm object.

    This fixture uses another fixture, mock_pdf_path, that creates a temporary directory structure and creates a mock PDF file
    with the specified content.

    Args:
        mock_pdf_path (pathlib.Path): The path to the created mock PDF file.

    Returns:
        tax_form (TaxForm): TaxForm model object
    """
    tax_form = TaxForm(
        tax_form=mock_pdf_path,
    )

    return tax_form
