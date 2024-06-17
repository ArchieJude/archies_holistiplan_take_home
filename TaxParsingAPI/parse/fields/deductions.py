from dataclasses import dataclass, field
import regex as re
from typing import List, Pattern, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase


@dataclass
class Deductions(FieldBase):
    """

    Line 12: Deductions

    7.pdf
        Standard deduction or itemized deductions (from Schedule A)

        27,700.

    """

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<statement>Standard deduction or itemized deductions \(from Schedule A\))$",
            r"(?P<statement>Standard deduction or itemized deductions \(from Schedule A\))",
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
