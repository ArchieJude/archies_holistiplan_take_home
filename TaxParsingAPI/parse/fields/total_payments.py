from dataclasses import dataclass, field
from typing import List, Pattern, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase


@dataclass
class TotalPayments(FieldBase):
    """

    Line 33: Add lines 25d, 26, and 32. These are your total payments


    """

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<statement>Add lines 25d, 26, and 32\. These are your total payments)$",
            r"(?P<statement>Add lines \w{2}d, \w{2}, and \w{2}\. These are your total payments)",
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
