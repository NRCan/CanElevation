# Couche optimisée des bâtiments - GeoParquet - Série CanElevation

La couche optimisée des bâtiments est un jeu de données vectoriel qui recense les meilleures emprises de bâtiments à l'échelle du Canada. Grâce à un processus de priorisation des emprises, seules les meilleures sont conservées. Cette couche, qui contient plus de 10 millions d'emprises de bâtiments, est offerte au format **GeoParquet**, optimisé pour l'infonuagique. Ce tutoriel présente l'utilisation du format GeoParquet pour accéder à ces données de manière efficace et performante.

## Qu'est-ce que GeoParquet?

**GeoParquet** est un format de fichier géospatial basé sur [Apache Parquet](https://parquet.apache.org/), conçu pour stocker et traiter efficacement des données vectorielles volumineuses. Il combine les avantages suivants :

* **Compression optimale** : Réduction significative de la taille des fichiers
* **Lecture sélective** : Possibilité de lire uniquement les colonnes ou les zones géographiques nécessaires
* **Performance** : Accès rapide aux données, même pour de très grands jeux de données
* **Interopérabilité** : Compatible avec les outils modernes (Python, GDAL, QGIS, DuckDB, etc.)
* **Stockage en colonnes** : Optimisé pour les requêtes analytiques

## Pourquoi GeoParquet?

Le format GeoParquet offre des avantages par rapport aux formats traditionnels comme le GeoPackage (GPKG). Voici une comparaison pour la couche optimisée des bâtiments :

| **Critère** | **GeoParquet** | **GeoPackage** |
|-------------|----------------|----------------|
| **Taille du fichier** | ~2.3 Go | ~5.6 Go |
| **Compression** | Excellente (60% de réduction) | Modérée |
| **Lecture sélective (bbox)** | Oui (filtrage côté serveur) | Non (téléchargement complet requis) |
| **Performance de lecture** | Très rapide (colonnes ciblées) | Modérée |
| **Accès distant (S3/HTTP)** | Optimisé (lecture partielle) | Peu efficace |
| **Interopérabilité** | Python, GDAL, QGIS, DuckDB, etc. | Universel (mais moins performant) |


GeoParquet organise les données en groupe d'entités, qui sont des blocs de lignes permettant une lecture efficace et sélective. Dans les fichiers GeoParquet optimisés, la boîte englobante (bbox) de chaque groupe d'entité peut être stockée dans les métadonnées du fichier, ce qui facilite le filtrage spatial. Ainsi, lors d'une lecture avec un filtre spatial, la bbox de chaque groupe d'entité est comparée à la zone de requête ; seuls les groupe d'entité dont la bbox intersecte la zone demandée sont lus, ce qui réduit le volume de données à traiter. Le nombre d’entités par groupe d'entité (par exemple 65 536) est paramétrable lors de la création du fichier et peut varier selon les besoins d’optimisation.

---

## Données disponibles

La couche optimisée des bâtiments en format GeoParquet est accessible via :

* **URL FTP** : [https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet](https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet)

**Caractéristiques du jeu de données :**

* **Nombre d'emprises** : 10+ millions de bâtiments
* **Taille du fichier** : ~2.3 Go (format GeoParquet)
* **Couverture géographique** : Canada
* **Système de coordonnées** : EPSG:4617 (NAD83 CSRS géographique)


## Résumé des tutoriels

Ce guide est divisé en 2 tutoriels pour vous accompagner dans l'installation des dépendances et l'utilisation de la couche optimisée des bâtiments en format GeoParquet :

1. **[Utilisation avec Python et GDAL](acces-python-gdal.md)** : Accès et manipulation des données avec Python (GeoPandas) et la ligne de commande (ogr2ogr)

2. **[Utilisation avec QGIS](acces-qgis.md)** : Chargement et visualisation des données avec QGIS et le plugin GeoParquet Downloader



## Public cible

Ces tutoriels s'adressent à :

* **Analystes SIG** souhaitant manipuler des données vectorielles volumineuses dans QGIS
* **Développeurs Python** utilisant GeoPandas et PyArrow pour des analyses géospatiales
* **Utilisateurs GDAL** automatisant le traitement de données avec ogr2ogr
* **expert en science des données** exploitant des formats optimisés pour le cloud (S3, HTTP)

!!! note "Prérequis"
    Une connaissance de base en SIG et en ligne de commande est recommandée pour suivre les tutoriels Python/GDAL. Le tutoriel QGIS est accessible aux utilisateurs débutants.

## Pour en savoir plus
Pour de plus amples informations sur la couche optimisée des bâtiments, vous êtes les bienvenus à consulter la page du produit [Bâtiments extraits automatiquement](https://ouvert.canada.ca/data/fr/dataset/7a5cda52-c7df-427f-9ced-26f19a8a64d6). Vous y trouverez la spécification du produit, l'index des projets ainsi que les répertoires de téléchargements par projet (geopackage et shapefile). 