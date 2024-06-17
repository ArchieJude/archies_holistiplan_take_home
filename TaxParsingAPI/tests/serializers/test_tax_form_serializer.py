import pytest
from TaxParsingAPI.serializers import TaxFormSerializer, get_default_tax_fields
from rest_framework.test import APIRequestFactory



@pytest.mark.django_db
def test_tax_form_representation_one_field(serialized_tax_form_with_one_field):
    """
    Test the representation of a tax form with one tax field.

    This test verifies that the TaxFormSerializer correctly serializes a tax form
    instance with all the fields. It checks that the serialized data matches the expected
    output, including the URL, ID, tax form URL, tax fields details, and the amount
    to be paid.

    Steps:
    1. Create an instance of APIRequestFactory to simulate a GET request.
    2. Initialize the tax form serializer with validated data.
    3. Create a tax form instance using the serializer.
    4. Re-initialize the serializer with the created tax form instance and the request context.
    5. Serialize the tax form instance to get the data dictionary.
    6. Define the expected output for the serialized tax form data.
    7. Assert that the serialized data matches the expected output.

    Args:
        serialized_tax_form_with_one_field (TaxFormSerializer): Serializer with validated data
                                                                for creating a tax form instance.
    """
    
    factory = APIRequestFactory()
    request = factory.get("/")
    
    tax_form_serializer = serialized_tax_form_with_one_field
    tax_form = tax_form_serializer.create(validated_data=tax_form_serializer.validated_data)
    #instance = tax_form
    tax_form_serializer = TaxFormSerializer(
        instance=tax_form, context={"request": request}
    )
   
    data = tax_form_serializer.data
    # Expected output
    expected_data = {
        "url": f'http://testserver/api/tax-forms/{tax_form.id}/',
        "id": str(tax_form.id),
        "tax_form": f"http://testserver/{tax_form.tax_form.name}",
        "tax_fields": [
            {
                "tax_field": tax_field['tax_field'],
                "instruction_text": tax_form.get_tax_field(tax_field['tax_field']).instruction_text,
                "instruction_matched_pattern": tax_form.get_tax_field(tax_field['tax_field']).instruction_matched_pattern,
                "value_text": tax_form.get_tax_field(tax_field['tax_field']).value_text,
                "value_normalized_text": tax_form.get_tax_field(tax_field['tax_field']).value_normalized_text,
                "value_in_numeric": tax_form.get_tax_field(tax_field['tax_field']).value_in_numeric,
                "value_matched_pattern": tax_form.get_tax_field(tax_field['tax_field']).value_matched_pattern,
                "page_number": tax_form.get_tax_field(tax_field['tax_field']).page_number,
            } for tax_field in data['tax_fields']
        ],
        'pay_this_amount': tax_form.pay_this_amount
    }


    assert data == expected_data


@pytest.mark.django_db
def test_tax_form_representation_all_field(serialized_tax_form_with_all_field):
    """
    Test the representation of a tax form with all the tax fields.

    This test verifies that the TaxFormSerializer correctly serializes a tax form
    instance with all the tax fields. It checks that the serialized data matches the expected
    output, including the URL, ID, tax form URL, tax fields details, and the amount
    to be paid.

    Steps:
    1. Create an instance of APIRequestFactory to simulate a GET request.
    2. Initialize the tax form serializer with validated data.
    3. Create a tax form instance using the serializer.
    4. Re-initialize the serializer with the created tax form instance and the request context.
    5. Serialize the tax form instance to get the data dictionary.
    6. Define the expected output for the serialized tax form data.
    7. Assert that the serialized data matches the expected output.

    Args:
        serialized_tax_form_with_one_field (TaxFormSerializer): Serializer with validated data
                                                                for creating a tax form instance.
    """
    factory = APIRequestFactory()
    request = factory.get("/")
    
    tax_form_serializer = serialized_tax_form_with_all_field
    tax_form = tax_form_serializer.create(validated_data=tax_form_serializer.validated_data)
   
    tax_form_serializer = TaxFormSerializer(
        instance=tax_form, context={"request": request}
    )
   
    data = tax_form_serializer.data
    expected_data = {
        "url": f'http://testserver/api/tax-forms/{tax_form.id}/',
        "id": str(tax_form.id),
        "tax_form": f"http://testserver/{tax_form.tax_form.name}",
        "tax_fields": [
            {
                "tax_field": tax_field['tax_field'],
                "instruction_text": tax_form.get_tax_field(tax_field['tax_field']).instruction_text,
                "instruction_matched_pattern": tax_form.get_tax_field(tax_field['tax_field']).instruction_matched_pattern,
                "value_text": tax_form.get_tax_field(tax_field['tax_field']).value_text,
                "value_normalized_text": tax_form.get_tax_field(tax_field['tax_field']).value_normalized_text,
                "value_in_numeric": tax_form.get_tax_field(tax_field['tax_field']).value_in_numeric,
                "value_matched_pattern": tax_form.get_tax_field(tax_field['tax_field']).value_matched_pattern,
                "page_number": tax_form.get_tax_field(tax_field['tax_field']).page_number,
            } for tax_field in get_default_tax_fields()
        ],
        'pay_this_amount': tax_form.pay_this_amount
    }


    assert data == expected_data
    
     
@pytest.mark.django_db
def test_negative_pay_this_amount(tax_form_negative_pay_this_amount):
    """
    Test the handling of a negative pay_this_amount value.

    This test verifies that the TaxForm model correctly handles and stores a 
    negative value for the pay_this_amount field. It asserts that the stored 
    value matches the expected negative amount.

    Args:
        tax_form_negative_pay_this_amount (TaxFormSerializer): Serializer with validated data
                                                               for creating a tax form instance
                                                               with a negative pay_this_amount value.
    """
    tax_form = tax_form_negative_pay_this_amount.create(validated_data=tax_form_negative_pay_this_amount.validated_data)

    pay_this_amount=tax_form.pay_this_amount
    assert pay_this_amount == -233
 
 
@pytest.mark.django_db
def test_positive_pay_this_amount(tax_form_positive_pay_this_amount):
    """
    Test the handling of a postive pay_this_amount value.

    This test verifies that the TaxForm model correctly handles and stores a 
    positive value for the pay_this_amount field. It asserts that the stored 
    value matches the expected positive amount.

    Args:
        tax_form_positive_pay_this_amount (TaxFormSerializer): Serializer with validated data
                                                               for creating a tax form instance
                                                               with a positive pay_this_amount value.
    """
    tax_form = tax_form_positive_pay_this_amount.create(validated_data=tax_form_positive_pay_this_amount.validated_data)

    pay_this_amount=tax_form.pay_this_amount
    assert pay_this_amount == 3642