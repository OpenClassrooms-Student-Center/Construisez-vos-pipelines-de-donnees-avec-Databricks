# P2C3 — Le nouveau besoin

Deux messages sont arrivés le même jour. Le premier concerne l'application que vous venez de livrer. Le second vient de gens qui l'ont vue passer et qui voudraient quelque chose, eux aussi.

## 1. Claire, à propos de l'application

> **De :** Claire, responsable marketing\
> **Objet :** Liste de décrochage
>
> J'ai testé l'application, elle fait exactement ce que je voulais. Un seul souci : à 50 % de baisse, les abonnés que je vois sont déjà partis, ou presque. Je préfère les relancer plus tôt. Tu peux mettre le seuil à 30 % par défaut ? Je garde le curseur pour descendre ou remonter si besoin.
>
> Claire

## 2. Les responsables régionaux

> **De :** Thomas, responsable Bretagne, pour les responsables régionaux\
> **Objet :** Suivi des écoutes par région
>
> Bonjour,
>
> Claire nous a montré la liste des abonnés en décrochage, et ça nous a donné une idée. Chaque lundi à 9 h, nous faisons un point en visio entre responsables régionaux. Aujourd'hui, nous n'avons aucun chiffre d'écoute à nous mettre sous la dent.
>
> Ce qu'il nous faudrait :
>
> - le nombre d'écoutes de la semaine passée, pour chaque région ;
> - le nombre d'abonnés qui ont écouté au moins une fois dans la semaine, par région ;
> - l'évolution sur les dix dernières semaines, pour voir si une région décroche ;
> - la possibilité de distinguer gratuit et premium.
>
> L'idéal serait de recevoir ça dans nos boîtes mail le lundi matin, avant la réunion. Nous serons sept à le lire. Aucun de nous ne fait de SQL, et nous n'avons pas besoin du détail abonné par abonné : les totaux par région nous suffisent.
>
> Merci d'avance,\
> Thomas

## Ce que vous devez faire

1. Traitez la demande de Claire : une seule ligne à modifier dans `app.py`, puis le redéploiement de l'application existante.
2. Pour la demande des responsables régionaux, ne construisez rien. Choisissez la brique qui y répond (dashboard, Genie ou application), en passant le besoin aux quatre critères du chapitre : type de besoin, public, enjeu de fiabilité, coût de maintenance.

## Ce que vous rendez

| Élément | Format |
|---|---|
| La ligne de code modifiée | La ligne, telle qu'elle est dans `app.py` |
| La preuve du redéploiement | Le nombre d'abonnés affiché par l'application au seuil par défaut, avant et après |
| Votre recommandation pour les responsables régionaux | Cinq phrases au plus, un critère par phrase |
