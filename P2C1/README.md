# P2C1 — Restituez vos analyses avec les dashboards AI/BI

| Fichier | À quoi il sert |
|---|---|
| [`maquette-indicateur.png`](maquette-indicateur.png) | La maquette envoyée par Claire pour le nouvel indicateur |
| [`checklist-partage.md`](checklist-partage.md) | La fiche à remplir avant de publier |
| [`solution.sql`](solution.sql) | Les requêtes du corrigé |
| [`dashboard-engagement-frequence.lvdash.json`](dashboard-engagement-frequence.lvdash.json) | Le dashboard de référence, indicateur compris |

## Importer le dashboard de référence

Le fichier `.lvdash.json` contient tout le dashboard : jeux de données, mesures, visualisations et filtres. Si votre propre dashboard ne se comporte pas comme prévu, importez celui-ci et comparez.

1. Ouvrez **Dashboards** dans la barre latérale.
2. Cliquez sur la flèche à droite du bouton **Create dashboard**, puis sur **Import dashboard from file**.
3. Choisissez le fichier, puis cliquez sur **Import dashboard**.

Le dashboard est rangé dans votre dossier personnel. Il lit trois tables du schéma `frequence.socle` : `ecoutes`, `abonnements` et `ecoutes_enrichies`. Cette dernière est créée pendant le chapitre P1C3 ; si elle manque, la visualisation « Écoutes par genre » affichera une erreur.

Une fois importé, ouvrez l'onglet **Data** : le jeu de données `ecart_offres` porte la mesure `minutes_par_abonne`, celle que l'activité vous demande de construire.
