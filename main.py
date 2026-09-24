# 1. Importation et préparation des données
# 2. Calcul des salaires mensuels
# 3. Calcul des statistiques salariales
# 4. Affichage des résultats
# 5. Qualité du code, optimisation

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
    # print(
    #     f"{employe["name"]: <10} | {employe["job"]: <15} | salaire mensuel: {salaire_mensuel:.2f}€"
    # )

    # Calcul du salaire mensuel
    salaire_mensuel: float = salaire_hebdo * 4
    return salaire_mensuel

# =============================================================================
# 1. Importation et préparation des données
# =============================================================================
import json

with open("datas/employes-data.json", "r", encoding="utf-8") as f:
    data : dict = json.load(f)


rapport: dict = {}
# print(data)

for filiale in data:
    # print(filiale)
    # print()
    rapport[filiale] = []
    for line in data[filiale]:
        # print(line)
        # print(
        #     f"{line["name"]: <12} | {line["job"]: <15} | {line["hourly_rate"]: <5} | {line["weekly_hours_worked"]: <5} | {line["contract_hours"]: <5}"
        # )
        salaire = calcul_salaire_mensuel(line)
        rapport[filiale].append(
            {
                "name": line["name"],
                "job": line["job"],
                "salary": salaire,
            }
        )
        print(
            f"{line["name"]: <10} | {line["job"]: <15} | salaire mensuel: {salaire:.2f}€"
        )
    # for key, value in line.items():
    #     print(f"{key: <25} : {value}")
    #     print(f"{value: <25} | ")
    # print(key)
    # print(value)
    print()
print(rapport)
for filiale in rapport:
    print(rapport[filiale])
