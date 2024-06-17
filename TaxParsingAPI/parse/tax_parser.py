from dataclasses import dataclass, field
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm
from TaxParsingAPI.parse.fields.total_income import TotalIncome
from TaxParsingAPI.parse.fields.adjusted_gross_income import AdjustedGrossIncome
from TaxParsingAPI.parse.fields.deductions import Deductions
from TaxParsingAPI.parse.fields.taxable_income import TaxableIncome
from TaxParsingAPI.parse.fields.total_tax import TotalTax
from TaxParsingAPI.parse.fields.total_payments import TotalPayments
from TaxParsingAPI.parse.fields.overpaid import Overpaid
from TaxParsingAPI.parse.fields.amount_owed import AmountOwed

from typing import Optional, get_args, _UnionGenericAlias, Union

"""
TaxParser is an orchestrator of fields
"""
 
@dataclass
class TaxParser:
    """
    Orchestrator of all the tax field classes. In the future, this class
    could reduce the boundary, or the search space of a tax field by using the
    previous tax field's boundary space (recursively) since tax fields appear in 
    order, natural reading style.

    Attributes:
        preprocessed_tax_form (PreprocessTaxForm): The preprocessed tax form data.
        total_income (Optional[TotalIncome]): Parsed total income data, initialized in __post_init__.
        adjusted_gross_income (Optional[AdjustedGrossIncome]): Parsed adjusted gross income data, initialized in __post_init__.
        deductions (Optional[Deductions]): Parsed deductions data, initialized in __post_init__.
        taxable_income (Optional[TaxableIncome]): Parsed taxable income data, initialized in __post_init__.
        total_tax (Optional[TotalTax]): Parsed total tax data, initialized in __post_init__.
        total_payments (Optional[TotalPayments]): Parsed total payments data, initialized in __post_init__.
        overpaid (Optional[Overpaid]): Parsed overpaid amount data, initialized in __post_init__.
        amount_owed (Optional[AmountOwed]): Parsed amount owed data, initialized in __post_init__.
    """
    preprocessed_tax_form: PreprocessTaxForm
    total_income: Optional[TotalIncome] = field(init=False,default = None)
    adjusted_gross_income: Optional[AdjustedGrossIncome] = field(init=False,default=None)
    deductions: Optional[Deductions] = field(init=False,default=None)
    taxable_income: Optional[TaxableIncome] = field(init=False,default=None)
    total_tax: Optional[TotalTax] = field(init=False,default=None)
    total_payments: Optional[TotalPayments] = field(init=False,default=None)
    overpaid: Optional[Overpaid] = field(init=False,default=None)
    amount_owed: Optional[AmountOwed] = field(init=False,default=None)


    
    def __post_init__(self):
        self.total_income = TotalIncome(preprocessed_tax_form=self.preprocessed_tax_form)
        self.adjusted_gross_income = AdjustedGrossIncome(preprocessed_tax_form=self.preprocessed_tax_form)
        self.deductions = Deductions(preprocessed_tax_form=self.preprocessed_tax_form)
        self.taxable_income = TaxableIncome(preprocessed_tax_form=self.preprocessed_tax_form)
        self.total_tax = TotalTax(preprocessed_tax_form=self.preprocessed_tax_form)
        self.total_payments = TotalPayments(preprocessed_tax_form=self.preprocessed_tax_form)
        self.overpaid = Overpaid(preprocessed_tax_form=self.preprocessed_tax_form)
        self.amount_owed = AmountOwed(preprocessed_tax_form=self.preprocessed_tax_form)
    

    @classmethod
    def get_field_type(cls, field: str) -> Union[TotalIncome,AdjustedGrossIncome]:
        """
        Get the type of a given field in the TaxParser class.

        Args:
            field (str): The field name to get the type for.

        Returns:
            type: The type of the field.

        Raises:
            AttributeError: If the field is not a valid attribute of the class.
        """
        if field in cls.__annotations__:
            # Check if the field_type is an Optional (a _GenericAlias)
            field_type = cls.__annotations__[field]
            if isinstance(field_type, _UnionGenericAlias) and field_type.__origin__ is Union:
                # Extract the first argument from the Optional[...]
                return get_args(field_type)[0]
            return field_type
        
        else:
            raise AttributeError(f"{field} is not a valid attribute of {cls.__name__}")
