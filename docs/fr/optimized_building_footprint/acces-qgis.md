# Utilisation avec QGIS

Ce tutoriel présente l'accès et la visualisation de la couche optimisée des bâtiments au format GeoParquet avec **QGIS**. QGIS prend en charge nativement la lecture des fichiers GeoParquet.

!!! warning "Visionnement en continu"
    Bien que le GeoParquet permette la lecture en continu (*streaming*), il n'est pas le format le plus optimisé pour la seule visualisation. Cependant, il représente le meilleur compromis, car la donnée lue en continu contient les informations vectorielles et attributaires.

    Si votre utilisation est principalement la visualisation, nous recommandons fortement de télécharger le GeoParquet ou de faire une présélection de votre zone d'intérêt. Les performances seront nettement supérieures (voir [Utilisation avec Python et GDAL](acces-python-gdal.md)).

## Installation de QGIS

Pour accéder aux données GeoParquet dans QGIS, nous suggérons d'utiliser la version suivante :

* **QGIS 3.40 LTR** (Long Term Release) : La version stable avec les dépendances nécessaires. 

!!! info "Téléchargement de QGIS"
    Téléchargez et installez QGIS depuis le site officiel : [https://qgis.org/download/](https://qgis.org/download/)

## Chargement direct du GeoParquet

QGIS 3.40 et les versions ultérieures prennent en charge le format GeoParquet nativement. Vous pouvez charger directement un fichier GeoParquet local ou distant. Dans l'exemple qui suit, le GeoParquet hébergé sur le ftp sera utilisé.

```
https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet
```

### Étapes pour le chargement


!!! info "Bonnes pratiques"
    1- Pour faciliter la visualisation en *streaming* nous recommandons fortement de placer votre canevas sur la région voulue avec un échelle de zoom < à 1:50 000. Sinon, la visualisation peut prendre beaucoup de temps.     
    **Pour une visualisation réactive et fluide, nous recommandons de télécharger le fichier GeoParquet**.
    2- Définissez à l'avance le système de référence spatial de votre canevas sur `EPSG:4617`. Cela évitera les reprojections (à la volée).

1. **Ouvrir le Gestionnaire de sources de données**  
   Allez dans `Layer` → `Add Layer` → `Add Vector Layer`.

![Vector Data manager](../../assets/images/geoparquet_DataSourceManagement.png)
*Figure : Ouverture de l'interface du Gestionnaire de sources vectorielles de QGIS.*

2. **Type de source**  
   Assurez-vous que le type de source est défini sur `Protocol: HTTP(S), cloud, etc.`.

3. **Sélectionner le protocol**  
   Dans le menu déroulant **Type** de la section **Protocole**, choisissez l'option `HTTP/HTTPS/FTP`.

4. **Ajouter le lien**  
   Copiez-collez le lien du GeoParquet suivant : `https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet`

5. **Ajoutez la couche**  
   Cliquez sur `Add` pour ajouter la couche.

![QGIS Data Source Manager](../../assets/images/geoparquet_qgis_data_source_manager.png)

*Figure : Interface du Gestionnaire de sources de données QGIS pour ajouter un fichier GeoParquet.*

---

## Utilisation locale (fichier téléchargé)

Si vous avez téléchargé le fichier GeoParquet complet sur votre ordinateur, vous pouvez l'ouvrir directement dans QGIS :

1. **Télécharger le fichier** :  
   [https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet](https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet)

2. **Ouvrir dans QGIS** :  
   Suivez les étapes de la section [Chargement direct du GeoParquet](#chargement-direct-du-geoparquet) ci-dessus.

---

## Dépannage

### Problème : "GeoParquet format not supported"

**Cause :** Votre version de QGIS est antérieure à 3.40 ou GDAL n'a pas le support GeoParquet activé.

**Solution :**

1. Vérifiez votre version de QGIS : `Aide` → `À propos` (doit être ≥ 3.40)
2. Si la version est inférieure, mettez à jour QGIS vers la dernière LTR : [https://qgis.org/download/](https://qgis.org/download/)

### Problème : QGIS se fige lors du chargement du fichier complet

**Cause :** Le fichier GeoParquet complet contient plus de 10 millions d'emprises, ce qui peut ralentir QGIS si toutes les données sont chargées. Si votre canevas est vide et que vous êtes quand même à une échelle de 1: 50 000, QGIS charge tout le GeoParquet. 

**Solution :**
* Assurez-vous d'avoir une autre géométrie dans votre canevas, comme une limite de projet. Alors, QGIS ne chargera pas toute la donnée. 
* Une alternative est d'utiliser Python/GDAL pour pré-filtrer les données avant de les charger dans QGIS (voir [Utilisation avec Python et GDAL](acces-python-gdal.md))

---


