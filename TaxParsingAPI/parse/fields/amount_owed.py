from dataclasses import dataclass, field
from typing import List, Pattern, Optional, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase

from TaxParsingAPI.parse.fields.total_tax import TotalTax
from TaxParsingAPI.parse.fields.total_payments import TotalPayments


@dataclass
class AmountOwed(FieldBase):
    """
    Line 37: Amount Owed (If blank then 0)

    7.pdf
        Subtract line 33 from line 24. This is the amount you owe.
        For details on how to pay, go to www.irs.gov/Payments or see instructions
    """

    total_tax: Optional[TotalTax] = None
    total_payments: Optional[TotalPayments] = None

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"(?P<statement>Subtract line 33 from line 24\. This is the amount you owe\.)",
        ]
    )
    value_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<value>\d+([\,]\d*)*\.)$",
            r"^(?P<value>\d{2,}([\,]\d*)+\.?)$",
            r"^(?P<value>\d+([\,] *\d*)+\.?)$",
            r"^(?P<value>\d+([\,\.] *\d*)+\.?)$",
            r"^(?P<value>\d{3})",
            r"^(?P<value>[4-9][0-9])",
        ]
    )

    calculated_value: int = None

    def __post_init__(self):
        super().__post_init__()
        self.calculated_value = self._set_calculated_value()

    def _set_calculated_value(self) -> Optional[int]:
        """
        Calculate the owed amount based on total tax and total payments extractions.

        This method calculates the amount owed by comparing the total tax and total payments.
        The calculated value is the difference between total tax and total payments. If the
        calculated value is negative, it is set to 0.

        Returns:
            Optional[int]: The calculated owed amount. Returns None if the calculation cannot be performed.
        """
        if self.total_tax is None:
            self.total_tax = TotalTax(preprocessed_tax_form=self.preprocessed_tax_form)
        if self.total_payments is None:
            self.total_payments = TotalPayments(
                preprocessed_tax_form=self.preprocessed_tax_form
            )

        if (
            self.total_tax.value_ocr is not None
            and self.total_payments.value_ocr is not None
        ):
            total_payments_int = self.to_int(text=self.total_payments.value_ocr.text)
            total_tax_int = self.to_int(text=self.total_tax.value_ocr.text)

            calculated_value = total_tax_int - total_payments_int
            if calculated_value < 0:
                calculated_value = 0
            return calculated_value
