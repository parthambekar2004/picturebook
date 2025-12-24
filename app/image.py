import requests
import os

OUTPUT_DIR = "static/images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_image(prompt: str, page_number: int):
    safe_prompt = prompt.replace(" ", "%20")[:300]

    url = f"https://image.pollinations.ai/prompt/{safe_prompt}"

    image_path = f"{OUTPUT_DIR}/page_{page_number + 1}.png"

    response = requests.get(url)

    if response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path

    return None
