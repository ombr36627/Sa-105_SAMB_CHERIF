from datetime import datetime, timedelta
import csv
import matplotlib.pyplot as plt

# Fonction pour calculer la différence en heures entre deux timestamps
def calculer_difference_heures(debut, fin):
    format_date = '%Y-%m-%d %H:%M:%S'
    debut_dt = datetime.strptime(debut, format_date)
    fin_dt = datetime.strptime(fin, format_date)
    difference = (fin_dt - debut_dt).total_seconds() / 3600  # Conversion en heures
    return difference

# Fonction pour traiter les événements d'une semaine
def traiter_evenements_semaine(debut_semaine_evaluer, groupe_etudiants):
    total_heures_CM_semaine = 0
    total_heures_TD_semaine = 0
    total_heures_TP_semaine = 0
    donnees_groupe = []

    # Date de début fixée pour les cours (1er septembre 2021 à 8h15)
    debut_cours = datetime.strptime('2021-09-01 08:15:00', '%Y-%m-%d %H:%M:%S')

    debut_semaine_evaluer_dt = datetime.strptime(debut_semaine_evaluer, '%Y-%m-%d %H:%M:%S')
    fin_semaine_evaluer_dt = debut_semaine_evaluer_dt + timedelta(days=7)

    # Vérification si l'événement se situe dans la première semaine de cours
    premiere_semaine = debut_semaine_evaluer_dt <= debut_cours < fin_semaine_evaluer_dt

    with open('ORC.csv', 'r') as file:
        lines = file.readlines()

        for line in lines[1:]:
            colonnes = line.strip().split(',')

            salle = colonnes[3].strip('"')
            debut_evenement = colonnes[0].strip('"')
            fin_evenement = colonnes[1].strip('"')
            groupe = colonnes[4].strip('"')
            resume = colonnes[2].strip('"')

            debut_evenement_dt = datetime.strptime(debut_evenement, '%Y-%m-%d %H:%M:%S')

            if debut_semaine_evaluer_dt <= debut_evenement_dt < fin_semaine_evaluer_dt:
                if salle == "RT-Amphi":
                    total_heures_CM_semaine += calculer_difference_heures(debut_evenement, fin_evenement)
                elif salle in ["RT-Salle-TD3", "RT-Salle-TD4", "RT-Salle-TD2", "RT-Salle-TD1"]:
                    total_heures_TD_semaine += calculer_difference_heures(debut_evenement, fin_evenement)
                elif salle in ["RT-Labo reseaux 1-RT", "Labo reseaux 2", "RT-Labo Telecoms 1", "RT-Labo Informatique 1", "RT-Labo Electronique 1", "RT-Labo Informatique 3", "RT-Labo Telecoms 2", "RT-Labo Informatique 2"]:
                    total_heures_TP_semaine += calculer_difference_heures(debut_evenement, fin_evenement)

                if groupe_etudiants in groupe:
                    donnees_groupe.append((debut_evenement, fin_evenement, salle, resume))

    return total_heures_CM_semaine, total_heures_TD_semaine, total_heures_TP_semaine, donnees_groupe


# Fonction pour générer le rapport CSV avec toutes les informations nécessaires
def generer_rapport_csv(nom_fichier, donnees):
    entetes = ['Début événement', 'Fin événement', 'Salle', 'Résumé']

    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(entetes)

        for donnee in donnees:
            writer.writerow(donnee)


# Fonction pour afficher le diagramme
def afficher_diagramme(total_CM, total_TD, total_TP):
    labels = ['CM', 'TD', 'TP']
    valeurs = [total_CM, total_TD, total_TP]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, valeurs, color=['blue', 'orange', 'green'])
    plt.xlabel('Types de Cours')
    plt.ylabel('Total d\'heures')
    plt.title('Répartition des heures par type de cours')
    plt.show()

# Date de début de la semaine à évaluer (au format '%Y-%m-%d %H:%M:%S')
def saisie_date_debut_semaine():
    while True:
        try:
            debut_semaine_evaluer = input("Entrez le début de la semaine (exemple : 2022-01-24 08:15:00) : ")
            # Vérification de la validité du format de la date
            datetime.strptime(debut_semaine_evaluer, '%Y-%m-%d %H:%M:%S')
            return debut_semaine_evaluer
        except ValueError:
            print("Format de date invalide. Assurez-vous de respecter le format (YYYY-MM-DD HH:MM:SS).")

def saisie_groupe_etudiants():
    while True:
        groupe_etudiants = input("Entrez le groupe d'étudiants (exemple : RT1Turing) : ")
        # Vérification de la présence de caractères alphanumériques
        if not groupe_etudiants.isalnum():
            print("Le groupe ne doit contenir que des lettres ou des chiffres.")
            continue
        # Si la saisie est valide, retourner le groupe d'étudiants en majuscules
        return groupe_etudiants

# Saisie du début de la semaine et du groupe d'étudiants avec vérification
debut_semaine_evaluer = saisie_date_debut_semaine()
groupe_etudiants = saisie_groupe_etudiants()

print("Début de la semaine :", debut_semaine_evaluer)
print("Groupe d'étudiants :", groupe_etudiants)
# Traitement des événements pour la semaine et le groupe spécifiés
total_heures_CM, total_heures_TD, total_heures_TP, donnees_groupe = traiter_evenements_semaine(debut_semaine_evaluer, groupe_etudiants)

# Vérification si donnees_groupe est vide
if not donnees_groupe:
    print("Aucune donnée trouvée pour cette période. Veuillez vérifier les informations saisies.")
else:
    # Génération du rapport CSV
    nom_fichier_rapport = 'rapport_groupe_etudiants.csv'
    generer_rapport_csv(nom_fichier_rapport, donnees_groupe)

    # Affichage des totaux sous forme de tableau
    print("Voici les différents cours durant la semaine : ", donnees_groupe)
    print(f"Total d'heures de CM pour la semaine : {total_heures_CM:.2f}")
    print(f"Total d'heures de TD pour la semaine : {total_heures_TD:.2f}")
    print(f"Total d'heures de TP pour la semaine : {total_heures_TP:.2f}")

    # Affichage du diagramme
    afficher_diagramme(total_heures_CM, total_heures_TD, total_heures_TP)

