from TaxParsingAPI.parse.fields.taxable_income import TaxableIncome
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

def test_taxable_income(preprocessed_tax_form_and_expected_taxable_income: Tuple[PreprocessTaxForm, str]):
    """
    Test the calculation of taxable income.

    This test verifies that the TaxableIncome class correctly extracts the
    taxable income from a given preprocessed tax form. It asserts that the
    extracted matches the expected taxable income.

    Args:
        preprocessed_tax_form_and_expected_taxable_income (Tuple[PreprocessTaxForm, str]):
            A tuple containing the preprocessed tax form and the expected taxable income as a string.
    """
    preprocessed_tax_form, expected_taxable_income = preprocessed_tax_form_and_expected_taxable_income
    taxable_income = TaxableIncome(preprocessed_tax_form=preprocessed_tax_form)
    
    assert expected_taxable_income == taxable_income.value_ocr.text
    
