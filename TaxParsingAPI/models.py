from django.db import models
from typing import Optional
import uuid
UPLOAD_TO = "tax_forms"

class TaxForm(models.Model):
    """
    Model representing a tax form.

    This class handles the storage and management of tax form files. It includes methods
    to retrieve associated tax fields and calculate the amount to be paid or overpaid.

    Attributes:
        id (UUIDField): The unique identifier for each tax form, generated automatically.
        tax_form (FileField): The file field for uploading the tax form.
        uploaded_at (DateTimeField): The timestamp when the tax form was uploaded, set automatically.

    Methods:
        __str__():
            Returns a string representation of the tax form file name.
        
        get_all_tax_fields():
            Retrieves all associated tax fields for the tax form.
        
        get_tax_field(tax_field) -> Optional['TaxField']:
            Retrieves a specific tax field associated with the tax form.
            Returns None if the tax field does not exist.
        
        pay_this_amount() -> int:
            Calculates the amount to be paid or overpaid based on the tax fields.
            Returns a negative amount if there is an amount owed, or a positive amount if there is an overpayment.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tax_form = models.FileField(upload_to=UPLOAD_TO)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tax_form}"
    
    def get_all_tax_fields(self):
        return self.tax_fields.all()
    
    def get_tax_field(self, tax_field)->Optional['TaxField']:
        try:
            return self.tax_fields.get(tax_field=tax_field)
        except TaxField.DoesNotExist:
            return None
    @property
    def pay_this_amount(self) -> int:
        
        amount_owed_field = self.get_tax_field(TaxField.AMOUNT_OWED)
        if amount_owed_field is not None:
            amount_owed:int = int(amount_owed_field.value_in_numeric)
            if amount_owed>0:
                return -amount_owed
        
        overpaid_field = self.get_tax_field(TaxField.OVERPAID)
        if overpaid_field is not None:
            overpaid:int = int(overpaid_field.value_in_numeric)
            if overpaid>0:
                return overpaid
                
        
        return 0  # or None, depending on your requirement

class TaxField(models.Model):
    """
    Model representing a field within a tax form.

    This class handles the storage and management of individual tax fields within a tax form.
    Each tax field is associated with a tax form and has various attributes such as the type of field,
    instruction text, and values in different formats.

    Attributes:
        TOTAL_INCOME (str): Constant for the total income field.
        ADJUSTED_GROSS_INCOME (str): Constant for the adjusted gross income field.
        DEDUCTIONS (str): Constant for the deductions field.
        TAXABLE_INCOME (str): Constant for the taxable income field.
        TOTAL_TAX (str): Constant for the total tax field.
        TOTAL_PAYMENTS (str): Constant for the total payments field.
        OVERPAID (str): Constant for the overpaid field.
        AMOUNT_OWED (str): Constant for the amount owed field.
        
        FIELD_CHOICES (list): List of tuples containing field choices and their descriptions.

        id (UUIDField): The unique identifier for each tax field, generated automatically.
        tax_form (ForeignKey): Foreign key linking the tax field to a tax form.
        tax_field (CharField): The type of the tax field, with choices from FIELD_CHOICES.
        instruction_text (CharField): The instruction text associated with the field.
        instruction_matched_pattern (CharField): The pattern matched in the instruction text.
        value_text (CharField): The text value of the field.
        value_normalized_text (CharField): The normalized text value of the field.
        value_in_numeric (DecimalField): The numeric value of the field.
        value_matched_pattern (CharField): The pattern matched in the value text.
        page_number (IntegerField): The page number where the field is located in the tax form.
    """
    TOTAL_INCOME = 'total_income'
    ADJUSTED_GROSS_INCOME = 'adjusted_gross_income'
    DEDUCTIONS = 'deductions'
    TAXABLE_INCOME = 'taxable_income'
    TOTAL_TAX = 'total_tax'
    TOTAL_PAYMENTS = 'total_payments'
    OVERPAID = 'overpaid'
    AMOUNT_OWED = "amount_owed"
    
    
    FIELD_CHOICES = [
        (TOTAL_INCOME, 'Total Income'),
        (ADJUSTED_GROSS_INCOME,'Adjusted Gross Income'),
        (DEDUCTIONS, 'Deductions'),
        (TAXABLE_INCOME, 'Taxable Income'),
        (TOTAL_TAX, 'Total Tax'),
        (TOTAL_PAYMENTS, 'Total Payments'),
        (OVERPAID, 'Overpaid'),
        (AMOUNT_OWED, 'Amount Owed')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tax_form = models.ForeignKey(TaxForm, related_name='tax_fields', on_delete=models.CASCADE)
 
    tax_field = models.CharField(
        max_length=50,
        choices=FIELD_CHOICES,
        default=TOTAL_INCOME,
    )
    
    
    instruction_text = models.CharField(max_length=255)
    instruction_matched_pattern = models.CharField(max_length=255)
    


    value_text = models.CharField(max_length=255)
    value_normalized_text = models.CharField(max_length=255)
    value_in_numeric = models.DecimalField(max_digits=10, decimal_places=2)
    value_matched_pattern = models.CharField(max_length=255)


    
    page_number = models.IntegerField(default=-1)
    

