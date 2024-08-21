# from fastapi import FastAPI, File, UploadFile, HTTPException
# import uvicorn
# import numpy as np
# from PIL import Image
# from io import BytesIO
# from tensorflow.keras.layers import TFSMLayer
#
# app = FastAPI()
#
# # Load the model using TFSMLayer
# MODEL = TFSMLayer("../saved_models/1", call_endpoint='serving_default')  # Update this path
# CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]  # Update class names as needed
#
#
# @app.get("/ping")
# async def ping():
#     return {"message": "Hello from server"}
#
#
# def read_file_as_image(data) -> np.ndarray:
#     try:
#         image = Image.open(BytesIO(data)).convert("RGB")  # Ensure image is in RGB format
#         image = np.array(image)
#         image = image.astype("float32") / 255.0  # Normalize pixel values to [0, 1]
#         return image
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
#
#
# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         # Read and preprocess the image
#         image = read_file_as_image(await file.read())
#         img_batch = np.expand_dims(image, 0)
#
#         # Make prediction
#         prediction = MODEL(img_batch)
#         predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
#         confidence = np.max(prediction[0])
#
#         return {
#             'class': predicted_class,
#             'confidence': float(confidence)
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)


from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
from PIL import Image
from io import BytesIO
import uvicorn
# import tensorflow as tf
from tensorflow.keras.layers import TFSMLayer
import os
app = FastAPI()

model_directory = "../saved_models"
model_version = max([int(i) for i in os.listdir(model_directory)])
model_path = os.path.join(model_directory, str(model_version))

# Load the model as a TFSMLayer
MODEL = TFSMLayer(model_path, call_endpoint='serving_default')

# Update with your actual class names
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        # Perform prediction using the TFSMLayer
        predictions = MODEL(img_batch)

        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])

        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

