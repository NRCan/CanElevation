!!! info "Accès au notebook"
    [📓 Télécharger le notebook Jupyter](./Get_Projects_Tiles_by_AOI_FR.ipynb){ .md-button .md-button--primary }
    
!!! warning "Aperçu statique"
    Ceci est un aperçu statique du notebook. Téléchargez le fichier notebook original pour exécuter le code de manière interactive.

# Identifier les projets lidar et les tuiles couvrant une zone d'intérêt
Ce tutoriel présente des exemples permettant de déterminer les projets lidar et les tuiles couvrant une région d'intérêt. Nous utilisons les fichiers d'index du produit [Nuages de points lidars - Série CanÉlévation](https://ouvert.canada.ca/data/fr/dataset/7069387e-9986-4297-9f55-0288e9676947). Nous utilisons principalement la librairie [GeoPandas](https://geopandas.org/en/stable/) pour manipuler les couches d'index et effectuer des requêtes spatiales.

Dans une application réelle, la liste des tuiles obtenues pour une zone d'intérêt pourrait être utilisée pour construire un flux de travail de traitement plus avancé tel que décrit dans le notebook portant sur la [création d'un modèle numérique d'élévation (MNE) à partir d'un nuage de point lidar en format COPC LAZ](./DEM_from_COPC_lidar_FR.ipynb).


## Étapes:

1) [Préparer l'environnement](#env)

2) [Importer les modules nécessaires](#import)

3) [Télécharger les index de produit](#download-index)

4) [Créer des objets GeoPandas](#create-gpd-object)

5) [Trouver les projets et tuiles couvrant une zone d’intérêt](#find-projects-tiles)

6) [Utiliser une zone d'intérêt dans une autre projection](#find-projects-tiles-other-proj)


<a id="env"></a>
## 1) Préparer l'environnement

Pour exécuter ces exemples localement, suivez les étapes suivantes :

### 1.1) Récupérer le code source

   Dans le répertoire de votre choix sur votre ordinateur, clonez le dépôt en utilisant la commande suivante :
   >```bash
   >git clone https://github.com/NRCan/CanElevation.git
   >```
   
   Ensuite, accédez au répertoire contenant les notebooks :
   >```bash
   >cd CanElevation/docs/fr/pointclouds
   >```

### 1.2) Installation conda

   Nous recommandons d’utiliser conda pour gérer les dépendances.
   
   Si vous ne l’avez pas encore installé, consultez les [instructions officielles d’installation de Miniconda](https://docs.anaconda.com/miniconda/install/#quick-command-line-install). Les étapes suivantes supposent que conda est accessible depuis votre ligne de commande.

### 1.3) Installation des dépendances

   Le fichier `docs\assets\env\environment.yml` contient toutes les dépendances nécessaires. Créez un nouvel environnement conda à l’aide de la commande suivante :
   >```bash
   >conda env create -n CanElevation_PointClouds --file docs/assets/env/environment.yml
   >```
   
   Ensuite, activez le nouvel environnement créé :
   >```bash
   >conda activate CanElevation_PointClouds
   >```

### 1.4) Démarrer Jupyter Notebook

   Pour démarrer Jupyter Notebook, exécutez :
   >```bash
   >jupyter notebook
   >```

Si vous rencontrez des problèmes ou souhaitez explorer d'autres options de lancement, consultez le [guide utilisateur de Jupyter Notebook](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html).

**Vous êtes maintenant prêt à exécuter les cellules de code du notebook.**

<a id="import"></a>
## 2) Importer les modules nécessaires

Dans les exemples suivants, nous utilisons principalement le module `geopandas`. Nous utilisons également le module `requests` pour télécharger les index et le module `zipfile` pour les extraire localement.


```python
import os
import requests
import zipfile
import geopandas as gpd
from shapely import box
from IPython.display import display
from ipywidgets import Output
```

<a id="download-index"></a>
## 3) Télécharger les index de produit

La [page du produit](https://open.canada.ca/data/en/dataset/7069387e-9986-4297-9f55-0288e9676947) contient les index des projets lidar distribués, ainsi que les tuiles lidar individuelles qui composent chaque projet. Avant de pouvoir travailler avec ces fichiers, nous devons les télécharger et extraire le contenu des fichiers compressées.


```python
# Définir les URLs des index des projets et des tuiles lidar
projects_url = 'https://canelevation-lidar-point-clouds.s3.ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARprojects_projetslidar.zip'
tiles_url = 'https://canelevation-lidar-point-clouds.s3.ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARtiles_tuileslidar.zip'

# Télécharger et extraire le contenu des index des projets et des tuiles lidar
for index_url in (projects_url, tiles_url):
    zipname = os.path.basename(index_url)
    basename = os.path.splitext(zipname)[0]
    
    response = requests.get(index_url)
    with open(zipname, 'wb') as file:
        file.write(response.content)
    
    with zipfile.ZipFile(zipname, 'r') as zip_ref:
        zip_ref.extractall(basename)
```

<a id="create-gpd-object"></a>
## 4) Créer des objets GeoPandas

Nous allons utiliser le module `geopandas` pour manipuler les fichiers d’index. Cette librairie offre des outils pour effectuer des opérations spatiales et géométriques. Pour plus de détails, consultez la [documentation de GeoPandas](https://geopandas.org/en/stable/).


```python
# Charger les index des projets et des tuiles LiDAR dans des objets GeoPandas. Le système de référence des index est NAD83(CSRS) - EPSG:4617
gdf_projects = gpd.read_file('Index_LiDARprojects_projetslidar/Index_LiDARprojects_projetslidar.shp')
gdf_tiles = gpd.read_file('Index_LiDARtiles_tuileslidar/Index_LiDARtiles_tuileslidar.shp')
```

<a id="find-projects-tiles"></a>
## 5) Trouver les projets et tuiles couvrant une zone d’intérêt

Un cas d'usage courant consiste à identifier les projets et les tuiles lidar qui couvrent une zone d’intérêt spécifique. Dans cet exemple, nous définissons une zone d’intérêt et utilisons une requête d’intersection spatiale pour déterminer quels projets et quelles tuiles la recoupent. Les résultats sont ensuite affichés à l’écran.


```python
# Définir la zone d’intérêt (AOI) sous forme de boîte englobante en NAD83(CSRS) (EPSG:4617)
aoi = box(-80, 43.20, -79.971, 43.225)
aoi_gdf = gpd.GeoDataFrame({'geometry': [aoi]}, crs=4617)

# Filtrer les projets et les tuiles lidar qui recoupent la zone d’intérêt
overlapping_projects = gdf_projects[gdf_projects.intersects(aoi_gdf.geometry.iloc[0])]
overlapping_tiles = gdf_tiles[gdf_tiles.intersects(aoi_gdf.geometry.iloc[0])]

# Afficher les résultats
out = Output()
with out:
    print(f"Overlapping LiDAR Projects:")
    for _, row in overlapping_projects.iterrows():
        print(f"Project: {row['Project']}, URL: {row['URL']}")
    
    print(f"Overlapping LiDAR Tiles:")
    for _, row in overlapping_tiles.iterrows():
        print(f"Project: {row['Project']}, Tile name: {row['Tile_name']}")
display(out)
```

<a id="find-projects-tiles-other-proj"></a>

## 6) Utiliser une zone d'intérêt dans une autre projection

Travaillez-vous avec des coordonnées projetées? Si vous connaissez le code EPSG de votre projection, vous pouvez facilement reprojeter votre zone d’intérêt avant d’effectuer les opérations d’intersection avec les index des projets et des tuiles lidar.

Dans l’exemple ci-dessous, nous adaptons le flux de travail précédent pour trouver les projets et les tuiles lidar qui croisent une zone d’intérêt projetée.


```python
# Définir la zone d’intérêt (AOI) sous forme de boîte englobante en NAD83(CSRS) | UTM zone 17N (EPSG:2958)
aoi_utm = box(580736, 4783785, 583114, 4785855)

# Créer un GeoDataFrame pour la zone d’intérêt avec le système NAD83(CSRS) | UTM zone 17N (EPSG:4617)
aoi_gdf = gpd.GeoDataFrame({'geometry': [aoi_utm]}, crs=2958)

# Reprojeter la zone d’intérêt en NAD83(CSRS) (EPSG:4617)
aoi_gdf = aoi_gdf.to_crs(epsg=4617)

# Filtrer les projets et les tuiles lidar qui recoupent la zone d’intérêt
overlapping_projects = gdf_projects[gdf_projects.intersects(aoi_gdf.geometry.iloc[0])]
overlapping_tiles = gdf_tiles[gdf_tiles.intersects(aoi_gdf.geometry.iloc[0])]

# Afficher les résultats
out = Output()
with out:
    print(f"Overlapping LiDAR Projects:")
    for _, row in overlapping_projects.iterrows():
        print(f"Project: {row['Project']}, URL: {row['URL']}")
    
    print(f"Overlapping LiDAR Tiles:")
    for _, row in overlapping_tiles.iterrows():
        print(f"Project: {row['Project']}, Tile name: {row['Tile_name']}")
display(out)
```
