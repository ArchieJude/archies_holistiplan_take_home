from TaxParsingAPI.parse.fields.overpaid import Overpaid
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

def test_overpaid(preprocessed_tax_form_and_expected_overpaid: Tuple[PreprocessTaxForm, str]):
    """
    Test the calculation of overpaid.

    This test verifies that the Overpaid class correctly calculates the 
    overpaid amount from a given preprocessed tax form. It asserts that the 
    calculated overpaid matches the expected overpaid.

    Args:
        preprocessed_tax_form_and_expected_overpaid (Tuple[PreprocessTaxForm, str]): 
            A tuple containing the preprocessed tax form and the expected total overpaid as a string.
    """
    preprocessed_tax_form, expected_overpaid = preprocessed_tax_form_and_expected_overpaid

    overpaid = Overpaid(preprocessed_tax_form=preprocessed_tax_form)
    
    expected_overpaid_int = Overpaid.to_int(expected_overpaid)

    assert expected_overpaid_int == overpaid.calculated_value
    
