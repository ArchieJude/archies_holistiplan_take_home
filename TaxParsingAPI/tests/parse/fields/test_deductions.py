from TaxParsingAPI.parse.fields.deductions import Deductions
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

def test_deductions(preprocessed_tax_form_and_expected_deductions:Tuple[PreprocessTaxForm,str]):
    """
    Test the extraction of deductions

    This test verifies that the TotalPayments class correctly calculates the 
    deductions from a given preprocessed tax form. It asserts that the 
    extracted deductions match the expected deductions.

    Args:
        preprocessed_tax_form_and_expected_deductions (Tuple[PreprocessTaxForm, str]): 
            A tuple containing the preprocessed tax form and the expected deductions as a string.
    """
    preprocessed_tax_form, expected_deductions = preprocessed_tax_form_and_expected_deductions
    deductions = Deductions(preprocessed_tax_form=preprocessed_tax_form)
    
    assert expected_deductions == deductions.value_ocr.text
    
