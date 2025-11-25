!!! info "Notebook Access"
    [📓 Download Jupyter Notebook](./Get_Projects_Tiles_by_AOI_EN.ipynb){ .md-button .md-button--primary }
    
!!! warning "Static Preview"
    This is a static preview of the notebook. Download the original notebook file to run the code interactively.

# Identify Lidar Projects and Tiles Covering an Area of Interest
This tutorial gives examples of how to find lidar projects and tiles covering a region of interest. We use the index files of the product [LiDAR Point Clouds - CanElevation Series](https://open.canada.ca/data/en/dataset/7069387e-9986-4297-9f55-0288e9676947). Primarily, we use the [geopandas](https://geopandas.org/en/stable/) module to manipulate the index layers and perform spatial queries.

In a real application, the list of tiles obtained for an area of interest (AOI) could be used to build a more advanced processing workflow as described in the notebook [creating a digital elevation model (DEM) from a lidar point cloud in COPC LAZ format](./DEM_from_COPC_lidar_EN.ipynb).


## Steps:

1) [Prepare the Environment](#1-prepare-the-environment)

2) [Import Necessary Modules](#2-import-necessary-modules)

3) [Download Product Indexes](#3-download-product-indexes)

4) [Create GeoPandas Objects](#4-create-geopandas-objects)

5) [Find Projects and Tiles Covering an Area of Interest](#5-find-projects-and-tiles-covering-an-area-of-interest)

6) [Using an Area of Interest in Another Projection](#6-using-an-area-of-interest-in-another-projection)


## 1) Prepare the Environment

To run these examples locally, follow these steps:

### 1.1) Retrieve the Source Code

   In a directory of your choice on your computer, clone the repository using the following command:
   >```bash
   >git clone https://github.com/NRCan/CanElevation.git
   >```
   
   Then, navigate to the directory containing the notebooks:
   >```bash
   >cd CanElevation/docs/en/pointclouds
   >```

### 1.2) Install Conda (if needed)

   We recommend using conda to manage dependencies.
   
   If you haven't already installed it, refer to the official [Miniconda installation instructions](https://docs.anaconda.com/miniconda/install/#quick-command-line-install). The following steps assume conda is available from your command line.

### 1.3) Install Project Dependencies

   The `docs\assets\env\environment.yml` file lists all necessary dependencies. Create a new conda environment using the following command:
   >```bash
   >conda env create -n CanElevation_PointClouds --file docs/assets/env/environment.yml
   >```
   
   Then, activate the newly created environment:
   >```bash
   >conda activate CanElevation_PointClouds
   >```

### 1.4) Start Jupyter Notebook

   To start Jupyter Notebook, run:
   >```bash
   >jupyter notebook
   >```

If you encounter issues or want to explore more launch options, refer to the [Jupyter Notebook User Guide](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html).

**You are now ready to run the code cells in the notebook.**

## 2) Import Necessary Modules

In the following examples, we primarily use the `geopandas` module. We also use the `requests` module to download indexes and the `zipfile` module to extract them locally.


```python
import os
import requests
import zipfile
import geopandas as gpd
from shapely import box
from IPython.display import display
from ipywidgets import Output
```

## 3) Download Product Indexes

The [product page](https://open.canada.ca/data/en/dataset/7069387e-9986-4297-9f55-0288e9676947) provides indexes for the distributed lidar projects, as well as the individual lidar tiles that make up each project. Before we can work with these files, we need to download and extract the contents of the compressed archives.


```python
# Define URLs for the lidar projects and tiles indexes
projects_url = 'https://canelevation-lidar-point-clouds.s3.ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARprojects_projetslidar.zip'
tiles_url = 'https://canelevation-lidar-point-clouds.s3.ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARtiles_tuileslidar.zip'

# Download and extract contents of the lidar projects and tiles indexes
for index_url in (projects_url, tiles_url):
    zipname = os.path.basename(index_url)
    basename = os.path.splitext(zipname)[0]
    
    response = requests.get(index_url)
    with open(zipname, 'wb') as file:
        file.write(response.content)
    
    with zipfile.ZipFile(zipname, 'r') as zip_ref:
        zip_ref.extractall(basename)
```

## 4) Create GeoPandas Objects

We will use the `geopandas` library to work with the index files. This library provides tools for both spatial and geometric operations. For more details, refer to the [GeoPandas documentation](https://geopandas.org/en/stable/).


```python
# Load the lidar projects and tiles indexes into GeoPandas objects. The coordinate reference system of the indexes is NAD83(CSRS) - EPSG:4617
gdf_projects = gpd.read_file('Index_LiDARprojects_projetslidar/Index_LiDARprojects_projetslidar.shp')
gdf_tiles = gpd.read_file('Index_LiDARtiles_tuileslidar/Index_LiDARtiles_tuileslidar.shp')
```

## 5) Find Projects and Tiles Covering an Area of Interest

A common use case is to identify the lidar projects and tiles that cover a specific region of interest. In this example, we define an area of interest and use a spatial intersection query to determine which projects and tiles intersect it. The results are then printed to the screen.


```python
# Define the area of interest (AOI) as a bounding box in NAD83(CSRS) (EPSG:4617)
aoi = box(-80, 43.20, -79.971, 43.225)
aoi_gdf = gpd.GeoDataFrame({'geometry': [aoi]}, crs=4617)

# Filter lidar projects and tiles intersecting the AOI
overlapping_projects = gdf_projects[gdf_projects.intersects(aoi_gdf.geometry.iloc[0])]
overlapping_tiles = gdf_tiles[gdf_tiles.intersects(aoi_gdf.geometry.iloc[0])]

# Display results
out = Output()
with out:
    print(f"Overlapping lidar projects:")
    for _, row in overlapping_projects.iterrows():
        print(f"  Project: {row['Project']}, URL: {row['URL']}")
    
    print(f"\nOverlapping lidar tiles:")
    for _, row in overlapping_tiles.iterrows():
        print(f"  Project: {row['Project']}, Tile name: {row['Tile_name']}")
display(out)
```

## 6) Using an Area of Interest in Another Projection

Working with projected coordinates? If you know the EPSG code of your projection, you can easily reproject the area of interest before performing intersection operations with the project and tile indexes.

In the example below, we adapt the previous workflow to find the lidar projects and tiles that intersect a projected area of interest.


```python
# Define the area of interest (AOI) as a bounding box in NAD83(CSRS) | UTM zone 17N (EPSG:2958)
aoi_utm = box(580736, 4783785, 583114, 4785855)

# Create a GeoDataFrame for the AOI using the NAD83(CSRS) | UTM zone 17N (EPSG:2958)
aoi_gdf = gpd.GeoDataFrame({'geometry': [aoi_utm]}, crs=2958)

# Reproject the AOI to the NAD83(CSRS) (EPSG:4617)
aoi_gdf = aoi_gdf.to_crs(epsg=4617)

# Filter lidar projects and tiles intersecting the AOI
overlapping_projects = gdf_projects[gdf_projects.intersects(aoi_gdf.geometry.iloc[0])]
overlapping_tiles = gdf_tiles[gdf_tiles.intersects(aoi_gdf.geometry.iloc[0])]

# Display results
out = Output()
with out:
    print(f"Overlapping lidar projects:")
    for _, row in overlapping_projects.iterrows():
        print(f"  Project: {row['Project']}, URL: {row['URL']}")
    
    print(f"\nOverlapping lidar tiles:")
    for _, row in overlapping_tiles.iterrows():
        print(f"  Project: {row['Project']}, Tile name: {row['Tile_name']}")
display(out)
```
