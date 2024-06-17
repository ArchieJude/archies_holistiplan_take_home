from TaxParsingAPI.parse.fields.total_income import TotalIncome
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm


def test_total_income(preprocessed_tax_form_and_expected_total_income: Tuple[PreprocessTaxForm, str]):
    """
    """
    preprocessed_tax_form, expected_total_income = preprocessed_tax_form_and_expected_total_income

    total_income = TotalIncome(preprocessed_tax_form=preprocessed_tax_form)
    
    
    
    assert expected_total_income == total_income.value_ocr.text
    
