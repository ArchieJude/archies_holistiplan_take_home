from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm
from TaxParsingAPI.parse.fields.total_tax import TotalTax
from typing import Tuple

def test_total_tax(preprocessed_tax_form_and_expected_total_tax:Tuple[PreprocessTaxForm,str]):
    """
    Test the calculation of total payments.

    This test verifies that the TotalPayments class correctly calculates the 
    total payments from a given preprocessed tax form. It asserts that the 
    calculated total payments match the expected total payments.

    Args:
        preprocessed_tax_form_and_expected_total_payments (Tuple[PreprocessTaxForm, str]): 
            A tuple containing the preprocessed tax form and the expected total payments as a string.
    """
    preprocesssed_form, expected_total_tax= preprocessed_tax_form_and_expected_total_tax
    total_tax = TotalTax(preprocessed_tax_form=preprocesssed_form)
    
    assert expected_total_tax == total_tax.value_ocr.text
    
