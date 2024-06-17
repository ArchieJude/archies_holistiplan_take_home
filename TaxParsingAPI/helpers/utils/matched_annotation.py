from dataclasses import dataclass
from typing import Pattern, Match, Optional
from TaxParsingAPI.helpers.tax_form_helper import OCRPage
from TaxParsingAPI.helpers.utils.annotation import Annotation
import regex as re


@dataclass
class MatchedAnnotation(Annotation):
    """
    Data class for representing a matched OCR annotation.

    This class extends the Annotation class to include additional information about
    the page on which the annotation was found, the match details, the matching pattern,
    and the normalized text.

    Attributes:
        page (Optional[OCRPage]): The OCRPage instance where the annotation was found. Defaults to None.
        page_index (int): The index of the page where the annotation was found. Defaults to -1.
        match (Optional[Match]): The match object containing details of the pattern match. Defaults to None.
        pattern (Pattern): The pattern that matched the text. Defaults to an empty string.
        normalized_text (str): The normalized text with spaces removed. Defaults to an empty string.
    """
    page: Optional[OCRPage] = None
    page_index: int = -1
    match: Optional[Match] = None
    pattern: Pattern = "" # pattern that matched
    normalized_text:str = "" 
    
    def __post_init__(self):
        """
        Post-initialization method to normalize the text.
        """
        self.normalized_text = self._normalize_text()
    
    def _normalize_text(self)->str:
        """
        Normalize the text by removing spaces.

        This method replaces all spaces in the text with nothing.

        Returns:
            str: The normalized text with spaces removed.
        """
        regex = r"[ ]"
        subst = ""
        normalized_text = re.sub(regex, subst, self.text, re.MULTILINE)
        return normalized_text

    @classmethod
    def from_annotation(cls, page: OCRPage, page_index: int, match:Match, pattern:Pattern, annotation: Annotation) -> 'MatchedAnnotation':
        """
        Create a MatchedAnnotation instance from an existing Annotation.

        This class method allows creating a MatchedAnnotation instance using the details from
        an existing Annotation, along with additional information about the page, match, and pattern.

        Args:
            page (OCRPage): The OCRPage instance where the annotation was found.
            page_index (int): The index of the page where the annotation was found.
            match (Match): The match object containing details of the pattern match.
            pattern (str): The pattern that matched the text.
            annotation (Annotation): The original Annotation instance.

        Returns:
            MatchedAnnotation: A new MatchedAnnotation instance with the combined details.
        """
        return cls(
            page=page,
            page_index=page_index,
            match=match,
            pattern=pattern,
            text=annotation.text,
            bbox=annotation.bbox,
            center=annotation.center,
        )