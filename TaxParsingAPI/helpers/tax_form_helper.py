from dataclasses import dataclass, field, asdict
from pathlib import Path
from TaxParsingAPI.helpers.utils.annotation import Annotation
from TaxParsingAPI.helpers.utils.ocr_wrapper import OcrWrapper
from typing import List, Dict
import json
from pdf2image import convert_from_path, convert_from_bytes
from HolistiplanTakeHome.settings import MEDIA_ROOT


@dataclass
class PreprocessTaxForm:
    """
    Data class for preprocessing tax form files.

    This class handles various attributes and methods related to the preprocessing of tax forms,
    including the file path, file bytes, image directories, and OCR data. It sets up
    default directories for images, extracted text, and annotations.

    Attributes:
        file_path (Path): The path to the tax form PDF file.
        file_bytes (bytes): The bytes of the PDF file, if loaded.
        image_directory (Path): The directory where images extracted from the PDF are stored.
        text_from_pdf_directory (Path): The directory where text extracted from the PDF is stored.
        image_file_paths (List[Path]): A list of paths to the image files extracted from the PDF.
        annotations_directory (Path): The directory where annotations related to the PDF are stored.
        ocr_pages (Dict[int, 'OCRPage']): A dictionary mapping page numbers to OCRPage objects containing OCR data.

        base_dir (Path): The base directory for storing tax form related files.
        base_image_directory (Path): The base directory for storing extracted images.
        base_text_from_pdf_directory (Path): The base directory for storing extracted text.
        base_annotations_directory (Path): The base directory for storing annotations.
        base_annotations_over_images_dir (Path): The base directory for storing annotations over images.
        
        
    Methods:
        _get_image_file_paths(self) -> List[Path]:
            Retrieve and sort image file paths from the image directory.
        
        _convert_to_pdf_to_image(self) -> None:
            Convert the PDF file to images and save them in the image directory.
        
        _set_ocr_pages(self) -> List[Dict[int, 'OCRPage']]:
            Set the OCR pages for the tax form.
        
        _ocr_and_save(self, annotation_file_path: Path, image_file_path: Path) -> List[Annotation]:
            Perform OCR on the provided image file and save the annotations to a JSON file.
        
        _save_annotations_over_images(self) -> None:
            Save annotated images to visualize OCR results.
        
        _set_base_directories(self) -> None:
            Set base directories relative to the file path.
        
        _ensure_base_directories_exist(self) -> None:
            Ensure all base directories for extracted data from the PDF exist.
    """

    file_path: Path = None
    file_bytes: bytes = None
    image_directory: Path = None
    text_from_pdf_directory: Path = None
    image_file_paths: List[Path] = field(default_factory=lambda: {})
    annotations_directory: Path = None
    ocr_pages: Dict[int, "OCRPage"] = field(default_factory=lambda: {})

    base_dir: Path = MEDIA_ROOT / "tax_forms"
    base_image_directory: Path = field(init=False, default=base_dir / "images")
    base_text_from_pdf_directory: Path = field(
        init=False, default=base_dir / "text_from_pdf"
    )
    base_annotations_directory: Path = field(init=False, default=base_dir / "annotations")
    base_annotations_over_images_dir: Path = field(
        init=False, default=base_dir / "annotations_over_images"
    )

    def __post_init__(self):

        self._set_base_directories()
        self._ensure_base_directories_exist()

        self.image_directory = self.base_image_directory / self.file_path.stem
        self.text_from_pdf_directory = (
            self.base_text_from_pdf_directory / self.file_path.stem
        )
        self.annotations_directory = self.base_annotations_directory / self.file_path.stem

        self._convert_to_pdf_to_image()

        self.image_file_paths = self._get_image_file_paths()

        self.ocr_pages = self._set_ocr_pages()
        self._save_annotations_over_images()

    def _get_image_file_paths(self) -> List[Path]:
        """
        Retrieve and sort image file paths from the image directory.

        This method retrieves all PNG image file paths from the image directory,
        sorts them based on the numeric value in their filename, and returns the
        sorted list of paths.

        Returns:
            List[Path]: A list of sorted image file paths.
        """
        image_file_paths = list(self.image_directory.glob("*.png"))
        image_file_paths = sorted(
            image_file_paths, key=lambda x: int(x.stem.split("_")[-1])
        )
        return image_file_paths

    def _convert_to_pdf_to_image(self) -> None:
        """
        Convert the PDF file to images and save them in the image directory.

        This method converts each page of the PDF file into a separate image and saves
        them in the image directory. It handles both file paths and file bytes. If the
        image directory does not exist, it is created. Each image is saved with a filename
        indicating the page number.

        Returns:
            None
        """
        # Path to the PDF file
        if self.file_path.exists():
            # Save each page as an image
            if not self.image_directory.exists():
                # Convert PDF to images
                images = convert_from_path(self.file_path)
                self.image_directory.mkdir()

                for i, image in enumerate(images):

                    image_file_path = self.image_directory / f"page_{i + 1}.png"
                    if not image_file_path.exists():
                        image.save(image_file_path, "PNG")

                        print("PDF pages have been converted to images successfully.")

        elif self.file_bytes is not None:
            # Save each page as an image
            if not self.image_directory.exists():
                # Convert PDF to images
                images = convert_from_bytes(self.file_bytes)
                self.image_directory.mkdir()

                for i, image in enumerate(images):

                    image_file_path = self.image_directory / f"page_{i + 1}.png"
                    if not image_file_path.exists():
                        image.save(image_file_path, "PNG")

                        print("PDF pages have been converted to images successfully.")

    def _set_ocr_pages(self) -> List[Dict[int, "OCRPage"]]:
        """
        Set the OCR pages for the tax form.

        This method processes each image file path to generate or load OCR annotations. It checks if the
        annotations directory exists and if not, it creates it. For each image file, it either reads the
        existing annotations from a JSON file or performs OCR, using _ocr_and_save method, to generate and save new annotations.
        The annotations are then added to the OCRPage instances and stored in a dictionary.

        Returns:
            List[Dict[int, 'OCRPage']]: A dictionary mapping page numbers to OCRPage objects containing OCR data and annotations.
        """
        pages: Dict[int, "OCRPage"] = {}
        for page_num, image_file_path in enumerate(self.image_file_paths):
            annotation_file_path = (
                self.annotations_directory / f"{image_file_path.stem}.json"
            )

            if not self.annotations_directory.exists():
                self.annotations_directory.mkdir()
                annotations = self._ocr_and_save(
                    annotation_file_path=annotation_file_path,
                    image_file_path=image_file_path,
                )
                if pages.get(page_num):
                    pages[page_num].annotations += annotations
                else:
                    pages[page_num] = OCRPage(
                        tax_file=self, page_number=page_num, annotations=annotations
                    )
            elif not annotation_file_path.exists():
                annotations = self._ocr_and_save(
                    annotation_file_path=annotation_file_path,
                    image_file_path=image_file_path,
                )
                if pages.get(page_num):
                    pages[page_num].annotations += annotations
                else:
                    pages[page_num] = OCRPage(
                        tax_file=self, page_number=page_num, annotations=annotations
                    )

            else:
                with open(annotation_file_path, "r") as j:

                    json_annotation = json.load(j)
                    for item in json_annotation:
                        if pages.get(page_num):
                            pages[page_num].annotations.append(
                                Annotation(
                                    text=item["text"],
                                    bbox=item["bbox"],
                                    center=item["center"],
                                )
                            )
                        else:
                            pages[page_num] = OCRPage(
                                tax_file=self,
                                page_number=page_num,
                                annotations=[
                                    Annotation(
                                        text=item["text"],
                                        bbox=item["bbox"],
                                        center=item["center"],
                                    )
                                ],
                            )

        return pages

    def _ocr_and_save(
        self, annotation_file_path: Path, image_file_path: Path
    ) -> List[Annotation]:
        """
        Perform OCR on the provided image file and save the annotations to a JSON file.

        This method uses the OcrWrapper to perform OCR on the specified image file. It then
        processes the annotations, converts them to a JSON-serializable format, and saves
        them to the specified annotation file path. Finally, it returns the list of annotations.

        Args:
            annotation_file_path (Path): The path to the JSON file where annotations will be saved.
            image_file_path (Path): The path to the image file on which OCR will be performed.

        Returns:
            List[Annotation]: A list of Annotation objects obtained from the OCR process.
        """
        ocr_wrapper = OcrWrapper(image=str(image_file_path))

        to_save = []
        for annotation in ocr_wrapper.annotations:
            temp = {}
            temp["text"] = annotation.text
            temp["bbox"] = annotation.bbox
            temp["center"] = annotation.center

            to_save.append(temp)

        json_data = json.dumps(to_save, indent=4)

        with open(annotation_file_path, "w") as file:
            file.write(json_data)

        return ocr_wrapper.annotations

    def _save_annotations_over_images(self) -> None:
        """
        Save annotated images to visualize OCR results.

        This method generates images with OCR annotations overlayed on top of the original images.
        It saves these annotated images in a specified directory, annotations_over_images_dir, allowing for easy examination of the OCR results.
        If the directory for saving the annotated images does not exist, it is created.

        Returns:
            None
        """
        annotations_over_images_dir = (
            self.base_annotations_over_images_dir / self.file_path.stem
        )

        if not annotations_over_images_dir.exists():
            annotations_over_images_dir.mkdir()

        for page_num, image_file_path in enumerate(self.image_file_paths):
            annotations_over_images_file_path = (
                annotations_over_images_dir / f"{image_file_path.stem}.png"
            )
            if not annotations_over_images_file_path.exists():
                ocr_wrapper = OcrWrapper(image=str(image_file_path))
                image = ocr_wrapper.ocr_mac.annotate_PIL()
                image.save(annotations_over_images_file_path)

    def _set_base_directories(self)->None:
        """
        Set base directories relative to the file path.

        This method sets up various base directories for storing images, extracted text, 
        annotations, and annotated images. The directories are set relative to the directory
        containing the tax form file.

        Example:
            If self.file_path = ".../tax_forms/test.pdf",
            then base_dir = ".../tax_forms/"

        The following base directories are set:
            - base_image_directory: Directory for storing images.
            - base_text_from_pdf_directory: Directory for storing text extracted from the PDF.
            - base_annotations_directory: Directory for storing annotations.
            - base_annotations_over_images_dir: Directory for storing annotated images.

        Returns:
            None
        """
   
        base_dir = self.file_path.parent
        base_image_directory = base_dir / "images"
        base_text_from_pdf_directory = base_dir / "text_from_pdf"
        base_annotations_directory = base_dir / "annotations"
        base_annotations_over_images_dir = base_dir / "annotations_over_images"

        self.base_dir = base_dir
        self.base_image_directory = base_image_directory
        self.base_text_from_pdf_directory = base_text_from_pdf_directory
        self.base_annotations_directory = base_annotations_directory
        self.base_annotations_over_images_dir = base_annotations_over_images_dir

    def _ensure_base_directories_exist(self):
        """
        Ensure all base directories for extracted data from the PDF exist.

        This method checks if the base directories for storing various types of extracted 
        data from the PDF (images, text, annotations, and annotated images) exist. If any 
        of these directories do not exist, it creates them.

        Directories:
            - base_image_directory: Directory for storing images.
            - base_text_from_pdf_directory: Directory for storing text extracted from the PDF.
            - base_annotations_directory: Directory for storing annotations.
            - base_annotations_over_images_dir: Directory for storing annotated images.

        Returns:
            None
        """
        if not self.base_image_directory.exists():
            self.base_image_directory.mkdir()
        if not self.base_text_from_pdf_directory.exists():
            self.base_text_from_pdf_directory.mkdir()
        if not self.base_annotations_directory.exists():
            self.base_annotations_directory.mkdir()
        if not self.base_annotations_over_images_dir.exists():
            self.base_annotations_over_images_dir.mkdir()


@dataclass
class OCRPage:
    """
    Data class for representing an OCR page of a tax form.

    This class encapsulates the OCR data for a single page of a tax form, including 
    the tax form instance, page number, and a list of annotations.

    Attributes:
        tax_file (PreprocessTaxForm): The instance of the preprocessed tax form.
        page_number (int): The page number of the tax form.
        annotations (List[Annotation]): A list of Annotation objects containing OCR data.

    Methods:
        to_json() -> str:
            Converts the annotations of the OCR page to a JSON string.
    """
    tax_file: PreprocessTaxForm
    page_number: int
    annotations: List[Annotation]

    def to_json(self) -> str:
        temp_annotations = []
        for annotation in self.annotations:
            temp_annotations.append(asdict(annotation))
        return json.dumps(temp_annotations, indent=4)
