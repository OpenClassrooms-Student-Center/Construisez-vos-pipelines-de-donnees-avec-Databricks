-- =============================================================================
-- P2C1 — Solution de l'activité : minutes d'écoute par abonné, par offre
-- Reformulation : durée totale écoutée, divisée par le nombre d'abonnés
-- distincts ayant écouté, par offre active à la date de chaque écoute,
-- sur la période filtrée.
-- =============================================================================


-- 1. La requête de contrôle (point 4 de l'activité) ---------------------------
-- À exécuter dans l'éditeur SQL. Elle agrège toute la période : elle sert à
-- recalculer le chiffre à la main, pas à alimenter le dashboard.

SELECT a.offre,
       SUM(e.duree_ecoutee)                                           AS duree_totale_secondes,
       COUNT(DISTINCT e.id_utilisateur)                               AS abonnes_actifs,
       SUM(e.duree_ecoutee) / 60.0 / COUNT(DISTINCT e.id_utilisateur) AS minutes_par_abonne
FROM frequence.socle.ecoutes e
-- Jointure datée du chapitre P1C4 : une écoute, une seule période d'abonnement
JOIN frequence.socle.abonnements a
  ON  e.id_utilisateur = a.id_utilisateur
  AND e.horodatage >= a.date_debut
  AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
GROUP BY a.offre;

-- gratuit : 1 975 abonnés actifs, 265 minutes par abonné
-- premium : 1 387 abonnés actifs, 598 minutes par abonné

-- Contrôle sur un mois, premium, septembre 2026                -- attendu : 63 minutes
SELECT SUM(e.duree_ecoutee) / 60.0 / COUNT(DISTINCT e.id_utilisateur) AS minutes_par_abonne
FROM frequence.socle.ecoutes e
JOIN frequence.socle.abonnements a
  ON  e.id_utilisateur = a.id_utilisateur
  AND e.horodatage >= a.date_debut
  AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
WHERE a.offre = 'premium'
  AND e.horodatage >= '2026-09-01' AND e.horodatage < '2026-10-01';


-- 2. Le jeu de données du dashboard -------------------------------------------
-- Pour que l'indicateur réagisse au filtre de période, le jeu de données garde
-- le grain jour × offre × abonné. Le ratio n'est pas calculé ici : il est
-- défini comme une mesure (Add custom calculation), recalculée à chaque filtre.

SELECT DATE(e.horodatage)    AS jour,
       a.offre,
       e.id_utilisateur,
       SUM(e.duree_ecoutee)  AS duree_ecoutee,
       COUNT(*)              AS nb_ecoutes
FROM frequence.socle.ecoutes e
JOIN frequence.socle.abonnements a
  ON  e.id_utilisateur = a.id_utilisateur
  AND e.horodatage >= a.date_debut
  AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
GROUP BY DATE(e.horodatage), a.offre, e.id_utilisateur;

-- Mesure à créer dans le jeu de données, nommée minutes_par_abonne :
--
--   SUM(duree_ecoutee) / 60.0 / COUNT(DISTINCT id_utilisateur)
--
-- Le nombre d'abonnés distincts ne s'additionne pas d'un jour à l'autre :
-- c'est pour cela qu'on ne pré-agrège pas au grain jour × offre.


-- 3. Les deux variantes fausses, pour comparer les ordres de grandeur ---------

-- Durée moyenne d'une écoute, pas d'un abonné       -- gratuit 2,46 min, premium 2,90 min
SELECT a.offre, AVG(e.duree_ecoutee) / 60.0 AS minutes_par_ecoute
FROM frequence.socle.ecoutes e
JOIN frequence.socle.abonnements a
  ON  e.id_utilisateur = a.id_utilisateur
  AND e.horodatage >= a.date_debut
  AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
GROUP BY a.offre;

-- Moyenne des moyennes par abonné                    -- gratuit 2,47 min, premium 2,88 min
WITH par_abonne AS (
  SELECT a.offre, e.id_utilisateur, AVG(e.duree_ecoutee) / 60.0 AS minutes_moyennes
  FROM frequence.socle.ecoutes e
  JOIN frequence.socle.abonnements a
    ON  e.id_utilisateur = a.id_utilisateur
    AND e.horodatage >= a.date_debut
    AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
  GROUP BY a.offre, e.id_utilisateur
)
SELECT offre, AVG(minutes_moyennes) AS moyenne_des_moyennes
FROM par_abonne
GROUP BY offre;
