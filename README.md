
# Magic Card Identifier

This project helps you extract text from a Magic: The Gathering card image, detect the card title, and fetch its details from Scryfall.

## Requirements
- Python 3.x
- Tesseract OCR
- Libraries: `pytesseract`, `Pillow`, `requests`

## Installation
1. Install Python and Tesseract OCR.
2. Install the required libraries:
   ```
   pip install pytesseract pillow requests
   ```

## Usage
1. Place a card image in the project folder (replace `example_card.jpg`).
2. Run the script:
   ```
   python magic_card_identifier.py
   ```
3. The script will extract the title and search for card details on Scryfall.

## Note
Make sure Tesseract is correctly installed and added to your PATH.
