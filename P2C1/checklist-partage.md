# P2C1 — Checklist de partage : avant de publier le dashboard

Jeudi, le dashboard sera ouvert en séance devant le comité marketing. Deux des participants sont des prestataires externes. Avant de cliquer sur **Publish**, remplissez cette fiche : elle sert à choisir le mode de publication, et votre justification s'appuiera dessus.

## 1. Ce que lit le dashboard

Listez chaque jeu de données (onglet **Data** du dashboard) et les tables qu'il interroge. Pour vérifier, ouvrez l'onglet **Lineage** de chaque table dans le catalogue : le dashboard doit y apparaître en aval.

| Jeu de données | Tables lues | Table restreinte ? |
|---|---|:---:|
| | | ☐ oui ☐ non |
| | | ☐ oui ☐ non |
| | | ☐ oui ☐ non |
| | | ☐ oui ☐ non |

Rappel du chapitre P1C3 : `frequence.socle.utilisateurs` est la table dont vous avez restreint l'accès.

## 2. Qui va le lire

| Lecteurs | Combien | Ce qu'ils ont le droit de voir |
|---|---:|---|
| Équipe marketing de Fréquence | | |
| Prestataires externes | 2 | |

- [ ] Chaque lecteur a un accès au compte Databricks de l'entreprise. Sans cela, il ne pourra pas ouvrir le dashboard, quel que soit le mode choisi.
- [ ] Je partage à un **groupe** (par exemple `marketing`), pas à une liste de personnes.

## 3. Qui paie l'ouverture

- Warehouse qui exécutera les requêtes :
- Délai d'arrêt automatique :

Chaque ouverture du dashboard peut réveiller ce warehouse s'il est arrêté, et le temps qu'il reste allumé se paie.

## 4. Le mode de publication

La fenêtre **Publish** propose deux modes :

- **Share data permission** (par défaut) : le dashboard interroge les tables avec vos droits.
- **Individual data permission** : il les interroge avec les droits de la personne qui l'ouvre.

Mode retenu :

- [ ] Share data permission
- [ ] Individual data permission

| Ma justification, en deux phrases |
|---|
| |

## 5. À refaire à chaque nouvel indicateur

Le jour où une visualisation lira une table de plus, le mode choisi aujourd'hui peut ne plus convenir. Avant chaque republication, reprenez la section 1.
