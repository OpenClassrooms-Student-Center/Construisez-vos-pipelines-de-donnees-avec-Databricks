# P2C2 — Grille de lecture du SQL généré par Genie

Une réponse de Genie se lit en partant du SQL, pas de la phrase qui l'accompagne. La phrase peut être parfaitement rédigée et le chiffre faux. Passez chaque requête sur ces trois points, dans l'ordre.

## Les trois points

**1. Les tables et les jointures**

- Les tables lues sont-elles celles qu'il faut, et seulement celles-là ?
- Si `ecoutes` est jointe à `abonnements`, la jointure porte-t-elle sur l'utilisateur **et** sur les dates de la période d'abonnement ?
- Une table jointe sert-elle à quelque chose dans la suite de la requête ?

**2. Les filtres**

- La période correspond-elle à la question ? Partir de la date du jour ou de la dernière date des données ne donne pas le même trimestre.
- L'offre est-elle filtrée quand la question en parle, et seulement dans ce cas ?
- Une valeur filtrée existe-t-elle vraiment dans la colonne (`'mobile'`, `'premium'`…) ?

**3. L'agrégation**

- Ce qui est compté ou additionné est-il bien ce que demande la question ?
- Pour un pourcentage : que vaut le dénominateur ?
- L'unité annoncée dans la réponse est-elle celle de la colonne ? Relisez la description de la colonne dans le catalogue.

## Question 1 — « quelle part des écoutes premium se fait sur mobile ce trimestre ? »

| Résultat annoncé par Genie |
|---|
| |

```sql
-- Collez ici le SQL généré
```

| Point | Validé ? | Ce que j'ai vu dans le SQL |
|---|:---:|---|
| 1. Tables et jointures | ☐ oui ☐ non | |
| 2. Filtres | ☐ oui ☐ non | |
| 3. Agrégation | ☐ oui ☐ non | |

Verdict : ☐ exploitable ☐ exploitable après correction de l'agent ☐ à réécrire en SQL

| Mon argumentation, en trois phrases |
|---|
| |

## Question 2 — « quels sont nos meilleurs abonnés ? »

| Résultat annoncé par Genie |
|---|
| |

| Définition de « meilleurs » retenue par Genie |
|---|
| |

Cette définition est-elle dite dans la réponse ? ☐ oui ☐ non

```sql
-- Collez ici le SQL généré
```

| Point | Validé ? | Ce que j'ai vu dans le SQL |
|---|:---:|---|
| 1. Tables et jointures | ☐ oui ☐ non | |
| 2. Filtres | ☐ oui ☐ non | |
| 3. Agrégation | ☐ oui ☐ non | |

Verdict : ☐ exploitable ☐ exploitable après correction de l'agent ☐ à réécrire en SQL

| Mon argumentation, en trois phrases |
|---|
| |

| Ce qu'il faudrait préciser, et à qui |
|---|
| |

## Deux réflexes à garder

Ne validez pas un point parce que le résultat « a l'air bon » : validez-le parce que vous l'avez lu dans le SQL.

Si vous corrigez la requête à la main, notez aussi ce qu'il faudrait changer dans l'agent (une instruction, un exemple de requête, une description de colonne). Sinon, la semaine prochaine, Claire retombera sur la même réponse.
