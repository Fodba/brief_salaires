# 1. Importation et préparation des données
# 2. Calcul des salaires mensuels
# 3. Calcul des statistiques salariales
# 4. Affichage des résultats
# 5. Qualité du code, optimisation


# =============================================================================
# 1. Importation et préparation des données
# =============================================================================

import json

with open("datas/employes-data.json", "r", encoding="utf-8") as f:
    data : dict = json.load(f)


# ============================================================================
# 2. Calcul des salaires mensuels
# ============================================================================

def calcul_salaire_mensuel(employe: dict) -> float:
    """
    Calcule le salaire mensuel d'un employé
    Args:
        employe : dictionnaire des données de l'employé
    Returns:
        float: salaire mensuel calculé sur le taux horaire et les heures travaillées
    """

    # récupération des données à utiliser
    salaire: int = employe["hourly_rate"]
    temps_de_travail: int = employe["weekly_hours_worked"]
    heures_contrat: int = employe["contract_hours"]

    # Calcul du salaire hebdomadaire sur la base horaire du contrat
    salaire_hebdo: float = salaire * heures_contrat

    # Mise à jour avec les heures supplémentaires
    if temps_de_travail > heures_contrat:
        ecart = temps_de_travail - heures_contrat
        salaire_hebdo += (salaire * 1.5) * ecart

    # Calcul du salaire mensuel
    salaire_mensuel: float = salaire_hebdo * 4
    return salaire_mensuel


# ============================================================================
# 3. Calcul des statistiques salariales
# ============================================================================

def calcul_stats_filiale(rapport_salarial: dict,filiale:str) -> tuple:
    """"""
    salaire_max: float = 0
    salaire_min: float = 1000000000000
    salaire_total: float = 0
    salaire_moyen: float = 0
    count: int = 0

    for ligne in rapport_salarial:
        
        salaire_total += ligne["salary"]
        count += 1
        
        if ligne["salary"] > salaire_max:
            salaire_max = ligne["salary"]
        if ligne["salary"] < salaire_min:
            salaire_min = ligne["salary"]

    salaire_moyen = salaire_total / count

    print(f"{"="*50}")
    print(f"{filiale.upper()} : statistiques")
    print(f"{"="*50}")
    print(f"le salaire le plus élevé est {salaire_max:.2f}€")

    print(f"le salaire le plus bas est {salaire_min:.2f}€")
    print(f"le salaire moyen est de {salaire_moyen:.2f}€")
    print(f"{"="*50}")
    return salaire_min,salaire_max,salaire_moyen
            

def calcul_stats_entreprise(rapport_complet: dict)-> dict:
    # print(rapport_complet)

    salaire_max: float = 0
    salaire_min: float = 1000000000000
    salaire_total: float = 0
    salaire_moyen: float = 0
    count: int = 0

    for filiale in rapport_complet:
        
        min, max, moyen = calcul_stats_filiale(rapport_complet[filiale],filiale)

        salaire_total += moyen
        count += 1

        
        
        if max > salaire_max:
            salaire_max = max
        if min < salaire_min:
            salaire_min = min

    salaire_moyen = salaire_total / count

    print(f"{"="*50}")
    print(f"Entreprise : statistiques globales")
    print(f"{"="*50}")
    print(f"le salaire le plus élevé est {salaire_max:.2f}€")

    print(f"le salaire le plus bas est {salaire_min:.2f}€")
    print(f"le salaire moyen est de {salaire_moyen:.2f}€")
    

# ============================================================================
# 4. Affichage des résultats
# ============================================================================

rapport: dict = {}

for filiale in data:
    cle = filiale.upper()
    rapport[cle] = []
    print(f"{"="*50}")
    print(f"{cle} : Salaires mensuels")
    print(f"{"="*50}")
    for line in data[filiale]:
        salaire = calcul_salaire_mensuel(line)
        rapport[cle].append(
            {
                "name": line["name"],
                "job": line["job"],
                "salary": salaire,
            }
        )
        print(
            f"{line["name"]: <10} | {line["job"]: <15} | salaire mensuel: {salaire:>8.2f}€"
        )



calcul_stats_entreprise(rapport)


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