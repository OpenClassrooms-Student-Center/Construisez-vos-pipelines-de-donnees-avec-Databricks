# Outils

Rien dans ce dossier n'est nécessaire pour suivre le cours. Il est là pour ceux qui veulent comprendre d'où viennent les données, ou refaire une manipulation montrée en vidéo.

## `ecoutes_extrait_horodatage_fr.csv`

Les 3 000 premières écoutes de `ecoutes.csv`, avec les horodatages écrits à la française : `15/03/2026 18:42:07` au lieu de `2026-03-15 18:42:07`.

C'est le fichier utilisé dans le screencast du chapitre P1C3. Importez-le dans un schéma de test pour voir ce que fait l'assistant d'import face à ce format : la colonne `horodatage` arrive en texte, et la forcer en *timestamp* dans l'aperçu la vide. La conversion se fait ensuite en SQL :

```sql
SELECT to_timestamp(horodatage, 'dd/MM/yyyy HH:mm:ss') AS horodatage
FROM <votre_schema_de_test>.ecoutes_extrait_horodatage_fr;
```

Ne le chargez pas dans `frequence.socle` : ce n'est pas une table du socle.

## `generation-donnees/generate_frequence.py`

Le script qui produit les cinq fichiers CSV de Fréquence. Il tire ses valeurs au hasard, mais avec une graine fixe : relancé tel quel, il redonne exactement les fichiers du dépôt.

Il demande Python 3.10 ou plus récent, avec `numpy` et `pandas` :

```bash
pip install numpy pandas
cd outils/generation-donnees
python generate_frequence.py --out ./sortie
```

Comptez quelques secondes. Le dossier `sortie/` contient alors `ecoutes.csv`, `titres.csv`, `abonnements.csv`, `utilisateurs.csv` et `playlists.csv`.

Trois options :

| Option | Effet |
|---|---|
| `--out <dossier>` | Dossier où écrire les fichiers |
| `--horodatage fr` | Écrit les horodatages d'`ecoutes.csv` à la française |
| `--seed <nombre>` | Change la graine, donc les données. Par défaut : `2026` |

Changer la graine donne un jeu de données de même forme, mais avec d'autres valeurs : les résultats attendus indiqués dans le cours ne seront plus les bons.

Vérifié avec Python 3.13, numpy 2.5 et pandas 3.0. Une version très différente de numpy peut produire d'autres tirages pour la même graine.
