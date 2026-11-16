-- =============================================================================
-- P1C3 — Solution de l'activité : la table frequence.socle.playlists
-- Le chargement se fait avec l'assistant d'import (New > Add or upload data >
-- Create or modify table), destination frequence > socle > playlists.
-- Les valeurs attendues sont indiquées en commentaire.
-- =============================================================================

-- 1. Documenter la table et ses colonnes clés --------------------------------

COMMENT ON TABLE frequence.socle.playlists IS
  'Grain : un ajout d’un titre à une playlist. Source : export de la plateforme d’écoute, chargé à la main. Fraîcheur : ponctuelle, ajouts du 06/06/2025 au 30/09/2026. Propriétaire : équipe data. Attention : un même titre peut figurer deux fois dans une playlist, ajouté à des dates différentes.';

ALTER TABLE frequence.socle.playlists
  ALTER COLUMN id_playlist COMMENT 'Identifiant de la playlist (une playlist regroupe plusieurs lignes)';

ALTER TABLE frequence.socle.playlists
  ALTER COLUMN id_titre COMMENT 'Titre ajouté, à joindre à frequence.socle.titres';

ALTER TABLE frequence.socle.playlists
  ALTER COLUMN date_ajout COMMENT 'Date d’ajout du titre à la playlist (fichier source au format JJ/MM/AAAA)';


-- 2. Contrôles ----------------------------------------------------------------

-- Nombre de lignes, à comparer au fichier                     -- attendu : 33 034
SELECT COUNT(*) AS nb_lignes
FROM frequence.socle.playlists;

-- Identifiants nuls                                           -- attendu : 0
SELECT COUNT(*) AS id_nuls
FROM frequence.socle.playlists
WHERE id_playlist IS NULL OR id_titre IS NULL;

-- Dates nulles, y compris celles perdues à la conversion      -- attendu : 0
SELECT COUNT(*) AS dates_nulles
FROM frequence.socle.playlists
WHERE date_ajout IS NULL;

-- Bornes des dates : deux dates lisibles                      -- attendu : 2025-06-06 et 2026-09-30
SELECT MIN(date_ajout) AS premier_ajout, MAX(date_ajout) AS dernier_ajout
FROM frequence.socle.playlists;

-- Doublons sur le couple (playlist, titre)                    -- attendu : 37 lignes
-- Ce n'est pas une erreur de chargement : le même titre a été ajouté deux fois
-- à la même playlist, à des dates différentes. On le consigne dans la description.
SELECT id_playlist, id_titre, COUNT(*) AS nb_ajouts
FROM frequence.socle.playlists
GROUP BY id_playlist, id_titre
HAVING COUNT(*) > 1;


-- 3. Table dérivée ------------------------------------------------------------

CREATE TABLE frequence.socle.ajouts_par_genre AS
SELECT t.genre, COUNT(*) AS nb_ajouts
FROM frequence.socle.playlists p
JOIN frequence.socle.titres t ON p.id_titre = t.id_titre
GROUP BY t.genre;

-- Douze genres, menés par Rap FR (6 396), Pop (5 948) et Rock (4 236)
SELECT * FROM frequence.socle.ajouts_par_genre ORDER BY nb_ajouts DESC;

-- Le lineage d'ajouts_par_genre (onglet Lineage > See Lineage Graph) doit
-- montrer playlists et titres en amont, et rien en aval.
