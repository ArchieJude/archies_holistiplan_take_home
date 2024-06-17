from TaxParsingAPI.parse.fields.field_base import FieldBase
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm

def test_initialization_of_field_base(preprocessed_tax_form:PreprocessTaxForm):
    """
    This test checks if an instance of the FieldBase class is correctly created
    when initialized with a preprocessed_tax_form. It asserts that the created
    instance is indeed of type FieldBase.

    Args:
        preprocessed_tax_form (PreprocessTaxForm): The preprocessed tax form data used to 
                                     initialize the FieldBase instance.
    """
    field_base = FieldBase(preprocessed_tax_form=preprocessed_tax_form)
    assert isinstance(field_base, FieldBase)
