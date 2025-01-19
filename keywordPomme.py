from mtgsdk import *
import json
from tqdm import tqdm  # Importation de tqdm

# Génération du dictionnaire whiteAngel avec une barre de progression
whiteAngel = {}

# Récupération des ensembles
sets = Set.all()

# Utilisation de tqdm pour afficher la barre de progression
for x in tqdm(sets, desc="Traitement des ensembles", unit="ensemble"):
    try:
        white_cards = Card.where(set=x.code).where(color='white').where(subtypes='Angel').all()
        whiteAngel[x.code] = [(y.multiverse_id , y.name , y.supertypes, y.types, y.subtypes, y.rarity, y.mana_cost, y.colors, y.image_url) for y in white_cards]
    except Exception as e:
        print(f"Erreur avec l'ensemble {x.code} : {e}")

#Conversion du dictionnaire en JSON et affichage
print(json.dumps(whiteAngel, indent=4))

with open("whiteAngel.json", "w") as fichier:
    json.dump(whiteAngel, fichier, indent=4)


def load_json_from_file(filename):
    with open(filename, 'r') as file:
        json_data = json.load(file)
    return json_data
import json

# # Charger le JSON à partir du fichier
# data = load_json_from_file("whiteAngel.json")

# # Créer une liste pour stocker les ratios
# ratios = []

# # Parcourir chaque ensemble pour obtenir le nombre d'anges et le nombre total de cartes
# for key, elem in data.items():
#     # Compter le nombre d'anges
#     num_angels = len(elem)
    
#     # Compter le nombre total de cartes dans l'ensemble
#     total_cards = Card.where(set=key).all()  # Assuming Card.where(set=key).all() gives you the total cards
#     num_total_cards = len(total_cards)

#     # Calculer le ratio (en évitant la division par zéro)
#     ratio = num_angels / num_total_cards if num_total_cards > 0 else 0

#     # Ajouter le ratio à la liste
#     ratios.append((key, num_angels, num_total_cards, ratio))

# # Trier les ratios par ordre décroissant
# ratios.sort(key=lambda x: x[3], reverse=True)

# # Obtenir les 5 ensembles avec les meilleurs ratios
# top_5_ratios = ratios[:5]

# # Afficher les 5 ensembles avec le meilleur ratio d'anges
# for set_code, num_angels, num_total_cards, ratio in top_5_ratios:
#     print(f"Ensemble: {set_code}, Nombre d'anges: {num_angels}, Nombre total de cartes: {num_total_cards}, Ratio: {ratio:.2f}")
