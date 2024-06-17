from TaxParsingAPI.parse.fields.adjusted_gross_income import AdjustedGrossIncome
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

def test_adjusted_gross_income(preprocessed_tax_form_and_expected_adjusted_gross_income:Tuple[PreprocessTaxForm,str]):
    """
    Test the calculation of adjusted gross income.

    This test verifies that the AdjustedGrossIncome class correctly extracts the
    adjusted gross income from a given preprocessed tax form. It asserts that the
    extracted matches the expected adjusted gross income.

    Args:
        preprocessed_tax_form_and_expected_adjusted_gross_income (Tuple[PreprocessTaxForm, str]):
            A tuple containing the preprocessed tax form and the expected adjusted gross income as a string.
    """
    preprocessed_tax_form, expected_adjusted_gross_income = preprocessed_tax_form_and_expected_adjusted_gross_income
   
    adjusted_gross_income = AdjustedGrossIncome(preprocessed_tax_form=preprocessed_tax_form) 
    
    assert expected_adjusted_gross_income == adjusted_gross_income.value_ocr.text
    
