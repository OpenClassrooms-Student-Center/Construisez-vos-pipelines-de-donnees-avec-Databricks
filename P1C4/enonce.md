# P1C4 — Les trois questions de Claire

> **De :** Claire, responsable marketing\
> **Objet :** Pour jeudi
>
> Merci pour le top des genres et les heures d'écoute, c'est exactement ce qu'il me fallait. Pour la réunion de jeudi, j'aurais besoin de trois choses de plus :
>
> 1. Comment évoluent les écoutes au fil de l'année ? Je voudrais voir si on a des saisons.
> 2. Sur quel terminal nos abonnés écoutent-ils le plus ? Gratuits et premium séparément, je soupçonne qu'ils ne se ressemblent pas.
> 3. Combien de nos abonnés premium n'ont rien écouté depuis un mois ? Un pourcentage me suffit.
>
> Et une question qui n'a rien à voir avec les chiffres : je prépare le budget de l'an prochain. Si on passe sur un vrai compte Databricks, quelle taille de warehouse faudrait-il pour ce genre de requêtes ?
>
> Claire

## Ce que vous devez faire

1. **Reformulez chaque question** en une phrase précise, avant d'écrire la moindre ligne de SQL : ce que l'on compte, sur quelle période, et à quelle date l'offre de l'abonné est lue.
2. **Contrôlez la jointure** entre `ecoutes` et `abonnements` avec la requête de couverture du chapitre. Tant que ses trois nombres ne sont pas égaux, n'allez pas plus loin.
3. **Écrivez les trois requêtes**, en commentant dans le SQL chaque choix de jointure et de filtre.
4. **Notez le temps d'exécution** de chacune, affiché sous le résultat.
5. **Répondez à la question budgétaire** en trois phrases : la taille que vous choisiriez, et pourquoi.

## Deux rappels

- Pour la troisième question, comptez 30 jours. Les données s'arrêtent au 30 septembre 2026 : ces 30 jours se comptent à partir de la dernière écoute présente dans la table, pas de la date du jour.
- Un abonné peut avoir changé d'offre en cours d'année. L'offre qui compte est celle qui était active au moment de l'écoute.

## Ce que vous rendez

| Élément | Format |
|---|---|
| La requête de contrôle de couverture et son résultat | SQL, avec le résultat en commentaire |
| Les trois requêtes, commentées | SQL |
| Leurs résultats et leurs temps d'exécution | Un tableau ou une capture par requête |
| Votre recommandation de taille de warehouse | Trois phrases |
