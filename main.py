# 1. Importation et préparation des données
# 2. Calcul des salaires mensuels
# 3. Calcul des statistiques salariales
# 4. Affichage des résultats
# 5. Qualité du code, optimisation


# =============================================================================
# 1. Importation et préparation des données
# =============================================================================

# Import des modules python nécessaires
import json
import statistics

# Ouverture du fichier de données et enregistrement dans la variable "datas"
with open("datas/employes-data.json", "r", encoding="utf-8") as f:
    datas : dict = json.load(f)


# ============================================================================
# 2. Calcul des salaires mensuels
# ============================================================================

def calcul_salaire_mensuel(employe: dict,calculer_heures_vraiment_travaillees: bool = False) -> float:
    """Calcule le salaire mensuel d'un employé

    Args:
        employe (dict): dictionnaire des données de l'employé

    Returns:
        float: salaire mensuel calculé sur le taux horaire et les heures travaillées
    """

    # récupération des données à utiliser
    salaire: int = employe["hourly_rate"]
    temps_de_travail: int = employe["weekly_hours_worked"]
    heures_contrat: int = employe["contract_hours"]
    salaire_hebdo: float = 0

    # Calcul du salaire hebdomadaire sur la base horaire du contrat ou sur les heures vraiment travaillées
    if calculer_heures_vraiment_travaillees:
        if temps_de_travail <= heures_contrat:
            salaire_hebdo = salaire * temps_de_travail
        else:
            salaire_hebdo = salaire * heures_contrat

    # Mise à jour avec les heures supplémentaires
    if temps_de_travail > heures_contrat:
        ecart = temps_de_travail - heures_contrat
        salaire_hebdo += salaire * (ecart * 1.5)

    # Calcul du salaire mensuel
    salaire_mensuel: float = salaire_hebdo * 4
    return salaire_mensuel


# ============================================================================
# 3. Calcul des statistiques salariales
# ============================================================================

def calcul_stats_filiale(rapport_salarial: dict,filiale:str) -> tuple:
    """Calcule les statistiques salariales d'une filiale

    Args:
        rapport_salarial (dict): le rapport dont les stats doivent être tirées
        filiale (str): nom de la filiale concernée

    Returns:
        tuple: le salaire minumum, le salaire maximum et le salaire moyen pour une filiale
    """
    salaire_max: float = 0
    salaire_min: float = 1000000000000
    salaire_total: list = []
    salaire_moyen: float = 0
    count: int = 0

    for ligne in rapport_salarial:
        
        salaire_total.append(ligne["salary"])
        count += 1
        
        if ligne["salary"] > salaire_max:
            salaire_max = ligne["salary"]
        if ligne["salary"] < salaire_min:
            salaire_min = ligne["salary"]

    salaire_moyen = statistics.mean(salaire_total)

    return salaire_min, salaire_max, salaire_moyen
            

def calcul_stats_entreprise(rapport_complet: dict)-> dict:
    """Calcule les statistiques salariales d'une entreprise pour toutes ses filiales.
    
    Args:
        rapport_complet (dict): le rapport dont les stats doivent être tirées
    
    Returns:
        dict: le salaire minumum, le salaire maximum et le salaire moyen pour l'entreprise
    """

    salaire_max: float = 0
    salaire_min: float = 1000000000000
    salaire_total: list = []
    salaire_moyen: float = 0
    dict_stats: dict = {}
    count: int = 0

    for filiale in rapport_complet:
        
        min, max, moyen = calcul_stats_filiale(rapport_complet[filiale],filiale)
        dict_stats[filiale] = {
            "minimum": min,
            "maximum": max,
            "moyen": moyen
        }

        salaire_total.append(moyen)
        count += 1
        
        if max > salaire_max:
            salaire_max = max
        if min < salaire_min:
            salaire_min = min

    salaire_moyen = statistics.mean(salaire_total)

    dict_stats["ENTREPRISE"] = {
            "minimum": salaire_min,
            "maximum": salaire_max,
            "moyen": salaire_moyen
    }

    return dict_stats
    
# 6883.00€ salaire moyen avec le jeu de données adéquat

# ============================================================================
# 4. Affichage des résultats
# ============================================================================

def afficher_rapport_salaire(rapport: dict,nom_entreprise: str) -> None:

    print(f"{"="*59}")
    print(f"{nom_entreprise} : Salaires mensuels")
    print(f"{"="*59}")
    for ligne in rapport[nom_entreprise]:

        print(
            f"{ligne["name"]: <10} | {ligne["job"]: <15} | salaire mensuel: {ligne["salary"]:>10.2f}€"
        )
    print(f"{"="*59}\n")

def afficher_stats(rapport: dict,nom_entreprise: str)-> None:
    for filiale in rapport:
        print(f"{"="*59}")
        print(f"{filiale.upper()} : statistiques")
        print(f"{"="*59}")
        # print(rapport[filiale])

        print(f"{"le salaire le plus élevé est ":^40}{rapport[filiale]["maximum"]:>15.2f}€")

        print(f"{"le salaire le plus bas est ":^40}{rapport[filiale]["minimum"]:>15.2f}€")
        print(f"{"le salaire moyen est de ":^40}{rapport[filiale]["moyen"]:>15.2f}€")
        print(f"{"="*59}\n")


# ============================================================================
# Programme principal
# ============================================================================


rapport: dict = {}

for filiale in datas:
    cle = filiale.upper()
    rapport[cle] = []
    for line in datas[filiale]:
        salaire = calcul_salaire_mensuel(line,True)
        rapport[cle].append(
            {
                "name": line["name"],
                "job": line["job"],
                "salary": salaire,
            }
        )

rapport2 = calcul_stats_entreprise(rapport)

for ligne in rapport:
    afficher_rapport_salaire(rapport,ligne)
afficher_stats(rapport2,ligne)
print()



# print(rapport)
# print()
# stats: list = []
# for filiale in rapport:
#     stats.append({
#         # "filiale": filiale,
#         filiale: calcul_stats_filiale(rapport[filiale])})
#     # print(rapport[filiale])

# print(stats)
# print()