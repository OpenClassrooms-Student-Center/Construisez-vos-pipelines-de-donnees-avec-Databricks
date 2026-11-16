-- =============================================================================
-- P1C4 — Solution de l'activité : les trois questions de Claire
-- À exécuter dans l'éditeur SQL, sur le Serverless Starter Warehouse.
-- Les valeurs attendues sont indiquées en commentaire.
-- =============================================================================


-- 0. Contrôle de couverture de la jointure ecoutes × abonnements ---------------
-- Une écoute doit se rattacher à une seule période d'abonnement : celle qui est
-- active à la date de l'écoute. Les trois nombres doivent être égaux.

SELECT COUNT(*) AS nb_lignes_ecoutes
FROM frequence.socle.ecoutes;                                -- attendu : 498 586

SELECT COUNT(*)                AS ecoutes_total,            -- attendu : 498 586
       COUNT(a.id_utilisateur) AS ecoutes_rattachees        -- attendu : 498 586
FROM frequence.socle.ecoutes e
LEFT JOIN frequence.socle.abonnements a
  ON  e.id_utilisateur = a.id_utilisateur
  AND e.horodatage >= a.date_debut
  AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP());

-- Pour mémoire : avec la condition sur id_utilisateur seule, ecoutes_total
-- monte à 679 356. Les écoutes des abonnés qui ont changé d'offre sont comptées
-- une fois par période d'abonnement : c'est la duplication que le contrôle révèle.


-- 1. Saisonnalité mensuelle ---------------------------------------------------
-- Nombre d'écoutes par mois, sur les douze mois.
-- Aucune jointure : la question ne parle pas d'offre.

SELECT DATE_TRUNC('month', horodatage) AS mois, COUNT(*) AS nb_ecoutes
FROM frequence.socle.ecoutes
GROUP BY mois
ORDER BY mois;

-- Douze lignes, de 38 038 écoutes (février 2026) à 46 403 (décembre 2025),
-- avec un creux en juillet-août (39 543 et 39 056).


-- 2. Terminal le plus utilisé par offre ---------------------------------------
-- Pour chaque offre, le terminal qui totalise le plus d'écoutes.
-- L'offre est celle active à la date de l'écoute : jointure datée obligatoire.

WITH par_terminal AS (
  SELECT a.offre, e.terminal, COUNT(*) AS nb_ecoutes
  FROM frequence.socle.ecoutes e
  JOIN frequence.socle.abonnements a
    ON  e.id_utilisateur = a.id_utilisateur
    AND e.horodatage >= a.date_debut
    AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
  GROUP BY a.offre, e.terminal
)
SELECT offre, terminal, nb_ecoutes
FROM par_terminal
-- QUALIFY filtre le résultat de la fonction de fenêtre, comme HAVING filtre un agrégat
QUALIFY ROW_NUMBER() OVER (PARTITION BY offre ORDER BY nb_ecoutes DESC) = 1;

-- gratuit : mobile, 153 213 écoutes
-- premium : mobile, 157 766 écoutes
-- Retirez la ligne QUALIFY pour voir le détail : les premium écoutent aussi sur
-- enceinte (39 868) et sur télévision (17 152), les gratuits jamais.


-- 3. Part des abonnés premium sans écoute depuis 30 jours ---------------------
-- Parmi les abonnés dont l'offre premium est active à la date de référence,
-- la part de ceux qui n'ont aucune écoute dans les 30 jours qui précèdent.
-- Date de référence : la dernière écoute du jeu de données, pas la date du jour.
-- Les dates d'abonnement font foi, pas la colonne statut.

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
actifs_30j AS (
  SELECT DISTINCT e.id_utilisateur
  FROM frequence.socle.ecoutes e CROSS JOIN ref
  WHERE e.horodatage > ref.date_ref - INTERVAL 30 DAYS
)
SELECT 100.0 * COUNT(*) FILTER (WHERE x.id_utilisateur IS NULL) / COUNT(*) AS part_sans_ecoute
FROM premium_actifs p
LEFT JOIN actifs_30j x ON p.id_utilisateur = x.id_utilisateur;

-- 1 176 abonnés premium actifs au 30 septembre 2026, dont 111 sans écoute
-- dans les 30 derniers jours : 9,44 %.
-- Avec un filtre statut = 'actif' à la place des dates, on part de 1 193
-- premium : 24 lignes sont encore « actif » alors que leur date de fin est passée.
-- Cette définition est celle que reprend l'application du chapitre P2C3.
