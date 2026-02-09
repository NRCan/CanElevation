# Accessing GeoParquet with Python and GDAL

This tutorial demonstrates how to access and manipulate the optimized building footprint layer in GeoParquet format using **Python (GeoPandas)** and **GDAL (ogr2ogr)**. These tools allow you to filter, transform, and export data efficiently.

!!! warning "For Linux and macOS"
    This tutorial uses examples designed for Windows. Multi-line commands show the line continuation character according to the shell: 

    - Windows Command Prompt (CMD): ^
    - Windows PowerShell: ` (backtick)
    
    On Linux/macOS (bash, zsh), replace these characters with \ to indicate line continuation. Always check which shell you are using before adapting the syntax.

## Conda Environment Setup
The following steps will guide you through setting up the environment needed to access and manipulate the GeoParquet building footprint data.

---

### Installing conda

The recommended Python environment uses **conda** to manage dependencies. If you have not installed conda yet:

1. Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)
2. Verify the installation by opening a terminal and typing:

```bash
conda --version
```

If the command returns a version number (e.g., `conda 24.1.2`), conda is correctly installed.

### Downloading the Environment File

The `environment_geoparquet.yaml` file contains all dependencies needed to work with GeoParquet data using Python and GDAL.

!!! info "Download the environment file"
	<a class="md-button md-button--primary" href="../../../assets/env/environment_geoparquet.yaml" download>📄 Download environment_geoparquet.yaml</a>

Save this file in a working directory on your computer.

### Creating the Environment

Open a terminal, navigate to the directory containing `environment_geoparquet.yaml`, then run:

```bash
conda env create -f environment_geoparquet.yaml -n env_geoparquet
```

This command will:

* Install Python 3.12
* Install the required libraries: `geopandas`, `pyarrow`, `shapely`, `libgdal-arrow-parquet`, `gdal`
* Install GDAL ≥ 3.10 with GeoParquet support

!!! tip "Installation time"
	Installation may take a few minutes depending on your internet connection. Conda will automatically download and install all required dependencies.

### Activating the Environment

Once the environment is created, activate it with:

```bash
conda activate env_geoparquet
```

Your command prompt should now display `(env_geoparquet)` at the beginning of the line, indicating the environment is active.

### Verifying the Installation

To verify that the installation was successful, run the following commands:

**1. Check Python version:**
```bash
python --version
```
Expected: `Python 3.12.x`

**2. Check for GeoParquet driver in GDAL:**
```bash
ogrinfo --formats | findstr Parquet
```
Expected: A line containing `Parquet` (e.g., `Parquet -raster,vector- (rw+): (Geo)Parquet`)

**3. Test Python imports:**
```bash
python -c "import geopandas; import pyarrow; print('OK - All modules are correctly installed')"
```
Expected: `OK - All modules are correctly installed`

!!! warning "Troubleshooting"
	If you encounter persistent issues, remove the environment with `conda env remove -n env_geoparquet` and recreate it. You can also consult the GDAL documentation for creating an environment with GeoParquet support: [https://gdal.org/en/stable/tutorials/vector_geoparquet_tut.html](https://gdal.org/en/stable/tutorials/vector_geoparquet_tut.html)

---

## Data Used

The optimized building footprint layer is accessible via the same URL. However, the function used in Python requires the S3 path. Here are the two links used:

* **S3 URL (for Python/GeoPandas):**  
  `s3://ftp-maps-canada-ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet`

* **/vsicurl/ URL (for GDAL/ogr2ogr):**  
  `/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet`

---

## Access with Python (GeoPandas)

GeoPandas, combined with PyArrow, allows you to efficiently read GeoParquet data with spatial filtering. GeoParquet supports lazy reading, so you only read the portions of the file you need. 

In a processing workflow, you can load only the desired footprints into memory, without importing the entire dataset. This is very useful for automating analysis workflows.

!!! warning "Activate environment and Python"
	Before following this tutorial, activate the conda environment and Python with:
	```bash
	conda activate env_geoparquet    
	python
	```
	You should see `>>>` in the console. You are now ready to use Python.


### Remote reading with bbox filtering

The following example will:

1. Read the GeoParquet layer hosted on S3.
2. Apply spatial filtering during reading
3. Return only the footprints within our spatial filter.

Here, we will load buildings for a bounding box covering Montreal:

```python
import geopandas as gpd

# S3 URL of the optimized building footprint layer
url = "s3://ftp-maps-canada-ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet"

# Define the bbox
bbox_mtl = (-74.0073, 45.3672, -73.4466, 45.7328)
# Read with bbox pre-filtering
gpq_subset = gpd.read_parquet(url, bbox=bbox_mtl)
# Number of footprints retrieved
print(f"Number of buildings: {len(gpq_subset)}")
# Show first rows
print(gpq_subset.head())
```

Expected console output:
```console 
Number of buildings: 535431
							 feature_id  ...                                           geometry
0  f0e433ba-ef00-416f-88f4-d189e7535ac1  ...  POLYGON ((-73.86742 45.50376, -73.86729 45.503...
1  4c3be1d5-1b26-41a1-abe2-fc0d35032e6d  ...  POLYGON ((-73.60723 45.55632, -73.60721 45.556...
2  b1abac13-733e-4539-8226-6ac62a60a712  ...  POLYGON ((-73.79093 45.487, -73.7908 45.48706,...
3  b850c5ae-b133-4fc4-9ce1-d0cae4141d19  ...  POLYGON ((-73.83886 45.49419, -73.83873 45.494...
4  442f783d-73a2-4a5b-84b2-12a13781fa7e  ...  POLYGON ((-73.84561 45.47849, -73.84548 45.478...

[5 rows x 25 columns]
```

### Refinement with polygon geometry

If the bbox used for filtering is too coarse, you can further refine the selection as needed. This is a more realistic example. After reading the Montreal footprints, we will keep only those around the Montreal Olympic Stadium. The following steps are performed in the example:

1. Read the GeoParquet layer hosted on S3.
2. Apply spatial filtering during reading
3. Return only the footprints within our spatial filter.
4. Further refine the selection with a more precise geometry (can be any geometry).

```python
import geopandas as gpd
from shapely.geometry import box

#---|1) Filtering at read |-------
# S3 URL of the GeoParquet
url = "s3://ftp-maps-canada-ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet"

# Define the bbox (Montreal)
bbox_mtl = (-74.0073, 45.3672, -73.4466, 45.7328)

# Read with bbox pre-filtering
gpq_subset = gpd.read_parquet(url, bbox=bbox_mtl)
print(f"Number of buildings: {len(gpq_subset)}")

#---|2) Refine the selection |-------
# Define the limit as a polygon (bbox)
limite = (-73.565,45.543, -73.521,45.575)
polygon_limite = box(*limite)
gdf_limite = gpd.GeoDataFrame(geometry=[polygon_limite], crs=gpq_subset.crs)

# Perform the more precise selection
gpq_clip = gpd.sjoin(gpq_subset, gdf_limite, predicate="intersects", how="inner")

print(f"After intersection with the limit: {len(gpq_clip)} buildings")
```

**Expected result:**

![Selection of footprints around Olympic Stadium](../../assets/images/geoparquet_subset_montreal.png)

*Figure: Building footprints extracted around Montreal Olympic Stadium.*

!!! note "Refinement step"
	To simplify the tutorial, the geometry used to select footprints around the Olympic Stadium is a bbox. However, you can use a geopackage or shapefile read with the command `polygon_limite=gpd.read_file(path/to/limit.gpkg)`


### Saving the results

You can export the filtered data in various formats:

```python
# Save as GeoPackage
gpq_clip.to_file("batiments_stade_olympique.gpkg", driver="GPKG")

# Save as Shapefile
gpq_clip.to_file("batiments_stade_olympique.shp")

# Save as GeoJSON
gpq_clip.to_file("batiments_stade_olympique.geojson", driver="GeoJSON")

# Save as GeoParquet (for performance)
gpq_clip.to_parquet("batiments_stade_olympique.parquet")
```

!!! note "Recommended output format"
	The **GeoParquet** format is recommended to maintain performance benefits. For universal compatibility, use **GeoPackage** or **GeoJSON**.

---

## Access with ogr2ogr (GDAL)

GDAL provides the `ogr2ogr` command-line tool to manipulate vector data, including GeoParquet files. Recent versions support filtering at read time.

!!! info "Using ogr2ogr"
	Using ogr2ogr does not allow you to save the result of a spatial selection in a variable for later reuse. The data must be written to disk.

### Address format

To access remote data with GDAL, use the `/vsicurl/` prefix:

```
/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet
```
### Extraction with bbox filtering

!!! warning "Activating the environment"
	Before following this tutorial, activate the conda environment with:
	```bash
	conda activate env_geoparquet     
	```
	Once the environment is activated, you can use ogr/gdal commands in the console.


We will use our example to filter footprints in the Montreal bbox. We will save the result locally. The command will be constructed with the following parameters:

- `Output path`: The final footprints, filtered by your area of interest geometry (Montreal bbox)
- `/vsicurl/...`: Path to the remote GeoParquet on the FTP.
- `-spat xmin ymin xmax ymax`: Spatial filter by your *bounding box*
	- For the Montreal example, the values are: -74.0073 45.3672 -73.4466 45.7328
- `-nln`: Layer name in the output file (optional)

```bash
ogr2ogr ^
  Path/to/your/selection_buildings_ogr2ogr.gpkg ^
  "/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet" ^
  -spat -74.0073 45.3672 -73.4466 45.7328 ^
  -nln building_opti
```


### Extraction with geometry filtering (clipsrc)

ogr2ogr options also allow you to perform more than one operation in a single command. In the following example, you can, in a single command, filter footprints at read time, then select only those within a desired geometry. This geometry can be another bbox or the path to a polygon file (geopackage, shapefile, etc.).

To clip data with a specific polygon geometry, use the `-clipsrc` option. The following parameters are used:

- Output path: The final footprints, filtered by your area of interest geometry (not the bbox)
- `/vsicurl/...`: Path to the remote GeoParquet on the FTP
- `-spat xmin ymin xmax ymax`: Spatial filter by your *bounding box*
	- For the Montreal example, the values are: -74.0073 45.3672 -73.4466 45.7328
- `-clipsrc`: Path to the file used to clip geometries according to the provided limit (or a bbox).
- `-nln`: Layer name in the output file (optional)

!!! warning "Using `-clipsrc`"
	To simplify the tutorial, we use the coordinates of a bbox to clip the footprints from the first selection. This is the bbox surrounding the Montreal Olympic Stadium.

```bash

ogr2ogr ^
  Path/to/your/selection_buildings_ogr2ogr.gpkg ^
  "/vsicurl/https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet" ^
  -spat -74.0073 45.3672 -73.4466 45.7328 ^
  -clipsrc -73.565 45.543 -73.521 45.575 ^
  -nln building_opti
```

!!! warning "Difference between -spat and -clipsrc"
	* `-spat`: Selects geometries whose bbox intersects the specified bbox (faster)
	* `-clipsrc`: Actually clips geometries to the specified bbox (more precise but slower)

## Local usage

If you have downloaded the GeoParquet file locally, you can use it the same way by replacing the URL with the local path:

**Python:**

```python
import geopandas as gpd
from shapely.geometry import box

#---|1) Filtering at read |-------
# Local path to GeoParquet
url = "path/to/your/auto_building_opti_2.parquet"

# Define the bbox (Montreal)
bbox_mtl = (-74.0073, 45.3672, -73.4466, 45.7328)

# Read with bbox pre-filtering
gpq_subset = gpd.read_parquet(url, bbox=bbox_mtl)
print(f"Number of buildings: {len(gpq_subset)}")

#---|2) Refine the selection |-------
# Define the limit as a polygon (bbox)
limite = (-73.565,45.543, -73.521,45.575)
polygon_limite = box(*limite)
gdf_limite = gpd.GeoDataFrame(geometry=[polygon_limite], crs=gpq_subset.crs)

# Perform the more precise selection
gpq_clip = gpd.sjoin(gpq_subset, gdf_limite, predicate="intersects", how="inner")

print(f"After intersection with the limit: {len(gpq_clip)} buildings")

```

**ogr2ogr:**

```bash

ogr2ogr ^
  Path/to/your/selection_buildings_ogr2ogr.gpkg ^
  "path/to/your/auto_building_opti_2.parquet" ^
  -spat -74.0073 45.3672 -73.4466 45.7328 ^
  -clipsrc -73.565 45.543 -73.521 45.575 ^
  -nln building_opti
```


---


!!! tip "Best practices"
	* **Always use spatial filtering** (`bbox` or `-spat`) for large datasets
	* **Use GeoParquet for outputs** if you plan to reuse the data (optimal performance)

---

## Summary

This tutorial presented two approaches to access the optimized building footprint layer in GeoParquet format:

* **Python (GeoPandas):** Reading, filtering, and exporting with flexible Python code
* **GDAL (ogr2ogr):** Command-line manipulation for automation and batch processing

!!! tip "Next steps"
	If you prefer a graphical interface, see the tutorial [Using with QGIS](acces-qgis.md).
