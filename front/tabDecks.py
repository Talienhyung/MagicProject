import dearpygui.dearpygui as dpg
import os

decksFolder = "storage\decks"
decks = os.listdir(decksFolder)

def create_tabDecks():
    with dpg.tab(label="Decks"):
        dpg.add_text("Contenu de l'onglet Decks")
        deckView = dpg.add_child_window(label="Decks", autosize_x=True, autosize_y=True)
        dpg.add_button(label="Ajouter un deck", callback=lambda: popup_deckName())

    def update_deckNumber():
        global decks
        for index in range(len(decks)):
            dpg.add_button(label=decks[index], callback=lambda s, a, u: showDeck(u), user_data=[index], parent=deckView)

    update_deckNumber()
    decks = len(os.listdir(decksFolder))

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

    if len(decks) <5:
        with open(deckPath, 'x', newline='') as f:
            f.write("Card Name,Card Type,Set,Rarity,Quantity,Mana Cost,Colors,ID,Card Text\n")
        return deckPath
    else:
        with dpg.window(label="Erreur", width=300, height=100):
            dpg.add_text("Vous ne pouvez pas créer plus de 5 decks.")
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item(dpg.last_item()))

def showDeck(deckIndex):
    deckIndex = deckIndex[0]
    deckPath = os.path.join(decksFolder, decks[deckIndex])
    deckName = deckPath.split('\\')[-1].split('.')[0]

    if not os.path.exists(deckPath):
        return

    with dpg.window(label=f"Deck: {deckName}", width=500, height=400):
        with open(deckPath, 'r') as f:
            lines = f.readlines()

        headers = lines[0].strip().split(',')
        entries = [line.strip().split(',') for line in lines[1:]]

        with dpg.child_window(autosize_x=True, autosize_y=True):
            for index, entry in enumerate(entries):
                for i, value in enumerate(entry):
                    if i in [0, 1, 4, 5, 8]:
                        dpg.add_text(f"{headers[i]}: {value}", wrap=300)
                dpg.add_button(label="Remove 1", callback=lambda s, a, u: remove_entry(u), user_data=[index, deckPath, deckIndex])
                dpg.add_separator()
                print("index : ", index)

def remove_entry(user_data):
    deckIndex = user_data[2]
    deckPath = user_data[1]
    index = user_data[0]
    print("remove index : ", index)
    with open(deckPath, 'r+') as f:
        lines = f.readlines()
        headers = lines[0].strip().split(',')
        entries = [line.strip().split(',') for line in lines[1:]]

        quantity_index = headers.index("Quantity")
        print(len(entries), index)
        entry = entries[index]
        entry[quantity_index] = str(int(entry[quantity_index]) - 1)

        if int(entry[quantity_index]) > 0:
            entries[index] = entry
        else:
            entries.pop(index)

        f.seek(0)
        f.write(','.join(headers) + '\n')
        for entry in entries:
            f.write(','.join(entry) + '\n')
        f.truncate()

    # Update the deck view
    dpg.delete_item(dpg.last_item())
    
    showDeck([deckIndex])