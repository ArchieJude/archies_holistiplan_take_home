from dataclasses import dataclass, field
from typing import List, Pattern, ClassVar
from TaxParsingAPI.parse.fields.field_base import FieldBase


@dataclass
class TotalIncome(FieldBase):
    """

    Line 9: Total Income

    7.pdf
        Add lines 1z, 2b, 3b, 4b, 5b, 6b, 7, and 8. This is your total income

        220,640.

    """

    statement_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<statement>(Add)[ ]*(lines)[ ]*(1z)[ \,\.]*(2b)[ \,\.]*(3b)[ \,\.]*(4b)[ \,\.]*(5b)[ \,\.]*(6b)[ \,\.]*(7)[ \,\.]*(and)[ \,\.]*(8)[ \,\.]*(This)[ ]*(is)[ ]*(your)[ ]*(total)[ ]*(income)[ ]*\.?)$",
            r"^(?P<statement>(Add)[ ]*(lines)[ ]*(\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*(7)[ \,\.]*(and)[ \,\.]*(8))[ \,\.]*(This)[ ]*(is)[ ]*(your)[ ]*(total)[ ]*(income)[ ]*\.?)$",
            r"(?P<statement>(Add)[ ]*(lines)[ ]*(\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*(7)[ \,\.]*(and)[ \,\.]*(8))[ \,\.]*(This)[ ]*(is)[ ]*(your)[ ]*(total)[ ]*(income)[ ]*\.?)$",
            r"(?P<statement>(Add)[ ]*(lines)[ ]*(\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*\w{2}[ \,\.]*(7)[ \,\.]*(and)[ \,\.]*(8))[ \,\.]*(This)[ ]*(is)[ ]*(your)[ ]*(total)[ ]*(income)[ ]*\.?)",
        ]
    )
    value_patterns: ClassVar[List[Pattern]] = field(
        default=[
            r"^(?P<value>\d+([\,]\d*)*\.)$",
            r"^(?P<value>\d{2,}([\,]\d*)*\.?)$",
            r"^(?P<value>\d+([\,]\d*)*\.?)$",
        ]
    )
