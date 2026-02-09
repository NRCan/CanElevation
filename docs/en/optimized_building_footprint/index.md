# Optimized Building Footprint Layer - GeoParquet - CanElevation Series

The optimized building footprint layer is a vector dataset that lists the best building footprints across Canada. Through a prioritization process, only the highest-quality footprints are retained. This layer, containing over 10 million building footprints, is provided in the **GeoParquet** format, optimized for cloud use. This guide introduces the use of the GeoParquet format to access these data efficiently and effectively.

## What is GeoParquet?

**GeoParquet** is a geospatial file format based on [Apache Parquet](https://parquet.apache.org/), designed for efficient storage and processing of large vector datasets. It offers the following advantages:

* **Optimal compression**: Significant reduction in file size
* **Selective reading**: Ability to read only the required columns or geographic areas
* **Performance**: Fast data access, even for very large datasets
* **Interoperability**: Compatible with modern tools (Python, GDAL, QGIS, DuckDB, etc.)
* **Columnar storage**: Optimized for analytical queries

## Why GeoParquet?

GeoParquet offers advantages over traditional formats like GeoPackage (GPKG). Here is a comparison for the optimized building footprint layer:

| **Criterion** | **GeoParquet** | **GeoPackage** |
|--------------|----------------|----------------|
| **File size** | ~2.3 GB | ~5.6 GB |
| **Compression** | Excellent (60% reduction) | Moderate |
| **Selective reading (bbox)** | Yes (server-side filtering) | No (full download required) |
| **Read performance** | Very fast (targeted columns) | Moderate |
| **Remote access (S3/HTTP)** | Optimized (partial reading) | Less efficient |
| **Interoperability** | Python, GDAL, QGIS, DuckDB, etc. | Universal (but less performant) |


GeoParquet organizes data into row groups, which are blocks of rows that enable efficient and selective reading. In optimized GeoParquet files, the bounding box (bbox) of each row group can be stored in the file metadata, facilitating spatial filtering. When reading with a spatial filter, the bbox of each row group is compared to the query area; only row groups whose bbox intersects the requested area are read, reducing the volume of data to process. The number of features per row group (e.g., 65,536) is configurable when creating the file and can be adjusted for optimization needs.

---

## Available Data

The optimized building footprint layer in GeoParquet format is available at:

* **FTP URL**: [https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet](https://ftp.maps.canada.ca/pub/nrcan_rncan/extraction/auto_building/auto_building_opti_2/auto_building_opti_2.parquet)

**Dataset characteristics:**

* **Number of footprints**: 10+ million buildings
* **File size**: ~2.3 GB (GeoParquet format)
* **Geographic coverage**: Canada
* **Coordinate system**: EPSG:4617 (NAD83 CSRS geographic)


## Tutorial Summary

This guide is divided into 2 tutorials to help you install dependencies and use the optimized building footprint layer in GeoParquet format:

1. **[Using with Python and GDAL](acces-python-gdal.md)**: Access and manipulate the data with Python (GeoPandas) and the command line (ogr2ogr)

2. **[Using with QGIS](acces-qgis.md)**: Load and visualize the data with QGIS and the GeoParquet Downloader plugin


## Target Audience

These tutorials are intended for:

* **GIS analysts** wishing to work with large vector datasets in QGIS
* **Python developers** using GeoPandas and PyArrow for geospatial analysis
* **GDAL users** automating data processing with ogr2ogr
* **Data science experts** leveraging cloud-optimized formats (S3, HTTP)

!!! note "Prerequisites"
	Basic knowledge of GIS and command line is recommended for the Python/GDAL tutorials. The QGIS tutorial is accessible to beginners.

## Learn More
For more information about the optimized building footprint layer, visit the [Automatically Extracted Buildings](https://open.canada.ca/data/en/dataset/7a5cda52-c7df-427f-9ced-26f19a8a64d6) product page. There you will find the product specification, project index, and download directories by project (geopackage and shapefile).
