from dataclasses import dataclass, field
from typing import List, Pattern, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase


@dataclass
class AdjustedGrossIncome(FieldBase):
    """

    Line 11: Adjusted Gross Income
    ***adjusted_gross_income = total_income - line_10 (Adjustments to income from Schedule 1, line 26)

    7.pdf
        Subtract line 10 from line 9. This is your adjusted gross income

        220,183.

    """

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<statement>Subtract line 10 from line 9\. This is your adjusted gross income)$",
            r"(?P<statement>Subtract line 10 from line 9\. This is your adjusted gross income)",
        ]
    )
    value_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<value>\d+([\,]\d*)*\.)$",
            r"^(?P<value>\d{2,}([\,]\d*)+\.?)$",
            r"^(?P<value>\d{3})",
            r"^(?P<value>[4-9][0-9])",
            r"^(?P<value>\d{2}\.?)",
            r"(?P<value>\d+)",
        ]
    )
