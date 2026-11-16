# frequence-decrochage

Une application Streamlit qui liste les abonnés premium dont les écoutes ont baissé d'un mois sur l'autre. Claire règle le seuil avec un curseur et exporte la liste en CSV pour son outil de relance.

| Fichier | Rôle |
|---|---|
| `app.py` | Le code de l'application : connexion au warehouse, requête de décrochage, affichage |
| `app.yaml` | La commande de lancement, et la variable qui reçoit l'identifiant du warehouse |
| `requirements.txt` | Les dépendances Python |

La règle de décrochage reprend les définitions du chapitre P1C4. La date de référence est la dernière écoute du jeu de données. Un abonné premium est un abonné dont l'offre premium est active à cette date. On compare ses écoutes des 30 derniers jours à celles des 30 jours précédents.

## Déployer l'application en Free Edition

Comptez une quinzaine de minutes, dont quelques-unes d'attente.

**1. Déposer le code.** Dans **Workspace**, ouvrez votre dossier personnel et créez un dossier `frequence-decrochage` (**Create** › **Folder**). Glissez-y les trois fichiers du tableau ci-dessus, ou passez par le menu ⋮ du dossier › **Import**.

**2. Créer l'application.** Ouvrez le sélecteur d'applications, en haut à droite, puis **Databricks Apps** › **+ Create app** › **Create a custom app**. Nommez-la `frequence-decrochage`. L'étape *Configure Git repository* est facultative : passez-la.

**3. Lui donner un warehouse.** À l'étape *Configure*, cliquez sur **+ Add resource** › **SQL warehouse**. Choisissez le *Serverless Starter Warehouse*, la permission *Can use*, et gardez la clé proposée : `sql-warehouse`. C'est le nom que `app.yaml` attend. Cliquez sur **Create app**, puis patientez deux ou trois minutes, le temps que le calcul de l'application démarre.

**4. Lui donner accès aux tables.** L'application lit les données sous sa propre identité, un principal de service, qui ne voit rien par défaut. Relevez son **App ID** dans le panneau *About the App* : c'est une suite de lettres et de chiffres séparés par des tirets. Dans l'éditeur SQL, exécutez ensuite :

```sql
GRANT USE CATALOG ON CATALOG frequence       TO `<app-id-de-l-application>`;
GRANT USE SCHEMA  ON SCHEMA  frequence.socle TO `<app-id-de-l-application>`;
GRANT SELECT ON TABLE frequence.socle.ecoutes     TO `<app-id-de-l-application>`;
GRANT SELECT ON TABLE frequence.socle.abonnements TO `<app-id-de-l-application>`;
```

Utilisez bien l'App ID, et non le nom affiché du principal (`app-xxxx frequence-decrochage`) : Unity Catalog ne reconnaît pas ce nom.

**5. Déployer.** Cliquez sur **Deploy**, indiquez le chemin du dossier, par exemple `/Workspace/Users/<votre-adresse>/frequence-decrochage`, et attendez l'état *Running*.

**6. Ouvrir.** Cliquez sur l'URL de l'application. À la première ouverture, Databricks vous demande d'autoriser l'application (*Permission Requested* › **Authorize**).

## Ce que vous devez voir

Au seuil par défaut, 0,50 : **216 abonnés**. En descendant le curseur à 0,30 : **290 abonnés**.

Pour vérifier que l'application lit les mêmes données que vous, copiez la requête `REQUETE_DECROCHAGE` de `app.py` dans l'éditeur SQL. L'éditeur affiche un champ pour le paramètre `:seuil` : saisissez `0.5`. Vous devez retrouver le même nombre de lignes.

## Si ça ne marche pas

| Ce que vous voyez | La cause probable |
|---|---|
| `INSUFFICIENT_PERMISSIONS … does not have USE CATALOG on Catalog 'frequence'` | Les `GRANT` de l'étape 4 manquent, ou ont été donnés au nom affiché au lieu de l'App ID |
| Le déploiement échoue et l'application passe à l'arrêt | Une erreur dans le code. Ouvrez l'onglet **Logs** : les messages les plus récents sont en haut |
| L'application est arrêtée alors qu'elle marchait la veille | Normal en Free Edition : elle s'arrête 24 heures après son démarrage. Cliquez sur **Start** |
| Impossible de créer l'application | La Free Edition en accepte trois au plus. Supprimez-en une, et prenez l'habitude de redéployer plutôt que de recréer |
| La liste n'a pas changé après une modification de `app.py` | L'application n'a pas été redéployée, ou elle l'a été depuis un autre dossier |

## Une remarque sur le seuil

Dans `app.py`, le seuil est transmis à la requête sous forme de `Decimal`, pas de nombre à virgule ordinaire. Le connecteur SQL envoie un `float` Python en précision simple : 0,30 arrive alors sous la forme 0,3000000119…, et les abonnés dont la baisse vaut exactement 30 % disparaissent de la liste. Au seuil 0,30, vous en verriez 286 au lieu de 290. C'est le genre d'écart qu'on ne repère qu'en comparant avec l'éditeur SQL.
