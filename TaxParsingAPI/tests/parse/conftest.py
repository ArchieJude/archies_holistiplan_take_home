import pytest
from typing import Dict,Tuple
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

@pytest.fixture
def preprocessed_tax_form_and_expected_total_income(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected total income.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected total income from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected total income.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected total income as a string.
    """
    
    expected_income_dict: Dict = {
        "7.pdf":"220,640.",
        "8a.pdf":"244,561.",
        "8b.pdf":"77,352",
        "8c.pdf":"18,803",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"234,650.",
        "2023_Samuel_Singletary.pdf":"245,350.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"394,486.",
        "2023senior.pdf":"91"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)
    return preprocessed_tax_form,expected_income_dict.get(tax_pdf_file_path.name)


@pytest.fixture
def preprocessed_tax_form_and_expected_adjusted_gross_income(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected adjusted gross income.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected adjusted gross income from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected adjusted gross income.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected adjusted gross income as a string.
    """
    
    adjusted_gross_income_dict: Dict = {
        "7.pdf":"220,183.",
        "8a.pdf":"243,103.",
        "8b.pdf":"77,352",
        "8c.pdf":"18,803",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"230,912.",
        "2023_Samuel_Singletary.pdf":"243,948.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"382,448.",
        "2023senior.pdf":"111"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)
    return preprocessed_tax_form,adjusted_gross_income_dict.get(tax_pdf_file_path.name)

@pytest.fixture
def preprocessed_tax_form_and_expected_deductions(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected deductions.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected deductions from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected deductions.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected deductions as a string.
    """
    
    deductions_dict: Dict = {
        "7.pdf":"27,700.",
        "8a.pdf":"27,700.",
        "8b.pdf":"29,200",
        "8c.pdf":"13,850",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"42,000.",
        "2023_Samuel_Singletary.pdf":"27,500.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"61,348.",
        "2023senior.pdf":"121"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)
    return preprocessed_tax_form,deductions_dict.get(tax_pdf_file_path.name)


@pytest.fixture
def preprocessed_tax_form_and_expected_taxable_income(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected taxable income.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected taxable income from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected taxable income.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected taxable income as a string.
    """
    taxable_income_dict: Dict = {
        "7.pdf":"192,482.",
        "8a.pdf":"212,356.",
        "8b.pdf":"48,148",
        "8c.pdf":"4, 939",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"179,080.",
        "2023_Samuel_Singletary.pdf":"215,747.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"289,430.",
        "2023senior.pdf":"151"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)

    return preprocessed_tax_form,taxable_income_dict.get(tax_pdf_file_path.name)


@pytest.fixture
def preprocessed_tax_form_and_expected_total_tax(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected total tax.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected total tax from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected total tax.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected total tax as a string.
    """
    total_tax_dict: Dict = {
        "7.pdf":"26,825.",
        "8a.pdf":"40,081.",
        "8b.pdf":"6,041",
        "8c.pdf":"175",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"25,233.",
        "2023_Samuel_Singletary.pdf":"42,048.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"80,789.",
        "2023senior.pdf":"241"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)        
    return preprocessed_tax_form,total_tax_dict.get(tax_pdf_file_path.name)


@pytest.fixture
def preprocessed_tax_form_and_expected_total_payments(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected total payments.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected total payments from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected total payments.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected total payments as a string.
    """
    total_payments_dict: Dict = {
        "7.pdf":"34,294.",
        "8a.pdf":"43,723.",
        "8b.pdf":"6,160",
        "8c.pdf":"1,983",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"25,000.",
        "2023_Samuel_Singletary.pdf":"30,100.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"67,068.",
        "2023senior.pdf":"331"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)
    return preprocessed_tax_form,total_payments_dict.get(tax_pdf_file_path.name)


@pytest.fixture
def preprocessed_tax_form_and_expected_overpaid(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected overpaid.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected overpaid from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected overpaid.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected overpaid as a string.
    """
    overpaid_dict: Dict = {
        "7.pdf":"7,469.",
        "8a.pdf":"3,642.",
        "8b.pdf":"119",
        "8c.pdf":"1,808",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"",
        "2023_Samuel_Singletary.pdf":"",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"",
        "2023senior.pdf":"341"
    }

    
    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)  
    return preprocessed_tax_form,overpaid_dict.get(tax_pdf_file_path.name)


@pytest.fixture
def preprocessed_tax_form_and_expected_amount_owed(tax_pdf_file_path:Path)->Tuple[PreprocessTaxForm, str]:
    """
    Fixture to create a PreprocessTaxForm instance and provide the expected amount owed.

    This fixture sets up a PreprocessTaxForm instance using the provided tax PDF file path, a pytest fixture,
    and retrieves the expected amount owed from a predefined dictionary based on the file name.
    It returns a tuple containing the PreprocessTaxForm instance and the expected amount owed.

    Args:
        tax_pdf_file_path (Path): The path to the tax PDF file used for preprocessing.

    Returns:
        Tuple[PreprocessTaxForm, str]: A tuple containing the PreprocessTaxForm instance and the expected amount owed as a string.
    """
    amount_owed_dict: Dict = {
        "7.pdf":"",
        "8a.pdf":"",
        "8b.pdf":"",
        "8c.pdf":"",
        "2023_Sample_Return_Peter_and_Paula_Professor.pdf":"233.",
        "2023_Samuel_Singletary.pdf":"11,948.",
        "2023_Tax_Return_MFJ_French_Family_CORRECTED.pdf":"13,721.",
        "2023senior.pdf":"371"
    }

    preprocessed_tax_form=PreprocessTaxForm(file_path=tax_pdf_file_path)
    return preprocessed_tax_form,amount_owed_dict.get(tax_pdf_file_path.name)