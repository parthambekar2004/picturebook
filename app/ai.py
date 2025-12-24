from app.event_extractor import extract_important_event
from app.image import generate_image  

async def process_page(page_text, page_no):
    event = extract_important_event(page_text)
    image_path = generate_image(event, page_no)

    return {
        "page": page_no + 1,
        "full_text": page_text,   
        "event": event,
        "image": image_path
    }

