import aiohttp
import asyncio
import base64
import logging
import json
import folium
import tkinter as tk
from tkinter import filedialog
from aiohttp import ClientTimeout

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

API_TOKEN = ""
API_BASE = "https://dev.geospy.ai"
API_ENDPOINT = "/predict"
FULL_API_URL = f"{API_BASE}{API_ENDPOINT}"

request_timeout = ClientTimeout(total=60)

collected_responses = []

async def convert_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    return encoded_string

async def post_image_data(session, encoded_image: str, file_path: str):
    data = {
        "inputs": {"image": encoded_image},
        "top_k": 25,
    }
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
    }

    try:
        async with session.post(FULL_API_URL, json=data, headers=headers, timeout=request_timeout) as resp:
            if resp.status == 200:
                response_data = await resp.json()
                collected_responses.append({file_path: response_data})
                logging.debug(f"Request successful for {file_path}: {response_data}")
            else:
                logging.error(f"Request failed for {file_path} with status {resp.status}: {await resp.text()}")
    except Exception as error:
        logging.error(f"Error during request for {file_path}: {error}")

async def process_images(image_files):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for path in image_files:
            encoded_img = await convert_image_to_base64(path)
            tasks.append(asyncio.create_task(post_image_data(session, encoded_img, path)))
            await asyncio.sleep(1)
        await asyncio.gather(*tasks)

    # Process collected responses and visualize on a map
    for response in collected_responses:
        for file_path, data in response.items():
            visualize_geospy_response(file_path, data)

def visualize_geospy_response(file_path, data):
    # Extract geographical information from data
    geo_predictions = data.get('geo_predictions', [])
    if not geo_predictions:
        logging.warning(f"No geo predictions found for {file_path}")
        return

    # Create a Folium map
    map = folium.Map(location=[0, 0], zoom_start=2)

    # Define a color palette for markers
    colors = [
        'red', 'blue', 'green', 'orange', 'purple', 'pink', 'gray', 'black', 'darkblue', 'darkgreen',
        'lightblue', 'lightgreen', 'lightred', 'darkred', 'darkpurple', 'cadetblue', 'lightgray', 'beige'
    ]

    # Assign a unique color to each prediction based on its index
    color_index = 0

    # Add markers for each coordinate in the response
    for prediction in geo_predictions:
        coordinates = prediction['coordinates']
        score = prediction['score']
        similarity_score_1km = prediction['similarity_score_1km']

        # Generate a color for this prediction based on the color palette
        color = colors[color_index % len(colors)]
        color_index += 1

        popup_text = f"Image: {file_path}<br>Score: {score}<br>Similarity Score 1km: {similarity_score_1km}"
        folium.Marker(location=coordinates, popup=popup_text).add_to(map)

    # Save the map to an HTML file
    map.save(f"{file_path}_map.html")


def select_images():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select Image Files", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    root.destroy()  # Destroy the root window after file selection
    return file_paths

image_files = select_images()
if image_files:
    asyncio.run(process_images(image_files))
