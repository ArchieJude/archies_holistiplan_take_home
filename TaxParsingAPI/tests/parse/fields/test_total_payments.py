from TaxParsingAPI.parse.fields.total_payments import TotalPayments
from typing import Tuple
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm


def test_total_payments(
    preprocessed_tax_form_and_expected_total_payments: Tuple[PreprocessTaxForm, str]
):
    """
    Test the calculation of total payments.

    This test verifies that the TotalPayments class correctly calculates the 
    total payments from a given preprocessed tax form. It asserts that the 
    calculated total payments match the expected total payments.

    Args:
        preprocessed_tax_form_and_expected_total_payments (Tuple[PreprocessTaxForm, str]): 
            A tuple containing the preprocessed tax form and the expected total payments as a string.
    """
    preprocessed_tax_form, expected_total_payments = (
        preprocessed_tax_form_and_expected_total_payments
    )
    total_payments = TotalPayments(preprocessed_tax_form=preprocessed_tax_form)

    assert expected_total_payments == total_payments.value_ocr.normalized_text
