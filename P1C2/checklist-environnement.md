# P1C2 — Checklist : votre environnement est-il prêt ?

Les fichiers de Fréquence arrivent demain. Aujourd'hui, assurez-vous que tout fonctionne, pour ne pas découvrir un problème de compte ou de warehouse au moment de charger les données. Cochez chaque point au fur et à mesure.

## Le compte

- [ ] J'ai créé mon compte depuis la page **Free Edition**, et non l'essai gratuit (*Try Databricks*) : on ne m'a demandé ni moyen de paiement, ni compte AWS, Azure ou Google Cloud.
- [ ] J'ai ajouté l'adresse de mon espace de travail aux favoris de mon navigateur.

## Le calcul

- [ ] Dans l'éditeur SQL, `SELECT 1 AS test_connexion;` renvoie `1`.
- [ ] Dans **SQL Warehouses**, le warehouse *Serverless Starter Warehouse* passe à l'état *Running* pendant l'exécution.
- [ ] Dans un notebook, une cellule SQL renvoie un résultat, avec le compute serverless sélectionné en haut du notebook.

## Le même résultat, aux deux endroits

Exécutez cette requête dans un notebook, puis dans l'éditeur SQL :

```sql
SELECT COUNT(*) AS nb_courses FROM samples.nyctaxi.trips;
```

- [ ] Le notebook et l'éditeur SQL renvoient le même nombre de courses.

## Les zones de l'interface

Pour chaque zone, notez en quelques mots à quoi elle sert.

| Zone | Je l'ai trouvée | À quoi elle sert |
|---|:---:|---|
| Workspace | ☐ | |
| Catalog | ☐ | |
| SQL Editor | ☐ | |
| SQL Warehouses | ☐ | |
| Dashboards | ☐ | |

## Si un point bloque

- **On vous demande un moyen de paiement ou un fournisseur cloud** : vous êtes sur l'essai gratuit. Revenez à la page Free Edition et recommencez l'inscription.
- **La requête ne se termine pas** : le warehouse démarre à la première requête. Regardez son état dans **SQL Warehouses** et patientez jusqu'à *Running*.
- **Le notebook renvoie une erreur alors que l'éditeur fonctionne** : le notebook n'a pas de compute sélectionné. Choisissez le compute serverless dans le sélecteur en haut, puis relancez la cellule.
