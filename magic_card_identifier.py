import pytesseract
from PIL import Image
import requests
import cv2
import re

def cleaning( imagelink):
    # Charger l'image
    image_path = imagelink
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un filtre de seuil pour améliorer la lisibilité du texte
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Sauvegarder l'image traitée
    processed_path = "processed_card.jpg"
    cv2.imwrite(processed_path, thresh)

    return processed_path


# Function to extract text from an image
def extract_text(processed_path):
    text = pytesseract.image_to_string(Image.open(processed_path))
    return text

# Function to find the title (first line of the text)
def find_title_advanced(text):
    lines = text.strip().split("\\n")
    title = min((line for line in lines if line.isalpha()), key=len, default=None)
    return title

# Function to search for card details on Scryfall
def search_scryfall(card_name):
    url = f"https://api.scryfall.com/cards/search?q={card_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["total_cards"] > 0:
            return data["data"][0]  # Return the first matching card
    return None

def search(img):
    # Example usage
    image_path = cleaning(img)  # Replace with your card image
    print("Extracting text from image...")
    text = extract_text(image_path)
    print("Text extracted:")
    print(text)

    print("\nDetecting title...")
    title = find_title_advanced(text)
    if title:
        print(f"Title detected: {title}")
        print("\nSearching for card details on Scryfall...")
        card_details = search_scryfall(title)
        if card_details:
            print("Card found on Scryfall:")
            print(f"Name: {card_details['name']}")
            print(f"Set: {card_details['set_name']}")
            print(f"Oracle Text: {card_details['oracle_text']}")
        else:
            print("No matching card found on Scryfall.")
    else:
        print("No title detected.")