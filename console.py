import os
import cv2
import pytesseract
import json
import psycopg2
import re
import mysql.connector

def connect_db(user, password, host, database):
    """Connect to MySQL database"""
    return mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )


def setup_tesseract():
    # Set the correct path to Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Preprocess the image for better OCR accuracy"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(image_path):
    """Extract text from the image using OCR"""
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image)
    print(text)
    return text

def extract_data(text):
    """Extract structured data from OCR text"""
    data = {
        "patient_name": re.search(r'Patient Name\s*:\s*(\w+)', text, re.IGNORECASE).group(1) if re.search(r'Patient Name\s*:\s*(\w+)', text, re.IGNORECASE) else "Unknown",
        "dob": re.search(r'DOB:\s*(\d{2}/\d{2}/\d{4})', text).group(1) if re.search(r'DOB:\s*(\d{2}/\d{2}/\d{4})', text) else "Unknown",
        "date": re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text).group(1) if re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text) else "Unknown",
        "difficulty_ratings": {
            "bending": int(re.search(r'Bending or Stooping:\s*(\d+)', text, re.IGNORECASE).group(1)) if re.search(r'Bending or Stooping:\s*(\d+)', text, re.IGNORECASE) else 0,
            "putting_on_shoes": int(re.search(r'Putting on shoes:\s*(\d+)', text, re.IGNORECASE).group(1)) if re.search(r'Putting on shoes:\s*(\d+)', text, re.IGNORECASE) else 0,
            "sleeping": int(re.search(r'Sleeping:\s*(\d+)', text, re.IGNORECASE).group(1)) if re.search(r'Sleeping:\s*(\d+)', text, re.IGNORECASE) else 0,
        }
    }
    return data

def save_json_to_file(data):
    """Save extracted JSON data to a file"""
    save_path = input("Enter the location to save the JSON file (including filename.json): ")

    # Ensure the user provided a filename
    if not save_path.endswith(".json"):
        print("Error: Please provide a valid JSON file name (e.g., output.json)")
        return

    # Extract directory from the given path
    save_dir = os.path.dirname(save_path)

    # If the directory doesn't exist, create it
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the JSON file
    with open(save_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"JSON data saved at {save_path}")

def connect_db():
    """Connect to MySQL database"""
    return mysql.connector.connect(
        user="root",
        password="9092",
        host="127.0.0.1",  # Correct host
        port=3306,
        database="patient_data"
    )

def store_data_in_db(data):
    """Store extracted JSON data in PostgreSQL database"""
    conn = connect_db()
    cursor = conn.cursor()
    # Ensure 'dob' is a valid date, otherwise store NULL
    dob_value = data["dob"] if data["dob"] not in ["Unknown", "", None] else "1970-01-01"

    cursor.execute("INSERT INTO patients (name, dob) VALUES (%s, %s);",
               (data["patient_name"], dob_value))

    patient_id = cursor.lastrowid  

    cursor.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s);", 
               (patient_id, json.dumps(data)))

    conn.commit()
    cursor.close()
    conn.close()

def main():
    setup_tesseract()
    print("\n===== Patient Form OCR Extraction =====")
    image_path = input("Enter the path to the image file: ")
    
    if not os.path.exists(image_path):
        print("Error: File not found!")
        return
    
    print("Processing OCR... Please wait...")
    extracted_text = extract_text(image_path)
    extracted_data = extract_data(extracted_text)
    
    print("\nExtracted JSON Data:")
    print(json.dumps(extracted_data, indent=4))
    
    save_json_to_file(extracted_data)
    
    store = input("Do you want to store this data in the database? (yes/no): ")
    if store.lower() == "yes":
        store_data_in_db(extracted_data)
        print("Data successfully stored in the database!")
    else:
        print("Data not stored.")

if __name__ == "__main__":
    main()
