from pathlib import Path

def test_tax_form_creation(db,tax_form_object) -> None:

    assert tax_form_object.id is not None
    assert isinstance(tax_form_object.tax_form,Path)


