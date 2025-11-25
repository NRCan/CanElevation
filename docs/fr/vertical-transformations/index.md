# Transformations verticales - Série CanÉlévation

## Mise en contexte

Au Canada, la gestion et l'intégration des données géospatiales 3D, en particulier les données lidar et leurs produits dérivés, occupent une place centrale dans de nombreux domaines d'application : modélisation hydrologique, inventaires forestiers, cartographie topographique, aménagement du territoire, etc. Pour plusieurs de ces domaines, la cohérence et l'alignement des données géospatiales 3D sont souvent des exigences incontournables.

Un des défis propres au contexte canadien est la coexistence de plusieurs systèmes de référence, à la fois horizontaux et verticaux. Par exemple, différentes versions (ou époques) du NAD83(CSRS) sont toujours en usage selon les juridictions et les périodes d'acquisition des données. Du côté vertical, deux systèmes altimétriques peuvent être rencontrés : le CGVD28, utilisé historiquement, et le CGVD2013, qui est aujourd'hui le standard canadien de référence altimétrique. Cette diversité peut complexifier la combinaison et l'analyse de jeux de données provenant de sources multiples. Une identification rigoureuse des systèmes utilisés, ainsi que la mise en œuvre de transformations (horizontales et verticales) appropriées, peuvent être nécessaires.

Ce tutoriel se veut un guide pratique présentant quelques exemples concrets de transformations verticales de nuages de points et de modèles numériques d'élévation (MNE) dans le contexte canadien. Il s'adresse à des utilisateurs avancés ou à ceux possédant une certaine expérience des outils et systèmes géospatiaux.

Pour une compréhension plus approfondie des systèmes de référence utilisés au Canada, de leurs conventions et de leur évolution, consultez la [page web des Levés géodésiques du Canada](https://ressources-naturelles.canada.ca/science-donnees/science-recherche/geomatique/science-recherche-systemes-reference-geodesique).

## Contenu

* [Préparation de l'environnement](environment-setup.md) - Installation et configuration des outils requis
* [Transformations matricielles](raster-transformations.md) - Transformations pour les modèles numériques d'élévation (MNE)
* [Transformations de nuages de points](pointcloud-transformations.md) - Transformations pour les nuages de points LiDAR, incluant les transformations d'époques

## Public cible

Ce tutoriel est conçu pour les utilisateurs avancés et les partenaires provinciaux et territoriaux qui doivent effectuer des transformations verticales précises de données géospatiales au Canada.
