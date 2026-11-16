-- =============================================================================
-- P2C2 — Requête de référence pour la question 1
-- « quelle part des écoutes premium se fait sur mobile ce trimestre ? »
-- À comparer au SQL généré par Genie. La question 2 n'a pas de requête de
-- référence : elle demande d'abord une définition de « meilleurs ».
-- =============================================================================

WITH ref AS (
  -- « Ce trimestre » = le dernier trimestre présent dans les données
  SELECT DATE_TRUNC('quarter', MAX(horodatage)) AS debut_trimestre
  FROM frequence.socle.ecoutes
),
ecoutes_premium AS (
  SELECT e.terminal
  FROM frequence.socle.ecoutes e
  -- Jointure datée : l'offre est celle active à la date de l'écoute
  JOIN frequence.socle.abonnements a
    ON  e.id_utilisateur = a.id_utilisateur
    AND e.horodatage >= a.date_debut
    AND e.horodatage <  COALESCE(a.date_fin, CURRENT_TIMESTAMP())
  CROSS JOIN ref
  WHERE a.offre = 'premium'
    AND e.horodatage >= ref.debut_trimestre
)
SELECT COUNT(*)                                              AS ecoutes_premium,
       COUNT(*) FILTER (WHERE terminal = 'mobile')           AS ecoutes_premium_mobile,
       ROUND(100.0 * COUNT(*) FILTER (WHERE terminal = 'mobile') / COUNT(*), 2) AS part_mobile_pct
FROM ecoutes_premium;

-- Attendu : 71 014 écoutes premium au troisième trimestre 2026, dont 39 156
-- sur mobile, soit 55,14 %.
--
-- Pour mémoire : avec une jointure sur id_utilisateur seul, on compte
-- 86 663 écoutes « premium » et on trouve 57,51 %.
