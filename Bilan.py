from decimal import Decimal
from Balance import scandir
import sys
import csv

class NoeudCompte:

    def __init__(self,code,debit,credit,sous_comptes=None):
        self.code = code
        self.debit = debit
        self.credit = credit
        self.sous_comptes = sous_comptes
        if (self.sous_comptes is None):
            self.sous_comptes = dict()

    def __str__(self):
        for sous_compte in self.sous_comptes.values():
            print(sous_compte)

        return f'{self.code}:{self.debit}:{self.credit}:[{str(self.sous_comptes)}]'

    def classerSousCompte(self, noeud):
        """ Cette méthode classe le noeud dans le tableau de sous_comptes correspondant. 
        Si le sous_compte n'existe pas, il le crée, l'ajoute à sous_comptes, et lui passe le noeud à classer.
        """

        # Etape 1: identifier le sous-compte
        code_sous_compte = noeud.code[0:len(self.code)+1]
        print(f'code_sous_compte: {code_sous_compte}')

        # Etape 1 bis: si le code sous-compte est le code compte du noeud à classer, on s'arrete
        if code_sous_compte == noeud.code:
            self.sous_comptes[code_sous_compte] = noeud
        else:
            # Etape 2: rechercher le sous-compte
            sous_compte_trouve = self.sous_comptes.get(code_sous_compte)

            # Etape 2 bis: créer le sous-compte s'il n'existe pas
            if sous_compte_trouve is None:
                sous_compte_trouve = NoeudCompte(code_sous_compte, Decimal(), Decimal())
                self.sous_comptes[code_sous_compte] = sous_compte_trouve
            
            # Etape 3: je demande au sous-compte trouvé de classer le noeud fourni en entrée
            sous_compte_trouve.classerSousCompte(noeud)
    
    def trouverSousCompte(self, code_sous_compte):
        """ Cette méthode renvoie le noeud qui correspond au sous-compte recherché. """
        if self.code == code_sous_compte:
            return self
        else:
            # Chercher parmi les enfans
            # identifier le compte
            code_a_chercher = code_sous_compte[0:len(self.code)+1]
            sous_compte_trouve = self.sous_comptes.get(code_a_chercher)
            if sous_compte_trouve is not None:
                return sous_compte_trouve.trouverSousCompte(code_sous_compte)
            else:
                return None

    def aggregerMontants(self):
        for sous_compte in self.sous_comptes.values():
            sous_compte.aggregerMontants()
            self.debit += sous_compte.debit
            self.credit += sous_compte.credit

def creer_bilan_csv(racine):

    def difference_compte(numero_compte):
        compte = racine.trouverSousCompte(numero_compte)
        if compte is not None:
            difference_self = Decimal(compte.debit) - Decimal(compte.credit)
            if difference_self < Decimal():
                return Decimal() - difference_self
            else:
                return difference_self
        else:
            return Decimal()
    
    def debit_compte(numero_compte):
        compte = racine.trouverSousCompte(numero_compte)
        if compte is not None:
            return Decimal(compte.debit)
        else:
            return Decimal()
        
    def credit_compte(numero_compte):
        compte = racine.trouverSousCompte(numero_compte)
        if compte is not None:
            return Decimal(compte.credit)
        else:
            return Decimal()

    # Données à écrire (liste de listes)
    data = [
        ["POSTE DU PASSIF", "VALEUR"],
        ["Capital", difference_compte("101") + difference_compte("108")],
        ["écart de réévaluation", difference_compte("105")],
        ["Réserves :", ""],
        ["- Réserves légales", difference_compte("1061")],
        ["- Réserves réglementés", difference_compte("1064")],
        ["- Autres", difference_compte("1063") + difference_compte("1068")],
        ["Report à nouveau", difference_compte("110") + difference_compte("119")],
        ["Résultat de l'exercice", "50046"],
        ["Provisions réglementés", difference_compte("14")],
        ["Total Capitaux propres", ""],
        ["Provisions", difference_compte("15")],
        ["Dettes", ""],
        ["- emprunts et dettes assimilés", difference_compte("16") + credit_compte("51")],
        ["- Avances et accomptes reçus", difference_compte("4191")],
        ["- Fournisseurs et comptes rattachés", difference_compte("40")],
        ["- Autres", difference_compte("41") + difference_compte("42") + difference_compte("43") + difference_compte("44") + difference_compte("45") + difference_compte("46")],
        ["Produit constatés d'avances", difference_compte("487")],
        [],
        ["TOTAL PASSIF"],
        [],
        ["POSTE DE L'ACTIF", "VALEUR BRUT", "AMORT. ET DEPRECIATIONS"],
        ["Immobilisations corporelles :"],
        ["- Fonds commerciales", difference_compte("206") + difference_compte("207"),difference_compte("2906") + difference_compte("2907")],
        ["- Autres", difference_compte("201") + difference_compte("203") + difference_compte("205") + difference_compte("208"), difference_compte("280") + difference_compte("2905") + difference_compte("2908")],
        ["Immobilisations corporelles", difference_compte("21") + difference_compte("22") + difference_compte("23"), difference_compte("281") + difference_compte("291")],
        ["Immobilisations financières", difference_compte("26") + difference_compte("27"), difference_compte("296") + difference_compte("297")],
        ["TOTAL 1"],
        ["Stock (hors marchandises)", difference_compte("31") + difference_compte("32") + difference_compte("33") + difference_compte("34") + difference_compte("35"), difference_compte("391") + difference_compte("392") + difference_compte("393") + difference_compte("394") + difference_compte("395")],
        ["Stock marchandises", difference_compte("37"), difference_compte("397")],
        ["Avances et accomptes versés", difference_compte("4091")],
        ["CREANCES"],
        ["- Clients et comptes rattachés", difference_compte("41"), difference_compte("491")],
        ["- Autres créances", difference_compte("40") - difference_compte("4091") + difference_compte("42") + difference_compte("43") + difference_compte("44") + difference_compte("45") + difference_compte("46"), difference_compte("496")],
        ["Valeurs mobilières de placement", difference_compte("50"), difference_compte("590")],
        ["Dispo (autres que caisses)", difference_compte("51") + difference_compte("54") + difference_compte("58")],
        ["Caisses", difference_compte("53")],
        ["TOTAL 2"],
        ["Charges constatés d'avances", difference_compte("486")],
        [],
        ["TOTAL ACTIF"]
    ]

    # Écriture dans un fichier CSV
    with open("Bilan.csv", "w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        writer.writerows(data)

def creer_compte_resultat_csv(racine):

    def difference_compte(numero_compte):
        compte = racine.trouverSousCompte(numero_compte)
        if compte is not None:
            difference_self = Decimal(compte.debit) - Decimal(compte.credit)
            if difference_self < Decimal():
                return Decimal() - difference_self
            else:
                return difference_self
        else:
            return Decimal()
    
    def debit_compte(numero_compte):
        compte = racine.trouverSousCompte(numero_compte)
        if compte is not None:
            return Decimal(compte.debit)
        else:
            return Decimal()
        
    def credit_compte(numero_compte):
        compte = racine.trouverSousCompte(numero_compte)
        if compte is not None:
            return Decimal(compte.credit)
        else:
            return Decimal()

    # Données à écrire (liste de listes)
    data = [
        ["CHARGES", "VALEUR"],
        ["Charges d'exploitation:"],
        ["- Achats de marchandises", difference_compte("607") + difference_compte("6097")],
        ["- Variations de stocks (m)", difference_compte("6037")],
        ["- Achats d'approvisionnement", difference_compte("601") + difference_compte("602") + difference_compte("603") + difference_compte("604") + difference_compte("605") + difference_compte("606")],
        ["- Variations de stocks", difference_compte("6031") + difference_compte("6032")],
        ["- Autres charges externes", difference_compte("61") + difference_compte("62")],
        ["- Impots taxes et assimilés", difference_compte("63")],
        ["- Rémunération perso", difference_compte("641") + difference_compte("644")],
        ["- Charges sociales", difference_compte("645") + difference_compte("646")],
        ["- Dotations aux amortissement", difference_compte("6811")],
        ["- Dotations aux provisions (et dépréciations)", difference_compte("6815") + difference_compte("6817")],
        ["- Autres charges (d'éxploitations)", difference_compte("65")],
        ["Charges financières", difference_compte("66") + credit_compte("686")],
        ["Charges exeptionnelles", difference_compte("67") + credit_compte("687")],
        ["Impots sur les bénéfices", difference_compte("695") + credit_compte("697")],
        [],
        ["PRODUITS", "VALEUR"],
        ["Produits d'exploitations :"],
        ["- Ventes de marchandises", difference_compte("707") + difference_compte("7097")],
        ["- Prod vendu", difference_compte("701") + difference_compte("706") + difference_compte("708") + difference_compte("7091") + difference_compte("7096") + difference_compte("7098")],
        ["- Prod stockée", difference_compte("713")],
        ["- Prod immobilisée", difference_compte("72")],
        ["- Subventions d'exploitations", difference_compte("74")],
        ["- Autres produits", difference_compte("75") + difference_compte("781") + difference_compte("791")],
        ["Produits financiers", difference_compte("76") + difference_compte("786") + difference_compte("796")],
        ["Produits exeptionnels", difference_compte("77") + difference_compte("787") + difference_compte("797")]
    ]

    # Écriture dans un fichier CSV
    with open("Compte_résultat.csv", "w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        writer.writerows(data)

racineCompte = NoeudCompte("",Decimal(), Decimal())
#racineCompte.sous_comptes[compteBanque.code] =compteBanque

if __name__ == '__main__':
    Balance = scandir(sys.argv[1])
    for compte in Balance.keys():
        (credit_balance, debit_balance) = Balance[compte]
        compte_a_classer = NoeudCompte(str(compte), Decimal(credit_balance), Decimal(debit_balance))
        racineCompte.classerSousCompte(compte_a_classer)        
    print(racineCompte)
    racineCompte.aggregerMontants()
    creer_bilan_csv(racineCompte)
    creer_compte_resultat_csv(racineCompte)
