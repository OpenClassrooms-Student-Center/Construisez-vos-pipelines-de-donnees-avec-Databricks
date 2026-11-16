# Construisez vos pipelines de données avec Databricks

Ce dépôt accompagne le cours OpenClassrooms. Il contient les données de **Fréquence**, le service de streaming musical fictif qui sert de fil rouge, et les documents à télécharger pour les activités « À vous de jouer ».

Vous n'avez besoin ni de Git ni de cloner quoi que ce soit. Pour récupérer un fichier, ouvrez-le sur GitHub et cliquez sur l'icône de téléchargement (*Download raw file*). Pour tout récupérer d'un coup : bouton **Code**, puis **Download ZIP**. Vous chargerez ensuite les fichiers dans votre espace Databricks Free Edition depuis votre ordinateur.

## Ce que contient le dépôt

| Dossier | Chapitre | Contenu |
|---|---|---|
| [`donnees/`](donnees/) | P1C3 | Les quatre fichiers du socle de Fréquence et leur dictionnaire |
| [`P1C2/`](P1C2/) | Prenez en main votre espace de travail Databricks | La checklist de vérification de votre environnement |
| [`P1C3/`](P1C3/) | Trouvez et chargez vos données dans le Lakehouse | Le fichier `playlists.csv`, la grille de vérification et la solution |
| [`P1C4/`](P1C4/) | Interrogez vos données avec le SQL Warehouse | L'énoncé des trois questions de Claire et la solution |
| [`P2C1/`](P2C1/) | Restituez vos analyses avec les dashboards AI/BI | La maquette de l'indicateur, la checklist de partage, la solution et le dashboard de référence |
| [`P2C2/`](P2C2/) | Interrogez vos données en langage naturel avec Genie | L'énoncé des deux questions, la grille de lecture du SQL et la requête de référence |
| [`P2C3/`](P2C3/) | Déployez une application avec Databricks Apps et Streamlit | L'énoncé du nouveau besoin et le code de l'application `frequence-decrochage` |
| [`outils/`](outils/) | — | Le générateur du jeu de données et un extrait daté à la française |

Les corrigés détaillés sont dans le cours, à la fin de chaque chapitre. Les fichiers `solution.sql` reprennent seulement les requêtes de ces corrigés, pour vous éviter de les recopier. Ouvrez-les une fois l'activité terminée : l'intérêt de l'exercice, c'est le raisonnement qui mène à la requête.

## Avant de commencer

Les données sont **synthétiques**. Les titres, les artistes et les abonnés sont inventés, et aucun fichier ne contient de donnée sur une personne réelle.

Elles couvrent une période fixe : du **1er octobre 2025 au 30 septembre 2026**. Retenez cette date de fin. Quand Claire parle de « ce mois-ci » ou de « ce trimestre », la référence est la dernière date présente dans les données, pas la date du jour.

Tous les fichiers sont au format CSV : séparateur virgule, ligne d'en-tête, encodage UTF-8.
