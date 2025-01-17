import dearpygui.dearpygui as dpg
import requests

def create_tabCards():
    with dpg.tab(label="Cards"):
        dpg.add_text("Card search")

        dpg.add_input_text(label="Card name", hint="Card name", tag="card_name_input")

        dpg.add_button(label="Search", callback=lambda: search(dpg.get_value("card_name_input")))

        results = dpg.add_text(label="Results")

        def search(card_name):
            print(f"Searching for card details for {card_name}")
            cards = search_scryfall(card_name)
            if cards:
                print(f"Found {len(cards)} cards")
                dpg.set_value(results, "")
                for card in cards:
                    dpg.add_text(f"Name: {card['name']}", parent=results)
                    dpg.add_text(f"Set: {card['set_name']}", parent=results)
                    dpg.add_text(f"Type: {card['type_line']}", parent=results)
                    dpg.add_text(f"Mana Cost: {card['mana_cost']}", parent=results)
                    dpg.add_text(f"Oracle Text: {card['oracle_text']}", parent=results)
                    dpg.add_separator(parent=results)


def search_scryfall(card_name):
    url = f"https://api.scryfall.com/cards/search?q={card_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    return None
