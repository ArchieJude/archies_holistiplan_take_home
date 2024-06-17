from dataclasses import dataclass, field
from ocrmac.ocrmac import OCR
from typing import List, Tuple, Union
from PIL.Image import Image
from typing import  List
from TaxParsingAPI.helpers.utils.annotation import Annotation

@dataclass()
class OcrWrapper:
    """
    Wrapper class for handling OCR processing on images.

    This class uses the OCR class to perform OCR on the provided image and stores the 
    resulting annotations. It initializes the OCR object and processes the annotations 
    to set their bounding boxes and centers.

    Attributes:
        image (Union[Image, str]): The image or the path to the image on which OCR is performed.
        ocr_mac (OCR): The OCR object that performs the recognition. Defaults to None.
        annotations (List[Annotation]): A list of Annotation objects containing OCR data.

    Methods:
        __post_init__():
            Initializes the OCR object and sets the annotations.
        
        _set_annotation(cls, annotations):
            Converts raw OCR output into a list of Annotation objects.
        
        get_center(cls, box):
            Calculates the center coordinates of a bounding box.
    """
    image: Union[Image, str]
    ocr_mac: OCR = None
    annotations: List[Annotation] = field(
        default_factory=list
    )

    def __post_init__(self):
        """
        Initialize the OCR object and set the annotations.

        This method initializes the OCR object with the provided image and sets the annotations
        by processing the output from the OCR recognition.
        """
        self.ocr_mac = OCR(image=self.image)
        self.annotations = self._set_annotation(
            annotations=self.ocr_mac.recognize(px=True)
        )        
     

    @classmethod
    def _set_annotation(cls, annotations)->List[Annotation]:
        """
        Convert raw OCR output into a list of Annotation objects.

        This method processes the raw OCR output to create a list of Annotation objects, 
        setting the text, bounding box, and center coordinates.

        Args:
            annotations: The raw OCR output containing text, confidence, and bounding box coordinates.

        Returns:
            List[Annotation]: A list of processed Annotation objects.
        """
        return [Annotation(text=text, bbox=bbox, center=cls.get_center(bbox)) for text, _, bbox in annotations]

     
    @classmethod
    def get_center(cls, box)->Tuple[float, float]:
        """
        Calculate the center coordinates of a bounding box.

        This method calculates the center coordinates (x, y) of the provided bounding box.

        Args:
            box (Tuple[float, float, float, float]): The bounding box coordinates in the format (x_min, y_min, x_max, y_max).

        Returns:
            Tuple[float, float]: The center coordinates of the bounding box.
        """
        x1, y1, x2, y2 = box
        return (x1 + x2) / 2, (y1 + y2) / 2
