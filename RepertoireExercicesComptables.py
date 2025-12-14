"""
Ce module fournit l'ensemble des opérations relatives au répertoire des exercices comptables.
"""
from datetime import date
from decimal import Decimal
from json import load as load_json_file
from typing import List


class MouvementComptable:
    """ Représente un mouvement comptable. """

    def get_code_compte(self) -> str:
        """ Renvoie le code du compte modifié par le mouvement. """
        pass

    def get_libelle(self) -> str | None:
        """Renvoie, si présent, le libellé spécifique à ce mouvement. """
        pass

    def get_montant_debit(self) -> Decimal:
        """ Renvoie le montant au débit pour ce mouvement. """
        pass

    def get_montant_credit(self) -> Decimal:
        """ Renvoie le montant au crédit pour ce mouvement. """
        pass


class EcritureComptable:
    """ Représente une écriture comptable et ses mouvements. """

    def get_identifiant(self) -> str:
        """ Renvoie la clef identifiant l'écriture comptable. """
        pass

    def get_date(self) -> date:
        """ Renvoie la date de l'écriture comptable. """
        pass

    def get_libelle(self) -> str:
        """ Renvoie le libellé général de l'écriture comptable. """
        pass

    def get_liste_mouvements(self) -> List[MouvementComptable]:
        """ Renvoie la liste des mouvements associés à l'écriture comptable. """
        pass


class JournalComptable:
    """ Représente un journal regroupant des écritures comptables. """
    
    def get_liste_ecritures(self) -> List[EcritureComptable]:
        """ Renvoie la liste des écritures contenues dans le journal. """
        pass


class RepertoireExercice:
    """ Cette classe fournit les moyens d'accès aux journaux d'un exercice comptable. """
    
    def get_liste_journaux(self) -> List[JournalComptable]:
        """ Renvoie la liste des journaux dans le répertoire comptable de cet exercice. """
        pass


class RepertoireExercicesComptables:
    """ Cette classe fournit les moyens d'accès aux exercies comptables. """

    def get_exercice_per_year(year: int) -> RepertoireExercice:
        """ Fournit l'exercice en fonction de l'année. """
        pass


###############################################
############## IMPLEMENTATIONS ################
###############################################


class JsonBasedMouvementComptable(MouvementComptable):

    ZERO = Decimal()

    def __init__(self, json):
        super().__init__()
        self._json = json
    
    def get_code_compte(self) -> str:
        return self._json.get("compte")
    
    def get_libelle(self) -> str:
        return self._json.get("libelle")
    
    def get_montant_credit(self) -> Decimal:
        credit = JsonBasedMouvementComptable.ZERO
        json_credit = self._json.get("credit")
        if json_credit is not None:
            credit = json_credit
        return credit
    
    def get_montant_debit(self) -> Decimal:
        debit = JsonBasedMouvementComptable.ZERO
        json_debit = self._json.get("debit")
        if json_debit is not None:
            debit = json_debit
        return debit
    

class JsonFileBasedEcritureComptable(EcritureComptable):

    def __init__(self, opened_file_pointer, identifiant):
        super().__init__()
        self._id = identifiant
        self._json_content = load_json_file(opened_file_pointer, parse_float=Decimal, parse_int=Decimal)
        self._mouvement_list = []
        for mouvement_json in self._json_content.get("ventilation"):
            self._mouvement_list.append(JsonBasedMouvementComptable(mouvement_json))
    
    def get_identifiant(self) -> str:
        return self._id

    def get_date(self) -> date:
        return date.fromisoformat(self._json_content.get("date"))
    
    def get_libelle(self) -> str:
        return self._json_content.get("libelle")
    
    def get_liste_mouvements(self) -> List[MouvementComptable]:
        return self._mouvement_list
    

class FileBasedReportoireExercice(RepertoireExercice):
    pass


class SimpleFileBasedRepertoireExercicesComptables(RepertoireExercicesComptables):

    def __init__(self, base_path):
        super().__init__()
        self._base_path = base_path
            