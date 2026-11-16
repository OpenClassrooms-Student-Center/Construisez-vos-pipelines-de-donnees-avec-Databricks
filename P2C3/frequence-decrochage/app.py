import os
from decimal import Decimal

import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

# --------------------------------------------------------------------------
# Paramètre métier : la SEULE valeur à modifier dans ce cours.
# 0.5 = on signale les abonnés dont les écoutes ont baissé d'au moins 50 %
# entre les 30 jours précédents et les 30 derniers jours.
# --------------------------------------------------------------------------
SEUIL_BAISSE = 0.5

# --------------------------------------------------------------------------
# 1. Connexion au SQL Warehouse
# Databricks Apps fournit l'identité de l'application (variables d'environnement
# lues par Config()). Aucun mot de passe ni jeton n'est écrit dans le code.
# --------------------------------------------------------------------------
cfg = Config()


def executer_requete(requete: str, parametres: dict) -> pd.DataFrame:
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
        credentials_provider=lambda: cfg.authenticate,
    ) as connexion:
        with connexion.cursor() as curseur:
            curseur.execute(requete, parametres)
            return curseur.fetchall_arrow().to_pandas()


# --------------------------------------------------------------------------
# 2. Règle de décrochage
# Mêmes définitions qu'au chapitre P1C4 : date de référence = dernière écoute
# du jeu de données ; abonné premium = offre premium active à cette date.
# On compare les écoutes des 30 derniers jours à celles des 30 jours précédents.
# --------------------------------------------------------------------------
REQUETE_DECROCHAGE = """
WITH ref AS (
  SELECT MAX(horodatage) AS date_ref FROM frequence.socle.ecoutes
),
premium_actifs AS (
  SELECT DISTINCT a.id_utilisateur
  FROM frequence.socle.abonnements a CROSS JOIN ref
  WHERE a.offre = 'premium'
    AND a.date_debut <= ref.date_ref
    AND (a.date_fin IS NULL OR a.date_fin > ref.date_ref)
),
periodes AS (
  SELECT e.id_utilisateur,
         COUNT_IF(e.horodatage >  ref.date_ref - INTERVAL 30 DAYS)              AS ecoutes_30j,
         COUNT_IF(e.horodatage <= ref.date_ref - INTERVAL 30 DAYS
              AND e.horodatage >  ref.date_ref - INTERVAL 60 DAYS)              AS ecoutes_30j_precedents
  FROM frequence.socle.ecoutes e CROSS JOIN ref
  WHERE e.horodatage > ref.date_ref - INTERVAL 60 DAYS
  GROUP BY e.id_utilisateur
)
SELECT p.id_utilisateur,
       p.ecoutes_30j_precedents,
       p.ecoutes_30j,
       ROUND(1 - p.ecoutes_30j / p.ecoutes_30j_precedents, 2) AS baisse
FROM periodes p
JOIN premium_actifs pa ON p.id_utilisateur = pa.id_utilisateur
WHERE p.ecoutes_30j_precedents > 0
  AND 1 - p.ecoutes_30j / p.ecoutes_30j_precedents >= :seuil
ORDER BY baisse DESC, p.ecoutes_30j_precedents DESC
"""

# --------------------------------------------------------------------------
# 3. Affichage Streamlit
# Streamlit relance tout le script à chaque interaction : quand le curseur
# bouge, la requête repart avec le nouveau seuil.
# --------------------------------------------------------------------------
st.set_page_config(page_title="Fréquence — décrochage premium", layout="wide")
st.title("Abonnés premium en perte d'engagement")

seuil = st.slider(
    "Baisse minimale des écoutes (30 derniers jours vs 30 jours précédents)",
    min_value=0.1,
    max_value=1.0,
    value=SEUIL_BAISSE,
    step=0.05,
    format="%.2f",
)

# Le seuil est transmis en Decimal : un float Python serait envoyé en FLOAT (32 bits)
# et 0.30 deviendrait 0.3000000119…, ce qui exclurait les baisses d'exactement 30 %.
liste = executer_requete(REQUETE_DECROCHAGE, {"seuil": Decimal(str(round(seuil, 2)))})

st.metric("Abonnés à relancer", len(liste))
st.dataframe(liste, use_container_width=True, hide_index=True)

st.download_button(
    label="Exporter pour l'outil de relance (CSV)",
    data=liste.to_csv(index=False).encode("utf-8"),
    file_name="frequence_relance.csv",
    mime="text/csv",
)
