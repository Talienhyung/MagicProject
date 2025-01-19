import dearpygui.dearpygui as dpg
import requests
import pytesseract
import cv2
import time
import numpy as np
import os
import threading

# Configuration
camera_url = 'http://192.168.1.189:8080/video'
capture_interval = 2
output_folder = "./captured_images/"
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Global variables
scanner_running = False
last_capture_time = time.time()
card_details = ""
card_text_id = None
cap = None 

def fetch_card_details(card_name):
    global card_details
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            card_data = response.json()
            card_details = f"Name: {card_data['name']}\n" \
                         f"Mana Cost: {card_data.get('mana_cost', 'N/A')}\n" \
                         f"Type: {card_data['type_line']}\n" \
                         f"Set: {card_data['set_name']}\n" \
                         f"Price: ${card_data['prices'].get('usd', 'N/A')}"
            stop_scanner()
        else:
            card_details = "Card not found"
    except Exception as e:
        card_details = f"Error fetching card details: {str(e)}"
    
    dpg.set_value(card_text_id, card_details)

def start_camera_scan():
    global scanner_running, last_capture_time, cap

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if cap is not None and cap.isOpened():
        cap.release() 

    cap = cv2.VideoCapture(camera_url)

    if not cap.isOpened():
        print("Error: Could not open camera stream.")
        return

    while scanner_running:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to retrieve frame from stream.")
                continue

            
            if time.time() - last_capture_time >= capture_interval:
                timestamp = int(time.time())
                filename = f"{output_folder}image_{timestamp}.jpeg"
                
               
                for f in os.listdir(output_folder):
                    os.remove(os.path.join(output_folder, f))
                
                
                cv2.imwrite(filename, frame)

                
                text = pytesseract.image_to_string(frame)
                if text.strip():
                    print(f"Detected Text: {text.strip()}")  

                    
                    dpg.configure_item(card_text_id, default_value="Fetching details...")
                    threading.Thread(target=fetch_card_details, args=(text.strip(),), daemon=True).start()

                last_capture_time = time.time()

           
            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                scanner_running = False
                break

            
            time.sleep(0.03) 

        except Exception as e:
            print(f"Scanner error: {e}")
            time.sleep(2)

    cap.release()
    cv2.destroyAllWindows()

def start_scanner_thread():
    global scanner_running
    if not scanner_running:
        scanner_running = True
        threading.Thread(target=start_camera_scan, daemon=True).start()

def stop_scanner():
    global scanner_running
    scanner_running = False

def create_tabScan():
    with dpg.tab(label="Scan"):
        dpg.add_text("Please scan the Title of the card")
        
       
        with dpg.group(horizontal=True):
            dpg.add_button(label="Start Scanner", callback=start_scanner_thread)
            dpg.add_button(label="Stop Scanner", callback=stop_scanner)
        
        
        scanner_window = dpg.add_child_window(label="Scanner Output", autosize_x=True, autosize_y=True)
        
        
        global card_text_id
        card_text_id = dpg.add_text("Scan a card to see details", wrap=400, parent=scanner_window)
