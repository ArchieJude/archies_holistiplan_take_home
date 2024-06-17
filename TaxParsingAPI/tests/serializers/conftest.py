import pytest
from TaxParsingAPI.models import TaxForm, TaxField
from django.core.files.uploadedfile import SimpleUploadedFile
from TaxParsingAPI.serializers import TaxFormSerializer, get_default_tax_fields
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm


@pytest.fixture
def serialized_tax_form_with_one_field(mock_pdf_path) -> TaxFormSerializer:
    """
    Fixture to create a TaxFormSerializer instance with one tax field.

    This fixture sets up the necessary related model, TaxField, and data for creating a
    TaxFormSerializer instance with one tax field. It reads a mock PDF file,
    creates an uploaded file object, and prepares the data for the serializer.
    The serializer is then validated and returned for use in tests.

    Args:
        mock_pdf_path (pathlib.Path): The path to the mock PDF file created for testing.

    Returns:
        TaxFormSerializer: An instance of TaxFormSerializer with the provided data.
    """
    # Create related models first

    mock_path = mock_pdf_path

    with open(mock_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    uploaded_file = SimpleUploadedFile(
        name=mock_path.name, content=pdf_content, content_type="application/pdf"
    )
    # Data for the serializer

    preprocessed_tax_form = PreprocessTaxForm(
        file_path=mock_path,
    )

    data = {
        "tax_form": uploaded_file,
        "tax_fields": [{"tax_field": TaxField.ADJUSTED_GROSS_INCOME}],
        "preprocessed_tax_form": preprocessed_tax_form,
    }

    tax_form_serializer = TaxFormSerializer(data=data)
    tax_form_serializer.is_valid()

    return tax_form_serializer


@pytest.fixture
def serialized_tax_form_with_all_field(mock_pdf_path) -> TaxFormSerializer:
    """
    Fixture to create a TaxFormSerializer instance with all the tax fields.

    This fixture sets up the necessary related model, TaxField, and data for creating a
    TaxFormSerializer instance with all the tax fields. It reads a mock PDF file,
    creates an uploaded file object, and prepares the data for the serializer.
    The serializer is then validated and returned for use in tests.

    Args:
        mock_pdf_path (pathlib.Path): The path to the mock PDF file created for testing.

    Returns:
        TaxFormSerializer: An instance of TaxFormSerializer with the provided data.
    """

    mock_path = mock_pdf_path

    with open(mock_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    uploaded_file = SimpleUploadedFile(
        name=mock_path.name, content=pdf_content, content_type="application/pdf"
    )
    # Data for the serializer

    preprocessed_tax_form = PreprocessTaxForm(
        file_path=mock_path,
    )

    data = {
        "tax_form": uploaded_file,
        "tax_fields": get_default_tax_fields(),
        "preprocessed_tax_form": preprocessed_tax_form,
    }

    tax_form_serializer = TaxFormSerializer(data=data)
    tax_form_serializer.is_valid()

    return tax_form_serializer


@pytest.fixture
def tax_form_negative_pay_this_amount(
    mock_negative_pay_this_amount_pdf_path,
) -> TaxForm:
    """
    Fixture to create a TaxForm instance with a negative pay_this_amount value.

    This fixture sets up the necessary related model, TaxField, and data for creating a
    TaxForm instance with a negative pay_this_amount value. It reads a mock PDF
    file, creates an uploaded file object, and prepares the data for the serializer.
    The serializer is then validated and returned for use in tests.

    Args:
        mock_negative_pay_this_amount_pdf_path (pathlib.Path): The path to the mock PDF
                                                               file created for testing with a negative pay_this_amount value.

    Returns:
        TaxFormSerializer: An instance of TaxFormSerializer with the provided data.
    """

    mock_path = mock_negative_pay_this_amount_pdf_path

    with open(mock_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    uploaded_file = SimpleUploadedFile(
        name=mock_path.name, content=pdf_content, content_type="application/pdf"
    )
    # Data for the serializer

    preprocessed_tax_form = PreprocessTaxForm(
        file_path=mock_path,
    )

    data = {
        "tax_form": uploaded_file,
        "tax_fields": get_default_tax_fields(),
        "preprocessed_tax_form": preprocessed_tax_form,
    }

    tax_form_serializer = TaxFormSerializer(data=data)
    tax_form_serializer.is_valid()

    return tax_form_serializer


@pytest.fixture
def tax_form_positive_pay_this_amount(
    mock_positive_pay_this_amount_pdf_path,
) -> TaxForm:
    """
    Fixture to create a TaxForm instance with a positive pay_this_amount value.

    This fixture sets up the necessary related model, TaxField, and data for creating a
    TaxForm instance with a positive pay_this_amount value. It reads a mock PDF
    file, creates an uploaded file object, and prepares the data for the serializer.
    The serializer is then validated and returned for use in tests.

    Args:
        mock_positive_pay_this_amount_pdf_path (pathlib.Path): The path to the mock PDF
                                                               file created for testing with a positive pay_this_amount value.

    Returns:
        TaxFormSerializer: An instance of TaxFormSerializer with the provided data.
    """

    mock_path = mock_positive_pay_this_amount_pdf_path

    with open(mock_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    uploaded_file = SimpleUploadedFile(
        name=mock_path.name, content=pdf_content, content_type="application/pdf"
    )
    # Data for the serializer

    preprocessed_tax_form = PreprocessTaxForm(
        file_path=mock_path,
    )

    data = {
        "tax_form": uploaded_file,
        "tax_fields": get_default_tax_fields(),
        "preprocessed_tax_form": preprocessed_tax_form,
    }

    tax_form_serializer = TaxFormSerializer(data=data)
    tax_form_serializer.is_valid()

    return tax_form_serializer
