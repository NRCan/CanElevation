# Préparation de l'environnement pour les transformations verticales

Ce guide explique comment configurer l'environnement logiciel nécessaire pour effectuer des transformations verticales de données géospatiales au Canada.

## Installation des logiciels

Pour effectuer les transformations présentées dans ce tutoriel, nous recommandons l'installation de la plus récente version de la suite logicielle libre [OSGeo4W](https://trac.osgeo.org/osgeo4w/). Cette suite regroupe plusieurs outils géospatiaux *open-source* largement utilisés, notamment GDAL, PDAL, PROJ et QGIS.

!!! tip "Recommendations pour l'installation"
    Nous vous recommandons de choisir l'installation *Express install* ainsi que de choisir *QGIS LTR* dans la fenêtre *Select Packages*. Vous aurez ainsi tous les outils nécessaires au tutoriel. 
    Par défaut, l'installateur OSGeo4W réalise l'installation dans le répertoire C:\OSGeo4W. L'invite de commande à utiliser est celle se trouvant dans ce répertoire.

Les versions utilisées pour la conception du présent tutoriel sont :

* GDAL 3.10
* PDAL 2.8
* PROJ 9.6
* QGIS 3.40

Ces logiciels peuvent être utilisés de différentes manières : en ligne de commande, en tant que librairies Python, ou de façon interactive via une interface graphique (p. ex. QGIS). Dans ce guide, les exemples sont principalement présentés à l'aide de l'environnement en ligne de commande offert par la console OSGeo4W.

