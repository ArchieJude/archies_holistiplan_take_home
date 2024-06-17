from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Annotation:
    """
    Data class for representing an OCR annotation.

    This class encapsulates the details of an OCR annotation, including the recognized text,
    the bounding box coordinates, and the center coordinates.

    Attributes:
        text (str): The recognized text from the OCR process. Defaults to an empty string.
        bbox (Tuple[float, float, float, float]): The bounding box coordinates of the recognized text
                                                  in the format (x_min, y_min, x_max, y_max). Defaults to (-1, -1, -1, -1).
        center (Tuple[float, float]): The center coordinates of the bounding box. Defaults to (-1, -1).
    """
    text: str = ""
    bbox: Tuple[float, float, float, float] = field(default_factory=lambda: [-1,-1,-1,-1])
    center: Tuple[float, float] = field(default_factory=lambda: [-1,-1])

