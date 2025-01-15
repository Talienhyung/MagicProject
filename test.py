import json

def load_json_from_file(filename):
    with open(filename, 'r') as file:
        json_data = json.load(file)
    return json_data
import json

def antiDoublons ():
    # Charger le JSON à partir du fichier
    data = load_json_from_file("whiteAngel.json")

    # Nouveau dictionnaire pour stocker les ensembles sans doublons
    unique_whiteAngel = {}

    # Parcourir chaque ensemble
    for set_code, cards in data.items():
        # Dictionnaire pour suivre les noms des cartes déjà ajoutées
        seen_names = {}
        unique_cards = []
        
        for card in cards:
            multiverse_id = card[0]
            name = card[1]
            
            # Vérifier si le multiverse_id est défini et si le nom n'est pas déjà dans seen_names
            if multiverse_id is not None and name is not None and name not in seen_names:
                # Ajouter le nom à seen_names
                seen_names[name] = True
                
                # Ajouter la carte à unique_cards
                unique_cards.append(card)
        
        # Stocker les cartes uniques dans le dictionnaire par ensemble
        unique_whiteAngel[set_code] = unique_cards

    # Enregistrer les cartes uniques dans un nouveau fichier JSON
    with open("unique_whiteAngel.json", "w") as f:
        json.dump(unique_whiteAngel, f, indent=4)

    # Afficher le résultat
    print("Doublons supprimés, et le nouveau fichier unique_whiteAngel.json a été créé.")


def legen():
    # Charger le JSON à partir du fichier
    data = load_json_from_file("unique_whiteAngel.json")

    # Nouveau dictionnaire pour stocker les cartes légendaires
    legendary_cards = {}

    # Parcourir chaque ensemble
    for set_code, cards in data.items():
        # Liste pour stocker les cartes légendaires
        legendary_list = []
        
        for card in cards:
            multiverse_id = card[0]
            name = card[1]
            supertypes = card[2]  # On suppose que c'est une liste

            # Vérifier si la carte est légendaire
            if supertypes and "Legendary" in supertypes:
                # Ajouter la carte à legendary_list
                legendary_list.append(card)

        # Stocker les cartes légendaires dans le dictionnaire par ensemble
        if legendary_list:  # Ajouter l'ensemble uniquement s'il a des cartes légendaires
            legendary_cards[set_code] = legendary_list

    # Enregistrer les cartes légendaires dans un nouveau fichier JSON
    with open("legendary_whiteAngel.json", "w") as f:
        json.dump(legendary_cards, f, indent=4)

    # Afficher le résultat
    print("Les cartes légendaires ont été extraites et le fichier legendary_whiteAngel.json a été créé.")

def top_angel_sets(x):
    """
    Récupère les x ensembles avec le plus d'anges.
    :param x: Nombre d'ensembles à retourner.
    :return: Liste des x ensembles avec leurs nombres d'anges.
    """
    # Charger le JSON à partir du fichier
    data = load_json_from_file("whiteAngel.json")

    # Créer une liste pour stocker les ensembles avec leurs nombres d'anges
    angel_counts = []

    # Parcourir chaque ensemble pour compter les anges
    for set_code, cards in data.items():
        num_angels = len(cards)  # Compter le nombre d'anges
        angel_counts.append((set_code, num_angels))

    # Trier la liste par nombre d'anges (ordre décroissant)
    angel_counts.sort(key=lambda item: item[1], reverse=True)

    # Retourner les x premiers ensembles
    print( angel_counts[:x])


def countleg():
    # Charger le JSON à partir du fichier
    data = load_json_from_file("legendary_whiteAngel.json")

    # Variable pour stocker l'ensemble avec le plus de cartes légendaires
    max_legendary_set = ["", 0]  # [set_code, count]

    # Parcourir chaque ensemble pour compter les cartes légendaires
    for set_code, cards in data.items():
        num_legendaries = len(cards)  # Compter le nombre de légendaires
        
        # Vérifier si cet ensemble a plus de légendaires que le maximum actuel
        if num_legendaries > max_legendary_set[1]:
            max_legendary_set = [set_code, num_legendaries]


def top_legendary_sets(x):
    """
    Récupère les x ensembles avec le plus de cartes légendaires.
    :param x: Nombre d'ensembles à retourner.
    :return: Liste des x ensembles avec leurs nombres de cartes légendaires.
    """
    # Charger le JSON à partir du fichier
    data = load_json_from_file("legendary_whiteAngel.json")

    # Créer une liste pour stocker les ensembles avec leurs nombres de cartes légendaires
    legendary_counts = []

    # Parcourir chaque ensemble pour compter les cartes légendaires
    for set_code, cards in data.items():
        num_legendaries = len(cards)  # Compter le nombre de légendaires
        legendary_counts.append((set_code, num_legendaries))

    # Trier la liste par nombre de légendaires (ordre décroissant)
    legendary_counts.sort(key=lambda item: item[1], reverse=True)

    # Retourner les x premiers ensembles
    print(legendary_counts[:x])



def reaload():
    antiDoublons ()
    legen()
    countleg()
    top_angel_sets(7)
    top_legendary_sets(5)

reaload()