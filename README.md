# Patient Form OCR Extraction

This project extracts text from patient forms using Optical Character Recognition (OCR) with Tesseract, processes the extracted data, and stores it in a MySQL database.

## Features

- Extracts text from images using Tesseract OCR
- Preprocesses images for better OCR accuracy
- Parses structured data from extracted text
- Saves extracted data as a JSON file
- Stores structured data in a MySQL database

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- OpenCV (`cv2`)
- Tesseract OCR
- MySQL Server
- Required Python Libraries:
  ```sh
  pip install opencv-python pytesseract mysql-connector-python psycopg2
  ```

## Setup

### 1. Install and Configure Tesseract OCR

Download and install Tesseract OCR from [here](https://github.com/UB-Mannheim/tesseract/wiki). Update the Tesseract executable path in `setup_tesseract()` function:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### 2. Configure MySQL Database

Create a MySQL database and required tables:

```sql
CREATE DATABASE patient_data;
USE patient_data;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    dob DATE
);

CREATE TABLE forms_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    form_json JSON,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

Update the database credentials in `connect_db()` function if necessary.

### 3. Clone the Repository

```sh
git clone https://github.com/Suryapag/patient-form-ocr.git
cd patient-form-ocr
```

### 4. Run the Script

Execute the following command:

```sh
python script.py
```

### 5. Follow the Prompts

- Enter the image path
- Extract and display the text
- Save the extracted data as JSON
- Optionally store the data in the database

### 6. Verify the Stored Data

To verify the stored data in MySQL:

```sql
SELECT * FROM patients;
SELECT * FROM forms_data;
```

## Example Output

Extracted JSON:

```json
{
    "patient_name": "sutya",
    "dob": "01/01/1980",
    "date": "12/02/2024",
    "difficulty_ratings": {
        "bending": 3,
        "putting_on_shoes": 4,
        "sleeping": 2
    }
}
```

## License

This project is open-source and available under the MIT License.

## Author

[P.A. Surya](https://github.com/Suryapag)

