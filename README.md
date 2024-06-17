# TaxForm Processing API

## DEMO
https://streamable.com/t8pnc8

## Overview

The TaxForm Processing API is designed to handle the upload, processing, and analysis of tax forms. It includes features such as performing OCR on form images, extracting fields from tax forms, and storing the processed data in a structured format.

## Features

- Upload tax forms in PDF format.
- Perform OCR on tax form images.
- Extract and store various tax fields from the forms.
- Provide API endpoints for managing and retrieving tax forms and their fields.
- Calculate amounts owed or overpaid based on extracted data.

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django Rest Framework
- FPDF (for creating PDF Files)
- ocrmac (for OCR functionality)
- PIL (Pillow)
- pytest
- pdf2image (for converting PDF to image)
  - **brew install poppler** for pdf2image
- regex
- pytest_django
- djangorestframework-simplejwt


### Steps

1. Clone the repository:
    ```bash

    git clone https://github.com/ArchieJude/archies_holistiplan_take_home.git
    ```
2. Navigate into the rep

    ```bash

    cd archies_holistiplan_take_home
    ```
3. Export Django project settings:
    ```bash

    export DJANGO_SETTINGS_MODULE=HolistiplanTakeHome.settings
    ```
4. Create and activate a virtual environment:
    ```bash

    python3 -m venv env_archies_holistiplan_take_home
    source env_archies_holistiplan_take_home/bin/activate
    ```

5. Install the required packages:
    ```bash

    brew install poppler
    pip install -r requirements.txt
    ```

6. Set up the database:
    ```bash

    python manage.py makemigrations
    python manage.py migrate
    ```

7. Run pytest
   ```bash
   
   pytest
   ```
   **Out of 72, 69 should pass, 3 failing tests are due to problamatic pdf: 2023senior.pdf**

8. Set env vars for superuser and create superuser:

    ```bash
    export DJANGO_SUPERUSER_USERNAME='admin'
    export DJANGO_SUPERUSER_PASSWORD='admin'
    export DJANGO_SUPERUSER_EMAIL='admin@example.com'


    python manage.py createsuperuser --noinput
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

### Example Usage

To upload a tax form via browser

1. Navigate to http://127.0.0.1:8000/api/tax-forms/
2. Click the **Log In** button on the top right corner
3. Enter the default credentials, username:admin password:admin
4. Scroll all the way down to the POST section: click on the file upload button **Choose File** to upload PDF tax form document and then click on the **POST** button. It should take min or two because it is preprocessing the tax form by OCR-ing and other misc preprocessing steps.
5. You should be redirected to a new page where you can see the upload tax form's extracted tax fields
   
### API Endpoints

- **Upload Tax Form:**
    - `POST /api/tax-forms/`
    - Upload a PDF tax form to be processed.

- **Retrieve Tax Forms:**
    - `GET /api/tax-forms/`
    - Retrieve a list of all uploaded tax forms.

- **Retrieve Specific Tax Form:**
    - `GET /api/tax-forms/{id}/`
    - Retrieve details of a specific tax form, including extracted fields.


## Project Structure
```
HolistiplanTakeHome/
TaxParsingAPI/
├── helpers/
│   └── utils/
│       ├── annotation.py
│       ├── matched_annotation.py
│       ├── ocr_wrapper.py
│       └── tax_form_helper.py
├── migrations/
├── parse/
│   └── fields/
│       ├── adjusted_gross_income.py
│       ├── amount_owed.py
│       ├── deductions.py
│       ├── field_base.py
│       ├── overpaid.py
│       ├── taxable_income.py
│       ├── total_income.py
│       ├── total_payments.py
│       ├── total_tax.py
│       └── tax_parser.py
├── tax_forms/
├── tests/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
└── urls.py
```

## Key Classes and Methods

### Preprocessing

#### `PreprocessTaxForm` 

- Data class for preprocessing tax form files. 
- Orchestrates various preprocessing attributes and methods such as OCR-ing files, and setting up directories for storing file related images, texts, and imagine annotations

### Parsing 

#### `TaxParser` 

- Data class that encapsulates tax field parsing data classes. 
- Orchestrates all the tax field extractions through their respective tax field data class defined in `TaxParsingAPI/parse/fields`
  
#### `FieldBase` 

- A base data class for tax field, where all tax fields derive from.
- Holds methods that extracts tax field instruction statement and value through the use of regex and positional filtering of boundary boxes.
  
### Models 
#### `TaxForm` Model

- Represents a tax form.
- Stores the file, upload timestamp, and methods to retrieve and calculate fields.

#### `TaxField` Model

- Represents individual fields within a tax form.
- Stores field type, values, and page information.

### Serializers 
#### `TaxFormSerializer`

- Serializer for the `TaxForm` model.
- Custom methods for handling nested tax fields and preprocessing.

## The Approach

- The extraction logic relies on two components: text and the text's boundary box (x,y coordinate of where it is located in the pdf file)
  - Use regex to match text: 
    - for example:
      - tax field instruction: Subtract line 14 from line 11. If zero or less, enter -0-. This is your taxable income
      - tax field value: 192,482.
  - Use boundary box to reduce search space:
    - Since the tax field value always appear after tax field instruction in natural reading order, we can exclude values that appear elsewhere like before tax field instruction.
  
## Problems 
#### PDF file with incoherent values, `2023senior.pdf`
- Because the values for this pdf file is made up, my main extraction strategy for dealing with faulty extractions, calculating the expected value based on dependent extracted fields failed. For example, overpaid and amount owed fields are calculated by two tax fields: total tax and total payments. Ideas on how to solve for that particular complication, log it because it needs a manual review, if the checks and balances do not equate there is something seriously wrong: either the tax document is not filled out correctly or extraction logic is flawed.


## Contributing

Contributions are NOT welcomed.

## License

This project is licensed under a Proprietary License.

**Proprietary License**: All rights reserved. You may not use, distribute, or modify this code without explicit permission from the author.


