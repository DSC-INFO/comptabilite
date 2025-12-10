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

Balance=dict()


def calcul(ecriture_json):


    for mouvement in ecriture_json.get("ventilation"):

        compte=mouvement.get("compte")

        if mouvement.get("credit") is not None:
            crédits=mouvement.get("credit")
        else:
            crédits=Decimal()
        if mouvement.get("debit") is not None:
            debits=mouvement.get("debit")
        else:
            debits=Decimal()



        if compte in Balance.keys():

               (credit_balance, debit_balance) = Balance[compte]
               Balance[compte] = (credit_balance + crédits, debit_balance + debits)

        else:


            Balance[compte]=(crédits,debits)




def read_json(file_path):

    with open(file_path) as fichier2:

        b=json.load(fichier2,parse_float=Decimal)

        présence=calcul(b)


def scandir(dir_path):

    file_list=os.listdir(dir_path)

    for file in file_list:

        file_path=os.path.join(dir_path, file)

        if os.path.isdir(file_path):

            scandir(file_path)

        else:

            read_json(file_path)

    for compte in Balance.keys():
        (credit_balance, debit_balance) = Balance[compte]
        print (compte,credit_balance, debit_balance, sep=";")

#file_list=os.listdir(sys.argv[1])

#for file in file_list:

#   read_json(os.path.join((sys.argv[1]), file))

# boucle principale du programme
if __name__ == '__main__':
    scandir(sys.argv[1])

