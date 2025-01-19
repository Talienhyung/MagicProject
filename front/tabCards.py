import dearpygui.dearpygui as dpg
import requests
import os
import functools

cards=[]
deckPath = "storage\decks"
decks = os.listdir(deckPath)

def create_tabCards():
    global decks
    decks = os.listdir(deckPath)
    
    with dpg.tab(label="Cards"):
        dpg.add_text("Card search")

        dpg.add_input_text(label="Card name", hint="Card name", tag="card_name_input")

        dpg.add_button(label="Search", callback=lambda: search(dpg.get_value("card_name_input")))

        results = dpg.add_child_window(label="Results", autosize_x=True, autosize_y=True)

        def search(card_name):
            print(f"Searching for card details for {card_name}")
            global cards
            cards = search_scryfall(card_name)
            polishCards(cards)
            if cards:
                print(f"Found {len(cards)} cards")
                dpg.delete_item(results, children_only=True)
                for index, card in enumerate(cards):
                    dpg.add_text(f"Name: {card['name']}", parent=results)
                    dpg.add_text(f"Set: {card['set_name']}", parent=results)
                    dpg.add_text(f"Type: {card['type_line']}", parent=results)
                    for button in decks:
                        path = os.path.join(deckPath, button)
                        dpg.add_button(label=f"Add to {button}",parent=results, callback=lambda s, a, u: addCardToDeck(u), user_data=[index, path])
                    dpg.add_separator(parent=results)
            else:
                dpg.set_value(results, "No cards found")


def search_scryfall(card_name):
    url = f"https://api.scryfall.com/cards/search?q={card_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    return None

def addCardToDeck(user_data):
    global cards
    index= user_data[0]
    deckPath = user_data[1]
    card = cards[index]
    with open(deckPath, 'r+', newline='') as f:
        lines = f.readlines()
        card_exists = False
        for line in lines:
            if card['name'] == line.split(',')[0]:
                card_exists = True
                quantity = int(line.split(',')[4]) + 1
                lines[lines.index(line)] = line.replace(f",{line.split(',')[4]},", f",{quantity},")
                f.seek(0)
                f.writelines(lines)
                break
        if not card_exists:
            name = card['name'] = card['name'].replace(',', ';')
            type_line = card['type_line'].replace('—', '-')
            set_name = card['set_name'].replace(',', ';')
            oracle_text = card['oracle_text'].replace(',', ';')
            oracle_text = oracle_text.replace('—', '-')
            f.write(f"{name},{card['type_line']},{set_name},{card['rarity']},1,{card['mana_cost']},{card['colors']},{card['id']},{oracle_text}\n")
    print(f"Added {card['name']} to {deckPath}")
    return deckPath

def polishCards(cards):
    if not cards:
        return
    for card in cards:
        for key, value in card.items():
            if isinstance(value, str):
                card[key] = value.replace('\n', ' ')