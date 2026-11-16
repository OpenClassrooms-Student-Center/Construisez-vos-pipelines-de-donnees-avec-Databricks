# P1C3 — Grille de vérification : la table `playlists`

> « Voilà les playlists, tu sauras quoi en faire. »
> — Claire

Pas de mode d'emploi, pas de description des colonnes. Avant de dire à Claire que la table est prête, passez-la à travers ces quatre points. Notez ce que vous avez obtenu dans la dernière colonne : c'est votre livrable.

Le fichier compte **33 034 lignes**, en-tête non compris.

| # | Point à vérifier | Comment le vérifier | Ce que j'ai obtenu |
|---|---|---|---|
| 1 | **La table est au bon endroit** : `frequence.socle.playlists`, et nulle part ailleurs | `SHOW TABLES IN frequence.socle;` | |
| 2 | **Elle est décrite** : la table, et les colonnes `id_playlist`, `id_titre` et `date_ajout` | Onglet **Overview** de la table dans le catalogue, ou `DESCRIBE TABLE EXTENDED frequence.socle.playlists;` | |
| 3 | **Les contrôles passent** : nombre de lignes, identifiants nuls, doublons, dates nulles | Les requêtes de contrôle du chapitre, appliquées à `playlists` | |
| 4 | **Le lineage est visible** : `ajouts_par_genre` a bien deux tables en amont | Onglet **Lineage** de `ajouts_par_genre`, puis **See Lineage Graph** | |

## Ce que vous devez regarder de près

**Le type de `date_ajout`.** Les dates du fichier sont écrites à la française (`01/12/2025`). Dans l'aperçu de l'assistant d'import, vérifiez le type proposé et la valeur affichée : le 1er décembre 2025 doit apparaître comme `2025-12-01`, pas comme `2025-01-12`, ni comme du texte. Une fois la table créée, `SELECT MIN(date_ajout), MAX(date_ajout)` doit renvoyer deux dates.

**Un contrôle qui ne renvoie pas zéro.** Ce n'est pas forcément une erreur de chargement. Avant de corriger quoi que ce soit, regardez les lignes concernées et demandez-vous ce qu'elles disent de la source.

## La question à trancher

Si ce fichier arrivait chaque jour, faudrait-il automatiser son ingestion ? Répondez en trois phrases, en vous appuyant sur les critères du chapitre.
