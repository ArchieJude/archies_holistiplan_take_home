from dataclasses import dataclass, field

from typing import List, Pattern, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase


@dataclass
class TaxableIncome(FieldBase):
    """

    Line 15: Taxable Income

    7.pdf
        Subtract line 14 from line 11. If zero or less, enter -0-. This is your taxable income

        192,482.

            8a.pdf


    """

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<statement>Subtract line 14 from line 11. If zero or less, enter -0-. This is your taxable income)$",
            r"^(?P<statement>Subtract line 14 from line 11\.[ ]*(If zero or less, enter[ ]*-0-\.)?[ ]*(This is your taxable income\.?)?)",
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
