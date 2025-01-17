import dearpygui.dearpygui as dpg
import os

decksFolder = "storage\decks"

def create_tabDecks():
    with dpg.tab(label="Decks"):
        dpg.add_text("Contenu de l'onglet Decks")
        dpg.add_button(label="Ajouter un deck", callback=lambda: popup_deckName())

def popup_deckName():
    with dpg.window(label="Nom du deck", width=300, height=100):
        dpg.add_input_text(label="Nom du deck", hint="Nom du deck", tag="deck_name_input")
        # Utilisation de `dpg.add_group` au lieu de `add_same_line` pour créer des boutons côte à côte
        with dpg.group(horizontal=True):
            dpg.add_button(label="Annuler", callback=lambda: print("Création annulée"))
            dpg.add_button(label="Créer", callback=lambda: create_deckCSV(dpg.get_value("deck_name_input")))

def create_deckCSV(deckName):
    if deckName == "":
        return
    deckPath = f"{decksFolder}/{deckName}.csv"

    with open(deckPath, 'x', newline='') as f:
        f.write("Card Name,Card Type,Set,Rarity,Quantity,Mana Cost,Colors,ID,Card Text\n")
    return deckPath
