from TaxParsingAPI.models import (
    TaxForm,
    TaxField,
    UPLOAD_TO
)
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm
from TaxParsingAPI.parse.tax_parser import TaxParser
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm
from typing import List,Dict
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)
from HolistiplanTakeHome.settings import MEDIA_ROOT


def get_default_tax_fields()->List[Dict]:
    """
    Get a list of default tax fields.

    This function generates a list of dictionaries, each containing a tax field type 
    based on the predefined FIELD_CHOICES in the TaxField model. This can be used to 
    initialize or prepopulate tax fields.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains a single key-value pair
                    with the key "tax_field" and the value being one of the tax field type.
    """
    tax_fields = []

    for tax_field, _ in TaxField.FIELD_CHOICES:
        tax_fields.append({"tax_field": tax_field})

    return tax_fields


class TaxFieldSerializer(ModelSerializer):
    """
    Serializer for the TaxField model.
    """
    class Meta:
        model = TaxField
        fields = ["tax_field"]


class TaxFormSerializer(HyperlinkedModelSerializer):
    """
    Serializer for the TaxForm model.

    This serializer handles the serialization and deserialization of the TaxForm model,
    including nested tax fields. It provides custom logic for converting input data into 
    internal Python objects and for creating and representing TaxForm instances.

    Attributes:
        tax_fields (TaxFieldSerializer): Nested serializer for tax fields.

    Methods:
        to_internal_value(self, data):
            Custom method to handle pre-validation logic and convert input data into internal objects.
        
        create(self, validated_data):
            Custom method to create a TaxForm instance along with its associated tax fields.
        
        to_representation(self, instance):
            Custom method to represent a TaxForm instance, including additional fields for tax fields.
    """
    tax_fields = TaxFieldSerializer(many=True, required=False, read_only=True)
    

    class Meta:
        model = TaxForm
        fields = ["url", "id", "tax_form", "tax_fields"]
      
    def to_internal_value(self, data:Dict)->Dict:
        """
        Convert input data into internal Python objects.

        This method preprocesses the input data to create a PreprocessTaxForm instance if needed,
        and generates a list of tax fields with their respective details.

        Args:
            data (dict): The input data.

        Returns:
            dict: The converted data in internal format.
        """
        if not isinstance(data.get('preprocessed_tax_form'),PreprocessTaxForm):
            self.preprocessed_tax_form = PreprocessTaxForm(
                file_path=MEDIA_ROOT / UPLOAD_TO /  data["tax_form"].name,
                file_bytes = data['tax_form'].read()
            )
        else:
            self.preprocessed_tax_form = data['preprocessed_tax_form']
            
            
        tax_fields = []
        for tax_field_dict in data.get("tax_fields", get_default_tax_fields()):
            tax_field = tax_field_dict["tax_field"]

            field_type_class = TaxParser.get_field_type(tax_field)
            
            field_instance = field_type_class(
                preprocessed_tax_form=self.preprocessed_tax_form
            )

            instruction_text = field_instance.statement_ocr.text
            instruction_matched_pattern = field_instance.statement_ocr.pattern
            value_text = field_instance.value_ocr.text
            value_normalized_text = field_instance.value_ocr.normalized_text
            value_matched_pattern = field_instance.value_ocr.pattern
            page_number = field_instance.value_ocr.page.page_number
            
            if tax_field == TaxField.OVERPAID or tax_field == TaxField.AMOUNT_OWED and not value_text:
    
                value_in_numeric = field_instance.calculated_value
            else:
                value_in_numeric = field_instance.to_int(text=value_text)
                
            tax_fields.append(
                {
                    "tax_field": tax_field,
                    "instruction_text": instruction_text,
                    "instruction_matched_pattern": instruction_matched_pattern,
                    "value_text": value_text,
                    "value_normalized_text": value_normalized_text,
                    "value_in_numeric": value_in_numeric,
                    "value_matched_pattern": value_matched_pattern,
                    "page_number": page_number,
                }
            )
            
        self.preprocessed_tax_form=tax_fields
        return super().to_internal_value(data)
    
    
    def create(self, validated_data:Dict)->TaxForm:
        """
        Create a TaxForm instance along with its associated tax fields.

        This method creates a new TaxForm instance and its associated tax fields based on the
        preprocessed tax form data.

        Args:
            validated_data (dict): The validated data.

        Returns:
            TaxForm: The created TaxForm instance.
        """
        validated_data["tax_form"] = TaxForm.objects.create(tax_form=validated_data["tax_form"])

        tax_form = validated_data["tax_form"]

        for tax_field_dict in self.preprocessed_tax_form:
            
            
            tax_field = tax_field_dict["tax_field"]
            instruction_text = tax_field_dict["instruction_text"]
            instruction_matched_pattern = tax_field_dict["instruction_matched_pattern"]
            value_text = tax_field_dict["value_text"]
            value_normalized_text = tax_field_dict["value_normalized_text"]
            value_in_numeric = tax_field_dict["value_in_numeric"]
            value_matched_pattern = tax_field_dict["value_matched_pattern"]
            page_number = tax_field_dict["page_number"]

            tax_field_obj = TaxField.objects.create(
                tax_form=tax_form,
                tax_field=tax_field,
                instruction_text=instruction_text,
                instruction_matched_pattern=instruction_matched_pattern,
                value_text=value_text,
                value_normalized_text=value_normalized_text,
                value_in_numeric=value_in_numeric,
                value_matched_pattern=value_matched_pattern,
                page_number=page_number,
            )
 
            tax_field_obj.save()
        validated_data["tax_form"].save()
        return tax_form

    def to_representation(self, instance: TaxForm):
        """
        Represent a TaxForm instance, including additional fields for tax fields.

        This method adds extra fields to the tax field representation, such as instruction text,
        matched patterns, value text, and page number. It also includes the 'pay_this_amount' field.

        Args:
            instance (TaxForm): The TaxForm instance to represent.

        Returns:
            dict: The representation of the TaxForm instance.
        """
        representation = super().to_representation(instance)
        representation["pay_this_amount"] = instance.pay_this_amount
        for tax_field_dict in representation["tax_fields"]:
            # add more fields to see
            tax_field = tax_field_dict.get("tax_field")
            tax_field_obj = instance.get_tax_field(tax_field=tax_field)
            tax_field_dict["instruction_text"] = tax_field_obj.instruction_text
            tax_field_dict["instruction_matched_pattern"] = (
                tax_field_obj.instruction_matched_pattern
            )
            tax_field_dict["value_text"] = tax_field_obj.value_text
            tax_field_dict["value_normalized_text"] = (
                tax_field_obj.value_normalized_text
            )
            tax_field_dict["value_in_numeric"] = tax_field_obj.value_in_numeric
            tax_field_dict["value_matched_pattern"] = (
                tax_field_obj.value_matched_pattern
            )
            tax_field_dict["page_number"] = tax_field_obj.page_number


        
        if not instance.tax_fields.exists():
            representation["tax_fields"] = [{"tax_field": "default_field"}]

        return representation
