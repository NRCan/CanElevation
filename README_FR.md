![NRCan banner](docs/assets/images/nrcan-banner.png)

[English version](README.md)

# CanElevation

Le dépôt CanElevation fournit une documentation complète, des exemples et des outils pour travailler avec les données d'élévation canadiennes, incluant les nuages de points LiDAR et les transformations de datums verticaux.

## Aperçu

Ce dépôt contient  :

- **Notebooks Jupyter interactifs** - Tutoriels étape par étape pour le traitement des données d'élévation
- **Documentation** - Guides complets en français et en anglais
- **Données d'exemple** - Jeux de données d'exemple pour les tests et l'apprentissage

## Fonctionnalités principales

### Mosaïques MNE avec STAC

- Apprenez à rechercher, accéder et assembler des Modèles Numériques d'Élévation (MNE) à l'aide des API STAC (SpatioTemporal Asset Catalog)
- Exemples de flux de travail pour intégrer des MNE basés sur STAC dans vos analyses

### Traitement de nuages de points

- Création de modèles numériques d'élévation (MNE) à partir de données LiDAR
- Travail avec les formats COPC (Cloud Optimized Point Cloud)
- Filtrage et classification des données de nuages de points
- Intégration avec QGIS pour la visualisation

### Transformations verticales

- Conversion entre les datums verticaux canadiens (CGVD2013, CGVD28)
- Transformations basées sur des rasters
- Conversions de datums et d'époque pour nuages de points

### Utilisation du GeoParquet de la couche optimisée des bâtiments

- Apprenez à utiliser le GeoParquet de la couche optimisée des bâtiments à l'aide de Python et GDAL.
- Visualisez la couche à l'aide de QGIS.

*English version:*
   - [Python & GDAL Access](docs/en/optimized_building_footprint/python-gdal-access.md)
   - [QGIS Access](docs/en/optimized_building_footprint/qgis-access.md)
  

## 📖 Documentation

**Visitez notre documentation complète :** [https://nrcan.github.io/CanElevation/](https://nrcan.github.io/CanElevation/)

## Démarrage rapide

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/NRCan/CanElevation.git
   cd CanElevation
   ```

2. **Configurer l'environnement :**
   ```bash
   conda env create -n CanElevation --file docs/assets/env/environment.yml
   conda activate CanElevation
   ```

3. **Lancer Jupyter Notebook (Exemples de nuages de points):**
   ```bash
   jupyter notebook
   ```

4. **Ouvrir un notebook tutoriel** du répertoire `docs/fr/pointclouds/` ou `docs/en/pointclouds/`

## Sources de données

Ce dépôt fonctionne avec les données [Nuages de points lidar](https://ouvert.canada.ca/data/fr/dataset/7069387e-9986-4297-9f55-0288e9676947) et les [modèles numériques d'élévation](https://ouvert.canada.ca/data/fr/dataset/957782bf-847c-4644-a757-e383c0057995) de la Série CanÉlévation, qui fournit des données d'élévation de haute qualité pour le Canada.


## Licence

Ce projet est sous licence de la [License du gouvernement ouvert – Canada](https://ouvert.canada.ca/fr/licence-du-gouvernement-ouvert-canada).

## Support

Pour des questions ou du support :
- 📖 Consultez la [documentation](https://nrcan.github.io/CanElevation/)

- 🐛 Signalez les problèmes sur [GitHub Issues](https://github.com/NRCan/CanElevation/issues)
