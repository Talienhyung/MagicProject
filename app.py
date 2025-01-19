import dearpygui.dearpygui as dpg
from front.tabCards import *
from front.tabDecks import *
from front.tabScan import *

# Créer le contexte
dpg.create_context()

# Fenêtre principale
with dpg.window(tag="Primary Window"):
    dpg.add_text("Bienvenue dans l'application avec onglets modulaires !")

    # Barre d'onglets
    with dpg.tab_bar():
        create_tabDecks()
        create_tabCards()
        create_tabScan()


# Configurer et démarrer l'interface
dpg.create_viewport(title='Application avec Onglets', width=600, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()

# Détruire le contexte après fermeture
dpg.destroy_context()