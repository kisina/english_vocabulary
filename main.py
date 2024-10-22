#!/usr/bin/python3
import csv
import random
import os
from datetime import datetime

def enregistrer_score(score):
    today = datetime.now().isoformat()
    f = open("logs_utilisation.txt", "a")
    f.write(f"{today} - {score}\r\n")
    f.close()

def charger_verbes_irreguliers(chemin_fichier):
    liste_fichiers = os.listdir(chemin_fichier)
    liste_fichiers.sort()
    print("Fichier disponibles:")
    for fichier in liste_fichiers:
        a,b = fichier.split('.')
        print(f"- {a}")
    fichiers_selectionnes = input("Choisissez les fichiers (séparés par des virgules), ou taper entrée pour tous les sélectionner:\r\n")
    if fichiers_selectionnes == "":
        fichiers_selectionnes = []
        for fichier in liste_fichiers:
            a,b = fichier.split('.')
            fichiers_selectionnes.append(a)
    else:
        fichiers_selectionnes = [f for f in fichiers_selectionnes.split(',')]
        
    verbes_irreguliers = []
    for fichier in fichiers_selectionnes:
        chemin_fichier = f"./lists/{fichier}.csv"
        with open(chemin_fichier, newline='', encoding='utf-8') as csvfile:
            lecteur = csv.reader(csvfile)
            for ligne in lecteur:
                verbes_irreguliers.append(tuple(ligne))
    return verbes_irreguliers

def interroger_utilisateur(verbes_irreguliers, nombre_de_verbes):
    score = 0
    random.shuffle(verbes_irreguliers)
    #print(verbes_irreguliers)
    
    nombre_de_verbes_interroges = 0
    verbes_a_revoir = []
    for en, fr in verbes_irreguliers:
        reponse_utilisateur = input(f"\r\nTraduisez le mot français '{fr}' en anglais : ")
        if reponse_utilisateur.lower() == en.lower():
            print("Correct !")
            score += 1
        else:
            print(f"Incorrect. La réponse correcte est : '{en}'")
            verbes_a_revoir.append(fr + ' --> ' + en)
        nombre_de_verbes_interroges += 1
        if nombre_de_verbes_interroges >= nombre_de_verbes: break
    
    print(f"\nScore final : {score}/{nombre_de_verbes_interroges}")
    if score < nombre_de_verbes_interroges:
        print("Mots à revoir:")
        [print(verbe) for verbe in verbes_a_revoir]
    enregistrer_score(f"Score final : {score}/{nombre_de_verbes_interroges}")
    input(f"\r\nAppuyer sur entrée pour quitter")
    return f"Score final : {score}/{nombre_de_verbes_interroges}"

if __name__ == "__main__":
    chemin_fichier_csv = "lists"  # Remplacez par le chemin réel de votre fichier CSV
    verbes_irreguliers = charger_verbes_irreguliers(chemin_fichier_csv)
    
    if verbes_irreguliers:
        nombre_de_verbes = int(input("Combien de mots pour l'interrogation ?\r\n"))
        nombre_de_verbes = min(nombre_de_verbes, len(verbes_irreguliers))
        score = interroger_utilisateur(verbes_irreguliers, nombre_de_verbes)
        
    else:
        print("Erreur : Impossible de charger la liste des mots.")
