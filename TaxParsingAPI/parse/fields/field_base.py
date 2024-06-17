"""
provides common functionalities among fields
"""

from dataclasses import dataclass, field
from TaxParsingAPI.helpers.tax_form_helper import PreprocessTaxForm, OCRPage
import regex as re
from typing import List, Pattern, Dict, Optional, ClassVar
from TaxParsingAPI.helpers.utils.annotation import Annotation
from TaxParsingAPI.helpers.utils.matched_annotation import MatchedAnnotation


@dataclass
class FieldBase:
    """
    Base class for tax field classes, hanldes OCR data extraction from tax forms.

    This class is responsible for finding and setting OCR data for statements (tax field instruction) and
    values (respective tax field instruction value) from preprocessed tax forms. It uses predefined patterns,
    sorted in descending priority, to match and extract the relevant information.

    Attributes:
        preprocessed_tax_form (PreprocessTaxForm): The preprocessed tax form data.
        statement_ocr (MatchedAnnotation): The OCR data for the statement text (tax field instruction).
        value_ocr (MatchedAnnotation): The OCR data for the value text (value of corresponding tax field instruction).
        statement_patterns (ClassVar[List[Pattern]]): The list of regex patterns (in order of descending priority) to match statements.
        value_patterns (ClassVar[List[Pattern]]): The list of regex patterns (in order of descending priority to match values.
    """

    preprocessed_tax_form: PreprocessTaxForm

    statement_ocr: MatchedAnnotation = field(default_factory=MatchedAnnotation)
    value_ocr: MatchedAnnotation = field(default_factory=MatchedAnnotation)

    statement_patterns: ClassVar[List[Pattern]] = field(default=[])  # priority queue
    value_patterns: ClassVar[List[Pattern]] = field(default=[])

    def __post_init__(self):
        """
        Post-initialization method to set OCR data for statements and values.
        """
        self.statement_ocr = self.find_and_set_statement_ocr()
        self.value_ocr = self.find_and_set_value_ocr_page()

    def find_and_set_statement_ocr(self) -> MatchedAnnotation:
        """
        Find and set the OCR data for the statement text (tax field instruction).

        This method searches through the OCR pages and annotations to find a match
        for the statement using the predefined statement patterns. Returns the first match.

        Returns:
            MatchedAnnotation: The matched annotation for the statement text.
        """
        for _, page in self.preprocessed_tax_form.ocr_pages.items():
            for statement_pattern in self.statement_patterns:
                for page_index, annotation in enumerate(page.annotations):
                    statement_match = re.search(
                        statement_pattern, annotation.text, re.MULTILINE
                    )
                    if statement_match:
                        return MatchedAnnotation.from_annotation(
                            page=page,
                            page_index=page_index,
                            match=statement_match,
                            pattern=statement_pattern,
                            annotation=annotation,
                        )
        return MatchedAnnotation(
            page=OCRPage(
                tax_file=self.preprocessed_tax_form.file_path,
                page_number=-1,
                annotations=[],
            )
        )

    def find_and_set_value_ocr_page(self) -> MatchedAnnotation:
        """
        Find and set the OCR data for the value text (value of corresponding tax field instruction).

        This method searches for the value text corresponding to the statement. The value
        is typically found to the right of the statement within the same line. Thus a filtering
        function is used to filter out/disgard annotations that are not within the reasonable boundary.

        Returns:
            MatchedAnnotation: The matched annotation for the value text.
        """

        def filter_annotations(
            statement: MatchedAnnotation, annotations: List[Annotation]
        ) -> Dict[int, Annotation]:
            filtered_annotations: Dict[int, Annotation] = {}
            for page_index, annotation in enumerate(annotations):
                if statement.bbox[1] <= annotation.center[1] <= statement.bbox[3]:
                    filtered_annotations[page_index] = annotation

            return filtered_annotations

        # the corresponding value should be on the same page as the statement

        annotations = self.statement_ocr.page.annotations[
            self.statement_ocr.page_index + 1 :
        ]
        filtered_annotations = filter_annotations(
            statement=self.statement_ocr, annotations=annotations
        )

        for value_pattern in self.value_patterns:
            for page_index, annotation in filtered_annotations.items():
                value_match = re.search(value_pattern, annotation.text, re.MULTILINE)
                if value_match:

                    return MatchedAnnotation.from_annotation(
                        page=self.statement_ocr.page,
                        page_index=page_index,
                        match=value_match,
                        pattern=value_pattern,
                        annotation=annotation,
                    )

        return MatchedAnnotation(page=self.statement_ocr.page)

    @classmethod
    def to_int(cls, text) -> int:
        """
        Convert text to an integer by removing spaces, commas, and trailing dots.

        Args:
            text (str): The text to convert.

        Returns:
            int: The converted integer value. Returns 0 if conversion fails.
        """
        space_and_comma_regex = r"[ \,]"
        subst = ""
        normalized_text = re.sub(space_and_comma_regex, subst, text, re.MULTILINE)

        ending_dot_regex = r"[\.]$"
        normalized_text = re.sub(ending_dot_regex, subst, normalized_text, re.MULTILINE)

        normalized_text_to_int = 0
        try:
            normalized_text_to_int = int(normalized_text)
        except ValueError:
            print(f"Error: '{normalized_text}' is not a valid integer.")
        except TypeError:
            print("Error: The input provided is not a string or a number.")
        return normalized_text_to_int
