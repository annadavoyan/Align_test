import easyocr
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the OCR model
reader = easyocr.Reader(['en'])

def predict_employee_id(image_path):
    logger.info(f"Processing image at {image_path}")
    try:
        # Perform OCR on the image
        result = reader.readtext(image_path)
        logger.info(f"OCR result: {result}")
        
        # Extract the employee ID from the result
        for (bbox, text, prob) in result:
            if prob > 0.5:  # Confidence threshold
                return text.replace('-', '').strip()
        return None
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise
