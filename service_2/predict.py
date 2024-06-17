import easyocr
import sys

def predict_employee_id(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    
    for (bbox, text, prob) in result:
        if prob > 0.5:
            return text.replace('-', '').strip()
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    employee_id = predict_employee_id(image_path)
    if employee_id:
        print(f"Predicted Employee ID: {employee_id}")
    else:
        print("Could not read employee ID from image")
