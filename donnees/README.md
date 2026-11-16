# Les données de Fréquence

Quatre fichiers forment le socle que vous chargerez au chapitre P1C3, dans le catalogue `frequence`, schéma `socle`. Un cinquième, `playlists.csv`, arrive plus tard : il se trouve dans le dossier [`P1C3/`](../P1C3/), avec l'activité qui l'utilise.

| Fichier | Lignes | Une ligne correspond à |
|---|---:|---|
| `ecoutes.csv` | 498 586 | une écoute d'un titre par un utilisateur |
| `titres.csv` | 1 222 | un titre du catalogue musical |
| `abonnements.csv` | 4 030 | une période d'abonnement d'un utilisateur, à une offre donnée |
| `utilisateurs.csv` | 3 000 | un utilisateur (profil pseudonymisé) |

Comparez toujours le nombre de lignes de vos tables à cette colonne après un chargement.

## `ecoutes.csv`

| Colonne | Type | Description |
|---|---|---|
| `id_ecoute` | entier | Identifiant de l'écoute |
| `id_utilisateur` | entier | Utilisateur qui écoute (voir `utilisateurs.csv`) |
| `id_titre` | entier | Titre écouté (voir `titres.csv`) |
| `horodatage` | date et heure | Début de l'écoute, au format `2026-03-15 18:42:07` |
| `duree_ecoutee` | entier | Durée réellement écoutée, **en secondes** |
| `terminal` | texte | Appareil utilisé : `mobile`, `web`, `desktop`, `enceinte` ou `tv` |

Les écoutes vont du 1er octobre 2025 au 30 septembre 2026.

## `titres.csv`

| Colonne | Type | Description |
|---|---|---|
| `id_titre` | entier | Identifiant du titre |
| `titre` | texte | Nom du titre |
| `artiste` | texte | Nom de l'artiste |
| `genre` | texte | Un des douze genres du catalogue (Pop, Rap FR, Rock, Électro, Jazz…) |
| `duree_secondes` | entier | Durée du titre, en secondes. À ne pas confondre avec `ecoutes.duree_ecoutee`, la part réellement écoutée |
| `annee_sortie` | entier | Année de sortie |

## `abonnements.csv`

| Colonne | Type | Description |
|---|---|---|
| `id_abonnement` | entier | Identifiant de la période d'abonnement |
| `id_utilisateur` | entier | Utilisateur concerné |
| `offre` | texte | `gratuit` ou `premium` |
| `date_debut` | date | Premier jour de la période, au format `2026-03-15` |
| `date_fin` | date | Jour où la période s'arrête, exclu. Vide si la période est toujours en cours |
| `statut` | texte | `actif`, `resilie` ou `termine`, tel qu'exporté par l'outil de facturation |

Un même utilisateur peut avoir plusieurs lignes : chaque changement d'offre ouvre une nouvelle période. Les périodes commencent pour certaines avant octobre 2025, puisque des abonnés étaient déjà là avant le début des écoutes.

## `utilisateurs.csv`

| Colonne | Type | Description |
|---|---|---|
| `id_utilisateur` | entier | Identifiant pseudonymisé de l'utilisateur |
| `tranche_age` | texte | `18-24`, `25-34`, `35-44`, `45-54`, `55-64` ou `65+` |
| `region` | texte | Une des treize régions de France métropolitaine |
| `date_inscription` | date | Date de création du compte |

Ce fichier contient des données personnelles, même pseudonymisées. Au chapitre P1C3, vous en restreindrez l'accès.

## D'où viennent ces données

Elles sont produites par un script, à partir de règles écrites pour le cours (rythmes d'écoute, changements d'offre, goûts selon l'âge). Le script et son mode d'emploi sont dans [`outils/`](../outils/). Vous n'en avez pas besoin pour suivre le cours.
