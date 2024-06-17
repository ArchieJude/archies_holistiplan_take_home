from dataclasses import dataclass, field
from typing import List, Pattern, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase


@dataclass
class TotalTax(FieldBase):
    """

    Line 24: total tax

    7.pdf
        Add lines 22 and 23. This is your total tax
        26,825.

    """

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<statement>Add lines 22 and 23. This is your total tax)$",
            r"(?P<statement>Add lines \w{2} and \w{2}. This is your total tax)",
        ]
    )
    value_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<value>\d+([\,]\d*)*\.)$",
            r"^(?P<value>\d{2,}([\,]\d*)+\.?)$",
            r"^(?P<value>\d+([\,] *\d*)+\.?)$",
            r"^(?P<value>\d{3})",
            r"^(?P<value>[4-9][0-9])",
            r"^(?P<value>\d{2}\.?)",
            r"(?P<value>\d+)",
        ]
    )
