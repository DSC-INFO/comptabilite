# Créé par Desbois Hugo, le 09/11/2025 en Python 3.7
# import (permet d'utilser le module "")
# def (fonction)
# with as (avec "" qui est "")
# ""=""(renommer l'objet)
# file_list(list de fichier dans le dossier)
# os.path(chemin d'accès)
# join=(construction du chemin d'accès)

import json

import os

import sys

from decimal import Decimal


def calcul(ecriture_json):

    somme_debit =Decimal(0)

    somme_credit=Decimal(0)

    for mouvement in ecriture_json.get("ventilation"):

        if mouvement.get("debit") is not None:

            somme_debit=somme_debit+mouvement.get("debit")

        if mouvement.get("credit") is not None:

            somme_credit=somme_credit+mouvement.get("credit")

    difference_credit_debit=somme_credit-somme_debit

    return difference_credit_debit


def read_json(file_path):

    with open(file_path) as fichier2:

        b=json.load(fichier2,parse_float=Decimal)

        difference_credit_debit=calcul(b)

        if difference_credit_debit!=Decimal(0):

            print("erreur",file_path,difference_credit_debit)


def scandir(dir_path):

    file_list=os.listdir(dir_path)

    for file in file_list:

        file_path=os.path.join(dir_path, file)

        if os.path.isdir(file_path):

            scandir(file_path)

        else:

            read_json(file_path)


#file_list=os.listdir(sys.argv[1])

#for file in file_list:

#   read_json(os.path.join((sys.argv[1]), file))

# boucle principale du programme
if __name__ == '__main__':
    scandir(sys.argv[1])

