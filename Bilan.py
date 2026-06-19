from decimal import Decimal
from Balance import scandir
import sys

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



    

racineCompte = NoeudCompte("",Decimal(), Decimal())
#racineCompte.sous_comptes[compteBanque.code] =compteBanque

if __name__ == '__main__':
    Balance = scandir(sys.argv[1])
    for compte in Balance.keys():
        (credit_balance, debit_balance) = Balance[compte]
        compte_a_classer = NoeudCompte(str(compte), Decimal(credit_balance), Decimal(debit_balance))
        racineCompte.classerSousCompte(compte_a_classer)        
    print(racineCompte)