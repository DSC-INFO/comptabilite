# Créé par Desbois Hugo, le 09/11/2025 en Python 3.7

import json
# le module manipulant json
import os
# le module manipulant Systeme Exploitation
import sys
from decimal import Decimal

def read_json(file_path):
#fonction faisant:
    with open(file_path) as fichier2:
    #avec cela qui est un fichier2
        b=json.load(fichier2,parse_float=Decimal)
        #renommer le fichier2 en b
        somme_debit =Decimal(0)
        somme_credit=Decimal(0)
        for mouvement in b.get("ventilation"):
            if mouvement.get("debit") is not None:
                somme_debit=somme_debit+mouvement.get("debit")
            if mouvement.get("credit") is not None:
                somme_credit=somme_credit+mouvement.get("credit")
        difference_credit_debit=somme_credit-somme_debit
        if difference_credit_debit!=Decimal(0):
            print("erreur",file_path,difference_credit_debit)


file_list=os.listdir(sys.argv[1])
#liste des fichiers contenus dans le dossier
for file in file_list:

    read_json(os.path.join((sys.argv[1]), file))
    #os.path=chemin d'accès  join=construction du chemin d'accès


