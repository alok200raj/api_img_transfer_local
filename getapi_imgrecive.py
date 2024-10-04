import requests
import os
import base64
from datetime import datetime
import time

# Configuration
server_url = "http://156.197.247.2:8000/data"  # URL of the FastAPI server
save_path_base = "C:/Application/ATMS/MEDIA/Events"  # Base directory to save images on the new system
retry_interval = 10  # Retry interval in seconds

# Function to fetch and save images
def fetch_and_save_images():
    try:
        # Fetch data from the FastAPI server
        response = requests.get(server_url, timeout=10)
        
        if response.status_code == 200:
            images_data = response.json()
            
            # Get the current date to create the folder (same structure as the source)
            current_date = datetime.now().strftime('%Y-%m-%d')
            save_path = os.path.join(save_path_base, current_date)

            # Create the directory if it doesn't exist
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # Iterate over the received data and save the images
            for image_info in images_data:
                try:
                    image_id = image_info['_id']
                    image_data = image_info['image']  # Base64-encoded image
                    file_name = f"{image_id}.jpg"  # Assuming the image is .jpg

                    # Decode the image
                    image_bytes = base64.b64decode(image_data)

                    # Save the image in the specified path
                    file_path = os.path.join(save_path, file_name)
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"Image {file_name} saved at {file_path}")

                except Exception as err:
                    print(f"Failed to save image {image_id}: {err}")
        
        else:
            print(f"Failed to fetch data from server. Status code: {response.status_code}")

    except requests.ConnectionError:
        print("Connection failed. Retrying in 10 seconds...")
    except requests.Timeout:
        print("Request timed out. Retrying in 10 seconds...")

# Main loop to fetch and save images
while True:
    fetch_and_save_images()
    time.sleep(retry_interval)  # Wait for 10 seconds before retrying
