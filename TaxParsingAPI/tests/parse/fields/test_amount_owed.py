
from TaxParsingAPI.parse.fields.amount_owed import AmountOwed
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

def test_amount_owed(preprocessed_tax_form_and_expected_amount_owed:Tuple[PreprocessTaxForm,str]):
    """
    Test the extraction of amount owed.

    This test verifies that the AmountOwed class correctly extracts the 
    amount owed from a given preprocessed tax form. It asserts that the 
    extracted amount owed match the expected amount owed.

    Args:
        preprocessed_tax_form_and_expected_amount_owed (Tuple[PreprocessTaxForm, str]): 
            A tuple containing the preprocessed tax form and the expected amount owed as a string.
    """
    preprocessed_tax_form, expected_amount_owed= preprocessed_tax_form_and_expected_amount_owed
    amount_owed = AmountOwed(preprocessed_tax_form=preprocessed_tax_form)

    
    assert AmountOwed.to_int(expected_amount_owed) == amount_owed.calculated_value
    
