# Utilisation du GeoParquet avec Python et GDAL

Ce tutoriel présente l'accès et la manipulation de la couche optimisée des bâtiments en format GeoParquet avec **Python (GeoPandas)** et **GDAL (ogr2ogr)**. Ces outils permettent de filtrer, transformer et exporter les données de manière efficace.

!!! warning "Pour Linux et macOS"
    Ce tutoriel utilise des exemples conçus pour Windows. Les commandes multi‑lignes montrent le caractère de continuation utilisé selon le shell :
    - Windows Invite de commandes (CMD) : ^
    - Windows PowerShell : ` (accent grave)
  
    Sous Linux/macOS (bash, zsh), remplacez ces caractères par \ pour indiquer la continuation de ligne. Vérifiez toujours quel shell vous utilisez avant d'adapter la syntaxe.

## Configuration de l'environnement conda
Les prochaines étapes visent à vous guider dans la configuration de l'environnement nécessaire accéder et manipuler les données GeoParquet de la couche optimisée des bâtiments. 

---

### Installation de conda

L'environnement Python recommandé utilise **conda** pour gérer les dépendances. Si vous n'avez pas encore installé conda :

1. Téléchargez et installez [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou [Anaconda](https://www.anaconda.com/products/distribution)
2. Vérifiez l'installation en ouvrant un terminal et en tapant :

```bash
conda --version
```

Si la commande retourne un numéro de version (ex: `conda 24.1.2`), conda est correctement installé.

### Téléchargement du fichier d'environnement

Le fichier d'environnement `environment_geoparquet.yaml` contient toutes les dépendances nécessaires pour manipuler les données GeoParquet avec Python et GDAL.

!!! info "Téléchargement du fichier d'environnement"
    <a class="md-button md-button--primary" href="../../../assets/env/environment_geoparquet.yaml" download>📄 Télécharger environment_geoparquet.yaml</a>


Enregistrez ce fichier dans un répertoire de travail sur votre ordinateur.

### Création de l'environnement

Ouvrez un terminal, naviguez vers le répertoire contenant le fichier `environment_geoparquet.yaml`, puis exécutez :

```bash
conda env create -f environment_geoparquet.yaml -n env_geoparquet
```

Cette commande va :

* Installer Python 3.12
* Installer les bibliothèques nécessaires : `geopandas`, `pyarrow`, `shapely`, `libgdal-arrow-parquet`, `gdal`
* Installer GDAL ≥ 3.10 avec support GeoParquet

!!! tip "Temps d'installation"
    L'installation peut prendre quelques minutes selon votre connexion internet. Conda télécharge et installe automatiquement toutes les dépendances requises.

### Activation de l'environnement

Une fois l'environnement créé, activez-le avec :

```bash
conda activate env_geoparquet
```

Votre invite de commande devrait maintenant afficher `(env_geoparquet)` au début de la ligne, indiquant que l'environnement est actif.

### Vérification de l'installation

Pour vérifier que l'installation s'est déroulée correctement, exécutez les commandes suivantes :

**1. Vérifier la version de Python :**
```bash
python --version
```
Attendu : `Python 3.12.x`

**2. Vérifier la présence du driver GeoParquet dans GDAL :**
```bash
ogrinfo --formats | findstr Parquet
```
Attendu : Une ligne contenant `Parquet` (ex: `Parquet -raster,vector- (rw+): (Geo)Parquet`)

**3. Tester les imports Python :**
```bash
python -c "import geopandas; import pyarrow; print('OK - Tous les modules sont correctement installés')"
```
Attendu : `OK - Tous les modules sont correctement installés`

!!! warning "Résolution de problèmes"
    En cas de problèmes persistants, supprimez l'environnement avec `conda env remove -n env_geoparquet` et recommencez la création.
    Vous pouvez également consulter la documentation de GDAL détaillant la création d'un environnement supportant le GeoParquet [https://gdal.org/en/stable/tutorials/vector_geoparquet_tut.html](https://gdal.org/en/stable/tutorials/vector_geoparquet_tut.html)

---


## Données utilisées

La couche optimisée des bâtiments est accessible via le même url. Cependant, la fonction utilisée dans python nécessite le chemin s3. Voici les deux liens utilisés:

* **URL S3 (pour Python/GeoPandas)** :  
  `s3://ftp-maps-canada-ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet`

* **URL /vsicurl/ (pour GDAL/ogr2ogr)** :  
  `/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet`

---

## Accès avec Python (GeoPandas)

GeoPandas, combiné avec PyArrow, permet de lire efficacement les données GeoParquet avec filtrage spatial. Le GeoParquet prend en charge la lecture à la demande (lazy-read), ce qui permet de ne lire que les portions nécessaires du fichier. 

Dans une chaine de traitement, nous pouvons uniquement lire en mémoire les emprsies voulues, sans importer au complet la donnée. Très pratique lors de l'automatisation de processus d'analyses. 


!!! warning "Activation de l'environnement et python"
    Avant de suivre ce tutoriel, activez l'environnement conda et python avec :
    ```bash
    conda activate env_geoparquet    
    python
    ```
    Vous devrez voir `>>>` dans la console. Vous être prêts à utiliser python. 


### Lecture distante avec filtrage par bbox 

L'exemple suivant permet de:

1. Lire la couche GeoParquet hébergée sur S3. 
2. Appliquer un filtrage spatial lors de la lecture
3. Retourner uniquement les emprises dans notre filtre spatial. 


Ici, nous allons charger les bâtiments pour un bbox englobant Montréal:

```python
import geopandas as gpd

# URL S3 de la couche optimisée des bâtiments
url = "s3://ftp-maps-canada-ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet"

# Définir le bbox
bbox_mtl = (-74.0073, 45.3672, -73.4466, 45.7328)
# Lecture avec pré-filtrage bbox
gpq_subset = gpd.read_parquet(url, bbox=bbox_mtl)
# Nombre d'emprises récupérées
print(f"Nombre de bâtiments: {len(gpq_subset)}")
# Afficher les premières lignes
print(gpq_subset.head())
```

Résultat attendu dans la console 
```console 
Nombre de bâtiments: 535431
                             feature_id  ...                                           geometry
0  f0e433ba-ef00-416f-88f4-d189e7535ac1  ...  POLYGON ((-73.86742 45.50376, -73.86729 45.503...
1  4c3be1d5-1b26-41a1-abe2-fc0d35032e6d  ...  POLYGON ((-73.60723 45.55632, -73.60721 45.556...
2  b1abac13-733e-4539-8226-6ac62a60a712  ...  POLYGON ((-73.79093 45.487, -73.7908 45.48706,...
3  b850c5ae-b133-4fc4-9ce1-d0cae4141d19  ...  POLYGON ((-73.83886 45.49419, -73.83873 45.494...
4  442f783d-73a2-4a5b-84b2-12a13781fa7e  ...  POLYGON ((-73.84561 45.47849, -73.84548 45.478...

[5 rows x 25 columns]
```

### Affinement avec géométrie polygonale

Dans un context où le bbox utilisé en filtrage est trop grossier, nous pouvons affiner la sélection au besoin. Il s'agit d'un exemple plus près de la réalité. Une fois la lecture des emprises de Montréal effectuée, nous allons uniquement conserver celles autour du Stade Olympique de Montréal. Les étapes suivantes sont faites dans l'exemple: 

1. Lire la couche GeoParquet hébergée sur S3. 
2. Appliquer un filtrage spatial lors de la lecture
3. Retourner uniquement les emprsies dans notre filtre spatial. 
4. Affiner la sélection avec une géométrie voulue plus précise (peut être n'importe quelle géométrie). 



```python
import geopandas as gpd
from shapely.geometry import box

#---|1) Filtrage à la lecture |-------
# URL du GeoParquet sur S3
url = "s3://ftp-maps-canada-ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet"

# Définir la bbox (Montréal)
bbox_mtl = (-74.0073, 45.3672, -73.4466, 45.7328)

# Lecture avec pré-filtrage bbox
gpq_subset = gpd.read_parquet(url, bbox=bbox_mtl)
print(f"Nombre de bâtiments: {len(gpq_subset)}")

#---|2) Affinage de la sélection |-------
# Définir la limite comme un polygone (bbox)
limite = (-73.565,45.543, -73.521,45.575)
polygon_limite = box(*limite)
gdf_limite = gpd.GeoDataFrame(geometry=[polygon_limite], crs=gpq_subset.crs)

# Effectuer la sélection plus précise. 
gpq_clip = gpd.sjoin(gpq_subset, gdf_limite, predicate="intersects", how="inner")

print(f"Après intersection avec la limite: {len(gpq_clip)} bâtiments")
```

**Résultat attendu :**

![Selection of footprints around Olympic Stadium](../../assets/images/geoparquet_subset_montreal.png)

*Figure : Emprises de bâtiments extraites autour du Stade Olympique de Montréal.*

!!! note "Étape d'affinage"
    Dans le but de faciliter le tutoriel, la géométrie servant à la sélection des emprises autour du Stade Olympique de Montréal est un bbox. Cependant, vous pouvez passer un fichier geopackage ou shapefile lu avec la commande `polygon_limite=qpg.read_file(chemin/vers/limite.gpkg)`



### Sauvegarde des résultats

Vous pouvez exporter les données filtrées dans différents formats :

```python
# Sauvegarder en GeoPackage
gpq_clip.to_file("batiments_stade_olympique.gpkg", driver="GPKG")

# Sauvegarder en Shapefile
gpq_clip.to_file("batiments_stade_olympique.shp")

# Sauvegarder en GeoJSON
gpq_clip.to_file("batiments_stade_olympique.geojson", driver="GeoJSON")

# Sauvegarder en GeoParquet (pour conserver les performances)
gpq_clip.to_parquet("batiments_stade_olympique.parquet")
```

!!! note "Format de sortie recommandé"
    Le format **GeoParquet** est recommandé pour conserver les avantages de performance. Pour une compatibilité universelle, utilisez **GeoPackage** ou **GeoJSON**.

---

## Accès avec ogr2ogr (GDAL)

GDAL fournit l'outil en ligne de commande `ogr2ogr` pour manipuler les données vectorielles, y compris les fichiers GeoParquet. Les versions récentes supportent le filtrage à la lecture. 

!!! info "Utilisation ogr2ogr"
    L'utilisation de ogr2ogr ne permet pas de sauvegarder le résultats d'une sélection spatiale dans une variable, pour ensuite être réutilisée. Les données doivent être écrites sur le disque.

### Format d'adresse

Pour accéder aux données distantes avec GDAL, utilisez le préfixe `/vsicurl/` :

```
/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet
```
### Extraction avec filtrage bbox

!!! warning "Activation de l'environnement "
    Avant de suivre ce tutoriel, activez l'environnement conda avec :
    ```bash
    conda activate env_geoparquet     
    ```
    Une fois l'environnement activé, vous pouvez utliser les commandes ogr/gdal dans la console. 


Nous allons reprendre notre exemple pour filtrer les emprises dans le bbox de Montréal.  Nous allons sauvegarder le résultat en local. La commande sera construite avec les paramètres suivants:

- `Chemin de sortie` : Les emprises finales, filtrées par la géométrie de votre zone d'intérêt (bbox de Montréal)
- `/vsicurl/...` : Chemin du GeoParquet distant sur sur le FTP. 
- `-spat xmin ymin xmax ymax` : Filtre spatial par votre *bounding box*
    - Pour l’exemple de Montréal, les valeurs sont : -74.0073 45.3672 -73.4466 45.7328
- `-nln` : Nom de la couche (layer) dans le fichier de sortie (optionel)


```bash
ogr2ogr ^
  Chemin/vers/votre/selection_batiments_ogr2ogr.gpkg ^
  "/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet" ^
  -spat -74.0073 45.3672 -73.4466 45.7328 ^
  -nln batiement_opti
```

!!! warning "Pour linux et MacOS"
    Pour les utilisateurs des systèmes d'opération linux ou MacOS, raplacez les `^` par des `\`. Cela indique les sauts de lignes. 


### Extraction avec filtrage par géométrie (clipsrc)

Les options d'ogr2ogr nous permettent aussi de faire plus d'un traitement dans la même commande. Dans l'exemple qui suit, nous pouvons en une seule commande, filtrer à la lecture les emprises, puis sélectionner uniquement celles qui sont dans une géométrie voulue. Cette géométrie peut être un autre bbox ou encore le chemin vers un fichier polygonal (geopackage, shapefile, etc.). 

Pour découper les données avec une géométrie polygonale spécifique, utilisez l'option `-clipsrc`. Les paramètres suivants sont utilisés

- Chemin de sortie : Les emprises finales, filtrées par la géométrie de votre zone d'intérêt (pas le bbox)
- `/vsicurl/...` : Chemin du GeoParquet distant sur le FTP
- `-spat xmin ymin xmax ymax` : Filtre spatial par votre *bounding box*
    - Pour l’exemple de Montréal, les valeurs sont : -74.0073 45.3672 -73.4466 45.7328
- `-clipsrc` : Chemin vers le fichier servant à la découpe les géométries selon la limite fournie (ou un bbox).  
- `-nln` : Nom de la couche (layer) dans le fichier de sortie (optionel)

!!! warning "Utilisation de `-clipsrc`"
    Pour faciler le tutoriel, nous passons les coordonnées d'un bbox pour couper les emprises de la première sélection. Il s'agit du bbox entourant le Stade Olympique de Montréal. 

```bash

ogr2ogr ^
  Chemin/vers/votre/selection_batiments_ogr2ogr.gpkg ^
  "/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet" ^
  -spat -74.0073 45.3672 -73.4466 45.7328 ^
  -clipsrc -73.565 45.543 -73.521 45.575 ^
  -nln batiement_opti
```

!!! warning "Différence entre -spat et -clipsrc"
    * `-spat` : Sélectionne les géométries dont le bbox intersecte la bbox spécifiée (plus rapide)
    * `-clipsrc` : Découpe réellement les géométries au bbox spécifiée (plus précis mais plus lent)

## Utilisation en local

Si vous avez téléchargé le fichier GeoParquet localement, vous pouvez l'utiliser de la même manière en remplaçant l'URL par le chemin local :

**Python :**

```python
import geopandas as gpd
from shapely.geometry import box

#---|1) Filtrage à la lecture |-------
# URL du GeoParquet sur S3
url = "chemin/vers/votre/auto_building_opti_2.parquet"

# Définir la bbox (Montréal)
bbox_mtl = (-74.0073, 45.3672, -73.4466, 45.7328)

# Lecture avec pré-filtrage bbox
gpq_subset = gpd.read_parquet(url, bbox=bbox_mtl)
print(f"Nombre de bâtiments: {len(gpq_subset)}")

#---|2) Affinage de la sélection |-------
# Définir la limite comme un polygone (bbox)
limite = (-73.565,45.543, -73.521,45.575)
polygon_limite = box(*limite)
gdf_limite = gpd.GeoDataFrame(geometry=[polygon_limite], crs=gpq_subset.crs)

# Effectuer la sélection plus précise. 
gpq_clip = gpd.sjoin(gpq_subset, gdf_limite, predicate="intersects", how="inner")

print(f"Après intersection avec la limite: {len(gpq_clip)} bâtiments")

```

**ogr2ogr :**

```bash

ogr2ogr ^
  Chemin/vers/votre/selection_batiments_ogr2ogr.gpkg ^
  "chemin/vers/votre/auto_building_opti_2.parquet" ^
  -spat -74.0073 45.3672 -73.4466 45.7328 ^
  -clipsrc -73.565 45.543 -73.521 45.575 ^
  -nln batiement_opti
```


---


!!! tip "Meilleures pratiques"
    * **Toujours utiliser un filtrage spatial** (`bbox` ou `-spat`) pour les données volumineuses
    * **Utiliser GeoParquet pour les sorties** si vous comptez réutiliser les données (performances optimales)

---

## Résumé

Ce tutoriel a présenté deux approches pour accéder à la couche optimisée des bâtiments en format GeoParquet :

* **Python (GeoPandas)** : Lecture, filtrage et export avec du code Python flexible
* **GDAL (ogr2ogr)** : Manipulation en ligne de commande pour automatisation et batch processing

!!! tip "Prochaines étapes"
    Si vous préférez une interface graphique, consultez le tutoriel [Utilisation avec QGIS](acces-qgis.md).
