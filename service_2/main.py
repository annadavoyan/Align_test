from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
from service_2.ocr_model import predict_employee_id
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/image")
async def process_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded image
        image_path = f"uploads/{file.filename}"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Log the path of the saved image
        logger.info(f"Image saved to {image_path}")

        # Predict employee ID using the OCR model
        employee_id = predict_employee_id(image_path)

        # Log the result of the OCR
        logger.info(f"OCR Result: {employee_id}")

        if not employee_id:
            raise HTTPException(status_code=400, detail="Could not read employee ID from image")
        
        # Format the employee ID to a numeric format if needed
        formatted_employee_id = ''.join(filter(str.isdigit, employee_id))

        return {"employee_id": formatted_employee_id}

    except Exception as e:
        # Log the exception
        logger.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
