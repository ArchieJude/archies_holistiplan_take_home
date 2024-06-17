from dataclasses import dataclass, field
import regex as re
from typing import List, Pattern, Optional, ClassVar

from TaxParsingAPI.parse.fields.field_base import FieldBase
from TaxParsingAPI.parse.fields.total_tax import TotalTax
from TaxParsingAPI.parse.fields.total_payments import TotalPayments


@dataclass
class Overpaid(FieldBase):
    """

    Line 34: Overpaid (If blank then 0)

    7.pdf

        If line 33 is more than line 24, subtract line 24 from line 33. This is the amount you overpaid

        7,469.

    """

    total_tax: Optional[TotalTax] = None
    total_payments: Optional[TotalPayments] = None

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"(?P<statement>If line 33 is more than line 24, subtract line 24 from line 33\. This is the amount you overpaid)",
            r"(?P<statement>If line 33 is more than line 24, subtract line 24 from line 33\.[ ]*(This is the amount you overpaid)?)",
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
        Calculate the overpaid amount based on total tax and total payments extractions.

        This method calculates the overpaid amount by comparing the total payments and total tax.
        If total payments exceed total tax, the difference is returned as the calculated value.
        If not, the calculated value is set to 0.

        Returns:
            Optional[int]: The calculated overpaid amount. Returns None if the calculation cannot be performed.
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

            if total_payments_int > total_tax_int:
                calculated_value = total_payments_int - total_tax_int
            else:
                calculated_value = 0

            return calculated_value
