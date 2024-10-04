from fastapi import FastAPI
from datetime import datetime
import json
import base64
import os
import uvicorn

app1 = FastAPI()

# Configuration for the server and image directory
config = {
    "Server": {
        "HostIp": "156.197.247.2",
        "Port": 8000
    },
    "Image_Dir": "C:/Application/ATMS/MEDIA/Events"
}

# Define a set to store the sent document ids
sent_document_ids = set()

@app1.get("/data")
async def get_data():
    # Get the current date in 'YYYY-MM-DD' format
    current_date = datetime.now().strftime('%Y-%m-%d')
    image_dir = os.path.join(config['Image_Dir'], current_date)

    # List to store the filtered image data
    filtered_data = []
    
    # Check if the directory for today's date exists
    if not os.path.exists(image_dir):
        return {"error": f"No images found for the current date: {current_date}"}

    # Fetch all jpg images from the directory
    for file_name in os.listdir(image_dir):
        if file_name.endswith('.jpg'):
            image_id = file_name.split('.')[0]  # Use file name as an ID

            if image_id not in sent_document_ids:
                try:
                    file_path = os.path.join(image_dir, file_name)
                    with open(file_path, "rb") as f:
                        image_data = f.read()
                    
                    # Prepare the response data
                    data = {
                        '_id': image_id,
                        'DateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'image': base64.b64encode(image_data).decode('utf-8')
                    }
                    
                    filtered_data.append(data)
                    sent_document_ids.add(image_id)
                
                except Exception as err:
                    print(f"Failed to send image {file_name}: {err}")
    
    print(f"Images to be sent: {filtered_data}")
    
    return json.loads(json.dumps(filtered_data, default=str))

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(app1, host=config['Server']['HostIp'], port=config['Server']['Port'])
