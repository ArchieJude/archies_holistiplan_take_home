import pytest
from typing import Tuple
from pathlib import Path
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

TAX_DIR = Path(__file__).parent / "EngHwPDFs"


@pytest.fixture(params=[f.name for f in TAX_DIR.rglob("*.pdf")])
def tax_pdf_file_path(request)->Path:
    """
    Fixture to provide the path to each PDF file in the TAX_DIR directory.

    This fixture uses pytest's parametrize functionality to iterate over all PDF files
    in the TAX_DIR directory. For each test, it provides the path to one of these PDF files.

    Args:
        request (pytest.FixtureRequest): The request object provided by pytest, used to access 
                                         the parameter values.

    Returns:
        Path: The path to the current PDF file being tested.
    """
    file_path= Path(TAX_DIR) / request.param
    return file_path

@pytest.fixture
def preprocessed_tax_form(mock_pdf_path:Path)->Tuple[Path, str]:
    """
    Fixture to create a PreprocessTaxForm instance using a mock PDF file path.

    This fixture sets up a PreprocessTaxForm instance using the provided mock PDF file path.
    It returns the PreprocessTaxForm instance for use in tests.

    Args:
        mock_pdf_path (Path): The path to the mock PDF file created for testing.

    Returns:
        PreprocessTaxForm: An instance of PreprocessTaxForm initialized with the mock PDF file path.
    """

    return PreprocessTaxForm(file_path=mock_pdf_path)
