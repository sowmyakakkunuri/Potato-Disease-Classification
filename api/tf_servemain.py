from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
from PIL import Image
from io import BytesIO
import uvicorn
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

endpoint = "http://localhost:8501/v1/models/potatoes_model:predict"

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow the React frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Can restrict allowed methods
    allow_headers=["*"],  # Can restrict allowed headers
)



# Load the model as a TFSMLayer


# Update with your actual class names
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.get("/ping")
async def ping():
    return {"message": "Hello from server"}
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        json_data = {
            "instances" : img_batch.tolist()
        }
        requests.post(endpoint,json=json_data)

        response = requests.post(endpoint, json= json_data)

        prediction = np.array(response.json()["predictions"][0])
        predicted_class = CLASS_NAMES[np.argmax(prediction)]
        confidence = np.max(prediction)
        return {
            "class":predicted_class,
            "confidence":confidence
        }

        # Perform prediction using the TFSMLayer
        # predictions = MODEL(img_batch)
        #
        # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        # confidence = np.max(predictions[0])
        #
        # return {
        #     'class': predicted_class,
        #     'confidence': float(confidence)
        # }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

